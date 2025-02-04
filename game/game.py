"""db game"""
import sqlite3
import mariadb
import os

from menu import Menu, MenuItem, MenuOption, MenuTitle


class EnvManager:
    """manage env var"""
    def __init__(self):
        self.load()

    def load(self):
        """import env var"""
        try:
            with open('.env', 'r', encoding='utf-8') as envfile:
                for line in envfile:
                    if '=' in line:
                        #print(line.split('=')[0], "=", line.split('=')[1])
                        os.environ[line.split('=')[0]] = line.split('=')[1].replace('"','').strip()
        except FileNotFoundError:
            open('.env', 'x')
        except Exception as e:
            exit(1)

    def get(self, key:str) -> str:
        """set none var & read env var"""
        if not key in os.environ:
            os.environ[key] = input(f"Set {key}").replace('"','').strip()
        return os.environ[key]


def set_env():
    """import env var"""
    with open('.env', 'r', encoding='utf-8') as envfile:
        for line in envfile:
            if '=' in line:
                #print(line.split('=')[0], "=", line.split('=')[1])
                os.environ[line.split('=')[0]] = line.split('=')[1].replace('"','').strip()

set_env()

def clear(active=True):
    """Clear Console"""
    if active:
        os.system('cls' if os.name == 'nt' else 'clear')


def log():
    """print to log file"""
    # open(".log", "w")


class ManagerDB:
    """db communication"""
    def __init__(self, env: EnvManager):
        self.create_table(User.TABLE, User.SCHEMA)
        self.create_table(Location.TABLE, Location.SCHEMA)
        self.create_table(Character.TABLE, Character.SCHEMA)

    def close(self):
        """close db connection"""
        return None

    def raw(self, cmd, debug=False) -> str:
        """raw sql cmd"""
        return cmd

    def create_table(self, table: str, schema: str, debug: bool = False) -> str:
        """table into db"""
        cmd = f"CREATE TABLE IF NOT EXISTS {table} ({schema});"
        return cmd

    def save(self) -> None:
        """save db"""
        return None

    def insert(self, table: str, datav: list, debug: bool = False) -> str:
        """data into db"""
        data = ', '.join(datav)

        cmd = f"INSERT INTO {table} VALUES ({data});"
        return cmd

    def update(self, table: str, datakv: list, identifierkv: dict, debug: bool = False) -> str:
        """change data in db"""
        data = ', '.join(f"{k}={v}" for k, v in datakv.items())
        data.replace(':', '=')

        identifier = ' AND '.join(f"{k}={v}" for k, v in identifierkv.items())
        identifier.replace(':', '=')

        cmd = f"UPDATE {table} SET {data} WHERE {(identifier)};"
        return cmd

    def select(self, table: str, datak: list, identifierkv: dict = None, debug: bool = False) -> str:
        """get data in db"""
        data = ', '.join(datak)
        if identifierkv:
            identifier = ' AND '.join(
                f"{k}={v}" for k, v in identifierkv.items())
            identifier.replace(':', '=')
        else:
            identifier = None

        cmd = f"SELECT {data} FROM {table} WHERE {(identifier)}" if identifier else f"SELECT {data} FROM {table}"
        return cmd

    def delete(self, table: str, identifierkv: dict, debug: bool = False) -> str:
        """remove data in db"""
        identifier = ' AND '.join(f"{k}={v}" for k, v in identifierkv.items())
        identifier.replace(':', '=')

        cmd = f"DELETE FROM {table} WHERE identifier"
        return cmd

    def table_len(self, table: str) -> int:
        """len of table in db"""
        #ret = self.select(table, ['count(*)'])
        return 0

