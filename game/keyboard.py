import usysf

class Keyboard:
    """read async keyboard input"""
    def __init__(self):
        self.keys = {
            
        }
        self.bytemap = {
            b'\r': "enter",
            b'\x1b': "escape",
            b'H': "arrow_up",
            b'P': "arrow_down",
            b'M': "arrow_right",
            b'K': "arrow_left",
        }
        keyfilename = 'settings/keyboard.settings'
        try:
            open(keyfilename, 'x')
            with open(keyfilename, 'w') as keyfile:
                defaultkeys = [
                    "w=UP",
                    "s=DOWN",
                    "d=RIGHT",
                    "a=LEFT",
                    "esc=CLOSE",
                    "enter=ENTER",
                    " =ENTER",
                    "arrow_up=UP",
                    "arrow_down=DOWN",
                    "arrow_right=RIGHT",
                    "arrow_left=LEFT",
                    "escape=CLOSE",
                    "enter=ENTER",
                ]
                for defaultkey in defaultkeys:
                    keyfile.write(f"{defaultkey}\n")
                keyfile.close()
        except Exception as e: 
            usysf.log(f"KEYBIND ERROR: {e}")
        with open(keyfilename, 'r') as keyfile:
            for line in keyfile:
                kv = line.split('=')
                self.keys.update({kv[0]:kv[1].strip()})
            keyfile.close()
    
    def iskey(self):
        """if key pressed"""
        return False
    
    def readkey(self):
        """get key value"""
        return None
    
KEYBOARD = Keyboard()

try:
    import msvcrt

    class Keyboard_msvcrt(Keyboard):
        """windows keyboard"""
        def iskey(self):
            return msvcrt.kbhit()

        def readkey(self):
            try:
                if self.iskey():
                    key = msvcrt.getch()
                    if key in self.bytemap:
                        key = self.bytemap[key]
                    if str(key)[2] in self.keys:
                        key = self.keys[str(key)[2]]
                    if key in self.keys:
                        key = self.keys[key]
                    return key
            except KeyboardInterrupt: exit(0)
            return None
        
    KEYBOARD = Keyboard_msvcrt()
except Exception as e:
    usysf.log(f"FAILED IMPORT WINDOWS KEYBOARD: {e}")
try:
    import getch

    class Keyboard_getch(Keyboard):
        """linux keyboard"""
        def iskey(self):
            return True #if getch.getch() else False

        def readkey(self):
            try:
                if self.iskey():
                    key = getch.getch()
                    if key in self.bytemap:
                        key = self.bytemap[key]
                    if key in self.keys:
                        key = self.keys[key]
                    return key
            except KeyboardInterrupt: exit(0)
            return None
        
    KEYBOARD = Keyboard_getch()

except Exception as e:
    usysf.log(f"FAILED IMPORT LINUX KEYBOARD: {e}")