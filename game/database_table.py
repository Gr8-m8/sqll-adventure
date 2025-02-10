import usysf
from database import ManagerDB

class Table:
    """Generic table object"""
    TABLE = "template"
    TABLEKEY = "template_id"
    SCHEMA = f"{TABLEKEY} INTEGER NOT NULL PRIMARY KEY"

    @classmethod
    def INIT(cls: "Table", db: ManagerDB):
        """SETUP DATABASE TABLE"""
        db.create_table(cls.TABLE, cls.SCHEMA)

    def __init__(self, table_id: str) -> None:
        self.table_id = table_id

    @classmethod
    def create(cls, db: ManagerDB) -> str:
        """new user table row"""
        table_id = cls.len(db)+1
        db.insert(cls.TABLE, [str(table_id)])
        db.save()
        return str(table_id)

    @classmethod
    def get(cls: "Table", db: ManagerDB, table_id: str) -> "Table":
        """current game user"""
        attr = db.select(cls.TABLE, ['*'], {cls.TABLEKEY: table_id})[0]
        return cls(attr[0])

    @classmethod
    def list(cls: "Table",db: ManagerDB) -> list:
        """table entries"""
        ret = []
        for table in db.select(cls.TABLE, ['*']):
            ret.append(cls(table[0]))
        return ret

    @classmethod
    def len(cls: "Table", db: ManagerDB) -> int:
        """len user table entries"""
        return db.table_len(cls.TABLE)

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
    SCHEMA = f"{TABLEKEY} INTEGER NOT NULL PRIMARY KEY, name varchar(255) NOT NULL, mail varchar(255) NOT NULL"

    def __init__(self, user_id: str, name: str, mail: str) -> None:
        self.user_id: str = user_id
        self.name: str = name
        self.mail: str = mail

    def __str__(self):
        return f"({self.user_id}, {self.name}, {self.mail})"

    @classmethod
    def create(cls: "User", db: ManagerDB, name: str, mail: str) -> str:
        """new user table row"""
        user_id = cls.len(db)+1
        db.insert(cls.TABLE, [str(user_id), '"'+name+'"', '"'+mail+'"'])
        db.save()
        return str(user_id)

    @classmethod
    def get(cls: "User", db: ManagerDB, user_id: str) -> "User":
        """current game user"""
        attr = db.select(cls.TABLE, ['*'], {cls.TABLEKEY: user_id})[0]
        return cls(attr[0], attr[1], attr[2])

    @classmethod
    def list(cls: "User", db: ManagerDB) -> list:
        """user table entries"""
        ret = []
        users = db.select(cls.TABLE, ['*'])
        if users:
            for user in users:
                ret.append(cls(user[0], user[1], user[2]))
        return ret

    @classmethod
    def len(cls: "User", db: ManagerDB) -> int:
        """len user table entries"""
        return db.table_len(cls.TABLE)

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
    sqlite_SCHEMA = f"{TABLEKEY} INTEGER NOT NULL PRIMARY KEY, name varchar(255) NOT NULL, description varchar(255), location_id REFERENCES location(id), user_id REFERENCES users(id) NOT NULL"
    SCHEMA = f"{TABLEKEY} INTEGER NOT NULL PRIMARY KEY, name varchar(255) NOT NULL, description varchar(255), location_id varchar(255), user_id varchar(255), action varchar(1023)"

    def __init__(self, character_id: str, name: str, description: str, location_id: str, user_id: str, action: str) -> None:
        self.character_id = character_id
        self.name = name
        self.description = description
        self.location_id = location_id
        self.user_id = user_id
        self.action = action

    def __str__(self):
        return f"({self.character_id}, {self.name}, {self.description}, {self.location_id}, {self.user_id}, {self.action})"

    @classmethod
    def create(cls: "Character", db: ManagerDB, name: str, description: str, user_id: str, location_id: str = 'NULL') -> str:
        """new character table row"""
        character_id = cls.len(db)+1
        db.insert(cls.TABLE, [str(character_id), '"'+name+'"', '"'+description+'"', str(location_id), str(user_id), '"New"'])
        db.save()
        return str(character_id)

    @classmethod
    def get(cls: "Character", db: ManagerDB, character_id: str, user_id: str) -> "Character":
        """current user character"""
        attr = db.select(
            cls.TABLE,
            ['*'],
            {
                cls.TABLEKEY: character_id,
                User.TABLEKEY: user_id
            }
        )[0]
        return cls(attr[0], attr[1], attr[2], attr[3] if attr[3] else "NULL", attr[4], attr[5])

    @classmethod
    def list(cls: "Character", db: ManagerDB, user_id: str = None, location_id: str = None, character_id: str = None) -> list:
        """character table entries"""
        ret = []
        where = {}
        where.update({User.TABLEKEY: user_id}) if user_id else None
        where.update({Location.TABLEKEY: location_id}) if location_id else None
        fs = f"NOT {cls.TABLEKEY}"
        where.update({fs: character_id}) if location_id else None

        user_characters = db.select(cls.TABLE, ['*']) if not (user_id or location_id or character_id) else db.select(cls.TABLE, ['*'], where)
        if (user_characters):
            for character in user_characters:
                ret.append(
                    cls(
                        character_id=character[0],
                        name=character[1],
                        description=character[2],
                        location_id=character[3],
                        user_id=character[4],
                        action=character[5]
                    )
                )
        return ret

    @classmethod
    def len(cls: "Character", db: ManagerDB):
        """len character table entries"""
        return db.table_len(cls.TABLE)

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
    SCHEMA = f"{TABLEKEY} INTEGER NOT NULL PRIMARY KEY, name varchar(255) NOT NULL, description varchar(255)"

    def __init__(self, location_id: str, name: str, description: str) -> None:
        self.location_id = location_id
        self.name = name
        self.description = description

    def __str__(self):
        return f"({self.location_id}, {self.name}, {self.description})"

    @classmethod
    def create(cls: "Location", db: ManagerDB, name: str, description: str) -> str:
        """new location table row"""
        location_id = cls.len(db)+1
        db.insert(cls.TABLE, [str(location_id), '"'+name+'"', '"'+description+'"'])
        db.save()
        return str(location_id)

    @classmethod
    def list(cls: "Location", db: ManagerDB, location_id_exclude: str = None) -> list:
        """location table entries"""
        ret = []
        fs = f"NOT {cls.TABLEKEY}"
        locations = db.select(cls.TABLE, ['*']) if not location_id_exclude else db.select(cls.TABLE, ['*'], {fs: location_id_exclude})
        if locations:
            for location in locations:
                ret.append(cls(location[0], location[1], location[2]))
        return ret

    @classmethod
    def len(cls: "Location", db: ManagerDB) -> int:
        """len location table entries"""
        return db.table_len(cls.TABLE)

    @classmethod
    def get(cls: "Location", db: ManagerDB, location_id: str = None) -> "Location":
        """current character Location"""
        if location_id is None or location_id == "NULL":
            return cls(-1, "None", "Nowhere")

        attr = db.select(cls.TABLE, ['*'],
                         {cls.TABLEKEY: location_id})[0]
        return cls(attr[0], attr[1], attr[2])

    def id(self) -> str:
        """get id"""
        return self.location_id

    def display(self) -> str:
        """display str"""
        return f"{self.name} ({self.description})"

class Path(Table):
    TABLE = "paths"
    TABLEKEY = "path_id"
    SCHEMA = f"{TABLEKEY} INTEGER PRIMARYKEY NOT NULL"

class Inventory(Table):
    Table = "inventories"
    TABLEKEY = "inventory_id"
    SCHEMA = f"{TABLEKEY} INTEGER PRIMARY KEY NOT NULL, "

    def __init__(self, table_id: str, character_id: str, equipment_slot: str):
        super().__init__(table_id)
        self.inventory_id = table_id
        self.character_id = character_id
        self.equipment_slot = equipment_slot

class Item(Table):
    TABLE = "items"
    TABLEKEY = "item_id"
    SCHEMA = f"{TABLEKEY} INTEGER PRIMARY KEY NOT NULL, "

    def __init__(self, table_id: str, noun: str, adjective: str, verb: str, equipments_lot: str, inventory_id: str):
        super().__init__(table_id)
        self.item_id = table_id
        self.noun = noun
        self.adjective = adjective
        self.verb = verb
        self.equipment_slot = equipments_lot
        self.inventory_id = inventory_id