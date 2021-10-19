import subprocess

def get_application_running():
    cmd = 'powershell "gps | where {$_.MainWindowTitle } | select Description,Id'
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    remove_top = 0
    list_app = []
    for line in proc.stdout:
        if not line.decode()[0].isspace():
            remove_top = remove_top + 1
            if remove_top > 2:
                list_app.append(
                    {line.decode().rstrip()[:23].replace(' ', ''): line.decode().rstrip()[23:].replace(' ', '')})
    return list_app
