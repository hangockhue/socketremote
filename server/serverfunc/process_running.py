import psutil
import subprocess

def get_process_running():
    application_running = []

    for proc in psutil.process_iter(['pid', 'name']):
        application_running.append(proc.info)

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