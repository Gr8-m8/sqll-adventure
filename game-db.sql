DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS locations;
DROP TABLE IF EXISTS characters;

CREATE TABLE users (
        user_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        name varchar(255) NOT NULL,
        mail varchar(255) NOT NULL
);

CREATE TABLE locations (
        location_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        name varchar(255) NOT NULL,
        description varchar(255)
);

CREATE TABLE characters (
        character_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        name varchar(255) NOT NULL,
        description varchar(255),
        location_id REFERENCES location(id),
        user_id REFERENCES users(id) NOT NULL
);


INSERT INTO users (name, mail) VALUES
        ("legend27", "legend27@gmail.com"),
        ("stevo", "stevo.gamer@hotmail.com"),
        ("Gunther Clein", "gunther.clein@gmail.com"),
        ("Maski Hallonen", "maski.hallonen@email.fi");

INSERT INTO locations (name, description) VALUES
        ("Forest", "Big Trees, Greenery, Wolfs, Spiders"),
        ("Rexington City", "Small houses surrounding the large Kings Spire"),
        ("The Rainbow Factory", "Transportbelts, robotarms, alarming amount of uranium. Infested with CEO goblins"),
        ("The gaslight cabin", "Does not exsist"),
        ("Your Walls", "Your Walls");

INSERT INTO characters (name, description, location_id, user_id) VALUES
        ("Rec R. Urson", "Elven Mage", 3, 3),
        ("The Creature", "Unsetteling", 5, 2),
        ("Turloch, the Unbreakable", "Paladin of Kohuur", 1, 1),
        ("Takki Crawn", "Human Rogue", 2, 4),
        ("Jim", "Etheral Artificer", 2, 3);