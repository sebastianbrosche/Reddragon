# -*- coding: utf-8 -*-
"""
IOM Race Selection System

Players enter a room before Limbo where they can select their race.
After selecting, they can enter the portal to the main world.
"""

from evennia import DefaultRoom, DefaultObject, CmdSet, Command
from evennia.utils import create

RACE_DATA = {
    "human": {
        "name": "Human",
        "desc": "Humans are the most adaptable and versatile race. They have no particular strengths or weaknesses, making them excellent all-rounders.",
        "stats": {"str": 50, "dex": 50, "con": 50, "sta": 50, "int": 50, "wis": 50, "cha": 50},
        "skill_caps": {"warrior": 100, "thief": 100, "cleric": 100, "mage": 100, "ranger": 100},
    },
    "elf": {
        "name": "Elf",
        "desc": "Elves are graceful beings with high dexterity and intelligence. They excel as mages and rangers but are physically frail.",
        "stats": {"str": 40, "dex": 65, "con": 35, "sta": 45, "int": 60, "wis": 60, "cha": 60},
        "skill_caps": {"warrior": 60, "thief": 80, "cleric": 80, "mage": 100, "ranger": 100},
    },
    "dwarf": {
        "name": "Dwarf",
        "desc": "Dwarves are tough, strong, and resilient. They make excellent warriors with their high strength and constitution.",
        "stats": {"str": 65, "dex": 40, "con": 70, "sta": 60, "int": 45, "wis": 55, "cha": 40},
        "skill_caps": {"warrior": 100, "thief": 60, "cleric": 80, "mage": 50, "ranger": 70},
    },
    "orc": {
        "name": "Orc",
        "desc": "Orcs are brutishly strong with high strength and constitution. They are fearsome warriors but lack in mental faculties.",
        "stats": {"str": 70, "dex": 45, "con": 65, "sta": 60, "int": 30, "wis": 30, "cha": 25},
        "skill_caps": {"warrior": 100, "thief": 50, "cleric": 60, "mage": 30, "ranger": 60},
    },
    "halfling": {
        "name": "Halfling",
        "desc": "Halflings are small, nimble, and dexterous. They excel as thieves with their small size and quick reflexes.",
        "stats": {"str": 35, "dex": 70, "con": 40, "sta": 45, "int": 50, "wis": 50, "cha": 55},
        "skill_caps": {"warrior": 60, "thief": 100, "cleric": 70, "mage": 60, "ranger": 80},
    },
    "troll": {
        "name": "Troll",
        "desc": "Trolls are massive and incredibly strong with the highest constitution of any race. They regenerate health but are slow and dim.",
        "stats": {"str": 80, "dex": 30, "con": 80, "sta": 70, "int": 20, "wis": 20, "cha": 15},
        "skill_caps": {"warrior": 100, "thief": 30, "cleric": 40, "mage": 20, "ranger": 40},
    },
    "gnome": {
        "name": "Gnome",
        "desc": "Gnomes are small and intelligent with high intelligence and wisdom. They make excellent mages and clerics.",
        "stats": {"str": 35, "dex": 55, "con": 40, "sta": 40, "int": 70, "wis": 60, "cha": 50},
        "skill_caps": {"warrior": 40, "thief": 70, "cleric": 100, "mage": 100, "ranger": 50},
    },
    "kobold": {
        "name": "Kobold",
        "desc": "Kobolds are small, cunning reptilian creatures. They have moderate dexterity but are physically weak.",
        "stats": {"str": 30, "dex": 60, "con": 35, "sta": 40, "int": 45, "wis": 40, "cha": 30},
        "skill_caps": {"warrior": 50, "thief": 80, "cleric": 50, "mage": 60, "ranger": 70},
    },
    "drow": {
        "name": "Drow",
        "desc": "Drow are dark elves with high dexterity and intelligence. They excel as mages and thieves but are sensitive to light.",
        "stats": {"str": 45, "dex": 70, "con": 40, "sta": 50, "int": 60, "wis": 55, "cha": 50},
        "skill_caps": {"warrior": 70, "thief": 100, "cleric": 60, "mage": 100, "ranger": 80},
    },
    "half-elf": {
        "name": "Half-Elf",
        "desc": "Half-Elves combine human adaptability with elven grace. They are versatile and well-balanced.",
        "stats": {"str": 45, "dex": 60, "con": 45, "sta": 50, "int": 55, "wis": 55, "cha": 60},
        "skill_caps": {"warrior": 80, "thief": 80, "cleric": 80, "mage": 90, "ranger": 90},
    },
}

