"""db game"""
import random
import usysf
from menu import Menu, MenuItem, MenuOption, MenuTitle
from connection import ServerConnection
from database import MariaDB, Sqllite3DB, ManagerDB, OFFLINE
from database_table import User, Location, Character, Path, Item

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
        self.user = User.get(User, db, user_id)
        menu.close()

    def set_character_create(self, db: ManagerDB, menu: Menu) -> None:
        """create and assign game character"""
        name = input("Character Name\n> ")
        description = input("Character Description\n> ")
        location_id = Location.get_random(db).location_id
        self.set_character(
            Character.create(
                db,
                name,
                description,
                self.user.user_id,
                location_id
            ),
            self.user.user_id,
            db,
            menu
        )

    def set_character(self, character_id: str, user_id: str, db: ManagerDB, menu: Menu) -> None:
        """assign game character"""
        self.character = Character.get(Character, db, character_id, user_id)
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
        db.save()
        menu.close()
        

    def action_character(self, db: ManagerDB, menu: Menu, action: str):
        """set character action"""
        self.character.action_do(db, action)
        self.character.action = action
        db.save()
        menu.close()
        

    def explore(self, db: ManagerDB, menu: Menu):
        """Explore action"""
        printstr = "You found "
        events = [
            "ITEM",
            "LOCATION"
        ]
        event = random.choice(events)
        if event == "ITEM":
            printstr += "an item: "
            item_id = Item.create_generate(db, self.character.character_id)
            db.save()
            printstr += Item.get(Item, db, item_id).display()
            
        if event == "LOCATION":
            printstr += "a location: "
            location_id = Location.create_generate(db)
            db.save()
            printstr += Location.get(Location, db, location_id).display()
            path_id = Path.create(db, self.character.location_id, location_id)
            self.character.move(db, location_id)
            db.save()
        
        input(printstr)
        
        menu.close()

    def exit(self, db: ManagerDB) -> None:
        """Terminate Game"""
        db.close()
        usysf.clear()
        exit(0)

def main_game(game: Game, db: ManagerDB):
    """main game func"""
    def inventory(game: Game, db: ManagerDB):
        items = [MenuOption("Return", action=lambda: inventorymenu.close())]
        for item in Item.list(Item, db, game.character.character_id):
            items.append(MenuOption(item.display(), action=lambda it=item: it.use(db)))
        inventorymenu = Menu(MenuTitle("Adventure Game"),
                             MenuItem(f"Inventory of {game.character.name}"), items)
        
        Menu.display_menu(inventorymenu)

    users = [MenuOption(
        text="New User", action=lambda: game.set_user_create(db, usermenu))]
    for user in User.list(User, db):
        users.append(MenuOption(
            text=user, action=lambda id=user.user_id: game.set_user(id, db, usermenu)))

    usermenu = Menu(MenuTitle("Adventure Game"),
                    MenuItem("Select User"), users)
    Menu.display_menu(usermenu)

    if game.user.user_id == "0":
        game.exit(db)

    characters = [MenuOption(text="New Character", action=lambda: game.set_character_create(db, charactermenu))]
    for character in Character.list(Character, db, user_id=game.user.user_id):
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
            #MenuOption(text="New Location", action=lambda: game.set_location_create(db, locationmenu)),
            MenuOption(text="Inventory", action=lambda: inventory(game, db)),
            MenuOption(text="Explore", action=lambda: game.explore(db, locationmenu))
        ]
        for path in Path.list(db, game.character.location_id):
            fs = f"Go To: {Location.get(Location, db, path.destination_id).display()}"
            locations.append(MenuOption(text=fs, action=lambda id=path.destination_id: game.set_location(id, db, locationmenu)))

        character = game.character.display()
        location = Location.get(Location, db, game.character.location_id).display() if game.character.location_id else "None"
        character_other = Character.list(Character, db, location_id=game.character.location_id, character_id=game.character.character_id)
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
        status = usysf.shell("docker ps -f name=sql-adventure-db --format \"table {{.Status}}\"")
        input("CONTINUE")
        return status


    def host_start(connection: ServerConnection):
        try:
            status = usysf.shell("docker-compose up -d")
        except:
            status = None
        try:
            status = usysf.shell("docker-compose up -d")
        except:
            status = None
        input("CONTINUE")
        return status
    
    
    def host_stop():
        try:
            status = usysf.shell("docker-compose down")
        except:
            status = None
        try:
            status = usysf.shell("docker-compose down")
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
    connection: ServerConnection = ServerConnection()
    db: ManagerDB = ManagerDB(connection)
    game: Game = Game()
    
    maingameloop = True
    while maingameloop:
        menu_main(game, db, connection)

        if connection.offline or OFFLINE:
            db = Sqllite3DB(connection)
        else:
            db = MariaDB(connection)

        if game.start and ManagerDB.STATUS:
            User.INIT(db)
            Character.INIT(db)
            Location.INIT(db)
            Path.INIT(db)
            Item.INIT(db)
            main_game(game, db)