import usysf
from database import ManagerDB
from words import Words
import random

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
        return f"{self.TABLE} {self.TABLEKEY}:{self.table_id}"

    @staticmethod
    def create(table: "Table", db: ManagerDB) -> str:
        """new user table row"""
        table_id = table.len(db)+1
        db.insert(table.TABLE, [f'{table_id}'])
        db.save()
        return str(table_id)
    
    def create_generate(table: "Table", db: ManagerDB) -> str:
        return table.create(table, db)

    @staticmethod
    def get(table: "Table", db: ManagerDB, table_id: str) -> "Table":
        """table row"""
        attr = db.select(table.TABLE, ['*'], {table.TABLEKEY: table_id})[0]
        #usysf.log(attr)
        return table(*attr)
    
    @staticmethod
    def get_random(table: "Table", db: ManagerDB) -> "Table":
        """random row"""
        if Table.len(table, db) < 1:
            Table.create_generate(table, db)
        table_id = random.randint(1, Table.len(table, db))
        return Table.get(table, db, table_id)

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
        super().__init__(user_id)
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
            {"action": f'"{action}"'},
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
        super().__init__(location_id)
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
    def create_generate(db):
        """new random location table row"""
        name = Words.name_location()
        description = ", ".join([Words.adjective(), Words.adjective(), Words.adjective()])
        return Location.create(db, name, description)
    
    @staticmethod
    def get_random(db: ManagerDB) -> "Table":
        """random row"""
        if Location.len(Location, db) < 1:
            Location.create_generate(db)
        table_id = random.randint(1, Location.len(Location, db))
        return Table.get(Location, db, table_id)

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
    
class Path(Table):
    """link location table object"""
    TABLE = "paths"
    TABLEKEY = "path_id"
    SCHEMA = f"{TABLEKEY} PRIMARY KEY NOT NULL, location_id INTEGER, destination_id INTEGER"

    def __init__(self, path_id: str, location_id: str, destination_id: str):
        super().__init__(path_id)
        self.path_id = path_id
        self.location_id = location_id
        self.destination_id = destination_id

    @staticmethod
    def create(db: ManagerDB, location_id: str, destination_id: str) -> str:
        """new location table row"""
        path_id = Path.len(Path, db)+1
        db.insert(Path.TABLE, [f'{path_id}', f'{location_id}', f'{destination_id}'])
        db.save()
        return str(location_id)
    
    @staticmethod
    def list(db: ManagerDB, location_id: str = None) -> list:
        """location table entries"""
        ret = []
        if location_id:
            locations = db.select(Path.TABLE, [f'{Path.TABLEKEY}', 'location_id', 'destination_id'], {'location_id': location_id})
            destinations = db.select(Path.TABLE, [f'{Path.TABLEKEY}', 'destination_id', 'location_id'], {'destination_id': location_id})
            paths = locations+destinations
        else:
            paths = db.select(Path.TABLE, ['*'])
        
        if paths:
            for path in paths:

                usysf.log(path, "PATH")
                ret.append(Path(*path))
        return ret
    
    def display(self) -> str:
        """display str"""
        return f"{self.location_id} <-> {self.destination_id}"

class Item(Table):
    """item table object"""
    TABLE = "items"
    TABLEKEY = "item_id"
    SCHEMA = f"{TABLEKEY} INTEGER PRIMARY KEY NOT NULL, noun VARCHAR(63), adjective VARCHAR(63), verb VARCHAR(63), equipment_slot VARCHAR(63), character_id INTEGER, in_use INTEGER"

    def __init__(self, table_id: str, noun: str, adjective: str, verb: str, equipment_slot: str, character_id: str, in_use: str):
        super().__init__(table_id)
        self.item_id = table_id
        self.noun = noun
        self.adjective = adjective
        self.verb = verb
        self.equipment_slot = equipment_slot
        self.character_id = character_id
        self.in_use = in_use

    @staticmethod
    def create(db: ManagerDB, character_id: str, noun:str, adjective:str, verb:str, equpment_slot:str) -> str:
        """new item table row"""
        item_id = Item.len(Item, db)+1
        db.insert(Item.TABLE, [f'{item_id}', f'"{noun}"', f'"{adjective}"', f'"{verb}"', f'"{equpment_slot}"', f'{character_id}', f'0'])
        db.save()
        return str(item_id)
    
    @staticmethod
    def create_generate(db, character_id):
        """new random item row"""
        noun = Words.noun()
        adjective = Words.adjective()
        verb = Words.verb()
        equipment_slots = [
            "",
            "Hat",
            "Helmet",
            "Glasses",
            "Mask",
            "Shirt",
            "Chestplate",
            "Gloves",
            "Gauntlet",
            "Trousers",
            "Leggings",
            "Socks",
            "Shoes",
            "Weapon",
            "Shield"
        ]
        equpment_slot = random.choice(equipment_slots)
        return Item.create(db, character_id, noun, adjective, verb, equpment_slot)

    def trade(self, db: ManagerDB, character_id):
        """change item character"""
        self.character_id = character_id
        self.in_use = "False"
        return db.update(
            Item.TABLE, 
            {"in_use": f'"{self.in_use}"', Character.TABLEKEY: self.character_id},
            {Item.TABLEKEY: self.item_id}
        )

    def use(self, db: ManagerDB):
        """use item"""
        #unequip other
        self.in_use = '0'
        db.update(Item.TABLE, 
            {"in_use": f'"{self.in_use}"'},
            {Character.TABLEKEY: self.character_id, "equipment_slot": f"{self.equipment_slot}"}
        )
        #equip this
        self.in_use = '1'
        db.update(Item.TABLE, 
            {"in_use": f'"{self.in_use}"'},
            {Item.TABLEKEY: self.item_id}
        )

    def delete(self, db: ManagerDB):
        """remove item"""
        db.delete(Item.TABLE, {Item.TABLEKEY: self.item_id})

    def display(self) -> str:
        """display str"""
        return f"{self.verb} {self.adjective} {self.noun}-{self.equipment_slot} ({"EQUIPPED" if self.in_use == '1' else "STORED"})"