class CmdSelectRace(Command):
    """
    Select your race.
    
    Usage:
      select <race>
      select human
      select elf
      select list
    """
    key = "select"
    locks = "cmd:all()"
    
    def func(self):
        caller = self.caller
        args = self.args.strip().lower()
        
        if not args or args == "list":
            # Show available races
            caller.msg("|cAvailable Races:|n")
            for race_key, race_info in RACE_DATA.items():
                caller.msg(f"  |y{race_key}|n - {race_info['name']}: {race_info['desc'][:60]}...")
            caller.msg("\n|cUsage:|n select <race>")
            return
        
        if args not in RACE_DATA:
            caller.msg(f"|rUnknown race: {args}|n")
            caller.msg("Use 'select list' to see available races.")
            return
        
        # Set race
        race_info = RACE_DATA[args]
        caller.db.race = race_info["name"]
        caller.db.race_key = args
        
        # Apply racial stat bases
        from typeclasses.characters import RACE_STAT_BASES
        bases = RACE_STAT_BASES.get(race_info["name"], RACE_STAT_BASES["Human"])
        
        # Update traits if they exist
        if hasattr(caller, 'traits') and caller.traits:
            for stat, value in bases.items():
                trait = caller.traits.get(stat.lower())
                if trait:
                    trait.base = value
        
        # Update legacy db
        caller.db.strength = bases["str"]
        caller.db.dexterity = bases["dex"]
        caller.db.constitution = bases["con"]
        caller.db.stamina = bases["sta"]
        caller.db.intelligence = bases["int"]
        caller.db.wisdom = bases["wis"]
        caller.db.charisma = bases["cha"]
        
        # Set skill caps
        caller.db.skill_caps = race_info.get("skill_caps", {})
        
        # Set size based on race
        if args in ["troll"]:
            caller.db.size = "Large"
        elif args in ["halfling", "gnome", "kobold"]:
            caller.db.size = "Small"
        else:
            caller.db.size = "Medium"
        
        caller.msg(f"|gYou have selected the {race_info['name']} race!|n")
        caller.msg(f"|c{race_info['desc']}|n")
        caller.msg("\n|yYour racial stats have been applied.|n")
        caller.msg("You may now |yenter portal|n to begin your adventure.")
        caller.msg("Or type |yscore|n to see your character sheet.")

class RaceSelectionCmdSet(CmdSet):
    key = "race_selection"
    priority = 1
    
    def at_cmdset_creation(self):
        self.add(CmdSelectRace)

class RaceSelectionRoom(DefaultRoom):
    """
    Room where players select their race before entering the world.
    """
    
    def at_object_creation(self):
        super().at_object_creation()
        self.key = "Race Selection Hall"
        self.db.desc = """
|c=== Race Selection Hall ===|n

You stand in a mystical hall between worlds. Before you enter the realm
of Islands of Myth, you must choose your race.

|yA glowing sign hangs on the wall.|n

|wInstructions:|n
  1. Type |yselect list|n to see available races
  2. Type |yselect <race>|n to choose your race (e.g., |yselect human|n)
  3. Once selected, type |yenter portal|n to begin your adventure

|gRemember: Your race determines your base stats and guild skill caps.|n
        """
        self.cmdset.add(RaceSelectionCmdSet, permanent=True)
    
    def at_object_receive(self, moved_obj, source_location, **kwargs):
        """Called when an object enters this room."""
        super().at_object_receive(moved_obj, source_location, **kwargs)
        
        # If it's a character, send them the welcome message
        if moved_obj.has_account:
            moved_obj.msg("|cWelcome! Please select your race before entering the world.|n")
            moved_obj.msg("Type |yselect list|n to see available races.")

