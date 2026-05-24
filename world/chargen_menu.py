"""
Red Dragon MUD - Character Creation Menu
IOM-style race and class selection using Evennia's Character Creator
"""

from evennia.utils.evmenu import EvMenu

# IOM Races
IOM_RACES = [
    "Human", "Dwarf", "Elf", "Orc", "Gnome", "Halfling",
    "Half-Orc", "Half-Elf", "Troll", "Kobold"
]

# IOM Guilds (classes)
IOM_GUILDS = [
    "Warrior", "Thief", "Cleric", "Mage", "Ranger",
    "Bard", "Monk", "Cavalier", "Necromancer"
]


def menu_start_node(caller):
    """Welcome to character creation."""
    text = """
    |cWelcome to Darkstaff MUD Character Creation!|n
    
    You are about to create a new adventurer in the world of Islands of Myth.
    
    First, choose your race:
    """
    
    options = []
    for race in IOM_RACES:
        options.append({
            "desc": race,
            "goto": ("menu_confirm_race", {"race": race})
        })
    
    return text, options


def menu_confirm_race(caller, raw_string, **kwargs):
    """Confirm race selection."""
    race = kwargs.get("race", "Human")
    caller.db.chargen_race = race
    
    text = f"""
    You have chosen to be a |y{race}|n.
    
    Is this correct?
    """
    
    options = [
        {"desc": "Yes, continue", "goto": "menu_choose_guild"},
        {"desc": "No, go back", "goto": "menu_start_node"},
    ]
    
    return text, options


def menu_choose_guild(caller, raw_string, **kwargs):
    """Choose guild/class."""
    text = """
    Now choose your guild (class):
    
    Each guild determines your starting skills and abilities.
    """
    
    options = []
    for guild in IOM_GUILDS:
        options.append({
            "desc": guild,
            "goto": ("menu_confirm_guild", {"guild": guild})
        })
    
    return text, options


def menu_confirm_guild(caller, raw_string, **kwargs):
    """Confirm guild selection."""
    guild = kwargs.get("guild", "Warrior")
    caller.db.chargen_guild = guild
    
    race = getattr(caller.db, 'chargen_race', 'Human')
    
    text = f"""
    You have chosen:
    Race: |y{race}|n
    Guild: |y{guild}|n
    
    Ready to enter the world?
    """
    
    options = [
        {"desc": "Yes, create my character!", "goto": "menu_finish"},
        {"desc": "No, start over", "goto": "menu_start_node"},
    ]
    
    return text, options


def menu_finish(caller, raw_string, **kwargs):
    """Finalize character creation."""
    race = getattr(caller.db, 'chargen_race', 'Human')
    guild = getattr(caller.db, 'chargen_guild', 'Warrior')
    
    # Apply choices
    caller.db.race = race
    caller.db.guild = guild
    caller.db.guild_level = 1
    
    # Re-setup traits with correct race
    if hasattr(caller, '_setup_traits'):
        caller._setup_traits()
    
    # Set sdesc
    if hasattr(caller, 'sdesc'):
        caller.sdesc.add(f"a {race.lower()} {guild.lower()}")
    
    # Clear chargen state
    caller.db.chargen_step = None
    
    text = f"""
    |gCharacter created!|n
    
    Welcome, |y{caller.key}|n the |y{race} {guild}|n!
    
    You begin your journey in the Adventurer's Guild.
    Type |whelp|n for a list of commands.
    """
    
    options = []
    
    return text, options
