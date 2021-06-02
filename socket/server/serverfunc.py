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

    return winreg.OpenKey(aReg, aKey)


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
    except FileNotFoundError:
        return ''

def delete_value(link, name):
    try:
        asubkey = open_key(link)
        winreg.DeleteValue(asubkey, name)
        return "Xóa value thành công"
    except FileNotFoundError:
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
    except:
        return "Lỗi"

def create_key(link):
    links = link.split("\\")

    HKEY_NAME = links.pop(0)

    HKEY = get_hkey(HKEY_NAME)

    aKey = "\\".join(links)

    try:
        winreg.CreateKey(HKEY, aKey)
        return "Tạo Key thành công"
    except:
        return "Lỗi"

def delete_key(link):
    links = link.split("\\")

    HKEY_NAME = links.pop(0)

    HKEY = get_hkey(HKEY_NAME)

    aKey = "\\".join(links)

    try:
        winreg.DeleteKey(HKEY, aKey)
        return "Xóa Key thành công"
    except:
        return "Lỗi"


def on_press(key):
    print('{0} pressed'.format(
        key))
    return key


def on_release(key):
    print('{0} release'.format(
        key))
    if key == Key.esc:
        # Stop listener
        return False
# Collect events until released


def listening_keyboard(listening=True):
    if listening:
        with Listener(
                on_press=on_press) as listener:
            listener.join()
        print(listener)
        return listener
    else:
        return False


def shutdown_pc():
    os.system("shutdown /s /t 1")


listening_keyboard(True)