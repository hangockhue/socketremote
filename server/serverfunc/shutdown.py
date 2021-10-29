import os

def shutdown_pc():
    os.system("shutdown /s /t 100")

def logout_pc():
    os.system("shutdown -l")
