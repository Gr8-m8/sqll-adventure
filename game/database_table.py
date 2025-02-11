import usysf
from database import ManagerDB

class Table:
    """Generic table object"""
    TABLE = "template"
    TABLEKEY = "template_id"
    SCHEMA = "template_id INTEGER NOT NULL PRIMARY KEY"

    @classmethod
    def INIT(cls, db: ManagerDB):
        """SETUP DATABASE TABLE"""
        db.create_table(cls.TABLE, cls.SCHEMA)

    def __init__(self, table_id: str) -> None:
        self.table_id = table_id

    def __str__(self):
        return f"{self.table_id}"

    @staticmethod
    def create(table: "Table", db: ManagerDB) -> str:
        """new user table row"""
        table_id = table.len(db)+1
        db.insert(table.TABLE, [f'{table_id}'])
        db.save()
        return str(table_id)

    @staticmethod
    def get(table: "Table", db: ManagerDB, table_id: str) -> "Table":
        """current game user"""
        attr = db.select(table.TABLE, ['*'], {table.TABLEKEY: table_id})[0]
        usysf.log(attr)
        return table(*attr)

    @staticmethod
    def list(table: "Table", db: ManagerDB) -> list:
        """table entries"""
        ret = []
        for row in db.select(table.TABLE, ['*']):
            ret.append(table(*row))
        return ret

    @staticmethod
    def len(table: "Table", db: ManagerDB) -> int:
        """len user table entries"""
        return db.table_len(table.TABLE)

    def id(self):
        """get id"""
        return self.table_id

    def display(self) -> str:
        """display str"""
        return f"{self.table_id}"

class User(Table):
    """user table object"""
    TABLE = "users"
    TABLEKEY = "user_id"
    SCHEMA = "user_id INTEGER NOT NULL PRIMARY KEY, name varchar(255) NOT NULL, mail varchar(255) NOT NULL"

    def __init__(self, user_id: str, name: str, mail: str) -> None:
        self.user_id: str = user_id
        self.name: str = name
        self.mail: str = mail

    @staticmethod
    def create(db: ManagerDB, name: str, mail: str) -> str:
        """new user table row"""
        user_id = User.len(User, db)+1
        db.insert(User.TABLE, [f'{user_id}', f'"{name}"', f'"{mail}"'])
        db.save()
        return str(user_id)

    def __str__(self):
        return f"({self.user_id}, {self.name}, {self.mail})"

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
        self.character_id = character_id
        self.name = name
        self.description = description
        self.location_id = location_id
        self.user_id = user_id
        self.action = action

    def __str__(self):
        return f"({self.character_id}, {self.name}, {self.description}, {self.location_id}, {self.user_id}, {self.action})"

    @staticmethod
    def create(db: ManagerDB, name: str, description: str, user_id: str, location_id: str = 'NULL', action: str = 'New') -> str:
        """new character table row"""
        character_id = Character.len(Character, db)+1
        usysf.log(" ".join([f'{character_id}', f'"{name}"', f'"{description}"', f'{location_id}', f'{user_id}', f'{action}']))
        db.insert(Character.TABLE, [f'{character_id}', f'"{name}"', f'"{description}"', f'{location_id}', f'{user_id}', f'"{action}"'])
        db.save()
        return str(character_id)
    
    @staticmethod
    def get(table: "Character", db: ManagerDB, character_id: str, user_id: str) -> "Character":
        """current user character"""
        attr = db.select(Character.TABLE, ['*'],
            {
                Character.TABLEKEY: character_id,
                User.TABLEKEY: user_id
            }
        )[0]
        return Character(*attr)

    @staticmethod
    def list(table: "Character", db: ManagerDB, user_id: str = None, location_id: str = None, character_id: str = None) -> list:
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
                ret.append(Character(*character))
        return ret

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

    def display(self) -> str:
        """display str"""
        return f"{self.name} ({self.description}) \"{self.action}\""


class Location(Table):
    """location table object"""
    TABLE = "locations"
    TABLEKEY = "location_id"
    SCHEMA = "location_id INTEGER NOT NULL PRIMARY KEY, name varchar(255) NOT NULL, description varchar(255)"

    def __init__(self, location_id: str, name: str, description: str) -> None:
        self.location_id = location_id
        self.name = name
        self.description = description

    def __str__(self):
        return f"({self.location_id}, {self.name}, {self.description})"

    @staticmethod
    def create(db: ManagerDB, name: str, description: str) -> str:
        """new location table row"""
        location_id = Location.len(Location, db)+1
        db.insert(Location.TABLE, [f'{location_id}', f'"{name}"', f'"{description}"'])
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
                ret.append(Location(*location))
        return ret

    def display(self) -> str:
        """display str"""
        return f"{self.name} ({self.description})"