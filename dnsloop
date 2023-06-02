#!/bin/bash
####################################################################################
# example of execution - digging for google.com 1000 times and it displays the loop
# ./testdns google.com 1000
# example of execution - digging for google.com 1000 times and it does not dispaay the loop (the dd flag)
# ./testdns google.com 1000 dd
####################################################################################

print_and_delete() {  # THE FUNCTION CLEARS THE PRIVIOUS LINE AND PRINTS THE NEXT ONE
  local message=$1
  if [[ "$disloop" == "dd" ]]; then # if dd flag is set then don't display the loop
    printf "\r\033[K%s" "$message"
  else
    echo "$message"
  fi
  }

 host=$1; # specify the host to look for
 loops=$2; # specify the number of times to loop
 disloop=$3; # don't display the loop (dd)
 
 for ((i=1; i<=loops; i++)); do
  result=$(dig @8.8.8.8 $host +short)
  if [[ $result == *"1.1.1.1"* ]]; then
    print_and_delete "server1 -- 1.1.1.1"
  else
    print_and_delete "server2 -- 2.2.2.2"
  fi
 done
 
 echo
