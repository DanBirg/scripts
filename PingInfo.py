#!/usr/bin/env python3.7 

#############################################################
#       IN THE UPPER LINE USE ANY PYTHON 3.X YOU NEED
#
# TO RUN THI YOU NEED TO USE SUDO OR RUN IT WITH ROOT USER
# IT READS THE COMMAND LINE ARGUMENTS 
#
#                       TO EXECUTE:
# LINUX
#--------
# EXAMPLE 1: sudo ./PinfInfo.py 172.16.1.0/24
# EXAMPLE 1: sudo ./PinfInfo.py 172.16.1.0/24 172.16.2.0/23
#
# MAC
#---------
# EXAMPLE 1: sudo su - ; cd the/correct/location/ ; python3.x PingInfo.py 172.16.1.0/24
#
#############################################################
try:
    from icmplib import multiping
    import NetFuncs as nf             # <<<----- YOU CAN FIND IT IN https://github.com/DanBirg/scripts/blob/main/NetFuncs IT IS NOT A LIBRARY 
    import sys
    import socket
except ModuleNotFoundError:
    print("You don't have the correct package")


# MAIN
try:
    list_arg = []

    for i in sys.argv:
        list_arg.append(i)
    list_arg.pop(0)

    for arg in list_arg:
        print(arg)

        split_arg = arg.split('/')
        net = split_arg[0]
        sub = split_arg[1]

        start = nf.getNextIpAddress(nf.getNetworkAddress(net,sub))

        list = []
        for x in range(nf.getNetworkSize(sub)):
            ip = start
            start = nf.getNextIpAddress(ip)
            list.append(str(ip))

        try:
            # IF YOU'RE WORKING ON A WORKSTATION SUCH AS PC/MAC CONSIDER CHANGING THE CONCURRENT_TASKS TO AS PREDEFINED
            # YOU CAN PLAY WITH THE PARAMETERS SO YOU'LL GET A QUICKER RESPONSE FOR EXAMPLE CHANGE THE COUNT=1 AND CONCURRENT_TASKS=50
            hosts = multiping(list, count=2, interval=0.5, timeout=1.5, concurrent_tasks=20)
        except PermissionError:
            print(f"You don't have permissions to run this option")
            print("\n")
            sys.exit()

        except icmplib.exceptions.SocketPermissionError:
            print(f"You don't have permissions to run this option")
            print("\n")
            sys.exit()

        up = 0
        down = 0
        for host in hosts:
            if host.is_alive:
                try:
                    resolve = socket.gethostbyaddr(str(host.address))
                    print(f'{host.address:15} {resolve[0]:40}      up!')
                    up = up + 1
                    continue
                except socket.herror:
                    print(f'{host.address:15} no A record                                   up!')
                    up = up + 1
            else:
                try:
                    resolve = socket.gethostbyaddr(str(host.address))
                    print(f'{host.address:15} {resolve[0]:37}DOWN!')
                    down = down + 1
                    continue
                except socket.herror:
                    print(f'{host.address:15} no A record                          DOWN!')
                    down = down + 1
        print("===========================================================")
        print("IPs Up: " + str(up))
        print("IPs Down: " + str(down))
        print("")

except NameError:
    print("Invalid input 2")
except ValueError:
    print("Invalid input 3")
except ModuleNotFoundError:
    print("You don't have the correct module to run it")
except KeyboardInterrupt:
    print("Exiting")



