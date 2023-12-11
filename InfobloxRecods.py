#!/usr/bin/env python3.7

import requests
import json
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) # YOU CAN DELETE THIS LINE IF YOU HAVE HTTP OR HAVE A CERTIFICATE

def CheckForZone(username,password,zone_name):
    """ The function checks if a zone exists in the dns
    @:returns True if it exists and False if not
    @:param username - infoblox username
    @:param password - infoblox password
    @:param zone_name - the zone you need to check for existance"""

    host = 'https://infoblox.local'  # Replace with your Infoblox hostname or IP address
    
    #username = 'admin'
    #password = 'infoblox'
    #zone_name = 'fu.test'
    
    session = requests.Session()
    session.verify = False
    
    # Construct the API URL
    url = f"{host}/wapi/v2.10/zone_auth?fqdn={zone_name}"

    # Set up the API headers and auth credentials
    headers = {'Content-Type': 'application/json'}
    auth = (username, password)

    # Send the API request to search for the DNS zone
    response = requests.get(url, headers=headers, auth=auth, verify=False)

    # Check the API response status code
    if response.status_code == 200:
        # Parse the JSON response and check if any records were returned
        json_data = response.json()
        if json_data:
            #print(f"The zone {zone_name} exists.")
            return True
        else:
            #print(f"The zone {zone_name} does not exist.")
            return False
    else:
        print(f"API failed ")
        

def AddASingle(username,password):
    """ The function adds one A record and the relevant PTR record
    @:param username - infoblox username
    @:param password - infoblox password"""

    print("")
    print("CTRL+C to go back")
    while True:
        # ASKING FOR USER INPUT A RECORD AND IP ADDRESS
        print("")
        # print("!!! DON'T FORGET TO ADD DOMAIN NAME AFTER THE RECORD !!!")
        
        name = input("(AddASingle) Enter A record name <Without Domain-name>: ")
        domain = input("(AddASingle) Enter Domain-Name for the record: ")
        ip = input("(AddASingle) Enter the IP fot the record: ")
        
        if (name == "") or (ip == ""):
         print("")
         print("===One of the parameters has not been added===")
         print()
         continue
         
        if CheckForZone(username,password,domain) == False:
            print("zone does not exist")
            continue
            
        else:
            # CREATING A RECORD
            record = name + "." + domain

            # CREATING A PTR RECORD
            rev_ip = ip.split(".")
            ptr = rev_ip[3] + "." + rev_ip[2] + "." + rev_ip[1] + "." + rev_ip[0]

            # SENDING THE A RECORD###################################################################
            url = "https://infoblox.local/wapi/v2.7/record:a?_return_fields%2B=name,ipv4addr"
            session = requests.Session()
            session.verify = False
            payload = json.dumps({
              "name": record,
              "ipv4addr": ip
            })
            response = requests.request("POST", url, auth=(username, password), data=payload, verify=False)
            #print(response.text)
            
            # SENDING THE PTR RECORD###################################################################
            url = "https://infoblox.local/wapi/v2.7/record:ptr?_return_fields%2B=name,ptrdname,ipv4addr"
            payload = json.dumps({
              "name": ptr+".in-addr.arpa",
              "ptrdname": record,
              "ipv4addr": ip
            })
            response = requests.request("POST", url, auth=(username, password), data=payload, verify=False)
            print(response.text)

def ChangeAPtrList(username,password,record,new_ip,option):
    session = requests.Session()
    session.verify = False

    IB_HOST = "https://infoblox.local" # CHANGE THE URL FOR THE DNS NAME
    IB_VIEW = "default"
    RECORD_TYPE_A = "a"
    RECORD_TYPE_PTR = "ptr"

    session = requests.Session()
    session.verify = False  # Disable SSL verification, replace with valid cert in production
    
    api_endpoint = f"{IB_HOST}/wapi/v2.10"
    api_endpoint_a = f"{IB_HOST}/wapi/v2.10/record:{RECORD_TYPE_A}"
    api_endpoint_ptr = f"{IB_HOST}/wapi/v2.10/record:{RECORD_TYPE_PTR}"

    choice = option

    if (choice == "1"):
        OLD_RECORD_NAME = record
        NEW_RECORD_IP = new_ip

        response = requests.get(
            f'{api_endpoint_a}?name={OLD_RECORD_NAME}',
            auth=(username, password),
            verify=False
        )

        if response.status_code == 200:
            try:
                try:
                    record_data_a = json.loads(response.content)[0]
                    record_ref_a = record_data_a["_ref"]

                    api_data_a = {
                        "ipv4addr": f"{NEW_RECORD_IP}"
                    }

                    # Send 
                    api_endpoint_a = f"{IB_HOST}/wapi/v2.10/{record_ref_a}"
                    session.put(api_endpoint_a, auth=(username, password), data=json.dumps(api_data_a),verify=False)

                    print(f"{record} changed to {new_ip} record changed")
                except IndexError:
                    print(f"{record} did not change to {new_ip} no such A record           <<<<<<<<<<< check record")
                try:
                    ptr_query = f"ptrdname={OLD_RECORD_NAME}"
                    ptr_url = f"{api_endpoint_ptr}?{ptr_query}"
                    ptr_response = requests.get(ptr_url, auth=(username, password), verify=False)
                    ptr_json = json.loads(ptr_response.text)
                    ptr_obj_ref = ptr_json[0]["_ref"]
                    new_ptr = f"{NEW_RECORD_IP}"

                    # Update the PTR record object with the new name
                    ptr_data = {"ipv4addr":new_ptr}
                    ptr_url = f"{api_endpoint}/{ptr_obj_ref}"
                    requests.put(ptr_url, auth=(username, password), verify=False,data=json.dumps(ptr_data))
                    print(f"{record} changed to {new_ip} PTR record changed")
                except IndexError:
                    print(f"{record} did not change to {new_ip} no such PTR record           <<<<<<<<<<< check record")
            except IndexError:
                print("ERROR")
                
