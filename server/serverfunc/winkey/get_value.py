import winreg
from .open_key import open_key

def get_value(link, name):
    try:
        asubkey = open_key(link)
        return winreg.QueryValueEx(asubkey, name)[0]
    except Exception as e:
        print(e)
        return "Lỗi"