import pyautogui
import cv2
import numpy as np

def take_screenshot():
    screen = pyautogui.screenshot()

    frame = np.array(screen)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    frame = cv2.resize(frame, (1024, 576), interpolation=cv2.INTER_AREA)
    return frame