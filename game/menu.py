"""import"""
import os
import time

from textdecoration import textdecoration as textd

from keyboard import KEYBOARD
import usysf

class MenuItem:
    """Generic Menu Item"""

    def __init__(self, text: str = "", desc: str = "") -> None:
        self.text = text
        self.desc = desc

    def display_str(self):
        """Display format STR"""
        fs = f": {self.desc}" if self.desc else ""
        return f"{self.text}{fs}"

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
        if usysf.CLEAR:
            usysf.clear()

    def setfeedback(self, feedback):
        """Force Output"""
        self.feedback = feedback

    def display(self):
        """Console Output"""
        if usysf.CLEAR:
            usysf.clear()
        drawstr = ""
        drawstr += f"{self.title}\n"
        drawstr += f"{self.text}\n"
        self.options[self.options_cursor].selected = True
        for item in self.options:
            drawstr += f"{item}\n"
        self.options[self.options_cursor].selected = False

        if self.options[self.options_cursor].actiondesc:
            drawstr += f"{self.options[self.options_cursor].actiondesc}\n"

        if self.feedback:
            drawstr += f"{self.feedback}\n"

        print(drawstr)

    def action(self, blocking=True):
        """Activate Manu Item"""
        key = None
        waitforkey = True
        try:
            while waitforkey:
                if KEYBOARD.iskey():
                    waitforkey = False
                    key = KEYBOARD.readkey()
            

            if not blocking:
                waitforkey = False
                time.sleep(0.025)

        except KeyboardInterrupt:
                waitforkey = False
                self.close()

        #self.setfeedback(key)
        if key == "UP":
            self.options_cursor = (self.options_cursor-1) % len(self.options)

        if key == "DOWN":
            self.options_cursor = (self.options_cursor+1) % len(self.options)

        if key == "LEFT":
            try:
                self.options[self.options_cursor].action('<<')
            except Exception as e:
                usysf.log(f"MENU OPTION DECREESE ERROR: {e}")

        if key == "RIGHT":
            try:
                self.options[self.options_cursor].action('>>')
            except Exception as e:
                usysf.log(f"MENUOPTION INCREASE ERROR: {e}")

        if key == "ENTER":
            try:
                self.options[self.options_cursor].action()
            except Exception as e:
                usysf.log(f"MENUOPTION ACTIVATE ERROR: {e}")

        if key == "CLOSE":
            self.close()
