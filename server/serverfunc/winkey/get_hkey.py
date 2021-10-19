import winreg

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