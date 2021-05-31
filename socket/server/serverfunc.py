import psutil
import pyautogui
import cv2
import numpy as np
import os
from pynput.keyboard import Listener
import logging
import winreg

def open_key(link):
    links = link.split("\\")

    HKEY_NAME = links.pop(0)

    if HKEY_NAME == 'HKEY_LOCAL_MACHINE':
        HKEY = winreg.HKEY_LOCAL_MACHINE
    elif HKEY_NAME == 'HKEY_CLASSES_ROOT':
        HKEY = winreg.HKEY_CLASSES_ROOT
    elif HKEY_NAME == 'HKEY_CURRENT_USER':
        HKEY = winreg.HKEY_CURRENT_USER
    elif HKEY_NAME == 'HKEY_USERS':
        HKEY = winreg.HKEY_USERS
    else:
        HKEY = winreg.HKEY_CURRENT_CONFIG

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
    asubkey = open_key(link)

    return winreg.QueryValueEx(asubkey, name)[0]

def keylogger_listening():

    pass