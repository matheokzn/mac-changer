#!/usr/bin/env python

# [+] This is a Python2 program to change the MAC address on Unix devices using ifconfig
# [+] Current supported flags are: -i or --interface to change interface, -m or --mac to change MAC address
# [+] To run this program, clone the repository and execute the command below (replace <str> with your own settings):
# [+] 'sudo python <mac-changer.py> -i <interface> -m <mac>
# [+] Hack responsibly, always get permission, and don't get in trouble!
# [+] by matheo [dot] cc


# [+] Imports the python modules used in this program

import subprocess
import optparse
import re


# [+] Function to parse interface and MAC using one-liner , returns prompt with --help if improper arguments are entered
def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Select the interface to change")
    parser.add_option("-m", "--mac", dest="new_mac", help="Select the new MAC address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[+]Please specify an interface, use --help for more info.")
    elif not options.new_mac:
        parser.error("[+]Please specify a mac, use --help for more info.")
    return options


# [+] Function to take the interface down, change it, and bring it back up
def change_mac(interface, new_mac):
    print("[+] Changing MAC address for " + interface + " to " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


# [+] Function to print only the MAC address of the changed interface
def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[+]Could not read MAC address")


# [+] Runs get arguments to grab the input from the user
options = get_arguments()

# [+] Reads the current MAC in the selected interface,
current_mac = get_current_mac(options.interface)

# [+] Prints what the current MAC is in the selected interface
print("[+]The current MAC address is = " + str(current_mac))

# [+] Changes the MAC in he selected interface
change_mac(options.interface, options.new_mac)

# [+] Returns the final output of the program
current_mac = get_current_mac(options.interface)
if current_mac == options.new_mac:
    print("[+]The MAC address for interface " + options.interface + " was successfully changed to " + current_mac)
else:
    print("[+]The MAC address was not changed")




