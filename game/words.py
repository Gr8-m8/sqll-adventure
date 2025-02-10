from  wonderwords import RandomWord #https://pypi.org/project/wonderwords/
import random

wordsRW = RandomWord()
class Words:
    """word generator"""

    KEY_NOUN = "nouns"
    KEY_ADJECTIVE = "adjectives"
    KEY_VERB = "verbs"
    KEY_VAN = "van"
    KEY_NAME_CHARACTER = "name_character"
    KEY_NAME_LOCATION = "name_location"

    @classmethod
    def noun(cls: "words"):
        """random noun"""
        return wordsRW.word(include_parts_of_speech=[cls.KEY_NOUN])
    
    @classmethod
    def adjective(cls: "words"):
        """random adjective"""
        return wordsRW.word(include_parts_of_speech=[cls.KEY_ADJECTIVE])
    
    @classmethod
    def verb(cls: "words"):
        """random verb"""
        return wordsRW.word(include_parts_of_speech=[cls.KEY_VERB])
    
    @classmethod
    def van(cls: "words"):
        """random verb ing, adjective, noun"""
        return f"{cls.verb()}ing {cls.adjective()} {cls.noun()}"
    
    @classmethod
    def name_character(cls: "Words"):
        name = f"{random.choice([cls.adjective(), cls.verb()])}{cls.noun()}".capitalize()
        titles = [
            f"the {cls.adjective()}",
            f"of {cls.name_location()}"
        ]
        title = random.choice(titles)
        return f"{name} {title}"
    
    @classmethod
    def name_location(cls: "Words"):
        biomelist = [
            "Forest",
            "Mountains",
            "City",
            "Lake",
            "Dessert",
            "Plains",
            "Village",
            "Town",
            "Tundra",
            "Collage",
            "Wetlands",
            "Swamp",
            "Canyon",
            "Coast",
            "Road",
            "Hills",
            "Cave",
            "Jungle"
        ]
        biome = random.choice(biomelist)
        name = f"{random.choice([Words.noun(), Words.verb(), Words.adjective()])}{random.choice([Words.noun(), Words.verb()])}".capitalize()
        return f"{biome} of {name}"

    @classmethod
    def test(cls, key, times):
        t = times
        s = ""
        while not t == 0:
            t = max(-1, t-1)
            if key == cls.KEY_ADJECTIVE:
                s = cls.adjective()
            if key == cls.KEY_VERB:
                s = cls.verb()
            if key == cls.KEY_NOUN:
                s = cls.noun()
            if key == cls.KEY_VAN:
                s = cls.van()
            if key == cls.KEY_NAME_LOCATION:
                s = cls.name_location()
            if key == cls.KEY_NAME_CHARACTER:
                s = cls.name_character()
            
            if t < 0:
                input(f"[{t}] {s}")
            else:
                print(f"[{times-t}] {s}")
    

#Words.test(Words.KEY_VAN, 9)