def AddCSingle(username,password):
    """ The function adds Cname records
    @:param username - infoblox username
    @:param password - infoblox password"""

    while True:
        url = "https://infoblox.local/wapi/v2.7/record:cname"

        cname = input("Enter new Cname (without domain-name): ")
        cname_domain = input("Enter new Cname domain: ")
        canonical = input("Enter existing A record (without domain-name): ")
        canonical_domain = input("Enter existing A record domain: ")
        if (cname == "" or canonical == "" or cname_domain == "" or canonical_domain == ""):
            print("One of the parameters is missing!")
            print("\n")
            continue

        if((CheckForZone(username,password,cname_domain) == True) and (CheckForZone(username,password,canonical_domain) == False)):

            session = requests.Session()
            session.verify = False
            payload = json.dumps({
                "name": cname+'.'+cname_domain,
                "canonical": canonical+'.'+canonical_domain
            })

            response = requests.request("POST", url, auth=(username, password), data=payload, verify=False)
            #print(response.content.decode())
            record = f'{cname}.{cname_domain}'
            print(record)
            os.system(f"dig @infoblox.local {record} +short")
            print("=========================================")
        else:
            print("")
            print("one of the zones does not exist\n")
            continue

def ChangeCSingle(username,password):
    """ The function changes Cname records
        @:param username - infoblox username
        @:param password - infoblox password"""

    while True:
        old_cname = input("Enter existing CNAME (without domain-name): ")
        old_cname_domain = input("Enter existing CNAME domain: ")
        new_cname = input("Enter new Cname (without domain-name): ")
        new_cname_domain = input("Enter new Cname domain: ")
        if ((CheckForZone(username, password, old_cname_domain) == True) and (CheckForZone(username, password, new_cname_domain) == True)):
            search_url = f"https://infoblox.local/wapi/v2.10/record:cname?name={old_cname}.{old_cname_domain}"
            response = requests.get(search_url, auth=(username, password), verify=False)
            response_data = response.json()
            if len(response_data) == 0:
                print(f"No CNAME record found with name '{old_cname}.{old_cname_domain}'.")
            else:
                cname_record = response_data[0]

                # Modify the CNAME record name
                new_name = f"{new_cname}.{new_cname_domain}"
                cname_record['name'] = new_name

                # Update the CNAME record
                update_url = f'https://infoblox.test/wapi/v2.10/{cname_record["_ref"]}'

                response = requests.put(update_url, data=json.dumps(cname_record), auth=(username, password), verify=False)

                if response.status_code == 200:
                    print(f"CNAME '{old_cname}.{old_cname_domain}' changed to '{new_cname}.{new_cname_domain}'.")
                else:
                    print("Could not create the CNAME.")
        else:
            print("")
            print("one of the zones does not exist\n")
            continue
                


# MAIN======================

username = input("enter username: ")
password = input("enter password: ")

# THE FOLLOWING LINES WILL CHANGE A RECORDS BASED ON A TEXT FILE
with open('my/directory/path/file.txt', 'r') as file:
    for line in file:
        if line == "":
            continue
        split_line = line.split()
        try:
            ChangeAPtrList(username, password, split_line[0], split_line[1], '1')
            print(f"######################################")
        except IndexError:
            continue
        except Exception as e:
            print(f"error: {e}")
            continue
        
        
        
 # THE FILES  my/directory/path/file.txt SHOULD LOOK LIKE THIS:
 # test.funnycomp.loca 172.16.1.10
 # test1.funnycomp.loca 172.16.1.11
 # test2.funnycomp.loca 172.16.1.12
 # test3.funnycomp.loca 172.16.1.13
 # test4.funnycomp.loca 172.16.1.14
 #
 # IT SHOULD BE JUST A SIMPLE TEXT FILE WITH TWO COLUMNS:
 # FIRST COLUMN: THE FQDN THAT NEEDS ITS IP CHANGED
 # SECOND COLUMN: THE NEW IP ADDRESS
 




