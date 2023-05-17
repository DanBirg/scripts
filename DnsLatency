#!/usr/bin/env python3.7

import time
import sys
import subprocess
from datetime import datetime

default_times = 2000000 #<<<--- ENTER YOUR DEFAULT NUMBER OF TIMES TO QUERY DNS SERVER
default_latency = 0.7 #<<<--- ENTER YOUR DEFAULT VALID LATENCY 
default_dns = '8.8.8.8' #<<<--- ENTER YOUR DEFAULT DNS SERVER

def exiting_script():  # CTRL + C
    print('')
    print('')
    print('Exiting program')
    print('')
    sys.exit()

try:
    while True:
        hostname = input("Enter FQDN to query: ")
        dns = input("Enter DNS server to use: ")
        if dns == "":
            dns = default_dns
        times = input("Enter number of times to query <or leave blank>: ")
        if times == "":
            times = int(default_times)
        latency = input("What is the latency you want to display: ")
        if latency == "":
            latency = default_latency

        print('Quering the {} server'.format(dns))
        print('')
        for i in range(int(times)):
            start = time.time()
            start_now = datetime.now()
            subprocess.check_output('nslookup {} {}'.format(hostname,dns), shell=True)
            end = time.time()
            end_now = datetime.now()
            sum = end - start
            if sum > float(latency):
                print('start time is: ' + str(start_now))
                print(sum)
                print('end time is: ' + str(end_now))
                print('============================================')

except KeyboardInterrupt:  ## PRESSING THE CTRL+C
    exiting_script()


