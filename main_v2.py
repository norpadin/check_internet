# usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2021, all rights reserved."
__license__ = "BSD 3-Clause License."

import requests
import re
from scrapli.driver.core import IOSXEDriver
from time import sleep

my_device = {
    "host": "10.1.100.1",
    "auth_username": "dnauser",
    "auth_password": "Bvs3965!",
    "auth_strict_key": False,
}
show_acl = "sho run | in PYTHON"

URLs = [
    "ping www.cisco.com",
    "ping www.bvstv.com",
    "ping www.google.com",
]
internet = False
respuesta = False
file1 = "no_acl.txt"
file2 = "si_acl.txt"
file3 = "creo_acl.txt"


def quito_acl(my_device, show_acl):
    try:
        conn = IOSXEDriver(**my_device)
        conn.open()
        output = conn.send_command(show_acl)
        a = re.search("ip access-group PYTHON in", output)
        b = re.search("ip access-list extended PYTHON", output)
        if b == None:
            pass
        if (a == None) and (b != None):
            pass
        else:
            output = conn.send_configs_from_file(file1)
            print(output)
        conn.close()
    except:
        pass
    


def agrego_acl(my_device, show_acl):
    try:
        conn = IOSXEDriver(**my_device)
        conn.open()
        output = conn.send_command(show_acl)
        a = re.search("ip access-group PYTHON in", output)
        b = re.search("ip access-list extended PYTHON", output)
        if b == None:
            output = conn.send_configs_from_file(file3)
            print(output)
        if (a == None) and (b != None):
            output = conn.send_configs_from_file(file2)
            print(output)
        else:
            pass
        conn.close()
    except:
        pass
    
def testeo(my_device, i):
    try:
        conn = IOSXEDriver(**my_device)
        conn.open()
        print(i)
        result = conn.send_command(i)
        conn.close()
        print(result)
        if "!" in result:
            print("Sucess")
            return True
        else:
            print("Failure")
            return False
    except:
        return False
        pass

def main(internet):
    for i in URLs:
        if testeo(my_device, i):
            internet = True
            print(f"PING OK  {i}")
        else:
            print(f"FALLÓ {i}")
    if internet == True:
        quito_acl(my_device, show_acl)
    else:
        agrego_acl(my_device, show_acl)


if __name__ == "__main__":
    while True:
        main(internet)
        sleep(10)