class MariaDB(ManagerDB):
    """Mariadb db communication"""

    def __init__(self, env: EnvManager):
        self.db = None
        self.cursor = None
        try:
            self.db = mariadb.connect(
                user=env.get('DB_USER'),
                password=env.get('DB_USER_PWD'),
                host=env.get('IP'),
                port=int(env.get('PORT')),
                database=env.get('DB')
            )
            self.cursor = self.db.cursor()
            self.db.autocommit = False
            super().__init__(env)
        except Exception as e:
            print(e)
            exit(1)

    def close(self):
        self.db.close()
        return super().close()

    def raw(self, cmd, debug=False):
        """raw sql cmd"""
        cmd = super().raw(cmd)
        return self.cursor.execute(cmd).fetchall() if not debug else cmd

    def create_table(self, table: str, schema: str, debug: bool = False) -> list:
        """table into db"""
        cmd = f"CREATE TABLE IF NOT EXISTS {table} ({schema});"
        return self.cursor.execute(cmd).fetchall() if not debug else cmd

    def save(self) -> None:
        """save db"""
        return self.db.commit()

    def insert(self, table: str, datav: list, debug: bool = False) -> list:
        """data into db"""
        cmd = super().insert(table, datav, debug)
        return self.cursor.execute(cmd).fetchall() if not debug else cmd

    def update(self, table: str, datakv: list, identifierkv: dict, debug: bool = False) -> list:
        """change data in db"""
        cmd = super().update(table, datakv, identifierkv, debug)
        return self.cursor.execute(cmd).fetchall() if not debug else cmd

    def select(self, table: str, datak: list, identifierkv: dict = None, debug: bool = False) -> list:
        """get data in db"""
        cmd = super().select(table, datak, identifierkv, debug)
        return self.cursor.execute(cmd).fetchall() if not debug else cmd

    def delete(self, table: str, identifierkv: dict, debug: bool = False) -> list:
        """remove data in db"""
        cmd = super().delete(table, identifierkv, debug)
        return self.cursor.execute(cmd).fetchall() if not debug else cmd

    def table_len(self, table: str) -> int:
        """len of table in db"""
        ret = self.select(table, ['count(*)'])
        return int(ret[0][0])

class Sqllite3DB(ManagerDB):
    """sqlite3 db communication"""

    def __init__(self, env: EnvManager):
        self.db = sqlite3.connect(env.get('DB'))
        self.cursor = self.db.cursor()
        super().__init__(env)

    def close(self):
        return super().close()

    def raw(self, cmd, debug=False):
        """raw sql cmd"""
        cmd = super().raw(cmd)
        return self.cursor.execute(cmd).fetchall() if not debug else cmd

    def create_table(self, table: str, schema: str, debug: bool = False) -> list:
        """table into db"""
        cmd = f"CREATE TABLE IF NOT EXISTS {table} ({schema});"
        return self.cursor.execute(cmd).fetchall() if not debug else cmd

    def save(self) -> None:
        """save db"""
        return self.db.commit()

    def insert(self, table: str, datav: list, debug: bool = False) -> list:
        """data into db"""
        cmd = super().insert(table, datav, debug)
        return self.cursor.execute(cmd).fetchall() if not debug else cmd

    def update(self, table: str, datakv: list, identifierkv: dict, debug: bool = False) -> list:
        """change data in db"""
        cmd = super().update(table, datakv, identifierkv, debug)
        return self.cursor.execute(cmd).fetchall() if not debug else cmd

    def select(self, table: str, datak: list, identifierkv: dict = None, debug: bool = False) -> list:
        """get data in db"""
        cmd = super().select(table, datak, identifierkv, debug)
        return self.cursor.execute(cmd).fetchall() if not debug else cmd

    def delete(self, table: str, identifierkv: dict, debug: bool = False) -> list:
        """remove data in db"""
        cmd = super().delete(table, identifierkv, debug)
        return self.cursor.execute(cmd).fetchall() if not debug else cmd

    def table_len(self, table: str) -> int:
        """len of table in db"""
        ret = self.select(table, ['count(*)'])
        return int(ret[0][0])

class Table:
    """Generic table object"""
    TABLE = "template"
    TABLEKEY = "template_id"
    SCHEMA = "template_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT"

    def __init__(self, table_id: str) -> None:
        self.table_id = table_id

    @staticmethod
    def create(db: ManagerDB) -> str:
        """new user table row"""
        table_id = Table.len(db)+1
        db.insert(Table.TABLE, [str(table_id)])
        db.save()
        return str(table_id)

    @staticmethod
    def get(db: ManagerDB, table_id: str) -> "Table":
        """current game user"""
        attr = db.select(Table.TABLE, ['*'], {User.TABLEKEY: table_id})[0]
        return Table(attr[0])

    @staticmethod
    def list(db: ManagerDB) -> list:
        """table entries"""
        ret = []
        for table in db.select(Table.TABLE, ['*']):
            ret.append(Table(table[0]))
        return ret

    @staticmethod
    def len(db: ManagerDB) -> int:
        """len user table entries"""
        return db.table_len(Table.TABLE)

    def id(self):
        """get id"""
        return self.table_id

