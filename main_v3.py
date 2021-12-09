# usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2021, all rights reserved."
__license__ = "BSD 3-Clause License."

import requests
import re
from netmiko import ConnectHandler
from time import sleep

# '''Global Variables'''

my_device = {
    'device_type':'cisco_xe',
    'ip':'10.1.100.1',
    'username':'dnauser',
    'password':'Bvs3965!',
    'secret':'Bvs3965!',
    }

show_acl = "sho run | in PYTHON"

#URLs = [
#    "www.chuchu.com",
#    "www.qqww.com",
#    ]

URLs = [
    "www.cisco.com",
    "www.bvstv.com",
    "www.google.com",
]

internet = False
respuesta = False
file1 = "no_acl.txt"
file2 = "si_acl.txt"
file3 = "creo_acl.txt"


def quito_acl(my_device, show_acl):
    try:
        net_connect = ConnectHandler(**my_device)
        net_connect.enable()
        output = net_connect.send_command(show_acl)
        a = re.search("ip access-group PYTHON in", output)
        b = re.search("ip access-list extended PYTHON", output)
        if b == None:
            pass
        if (a == None) and (b != None):
            pass
        else:
            output = net_connect.send_config_from_file(file1)
            print(output)
        net_connect.disconnect()
    except:
        pass
    


def agrego_acl(my_device, show_acl):
    try:
        net_connect = ConnectHandler(**my_device)
        net_connect.enable()
        output = net_connect.send_command(show_acl)
        a = re.search("ip access-group PYTHON in", output)
        b = re.search("ip access-list extended PYTHON", output)
        if b == None:
            output = net_connect.send_config_from_file(file3)
            print(output)
        if (a == None) and (b != None):
            output = net_connect.send_config_from_file(file2)
            print(output)
        else:
            pass
        net_connect.disconnect()
    except: 
        pass

def main(internet):
    internet = False
    net_connect = ConnectHandler(**my_device)
    net_connect.enable()
    for i in URLs:
        pingresult = net_connect.send_command(f"ping {i}")
        print(pingresult)
        if "!" in pingresult:
            internet = True
            print(f"PING INTERNET OK  {i}")
        else:
            print(f"FALLO PING A  {i}")
    net_connect.disconnect()
    if internet == True:
        quito_acl(my_device, show_acl)
    else:
        agrego_acl(my_device, show_acl)

if __name__ == "__main__":
    while True:
        main(internet)
        sleep(30)
