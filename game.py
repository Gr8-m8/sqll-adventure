"""db game"""
import sqlite3
try:
    import mariadb
    OFFLINE = False
except ModuleNotFoundError:
    OFFLINE = True
import os

from menu import Menu, MenuItem, MenuOption, MenuTitle

class ServerConnection:
    """server connection"""
    def __init__(self):
        self.SERVER_HOST_PASSWORD="PASSWORD"
        self.DB_GAME_USER="game"
        self.DB_GAME_USER_PWD="game"
        self.DB_IP="127.0.0.1"
        self.DB_PORT="3306"
        self.DB_FILE="game.db"
        self.offline = True

    def get_data_txt(self) -> list:
        """connection data as str kv list"""
        return [
            f'SERVER_HOST_PASSWORD="{self.SERVER_HOST_PASSWORD}"',
            f'DB_GAME_USER="{self.DB_GAME_USER}"',
            f'DB_GAME_USER_PWD="{self.DB_GAME_USER_PWD}"',
            f'DB_IP="{self.DB_IP}"',
            f'DB_PORT="{self.DB_PORT}"',
            f'DB_FILE="{self.DB_FILE}"',
        ]
    
    def get_data(self) -> list:
        """connection data as v list"""
        return [
            self.SERVER_HOST_PASSWORD,
            self.DB_GAME_USER,
            self.DB_GAME_USER_PWD,
            self.DB_IP,
            self.DB_PORT,
            self.DB_FILE,
        ]

    def set_offline(self, val: bool):
        """set offline status"""
        self.offline = val

    def set_server_host_pw(self, val: str):
        """set db root pw"""
        self.SERVER_HOST_PASSWORD = val

    def set_ip(self, val: str):
        """set db ip"""
        self.DB_IP = val

    def set_port(self, val: str):
        """set db port"""
        self.DB_PORT = val

    def set_game_user(self, val: str):
        """set db service user"""
        self.DB_GAME_USER = val

    def set_game_user_pw(self, val: str):
        """set db service user pw"""
        self.DB_GAME_USER_PWD=val

    def set_db_file(self, val: str):
        """set db file"""
        self.DB_FILE=val

    def toENV(self, data: list = None):
        """values to .env for docker host"""
        try:
            open('.env', 'x', encoding='utf-8')
        except Exception as e:
            print(e)
        with open('.env', 'w', encoding='utf-8') as file:
            if not data:
                data = self.get_data_txt()
            for dataentry in data:
                file.write(dataentry+"\n")
            file.close()


    def toServerList(self, listname: str) -> list:
        """connection history"""
        try:
            open(f'{listname}_server.data', 'x', encoding='utf-8')
        except Exception as e:
            print(e)
        with open(f'{listname}_server.data', 'a', encoding='utf-8') as file:
            data = self.get_data_txt()
            file.write('|'.join(data)+"\n")
            file.close()
        return data

def clear(active=True):
    """Clear Console"""
    if active:
        os.system('cls' if os.name == 'nt' else 'clear')


def log(msg):
    """print to log file"""
    with open(".log", "a") as logfile:
        fs = f"{msg}\n"
        logfile.write(fs)


class ManagerDB:
    """db communication"""
    def __init__(self, connection: ServerConnection):
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

    def update(self, table: str, datakv: dict, identifierkv: dict, debug: bool = False) -> str:
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
            identifier = ' AND '.join(f"{k}={v}" for k, v in identifierkv.items())
            identifier.replace(':', '=')
        else:
            identifier = None

        fs1 = f"SELECT {data} FROM {table} WHERE {(identifier)}"
        fs2 = f"SELECT {data} FROM {table}"
        cmd = fs1 if identifier else fs2
        return cmd

    def delete(self, table: str, identifierkv: dict, debug: bool = False) -> str:
        """remove data in db"""
        identifier = ' AND '.join(f"{k}={v}" for k, v in identifierkv.items())
        identifier.replace(':', '=')

        cmd = f"DELETE FROM {table} WHERE identifier"
        return cmd

    def table_len(self, table: str) -> int:
        """len of table in db"""
        ret = 0
        get = self.select(table, ['count(*)'])
        if get:
            ret = get
        return get if get else ret

