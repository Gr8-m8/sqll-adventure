"""import"""
import os
import time
import msvcrt
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
                if msvcrt.kbhit():
                    waitforkey = False
                    key = msvcrt.getch()
            except KeyboardInterrupt:
                waitforkey = False
                self.close()

            if not blocking:
                waitforkey = False
                time.sleep(0.025)

        # self.feedback = "" #key #""
        self.setfeedback(key)
        if key in [b'H', b'w']:
            self.options_cursor = (self.options_cursor-1) % len(self.options)

        if key in [b'P', b's']:
            self.options_cursor = (self.options_cursor+1) % len(self.options)

        if key in [b'K', b'-', b'a']:
            try:
                self.options[self.options_cursor].action('<<')
            except Exception as e:
                print(e)

        if key in [b'M', b'+', b'd']:
            try:
                self.options[self.options_cursor].action('>>')
            except Exception as e:
                print(e)

        if key in [b'\r', b' ']:
            try:
                self.options[self.options_cursor].action()
            except Exception as e:
                print(e)

        if key in [b'\x1b', b'x', b'q']:
            self.close()
