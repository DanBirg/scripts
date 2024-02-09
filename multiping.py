#!/usr/bin/env python3.7

# it was tested for the python3.7 and above

import threading
import subprocess
import time
import datetime
import sys
import socket
import os
import NetFuncs as nf ## please import NetFuncs.py file for all the functions needed

# =============VARIABLES==============

to = 1 # timeout
hosts_file = "/location/of/your/file/multiping_hosts.txt"
edit_host_file = "vi /location/of/your/file/multiping_hosts.txt"

# =============FUNCTIONS==============

def exiting_script():  # CTRL + C
    print('\nExiting\n\n')
    sys.exit()

def checkPing(host):
    # Use the subprocess module to run the ping command
    result = subprocess.run(['ping', '-c', '1', '-W', '1', '-i', '0.2', host], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    res = str(result).split()
    if nf.checkValidIp(str(host)) == True:
        try:
            res = res[21]
        except IndexError:
            res = '0'
        try:
            name = socket.gethostbyaddr(host)
            name = name[0]
        except socket.herror:
            name = 'no dns record'
    if nf.checkValidIp(str(host)) == False:
        try:
            res = res[22]
        except IndexError:
            res = '0'
        try:
            name = socket.gethostbyname(host)
        except socket.gaierror:
            name = 'no dns record'

    # Check the return code to determine if the ping was successful
    if result.returncode == 0:
        #return True
        result = f'> {host:20}| {name:40}| Success {res:11}| {succ_dict[host] + 1:5}    |{fail_dict[host]:5}   '
        succ_dict[host] = succ_dict[host] + 1
        result_all.append(result)
    else:
        #return False
        result = f'> {host:20}| {name:40}| Fail               | {succ_dict[host]:5}    |{fail_dict[host] + 1:5}   '
        fail_dict[host] = fail_dict[host] + 1
        result_all.append(result)

# ================ MAIN ====================

try:
    os.system(edit_host_file)
    
    host_list = []
    result_all = []
    networks = []

    print("\033c") # clear the screen
    
    # opens the file where all the hosts are located
    try: 
        file = open(hosts_file, "r")
    except Exception as msg:
        print(msg)
        exit()
    lines = file.readlines() 

    # puts all the elements from the file to the list
    for line in lines:
            if "#" in line:
                continue
            host = line.split()
            try:
                subandnet = host[0].split('/')
            except IndexError:
                continue

            if len(subandnet) == 0:
                continue
            if len(subandnet) == 1:
                host_list.append(host[0])
            if len(subandnet) == 2:
                networks.append(subandnet)
              
    # add the ranges to the list of hosts to ping
    for net in networks:
        nwrk = net[0]
        sub = net[1]
        start = nf.getNextIpAddress(nf.getNetworkAddress(nwrk,sub))
        for x in range(nf.getNetworkSize(sub)):
            ip = start
            start = nf.getNextIpAddress(ip)
            host_list.append(str(ip))

    # creating the dictionaries for later use to monitor how many successes and how many fails
    succ_dict = {}
    fail_dict = {}
    for key in host_list:
        succ_dict.setdefault(key,0)
        fail_dict.setdefault(key,0)

    # starts the threading process
    threads = []
    count = 1
    while True:
        for host in host_list:
            thread = threading.Thread(target=checkPing, args=(host,))
            threads.append(thread)
            thread.start()
        
        for thread in threads: # Wait for all threads to finish
            thread.join()  
        result_all.sort()

        # displays the output after all the formating at ones
        print("\033c") # clear the screen
        print(f'Multiping V1.0\n')
        print(f'pinged ({count}) times')
        print(f'refresh ({to}s)')
        print(f'{datetime.datetime.now()}\n')
        print(f'| Host                | DNS Record                              | Result             |  Suceess |  Fail')
        print(f'========================================================================================================')

        # printing all the results 
        for res in result_all: 
            print(res)

        # resets the results for the next iteration
        result_all = []

        count+= 1
        time.sleep(to)
    

except KeyboardInterrupt:  ## PRESSING THE CTRL+C
    exiting_script()


