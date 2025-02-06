"""import"""
import os
import time

class Keyboard:
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
        try:
            open('keyboard.settings', 'x')
            with open('keyboard.settings', 'w') as keyfile:
                defaultkeys = [
                    "w=UP",
                    "s=DOWN",
                    "d=RIGHT",
                    "a=LEFT",
                    "esc=CLOSE",
                    "enter=ENTER",
                    " =ENTER",
                ]
                for defaultkey in defaultkeys:
                    keyfile.write(f"{defaultkey}\n")
                keyfile.close()
        except: pass
        with open('keyboard.settings', 'r') as keyfile:
            for line in keyfile:
                kv = line.split('=')
                self.keys.update({kv[0]:kv[1].strip()})
            keyfile.close()
    
    def iskey(self):
        return False
    
    def readkey(self):
        return None

if False:
    try:
        from pynput.keyboard import Events
    except Exception as e:
        print("KEYBOARD INSTALL ERROR:", e)
        exit(1)

    class Keyboard_pynput(Keyboard):
        def __init__(self):
            super().__init__()
            self.cooldown = 0

        def iskey(self) -> bool:
            with Events() as events:
                for event in events:
                    try:
                        key = event.key.name
                    except:
                        key = event.key.char
                    if key in self.keys:
                        return True
            return False
        
        def readkey(self) -> str:
            with Events() as events:
                for event in events:
                    try:
                        key = event.key.name
                    except:
                        key = event.key.char
                    if key in self.keys:
                        return self.keys[key]
            return None

    keyboardv = Keyboard_pynput()
else:
    import msvcrt

    class Keyboard_msvcrt(Keyboard):
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
        
    keyboardv = Keyboard_msvcrt()

from textdecoration import textdecoration as textd


def console_clear():
    """Clear Console"""
    CLEAR = True
    os.system('cls' if os.name == 'nt' else 'clear') if CLEAR else None


CONSOLECLEAR = True


class MenuItem:
    """Generic Menu Item"""

    def __init__(self, text: str = "", desc: str = "") -> None:
        self.text = text
        self.desc = desc

    def display_str(self):
        """Display format STR"""
        return f"{self.text}{f": {self.desc}" if self.desc else ""}"

    def __str__(self) -> str:
        return self.display_str()


class MenuTitle(MenuItem):
    """Title Menu Item"""

    def display_str(self):
        """Display format STR"""
        return f"{textd.PURPLE}=== {super().display_str()} ==={textd.END}"


class MenuOption(MenuItem):
    """Interactive Menu Item"""

    def __init__(self, text: str = "", desc: str = "", selected=False, action=None, actiondesc: str = "") -> None:
        super().__init__(text, desc)
        self.selected = selected
        self.action = action
        self.actiondesc = actiondesc

    def display_str(self):
        """Display format STR"""
        retur = ""
        if self.selected:
            retur += f"{textd.BGGRAY}"
        retur += f"{textd.BLUE}{super().display_str()}{textd.END}"
        return retur


class Menu:
    """Standard Menu Interface"""

    def __init__(self, title: MenuTitle, text: MenuItem, options: list) -> None:
        self.title = title
        self.text = text
        self.options = options
        self.feedback = ""
        self.options_cursor = 0
        self.active = False

    @staticmethod
    def display_menu(menu, blocking=True):
        """Manu function Loop"""
        menu.active = True
        while menu.active:
            menu.display()
            menu.action(blocking=blocking)

    def open(self):
        """Activate Menu"""
        self.active = True

    def close(self):
        """Deactivate Menu"""
        self.active = False
        if CONSOLECLEAR:
            console_clear()

    def setfeedback(self, feedback):
        """Force Output"""
        self.feedback = feedback

    def display(self):
        """Console Output"""
        if CONSOLECLEAR:
            console_clear()
        print(self.title)
        print(self.text)
        self.options[self.options_cursor].selected = True
        for item in self.options:
            print(item)
        self.options[self.options_cursor].selected = False

        if self.options[self.options_cursor].actiondesc:
            print(self.options[self.options_cursor].actiondesc)

        if self.feedback:
            print(self.feedback)

    def action(self, blocking=True):
        """Activate Manu Item"""
        key = None
        waitforkey = True
        while waitforkey:
            try:
                if keyboardv.iskey():
                    waitforkey = False
                    key = keyboardv.readkey()
            except KeyboardInterrupt:
                waitforkey = False
                self.close()

            if not blocking:
                waitforkey = False
                time.sleep(0.025)

        self.setfeedback(key)
        if key == "UP":
            self.options_cursor = (self.options_cursor-1) % len(self.options)

        if key == "DOWN":
            self.options_cursor = (self.options_cursor+1) % len(self.options)

        if key == "LEFT":
            try:
                self.options[self.options_cursor].action('<<')
            except Exception as e:
                print(e)

        if key == "RIGHT":
            try:
                self.options[self.options_cursor].action('>>')
            except Exception as e:
                print(e)

        if key == "ENTER":
            try:
                self.options[self.options_cursor].action()
            except Exception as e:
                print(e)

        if key == "CLOSE":
            self.close()
