import winreg
from .open_key import open_key

def delete_value(link, name):
    try:
        asubkey = open_key(link)
        winreg.DeleteValue(asubkey, name)
        return "Xóa value thành công"
    except Exception as e:
        print(e)
        return "Lỗi"