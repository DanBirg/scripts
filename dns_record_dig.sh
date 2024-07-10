#!/bin/bash

function is_ip_address {
  # Regex pattern for IPv4 address
  ip_pattern="^([0-9]{1,3}\.){3}[0-9]{1,3}$"

  if [[ $1 =~ $ip_pattern ]]; then
    # Check if each octet is within range (0-255)
    for octet in $(echo $1 | tr '.' ' '); do
      if [[ $octet -lt 0 || $octet -gt 255 ]]; then
        return 1  # Not a valid IP (out of range)
      fi
    done
    return 0  # Valid IP address
  else
    return 1  # Not a valid IP (format mismatch)
  fi
}



NAME_SERVER=8.8.8.8 #IP ADDRESS OF YOUR DNS SERVER
file="dns_records_list.txt" #YOU MUST HAVE IT IN YOUR DIRECTORY

vi $file

for line in $(cat "$file")
do
	echo $line
	echo ===============
	if is_ip_address "$line"; then
		dig @$NAME_SERVER -x $line +short
	else
		dig @$NAME_SERVER $line +short
	fi
echo ===============
echo
done