class OnboardingSign(DefaultObject):
    """
    The 'read me' sign that explains game mechanics.
    """
    
    def at_object_creation(self):
        super().at_object_creation()
        self.key = "a sign"
        self.aliases.add("sign")
        self.aliases.add("read me")
        self.db.desc = "A wooden sign with instructions for new adventurers."
    
    def return_appearance(self, looker):
        return """
|c═══════════════════════════════════════════════════════════════════════════|n
|c                         WELCOME TO RED DRAGON MUD                         |n
|c═══════════════════════════════════════════════════════════════════════════|n

|yHOW TO START:|n
  1. |wselect <race>|n     - Choose your race (try |wselect list|n)
  2. |wenter portal|n      - Enter the world
  3. |wlook|n              - See your surroundings
  4. |wnorth/east/etc|n    - Move around

|yLEVELING UP:|n
  - Kill monsters to gain experience
  - When you have enough XP, find |wJudge Achman|n in Illium City
  - Type |wtalk achman|n and select |wc (advance)|n
  - You gain stat points to allocate each level

|yGUILDS:|n
  - Guild masters are located throughout Illium City
  - Type |wtalk <master>|n to interact with them
  - Join guilds in order: alpha → bravo → charlie → delta → etc.
  - You must max out previous tiers before advancing
  - Each guild teaches unique skills and spells

|ySKILLS & SPELLS:|n
  - |wskills|n          - List your current skills
  - |wspells|n          - List your current spells
  - |wtrain <skill>|n   - Train a skill at a guild master
  - Training costs experience and has percentage caps per level

|yCOMBAT:|n
  - |wkill <monster>|n  - Attack a monster
  - |wwimpy <percent>|n - Set auto-flee threshold
  - |weat corpse|n      - Regain health by eating corpses

|yTRAVEL:|n
  - |wwarp|n             - Return to Adventurer's Guild
  - |wferry to <island>|n - Travel between islands (takes ~1 minute)
  - Some areas require special entry: |wenter cave|n, |wclimb tree|n, etc.

|yCOMMANDS:|n
  - |wscore|n            - View your character sheet
  - |winventory|n        - Check your items
  - |wwho|n              - See who is online
  - |whelp|n             - Get help on commands

|gGood luck, adventurer!|n

|c═══════════════════════════════════════════════════════════════════════════|n
        """

class CmdReadSign(Command):
    """
    Read the sign.
    
    Usage:
      read sign
      read me
    """
    key = "read"
    locks = "cmd:all()"
    
    def func(self):
        caller = self.caller
        args = self.args.strip().lower()
        
        # Find sign in room
        sign = None
        for obj in caller.location.contents:
            if obj.key == "a sign" or "sign" in obj.aliases.all():
                sign = obj
                break
        
        if not sign:
            caller.msg("There is nothing to read here.")
            return
        
        if args in ["sign", "me", "", "a sign"]:
            caller.msg(sign.return_appearance(caller))
        else:
            # Maybe they're trying to read something else
            caller.msg(f"You can't read '{args}'.")

class SignCmdSet(CmdSet):
    key = "sign_cmds"
    priority = 2
    
    def at_cmdset_creation(self):
        self.add(CmdReadSign)

def setup_race_selection():
    """Create the race selection room and portal to the main world."""
    from evennia import create_object, search_object
    from typeclasses.rooms import IOMRoom
    from typeclasses.exits import IOMExit
    
    # Create race selection room
    race_room = create_object(RaceSelectionRoom, key="Race Selection Hall")
    
    # Create onboarding sign
    sign = create_object(OnboardingSign, key="a sign")
    sign.location = race_room
    
    # Add read command to room
    race_room.cmdset.add(SignCmdSet, permanent=True)
    
    # Find or create limbo
    limbo = search_object("Limbo", typeclass=IOMRoom)
    if limbo:
        limbo = limbo[0]
    else:
        limbo = create_object(IOMRoom, key="Limbo")
        limbo.db.desc = "The void between worlds."
    
    # Create portal from race room to central square
    central = search_object("Central Square", typeclass=IOMRoom)
    if central:
        central = central[0]
    else:
        central = create_object(IOMRoom, key="Central Square")
        central.db.desc = "The bustling center of Illium City."
        central.db.domain = "gossamer"
        central.db.area = "Illium City"
    
    # Portal exit from race room
    portal = create_object(IOMExit, key="portal")
    portal.aliases.add("portal")
    portal.location = race_room
    portal.destination = central
    
    # Create exit from limbo to race room
    to_race = create_object(IOMExit, key="north")
    to_race.aliases.add("n")
    to_race.location = limbo
    to_race.destination = race_room
    
    print(f"Race selection room created: {race_room.id}")
    print(f"Portal to Central Square: {portal.id}")
    print(f"Limbo connects to race room: {to_race.id}")
    
    return race_room, central

if __name__ == "__main__":
    print("Run this from within Evennia with:")
    print("  @py from world.race_selection import setup_race_selection; setup_race_selection()")
