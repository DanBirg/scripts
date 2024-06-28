#!/usr/bin/env python3.7 

import subprocess

def getIdName():
    """ This function gets the name of the username connected to the unix machine 
    @:return username of the id"""
    id = subprocess.check_output("id -un | cut -d'(' -f1", shell=True)
    return id.decode().strip()

def splitIpAddress(ipaddress):
    """ This function splits the ip address into a list
    @:param ipaddress - the ip address to split
    @:return split_ipaddress - the list"""

    try:
        split_ipaddress = ipaddress.split('.')
        return split_ipaddress
    except Exception as e:
        print(e)

def checkValidIp(ipaddress):
    """ This function checks if the ip address that was entered is a legit ip address
    @:param ipaddress - the ip address to check
    @:return returns true if valid and false if not"""

    try:
        if len(splitIpAddress(ipaddress)) == 4:
            splitip = splitIpAddress(ipaddress)
            for octat in splitip:
                try:
                    if int(octat) >= 0 and int(octat) <= 255:
                        continue
                except ValueError:
                    return False
                else:
                    return False
            return True
        else:
            return False
    except Exception as e:
        print(e)

def convertToBinary(num):
    """ This function converts a number to binary
    @:param num - the value that needs convertion
    @:return binary_representation - the actual binary number of the original value"""

    try:
        if(type(num) == str):
            num = int(num)
            binary_representation = format(num, '08b')
            return binary_representation
        else:
            binary_representation = format(num,'08b')
            return binary_representation
    except Exception as e:
        print(e)

def getNextIpAddress(ipaddress):
    """ This function calculated the next ip address
    @:param ipaddress - the original ip address
    @:return next_ip_address - the next valid ip address"""

    try:
        if(ipaddress == '255.255.255.255'):
            return ipaddress
        else:
            ip_parts = splitIpAddress(ipaddress)
            ip_int = int(ip_parts[0]) * 256 ** 3 + int(ip_parts[1]) * 256 ** 2 + int(ip_parts[2]) * 256 + int(ip_parts[3])

            next_ip_int = ip_int + 1

            next_ip_address = '.'.join([str(next_ip_int >> 24 & 255), str(next_ip_int >> 16 & 255),
                                        str(next_ip_int >> 8 & 255), str(next_ip_int & 255)])

            return next_ip_address
    except Exception as e:
        print(e)

def getSubnetMask(subnetmask):
    """ This function returns the subnet mask in x.x.x.0 format
    @:param sunetmask - the suffix number
    @:return the x.x.x.0 format of return"""

    try:
        if int(subnetmask) > 0 and int(subnetmask) <= 32:
            subnet_bits = ''
            counter = 0
            for i in range(int(subnetmask)):
                subnet_bits = subnet_bits + '1'
                counter += 1
                if counter == 8:
                    subnet_bits = subnet_bits + '.'
                if counter == 16:
                    subnet_bits = subnet_bits + '.'
                if counter == 24:
                    subnet_bits = subnet_bits + '.'

            zeros = 32 - int(subnetmask)
            for j in range(zeros):
                subnet_bits = subnet_bits + '0'
                counter += 1
                if counter == 8:
                    subnet_bits = subnet_bits + '.'
                if counter == 16:
                    subnet_bits = subnet_bits + '.'
                if counter == 24:
                    subnet_bits = subnet_bits + '.'

            split_subnet_bits = subnet_bits.split('.')
            one = int(split_subnet_bits[0],2)
            two = int(split_subnet_bits[1],2)
            three = int(split_subnet_bits[2],2)
            four = int(split_subnet_bits[3],2)
            return f'{one}.{two}.{three}.{four}'

        else:
            return '-1'
    except Exception as e:
        print(e)

def getNetworkAddress(ipaddress,subnetmask):
    """ This function returns the network address of the network
    @:param ipaddress - the ip address to check
    @:param sunetmask - the /xx suffic num
    @:return network_address - the network address"""

    try:
        ip_parts = ipaddress.split('.')
        subnet = getSubnetMask(subnetmask)
        subnet_parts = subnet.split('.')

        network_parts = [str(int(ip_parts[i]) & int(subnet_parts[i])) for i in range(4)]
        network_address = '.'.join(network_parts)

        return network_address
    except Exception as e:
        print(e)

