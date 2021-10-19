import winreg
import struct
from .open_key import open_key
from .create_key import create_key


def set_value_file(link, name, value, value_type):
    try:
        if value_type == 'String':
            value_type = winreg.REG_SZ
        elif value_type == 'Binary':
            value_type = winreg.REG_BINARY
            value = struct.pack('<Q', int(value))
        elif value_type == 'DWORD':
            value = int(value)
            value_type = winreg.REG_DWORD
        elif value_type == 'QWORD':
            values = value.replace("00","").split(",")
            
            value = ''
            for i in values[::-1]:
                if i:
                    if i[0] == '0':
                        i = i[1]
                    value += i

            value = int(value, 16)

            value_type = winreg.REG_QWORD
        elif value_type == 'Multi-String':
            value = value.split(',')
            value_type = winreg.REG_MULTI_SZ
        else:
            value_type = winreg.REG_EXPAND_SZ
    except:
        return '0'

    try:
        asubkey = open_key(link)
    except Exception as e:
        print(e)
        a = create_key(link)
        
        if a == "Tạo Key thành công":
            asubkey = open_key(link)
        else:
            return '0'
    
    try:
        winreg.SetValueEx(asubkey, name, 0, value_type, value)
    except Exception as e:
        print(e)
        return '0'
        
    return '1'