class User(Table):
    """user table object"""
    TABLE = "users"
    TABLEKEY = "user_id"
    SCHEMA = "user_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, name varchar(255) NOT NULL, mail varchar(255) NOT NULL"

    def __init__(self, user_id: str, name: str, mail: str) -> None:
        super().__init__(user_id)
        self.user_id: str = user_id
        self.name: str = name
        self.mail: str = mail

    def __str__(self):
        return f"({self.user_id}, {self.name}, {self.mail})"

    @staticmethod
    def create(db: ManagerDB, name: str, mail: str) -> str:
        """new user table row"""
        user_id = User.len(db)+1
        db.insert(User.TABLE, [str(user_id), '"'+name+'"', '"'+mail+'"'])
        db.save()
        return str(user_id)

    @staticmethod
    def get(db: ManagerDB, user_id: str) -> "User":
        """current game user"""
        attr = db.select(User.TABLE, ['*'], {User.TABLEKEY: user_id})[0]
        return User(attr[0], attr[1], attr[2])

    @staticmethod
    def list(db: ManagerDB) -> list:
        """user table entries"""
        ret = []
        for user in db.select(User.TABLE, ['*']):
            ret.append(User(user[0], user[1], user[2]))
        return ret

    @staticmethod
    def len(db: ManagerDB) -> int:
        """len user table entries"""
        return db.table_len(User.TABLE)

    def id(self) -> str:
        """get id"""
        return self.user_id

    def display(self) -> str:
        """display str"""
        return f"{self.name} ({self.mail})"

class Character(Table):
    """character table object"""
    TABLE = "characters"
    TABLEKEY = "character_id"
    SCHEMA = "character_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, name varchar(255) NOT NULL, description varchar(255), location_id REFERENCES location(id), user_id REFERENCES users(id) NOT NULL"

    def __init__(self, character_id: str, name: str, description: str, location_id: str, user_id: str) -> None:
        super().__init__(character_id)
        self.character_id = character_id
        self.name = name
        self.description = description
        self.location_id = location_id
        self.user_id = user_id

    def __str__(self):
        return f"({self.character_id}, {self.name}, {self.description}, {self.location_id}, {self.user_id})"

    @staticmethod
    def create(db: ManagerDB, name: str, description: str, user_id: str, location_id: str = '"NULL"') -> str:
        """new character table row"""
        character_id = Character.len(db)+1
        db.insert(Character.TABLE, [str(
            character_id), '"'+name+'"', '"'+description+'"', str(location_id), str(user_id)])
        db.save()
        return str(character_id)

    @staticmethod
    def get(db: ManagerDB, character_id: str, user_id: str) -> "Character":
        """current user character"""
        attr = db.select(Character.TABLE, [
                         '*'], {Character.TABLEKEY: character_id, User.TABLEKEY: user_id})[0]
        return Character(attr[0], attr[1], attr[2], attr[3] if attr[3] else "NULL", attr[4])

    @staticmethod
    def list(db: ManagerDB, user_id: str = None) -> list:
        """character table entries"""
        ret = []
        query = db.select(
            Character.TABLE, ['*']) if not user_id else db.select(Character.TABLE, ['*'],{User.TABLEKEY: user_id})
        for character in query:
            ret.append(
                Character(
                    character_id=character[0],
                    name=character[1],
                    description=character[2],
                    location_id=character[3],
                    user_id=character[4]
                )
            )
        return ret

    @staticmethod
    def len(db: ManagerDB):
        """len character table entries"""
        return db.table_len(Character.TABLE)

    def move(self, db: ManagerDB, location_id: str) -> list:
        """change character location"""
        return db.update(
            Character.TABLE,
            {Location.TABLEKEY: location_id},
            {Character.TABLEKEY: self.character_id}
        )

    def id(self) -> str:
        """get id"""
        return self.character_id

    def display(self) -> str:
        """display str"""
        return f"{self.name} ({self.description})"


class Location(Table):
    """location table object"""
    TABLE = "locations"
    TABLEKEY = "location_id"
    SCHEMA = "location_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, name varchar(255) NOT NULL, description varchar(255)"

    def __init__(self, location_id: str, name: str, description: str) -> None:
        super().__init__(location_id)
        self.location_id = location_id
        self.name = name
        self.description = description

    def __str__(self):
        return f"({self.location_id}, {self.name}, {self.description})"

    @staticmethod
    def create(db: ManagerDB, name: str, description: str) -> str:
        """new location table row"""
        location_id = Location.len(db)+1
        db.insert(Location.TABLE, [str(location_id),
                  '"'+name+'"', '"'+description+'"'])
        db.save()
        return str(location_id)

    @staticmethod
    def list(db: ManagerDB, location_id_exclude: str = None) -> list:
        """location table entries"""
        ret = []
        query = db.select(Location.TABLE, ['*']) if not location_id_exclude else db.select(
            Location.TABLE, ['*'], {f"NOT {Location.TABLEKEY}": location_id_exclude})
        for location in query:
            ret.append(Location(location[0], location[1], location[2]))
        return ret

    @staticmethod
    def len(db: ManagerDB) -> int:
        """len location table entries"""
        return db.table_len(Location.TABLE)

    @staticmethod
    def get(db: ManagerDB, location_id: str = None) -> "Location":
        """current character Location"""
        if location_id is None or location_id == "NULL":
            return Location(-1, "None", "Nowhere")

        attr = db.select(Location.TABLE, ['*'],
                         {Location.TABLEKEY: location_id})[0]
        return Location(attr[0], attr[1], attr[2])

    def id(self) -> str:
        """get id"""
        return self.location_id

    def display(self) -> str:
        """display str"""
        return f"{self.name} ({self.description})"


