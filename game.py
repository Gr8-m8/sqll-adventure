"""sqllite3 import"""
import sqlite3
import os

from menu import Menu, MenuItem, MenuOption, MenuTitle 


def clear():
    """Clear Console"""
    os.system('cls' if os.name == 'nt' else 'clear')

class ManagerDB():
    """db communication"""
    def __init__(self):
        self.db = sqlite3.connect('game.db')
        self.cursor = self.db.cursor()

    def save(self):
        """save db"""
        self.db.commit()

    def insert(self, table, datav, debug = False):
        """data into db"""
        data = ', '.join(datav)

        cmd = f"INSERT INTO {table} VALUES ({data});"
        return self.cursor.execute(cmd).fetchall() if not debug else cmd

    def update(self, table, datakv, identifierkv, debug = False):
        """change data in db"""
        data = ', '.join(f"{k}={v}" for k,v in datakv.items())
        data.replace(':', '=')

        identifier = ' AND '.join(f"{k}={v}" for k,v in identifierkv.items())
        identifier.replace(':', '=')

        cmd = f"UPDATE {table} SET {data} WHERE {(identifier)};"
        return self.cursor.execute(cmd).fetchall() if not debug else cmd

    def select(self, table, datak, identifierkv = None, debug = False):
        """get data in db"""
        data = ', '.join(datak)
        if identifierkv:
            identifier = ' AND '.join(f"{k}={v}" for k,v in identifierkv.items())
            identifier.replace(':', '=')
        else:
            identifier = None

        cmd = f"SELECT {data} FROM {table} WHERE {(identifier)}" if identifier else f"SELECT {data} FROM {table}"
        return self.cursor.execute(cmd).fetchall() if not debug else cmd

    def delete(self, table, identifierkv, debug):
        """remove data in db"""
        identifier = ' AND '.join(f"{k}={v}" for k,v in identifierkv.items())
        identifier.replace(':','=')

        cmd = f"DELETE FROM {table} WHERE identifier"
        return self.cursor.execute(cmd).fetchall() if not debug else cmd

    def table_len(self, table):
        """len of table in db"""
        ret = self.select(table, ['count(*)'])
        return int(ret[0][0])

class User:
    """user table object"""
    TABLE = "users"
    TABLEKEY = "user_id"
    def __init__(self, user_id, name, mail):
        self.user_id = user_id
        self.name = name
        self.mail = mail

    def __str__(self):
        return f"({self.user_id}, {self.name}, {self.mail})"

    @staticmethod
    def create(db, name, mail):
        """new user table row"""
        user_id = User.len(db)+1
        db.insert(User.TABLE, [str(user_id), '"'+name+'"', '"'+mail+'"'])
        return str(user_id)

    @staticmethod
    def login(db, user_id):
        """current game user"""
        attr = db.select(User.TABLE, ['*'], {User.TABLEKEY: user_id})[0]
        return User(attr[0], attr[1], attr[2])

    @staticmethod
    def list(db, title = False):
        """user table entries"""
        ret = ""
        ret += "(user_id, name, mail)\n" if title else ""
        for user in db.select(User.TABLE, ['*']):
            ret += f"{user}\n"
        return ret

    @staticmethod
    def len(db):
        """len user table entries"""
        return db.table_len(User.TABLE)

class Character:
    """character table object"""
    TABLE = "characters"
    TABLEKEY = "character_id"
    def __init__(self, character_id, name, description, location_id, user_id):
        self.character_id = character_id
        self.name = name
        self.description = description
        self.location_id = location_id
        self.user_id = user_id

    def __str__(self):
        return f"({self.character_id}, {self.name}, {self.description}, {self.location_id}, {self.user_id})"

    @staticmethod
    def create(db, name, description, user_id, location_id = '"NULL"', ):
        """new character table row"""
        character_id = Character.len(db)+1
        db.insert(Character.TABLE, [str(character_id), '"'+name+'"', '"'+description+'"', str(location_id), str(user_id)])
        return str(character_id)

    @staticmethod
    def login(db, character_id, user_id):
        """current user character"""
        attr = db.select(Character.TABLE, ['*'], {Character.TABLEKEY: character_id, User.TABLEKEY: user_id})[0]
        return Character(attr[0],attr[1],attr[2],attr[3] if attr[3] else "NULL",attr[4])

    @staticmethod
    def list(db, user_id = None, title = False):
        """character table entries"""
        ret = ""
        ret += "(character_id, name, description, location_id, user_id)\n" if title else ""
        query = db.select(Character.TABLE, ['*']) if not user_id else db.select(Character.TABLE, ['*'], {User.TABLEKEY: user_id})
        for character in query: 
            ret += f"{character}\n"
        return ret

    @staticmethod
    def len(db):
        """len character table entries"""
        return db.table_len(Character.TABLE)

    def move(self, db, location_id):
        """change character location"""
        return db.update(Character.TABLE, {Location.TABLEKEY: location_id}, {Character.TABLEKEY: self.character_id})