class MariaDB(ManagerDB):
    """Mariadb db communication"""

    def __init__(self, connection: ServerConnection):
        self.db = None
        self.cursor = None
        try:
            self.db = mariadb.connect(
                user=str(connection.DB_GAME_USER),
                password=str(connection.DB_GAME_USER_PWD),
                host=str(connection.DB_IP),
                port=int(str(connection.DB_PORT)),
                database=str(connection.DB_FILE)
            )
            self.cursor = self.db.cursor()
            self.db.autocommit = False
            super().__init__(connection)
        except mariadb.Error as e:
            print("MARIADB ERROR:", e)
            exit(1)

    def close(self):
        self.db.close()
        return super().close()

    def raw(self, cmd, debug=False):
        """raw sql cmd"""
        cmd = super().raw(cmd)
        val = self.cursor.execute(cmd) if not debug else cmd
        try:
            return self.cursor.fetchall()
        except:
            return []

    def create_table(self, table: str, schema: str, debug: bool = False) -> list:
        """table into db"""
        cmd = f"CREATE TABLE IF NOT EXISTS {table} ({schema});"
        val = self.cursor.execute(cmd) if not debug else cmd
        try:
            return self.cursor.fetchall()
        except:
            return []

    def save(self) -> None:
        """save db"""
        return self.db.commit()

    def insert(self, table: str, datav: list, debug: bool = False) -> list:
        """data into db"""
        cmd = super().insert(table, datav, debug)
        val = self.cursor.execute(cmd) if not debug else cmd
        return

    def update(self, table: str, datakv: list, identifierkv: dict, debug: bool = False) -> list:
        """change data in db"""
        cmd = super().update(table, datakv, identifierkv, debug)
        val= self.cursor.execute(cmd) if not debug else cmd
        try:
            return self.cursor.fetchall()
        except:
            return []

    def select(self, table: str, datak: list, identifierkv: dict = None, debug: bool = False) -> list:
        """get data in db"""
        cmd = super().select(table, datak, identifierkv, debug)
        val = self.cursor.execute(cmd) if not debug else cmd
        try:
            return self.cursor.fetchall()
        except:
            return []

    def delete(self, table: str, identifierkv: dict, debug: bool = False) -> list:
        """remove data in db"""
        cmd = super().delete(table, identifierkv, debug)
        val= self.cursor.execute(cmd) if not debug else cmd
        try:
            return self.cursor.fetchall()
        except:
            return []

    def table_len(self, table: str) -> int:
        """len of table in db"""
        val = self.select(table, ['count(*)'])
        val = val[0][0]
        try:
            return val
        except:
            return 0

