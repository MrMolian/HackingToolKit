
class Passwords_Extractor:
    def __init__(self,temp_path=""):

        self.temp_path = temp_path

        # Imports of extractors
        from .Chrome.extractor import Chrome_Extractor
        extractors = [Chrome_Extractor]
        # Initalisation of Extractors
        self.extractors = [extractor(temp_path) for extractor in extractors]
        # Passwords
        self.pws = []
    def get_passwords(self):
        #1. Get Passwords
        for extractor in self.extractors : 
            pws = extractor.extract()
            for pw in pws : 
                self.pws.append(pw)
        return self.pws
if __name__ == "__main__":
    extractor = Passwords_Extractor()
    for pw in extractor.get_passwords() : 
        print(pw)