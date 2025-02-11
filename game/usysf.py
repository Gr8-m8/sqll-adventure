import os
import datetime

CLEAR = True
SESSION = datetime.datetime.now().strftime('%Y-%m-%d@%H-%M-%S')

def clear(active=CLEAR):
    """Clear Console"""
    if active:
        os.system('cls' if isWindows() else 'clear')


def log(msg: str, code: str="", logfile=SESSION, consolelog=True):
    """print to log file"""
    with open(f"{logfile}.log", "a") as logfile:
        fs = f"{code}: {msg}\n"
        logfile.write(fs)
        if consolelog:
            print(fs)
        

def shell(cmd):
    """execute shell command"""
    return os.system(cmd)

def isWindows():
    """is system is windows TRUE else FALSE"""
    return True if os.name == 'nt' else False