class Sqllite3DB(ManagerDB):
    """sqlite3 db communication"""

    def __init__(self, connection: ServerConnection):
        self.db = sqlite3.connect(connection.DB_FILE)
        self.cursor = self.db.cursor()
        super().__init__(connection)

    def close(self):
        return super().close()

    def raw(self, cmd, debug=False):
        """raw sql cmd"""
        cmd = super().raw(cmd)
        return self.cursor.execute(cmd).fetchall() if not debug else cmd

    def create_table(self, table: str, schema: str, debug: bool = False) -> list:
        """table into db"""
        cmd = f"CREATE TABLE IF NOT EXISTS {table} ({schema});"
        return self.cursor.execute(cmd) if not debug else cmd

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
    SCHEMA = "template_id INTEGER NOT NULL PRIMARY KEY"

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
    SCHEMA = "user_id INTEGER NOT NULL PRIMARY KEY, name varchar(255) NOT NULL, mail varchar(255) NOT NULL"

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
        users = db.select(User.TABLE, ['*'])
        if users:
            for user in users:
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
    sqlite_SCHEMA = "character_id INTEGER NOT NULL PRIMARY KEY, name varchar(255) NOT NULL, description varchar(255), location_id REFERENCES location(id), user_id REFERENCES users(id) NOT NULL"
    SCHEMA = "character_id INTEGER NOT NULL PRIMARY KEY, name varchar(255) NOT NULL, description varchar(255), location_id varchar(255), user_id varchar(255), action varchar(1023)"

    def __init__(self, character_id: str, name: str, description: str, location_id: str, user_id: str, action: str) -> None:
        super().__init__(character_id)
        self.character_id = character_id
        self.name = name
        self.description = description
        self.location_id = location_id
        self.user_id = user_id
        self.action = action

    def __str__(self):
        return f"({self.character_id}, {self.name}, {self.description}, {self.location_id}, {self.user_id}, {self.action})"

    @staticmethod
    def create(db: ManagerDB, name: str, description: str, user_id: str, location_id: str = 'NULL') -> str:
        """new character table row"""
        character_id = Character.len(db)+1
        db.insert(Character.TABLE, [str(character_id), '"'+name+'"', '"'+description+'"', str(location_id), str(user_id), '"New"'])
        db.save()
        return str(character_id)

    @staticmethod
    def get(db: ManagerDB, character_id: str, user_id: str) -> "Character":
        """current user character"""
        attr = db.select(
            Character.TABLE,
            ['*'],
            {
                Character.TABLEKEY: character_id,
                User.TABLEKEY: user_id
            }
        )[0]
        return Character(attr[0], attr[1], attr[2], attr[3] if attr[3] else "NULL", attr[4], attr[5])

    @staticmethod
    def list(db: ManagerDB, user_id: str = None, location_id: str = None, character_id: str = None) -> list:
        """character table entries"""
        ret = []
        where = {}
        where.update({User.TABLEKEY: user_id}) if user_id else None
        where.update({Location.TABLEKEY: location_id}) if location_id else None
        fs = f"NOT {Character.TABLEKEY}"
        where.update({fs: character_id}) if location_id else None

        user_characters = db.select(Character.TABLE, ['*']) if not (user_id or location_id or character_id) else db.select(Character.TABLE, ['*'], where)
        if (user_characters):
            for character in user_characters:
                ret.append(
                    Character(
                        character_id=character[0],
                        name=character[1],
                        description=character[2],
                        location_id=character[3],
                        user_id=character[4],
                        action=character[5]
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

    def action_do(self, db: ManagerDB, action: str) -> list:
        """change character action"""
        return db.update(
            Character.TABLE,
            {"action": '"'+action+'"'},
            {Character.TABLEKEY: self.character_id}
        )

    def id(self) -> str:
        """get id"""
        return self.character_id

    def display(self) -> str:
        """display str"""
        return f"{self.name} ({self.description}) \"{self.action}\""


class Location(Table):
    """location table object"""
    TABLE = "locations"
    TABLEKEY = "location_id"
    SCHEMA = "location_id INTEGER NOT NULL PRIMARY KEY, name varchar(255) NOT NULL, description varchar(255)"

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
        db.insert(Location.TABLE, [str(location_id), '"'+name+'"', '"'+description+'"'])
        db.save()
        return str(location_id)

    @staticmethod
    def list(db: ManagerDB, location_id_exclude: str = None) -> list:
        """location table entries"""
        ret = []
        fs = f"NOT {Location.TABLEKEY}"
        locations = db.select(Location.TABLE, ['*']) if not location_id_exclude else db.select(Location.TABLE, ['*'], {fs: location_id_exclude})
        if locations:
            for location in locations:
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
        self.start = False
        self.user: User = User("0", "NULL", "NULL")
        self.character: Character = Character("0", "NULL", "NULL", "NULL", "NULL", "NULL")

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
        self.set_character(
            Character.create(
                db,
                name,
                description,
                self.user.user_id),
            self.user.user_id,
            db,
            menu
        )

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

    def action_character(self, db: ManagerDB, menu: Menu, action: str):
        """set character action"""
        self.character.action_do(db, action)
        self.character.action = action
        menu.close()
        db.save()

    def exit(self, db: ManagerDB) -> None:
        """Terminate Game"""
        db.close()
        clear()
        exit(0)

def main_game(game: Game, db: ManagerDB):
    """main game func"""
    users = [MenuOption(
        text="New User", action=lambda: game.set_user_create(db, usermenu))]
    for user in User.list(db):
        users.append(MenuOption(
            text=user, action=lambda id=user.user_id: game.set_user(id, db, usermenu)))

    usermenu = Menu(MenuTitle("Adventure Game"),
                    MenuItem("Select User"), users)
    Menu.display_menu(usermenu)

    if game.user.user_id == "0":
        game.exit(db)

    characters = [MenuOption(text="New Character", action=lambda: game.set_character_create(db, charactermenu))]
    for character in Character.list(db, user_id=game.user.user_id):
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

    if game.character.character_id == "0":
        game.exit(db)

    gameloop = True
    while gameloop and game.user and game.character:
        locations = [
            MenuOption(text="Reload", action=lambda: locationmenu.close()),
            MenuOption(text="Action", action=lambda: game.action_character(db, locationmenu, input("Action\n> "))),
            MenuOption(text="New Location", action=lambda: game.set_location_create(db, locationmenu))
        ]
        for location in Location.list(db):
            fs = f"Go To: {location.display()}"
            locations.append(MenuOption(text=fs, action=lambda id=location.location_id: game.set_location(id, db, locationmenu)))

        character = game.character.display()
        location = Location.get(db, game.character.location_id).display() if game.character.location_id else "None"
        character_other = Character.list(db, location_id=game.character.location_id, character_id=game.character.character_id)
        character_other = '\n'.join(c.display() for c in character_other) if len(character_other)>0 else "Noone"
        text = f"Character: {character}\nAT {location}\n\nWITH\n{character_other}\n\nSelect Action"
        options = locations + \
            [MenuOption(text="Quit", action=lambda: game.exit(db))]

        locationmenu = Menu(MenuTitle("Adventure Game"),
                            MenuItem(text),
                            options
                        )
        Menu.display_menu(locationmenu)
        locationmenu.close()

def menu_host(game: Game, db: ManagerDB):

    def status():
        status = os.system("docker ps -f name=sql-adventure-db --format \"table {{.Status}}\"")
        input("CONTINUE")
        return status


    def host_start(connection: ServerConnection):
        try:
            status = os.system("docker-compose up -d")
        except:
            status = None
        try:
            status = os.system("docker-compose up -d")
        except:
            status = None
        input("CONTINUE")
        return status
    
    
    def host_stop():
        try:
            status = os.system("docker-compose down")
        except:
            status = None
        try:
            status = os.system("docker-compose down")
        except:
            status = None
        input("CONTINUE")
        return status
    
    def host_connect_confirm(menu:Menu, connection: ServerConnection):
        connection.toServerList("host")
        connection.toENV()
        menu.close()
    
    connection: ServerConnection = ServerConnection()
    connect_menu = Menu(
        MenuTitle("Adventure Game"),
        MenuItem("Connect Menu"),
        [
            MenuOption("Return", action=lambda: host_connect_confirm(connect_menu, connection)),
            MenuOption("Connect IP",  action=lambda: connection.set_ip(input("> "))),
            MenuOption("Connect Port", action=lambda: connection.set_port(input("> "))),
            MenuOption("Connect Host Password", action=lambda: connection.set_server_host_pw(input("> "))),
            MenuOption("Advanced Connect DB_FILE", action=lambda: connection.set_db_file(input("> "))),
            MenuOption("Advanced Connect DB_GAME_USER", action=lambda: connection.set_game_user(input("> "))),
            MenuOption("Advanced Connect DB_GAME_USER_PW", action=lambda: connection.set_game_user_pw(input("> "))),
            
        ]
    )
    
    host_menu = Menu(
        MenuTitle("Adventure Game"),
        MenuItem("Host Menu"),
        [
            MenuOption("Return", action= lambda: host_menu.close()),
            MenuOption("Configure Host", action=lambda: Menu.display_menu(connect_menu)),
            MenuOption("Start Host", action=lambda c=connection: host_start(c)),
            MenuOption("Stop Host", action= lambda: host_stop()),
            MenuOption("Status Host", action= lambda: "")
        ]
    )

    Menu.display_menu(host_menu)

def menu_connect(game: Game, menu: Menu, connection: ServerConnection):
    menu.close()
    connection.set_offline(False)

    def connect_confirm(connection: ServerConnection, game: Game):
        game.start = True
        connection.toServerList("connection")
        connect_menu.close()
    connect_menu = Menu(
        MenuTitle("Adventure Game"),
        MenuItem("Connect Menu"),
        [
            MenuOption("Confirm", action=lambda: connect_confirm(connection, game)),
            MenuOption("Connect IP",  action=lambda: connection.set_ip(input("> "))),
            MenuOption("Connect Port", action=lambda: connection.set_port(input("> "))),
            MenuOption("Advanced Connect DB_FILE", action=lambda: connection.set_db_file(input("> "))),
            MenuOption("Advanced Connect DB_GAME_USER", action=lambda: connection.set_game_user(input("> "))),
            MenuOption("Advanced Connect DB_GAME_USER_PW", action=lambda: connection.set_game_user_pw(input("> "))),
            
        ]
    )
    Menu.display_menu(connect_menu)

def menu_main(game: Game, db: ManagerDB, connection: ServerConnection):

    def main_menu_play(menu: Menu, game: Game):
        game.start=True
        menu.close()

    main_menu = Menu(
        MenuTitle("Adventure Game"),
        MenuItem("Main Menu"),
        [
            MenuOption("Play Offline", action=lambda: main_menu_play(main_menu, game)),
            MenuOption("Play Online", action=lambda: menu_connect(game, main_menu, connection)) if not OFFLINE else MenuOption("X Play Online Disabled"),
            MenuOption("Host Server", action=lambda: menu_host(game, db)) if not OFFLINE else MenuOption("X Host Server Disabled"),
            MenuOption("Quit Game", action=lambda: game.exit(db)),
        ]
    )

    Menu.display_menu(main_menu)


def main():
    """main scrip execution"""
    #connect = input("Connect Server:Port")

    connection: ServerConnection = ServerConnection()
    db: ManagerDB = ManagerDB(connection)
    game: Game = Game()
    
    menu_main(game, db, connection)

    if connection.offline or OFFLINE:
        db = Sqllite3DB(connection)
    else:
        db = MariaDB(connection)

    if game.start:
        main_game(game, db)

main()