class Location:
    """location table object"""
    TABLE = "locations"
    TABLEKEY = "location_id"
    def __init__(self, location_id, name, description):
        self.location_id = location_id
        self.name = name
        self.description = description

    def __str__(self):
        return f"({self.location_id}, {self.name}, {self.description})"

    @staticmethod
    def create(db, name, description):
        """new location table row"""
        location_id = Location.len(db)+1
        db.insert(Location.TABLE, [location_id, name, description])
        return str(location_id)

    @staticmethod
    def list(db, title = False):
        """location table entries"""
        ret = ""
        ret += "(location_id, name, description)\n" if title else ""
        for location in db.select(Location.TABLE, ['*']): ret += f"{location}\n"
        return ret

    @staticmethod
    def len(db):
        """len location table entries"""
        return db.table_len(Location.TABLE)


class Game:
    """local game"""
    def __init__(self):
        self.user = None
        self.character = None

    def set_user(self, user):
        """assign game user"""
        self.user = user

    def set_character(self, character):
        """assign game character"""
        self.character = character

def console_menu(db, game):
    """Console Menu Interface"""
    clear()
    mainloop = True
    while (mainloop):
        print(f"{''.join('=' for i in range(50))}\n{''.join(' ' for i in range(20))}ADVENTURE GAME \n")
        print(User.list(db, True))

        inp = input("select account (by id)\n> ")
        if not inp.isdigit() or int(inp) < 1 or int(inp) > db.table_len(User.TABLE):
            print("Create Account")
            name = input("Account Name\n> ")
            mail = input("Account Mail\n> ")
            inp = User.create(db, name, mail)
            db.save()
        game.user = User.login(db, inp)

        print(Character.list(db, game.user.user_id, True))
        #print(db.select(Character.TABLE, ['*'], {User.TABLEKEY: game.user.user_id}))

        inp = input("select character (by id)\n> ")
        if not inp.isdigit() or int(inp) < 1 or int(inp) > db.table_len(Character.TABLE):
            print("Create Character")
            name = input("Character Name\n> ")
            description = input("Character Description\n> ")
            inp = Character.create(db, name, description, game.user.user_id)
            db.save()
        game.character = Character.login(db, inp, game.user.user_id)
            

        clear()
        gameloop = True
        while (gameloop):
            print(f"AT {db.select(Location.TABLE, ['*'], {Location.TABLEKEY: game.character.location_id})} AS {game.character}\n")
            characters = db.select(Character.TABLE, ['*'], {Location.TABLEKEY: game.character.location_id, f"NOT {Character.TABLEKEY}":game.character.character_id})
            print(f"{'\n'.join(f'{character}' for character in characters)}\n")
            print(Location.list(db))

            inp = input("select location (by id)\n> ")
            if not inp.isdigit() or int(inp) < 1 or int(inp) > db.table_len(Location.TABLE):
                print("Create Location")
                name = input("Location Name\n> ")
                description = input("Location Description\n> ")
                inp = Location.create(db, name, description)
            game.character.move(db, inp)
            game.character.location_id = inp
            db.save()

            clear()

def main():
    """main scrip execution"""
    db = ManagerDB()
    game = Game()

    users = ["New User"]
    users_raw = User.list(db).splitlines()
    for user in users_raw:
        users.append(MenuOption(text=user, action=lambda: game.set_user(User.login(db, usermenu.options_cursor))))
    usermenu = Menu(MenuTitle("Adventure Game"),MenuItem("Select User"),users)
    usermenu.open()

    #characters


main()
