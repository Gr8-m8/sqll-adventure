import os

CLEAR = True
def clear(active=CLEAR):
    """Clear Console"""
    if active:
        os.system('cls' if isWindows() else 'clear')


def log(msg, logfile=""):
    """print to log file"""
    with open(f"logs/{logfile}.log", "a") as logfile:
        fs = f"{msg}\n"
        logfile.write(fs)

def shell(cmd):
    """execute shell command"""
    return os.system(cmd)

def isWindows():
    """is system is windows TRUE else FALSE"""
    return True if os.name == 'nt' else False