class Game:
    """local game"""

    def __init__(self):
        self.user: User = None
        self.character: Character = None

    def set_user_create(self, db: ManagerDB, menu: Menu) -> None:
        """create and assign game user"""
        name = input("Account Name\n> ")
        mail = input("Account Mail\n> ")
        self.set_user(User.create(db, name, mail), db, menu)

    def set_user(self, user_id: str, db: ManagerDB, menu: Menu) -> None:
        """assign game user"""
        self.user = User.get(db, user_id)
        menu.close()

    def set_character_create(self, db: ManagerDB, menu: Menu) -> None:
        """create and assign game character"""
        name = input("Character Name\n> ")
        description = input("Character Description\n> ")
        self.set_character(Character.create(
            db, name, description, self.user.user_id), self.user.user_id, db, menu)

    def set_character(self, character_id: str, user_id: str, db: ManagerDB, menu: Menu) -> None:
        """assign game character"""
        self.character = Character.get(db, character_id, user_id)
        menu.close()

    def set_location_create(self, db: ManagerDB, menu: Menu) -> None:
        """create and assign game character location"""
        name = input("Location Name\n> ")
        description = input("Location Description\n> ")
        self.set_location(Location.create(db, name, description), db, menu)

    def set_location(self, location_id: str, db: ManagerDB, menu: Menu) -> None:
        """assign game characer location"""
        self.character.move(db, location_id)
        self.character.location_id = location_id
        menu.close()
        db.save()

    def exit(self, db: ManagerDB) -> None:
        """Terminate Game"""
        db.close()
        clear()
        exit(0)

def main_game(game: Game, db: ManagerDB):
    """main game func"""
    # Menu.display_menu(Menu(MenuTitle("New User"),MenuItem(""), [MenuOption()])))]
    users = [MenuOption(
        text="New User", action=lambda: game.set_user_create(db, usermenu))]
    for user in User.list(db):
        users.append(MenuOption(
            text=user, action=lambda id=user.user_id: game.set_user(id, db, usermenu)))

    usermenu = Menu(MenuTitle("Adventure Game"),
                    MenuItem("Select User"), users)
    Menu.display_menu(usermenu)

    characters = [MenuOption(
        text="New Character", action=lambda: game.set_character_create(db, charactermenu))]
    for character in Character.list(db, game.user.user_id):
        characters.append(
            MenuOption(
                text=character,
                action=lambda id=character.character_id: 
                game.set_character(id, game.user.user_id, db, charactermenu)
            )
        )

    charactermenu = Menu(
        MenuTitle("Adventure Game"),
        MenuItem("Select Character"),
        characters
    )
    Menu.display_menu(charactermenu)

    gameloop = True
    while gameloop and game.user and game.character:
        locations = [MenuOption(
            text="New Location", action=lambda: game.set_location_create(db, locationmenu))]
        for location in Location.list(db):
            locations.append(MenuOption(text=f"Go To: {location.display(
            )}", action=lambda id=location.location_id: game.set_location(id, db, locationmenu)))

        text = f"Character: {game.character.display()}\nAT {Location.get(db, game.character.location_id).display() if game.character.location_id else "None"}\n\nSelect Action"
        options = locations + \
            [MenuOption(text="Quit", action=lambda: game.exit(db))]

        locationmenu = Menu(MenuTitle("Adventure Game"),
                            MenuItem(text), options)
        Menu.display_menu(locationmenu)
        locationmenu.close()

def main():
    """main scrip execution"""
    #connect = input("Connect Server:Port")

    env: EnvManager = EnvManager()
    db: ManagerDB = MariaDB(env)
    game: Game = Game()

    main_game(game, db)

    


main()