def getBroadcastAddress(ipaddress, subnetmask):
    """ This function returns the broadcast address of the network
    @:param ipaddress - the ip address to check
    @:param sunetmask - the /xx suffic num
    @:return broadcast_address - the broadcast address"""

    try:
        ip_parts = ipaddress.split('.')
        subnet = getSubnetMask(subnetmask)
        subnet_parts = subnet.split('.')

        complement_parts = [str(255 - int(subnet_parts[i])) for i in range(4)]

        broadcast_parts = [str(int(ip_parts[i]) | int(complement_parts[i])) for i in range(4)]
        broadcast_address = '.'.join(broadcast_parts)

        return broadcast_address
    except Exception as e:
        print(e)

def CheckIfNetworkAdd(network,start_range):
    """ This function checks if the second address provided is a network address address
    @:param network - the network with /xx suffix
    @:param start_range - the ip address to check
    @:return start_range - if the start_range address is identical to network then it returns the next available address"""

    try:
        split_network = network.split('/')
        network = split_network[0]
        ip_addr = start_range
        if ip_addr == network:
            next_ip_address = getNextIpAddress(ip_addr)
            start_range = next_ip_address
            #print(start_range)
            return start_range
        else:
            return start_range
    except Exception as e:
        print(e)

def getNetworkSize(subnet_mask):
    """ This function calculates how many hosts can be in this netwrok subnet
    @:param subnet_mask - the suffix length of the subnet mask
    @:return net_size - the number of hosts of this suffix"""

    try:
        netmask = getSubnetMask(subnet_mask)
        split_subnet = netmask.split('.')
        counter = 0
        for i in split_subnet:
            binary = convertToBinary(i)
            counter = counter + binary.count('0')

        net_size = 2 ** counter - 2
        return net_size
    except Exception as e:
        print(e)

def changeMacPatern(macaddress):
    """ This function takes any mac address pattern and returns only xxxx.yyyy.zzzz pattern
    @:param macaddress - any mac address pattern
    @:return xxxx.yyyy.zzzz mac address pattern"""
    
    try:
        if ':' in macaddress:
            split_mac = macaddress.split(':')
            mac_len = len(split_mac)
            if mac_len == 3:
                return (f'{split_mac[0]}.{split_mac[1]}.{split_mac[2]}')
            if mac_len == 6:
                return (f'{split_mac[0]}{split_mac[1]}.{split_mac[2]}{split_mac[3]}.{split_mac[4]}{split_mac[5]}')
        else:
            split_mac = macaddress.split('.')
            mac_len = len(split_mac)
            if mac_len == 1:
                split_mac = list(macaddress)
                return (f'{split_mac[0]}{split_mac[1]}{split_mac[2]}{split_mac[3]}.'
                        f'{split_mac[4]}{split_mac[5]}{split_mac[6]}{split_mac[7]}.'
                        f'{split_mac[8]}{split_mac[9]}{split_mac[10]}{split_mac[11]}')
            if mac_len == 3:
                return  macaddress
            if mac_len == 6:
                return (f'{split_mac[0]}{split_mac[1]}.{split_mac[2]}{split_mac[3]}.{split_mac[4]}{split_mac[5]}')
    except Exception as e:
        print(e)
        
def checkPing(host):
    """ the function checks if the address is pingable
    @:param host - the name of the hostname
    @:return returns true if it is pingalbe and false if not"""

    # Use the subprocess module to run the ping command
    result = subprocess.run(['ping', '-c', '1', '-W', '2', '-i', '1', host], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # Check the return code to determine if the ping was successful
    if result.returncode == 0:
        return True
    else:
        return False
        
    
    
 # MAIN
 
#print(splitIpAddress('1.1.1.1')) # ['1', '1', '1', '1']
#print(checkValidIp('1.1.1.1')) # True
#print(checkValidIp('255.255.255.2555')) # False
#print(convertToBinary(255)) # 11111111
#print(convertToBinary('255')) # 11111111
#print(getNextIpAddress('1.1.1.1')) # 1.1.1.2
#print(getNextIpAddress('255.255.255.255')) # 255.255.255.255
#print(getSubnetMask('24')) # 255.255.255.0
#print(getSubnetMask(24)) # 255.255.255.0
#print(getNetworkAddress('1.1.1.1','24')) # 1.1.1.0
#print(getNetworkAddress('1.1.1.1',24)) # 1.1.1.0
#print(getBroadcastAddress('1.1.1.1','24')) # 1.1.1.255
#print(checkIfNetworkAdd('1.1.1.0/24','1.1.1.0')) # 1.1.1.1
#print(checkIfNetworkAdd('1.1.1.0/24','1.1.1.2')) # 1.1.1.2
#print(getNetworkSize('24')) # 254
#print(getNetworkSize('21')) # 2046
