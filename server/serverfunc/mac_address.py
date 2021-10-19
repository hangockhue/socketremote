import os
import re

def get_mac_address():
    result = os.popen("ipconfig /all")
    text = result.read()
    mac_address = re.findall('Physical Address.+', text)[-1]
    mac_address = mac_address.split(":")[-1].strip()
    return mac_address
