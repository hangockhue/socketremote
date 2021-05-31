import psutil
import pyautogui
import cv2
import numpy as np
import os
from pynput.keyboard import Listener
import logging

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
    
    print(screen_shot)
    print(type(screen_shot))
    return screen_shot


def keylogger_listening():

    pass