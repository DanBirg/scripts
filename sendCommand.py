#!/usr/bin/env python3.7

import paramiko
import threading
import subprocess
import time
import datetime
import sys
import socket
import os
import vaultpass as vp # is present in the github
import NetFuncs as nf # is present in the github

def sendCommandParamiko(username,password,sw,command):
    if nf.checkPing(sw) == True:
        # set up SSH client
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(sw, username=username, password=password)
        stdin, stdout, stderr = client.exec_command(command)

        # read the output of the command
        output = stdout.read().decode('utf-8')
        print(f'{sw}\n')
        print(f'{output}\n')

        # close the connection
        client.close()
    else:
        print(f'{sw} is not responding')



sw = "/switches/file/location/eapi.conf"


command = input('Enter the command: ')

values = avp.main()
user = values['data']['usrname']
password = values['data']['pasword']

print(user)
print(password)
sys.exit()

try:
    file = open(sw, "r")
except Exception as msg:
    print(msg)
    exit()
lines = file.readlines()

sw_list = []

for line in lines:
    if 'connection' not in line:
        continue
    else:
        sw_name = line.strip('[connection:').strip().strip(']')
        sw_list.append(sw_name)


threads = []
for sw in sw_list:
    thread = threading.Thread(target=sendCommandParamiko, args=(user,password,sw,command))
    threads.append(thread)
    thread.start()

for thread in threads: # Wait for all threads to finish
    thread.join()
    #result_all.sort()

