import netmiko

# Enter the IP address of the switch here.
switch_ip = "10.20.30.40"

# Enter the username and password for the switch here.
username = "DanBirg"
password = ""

# Create a Netmiko SSH connection to the switch.
connection = netmiko.ConnectHandler(
    host=switch_ip,
    username=username,
    password=password,
    device_type="arista_eos",
)

# Send the command to the switch.
#connection.send_command("show version")

# Get the output of the command.
output = []
output.append(connection.send_command("show version"))
output.append(connection.send_command("show ip int br"))
output.append(connection.send_command("show int status"))
# Print the output of the command.
for i in output:
    print(type(i))

# Close the connection to the switch.
#connection.close()
