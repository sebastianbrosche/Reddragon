"""
Red Dragon MUD - Monster Database & Spawn System
Complete monster definitions with spawn locations and behaviors
"""

import random
from evennia import create_object
from typeclasses.npcs import Mob

# Monster definitions with full stats
MONSTERS = {
    # Low-level monsters (levels 1-5)
    "earwig": {
        "name": "an earwig",
        "aliases": ["earwig"],
        "level": 1,
        "hp": 15,
        "damage": "1d4",
        "exp": 25,
        "gold": (0, 5),  # min, max
        "spawn_areas": ["lobelands", "yensid_land", "newbie_areas"],
        "spawn_rate": 0.3,  # 30% chance per spawn tick
        "behavior": "passive",  # passive, aggressive, territorial
        "loot": [
            {"item": "earwig_carapace", "chance": 0.1},
        ],
        "description": "A giant earwig crawls about here.",
        "resistances": {},
        "special": None,
    },
    
    "bumble_bee": {
        "name": "a bumble bee",
        "aliases": ["bumble bee", "bee"],
        "level": 2,
        "hp": 20,
        "damage": "1d4+1",
        "exp": 35,
        "gold": (1, 8),
        "spawn_areas": ["lobelands", "yensid_land", "gossamer"],
        "spawn_rate": 0.25,
        "behavior": "aggressive",
        "loot": [
            {"item": "bee_stinger", "chance": 0.15},
            {"item": "honey_drop", "chance": 0.2},
        ],
        "description": "A large bumble bee buzzes around angrily.",
        "resistances": {},
        "special": None,
    },
    
    "rat": {
        "name": "a giant rat",
        "aliases": ["rat", "giant rat"],
        "level": 1,
        "hp": 12,
        "damage": "1d3",
        "exp": 15,
        "gold": (0, 3),
        "spawn_areas": ["sewers", "dungeon", "darkcaverns", "newbie_areas"],
        "spawn_rate": 0.4,
        "behavior": "passive",
        "loot": [
            {"item": "rat_tail", "chance": 0.1},
            {"item": "rat_fur", "chance": 0.2},
        ],
        "description": "A filthy giant rat scurries about.",
        "resistances": {},
        "special": None,
    },
    
    "spider": {
        "name": "a cave spider",
        "aliases": ["spider", "cave spider"],
        "level": 2,
        "hp": 22,
        "damage": "1d4+1",
        "exp": 40,
        "gold": (1, 10),
        "spawn_areas": ["caves", "dungeon", "darkcaverns", "forest"],
        "spawn_rate": 0.3,
        "behavior": "aggressive",
        "loot": [
            {"item": "spider_venom", "chance": 0.25},
            {"item": "spider_silk", "chance": 0.15},
        ],
        "description": "A venomous cave spider lurks in the shadows.",
        "resistances": {"poison": 50},
        "special": None,
    },
    
    "wolf": {
        "name": "a grey wolf",
        "aliases": ["wolf", "grey wolf"],
        "level": 3,
        "hp": 35,
        "damage": "1d6+2",
        "exp": 60,
        "gold": (2, 15),
        "spawn_areas": ["forest", "hills", "sombre", "gossamer"],
        "spawn_rate": 0.2,
        "behavior": "territorial",
        "loot": [
            {"item": "wolf_pelt", "chance": 0.3},
            {"item": "wolf_fang", "chance": 0.2},
        ],
        "description": "A grey wolf prowls here, eyes gleaming.",
        "resistances": {},
        "special": None,
    },
    
    # Mid-level monsters (levels 5-15)
    "goblin": {
        "name": "a goblin",
        "aliases": ["goblin"],
        "level": 5,
        "hp": 50,
        "damage": "1d8+2",
        "exp": 120,
        "gold": (5, 25),
        "spawn_areas": ["caves", "dungeon", "mountain"],
        "spawn_rate": 0.2,
        "behavior": "aggressive",
        "loot": [
            {"item": "goblin_dagger", "chance": 0.1},
            {"item": "goblin_armor", "chance": 0.05},
        ],
        "description": "A snarling goblin brandishes a crude weapon.",
        "resistances": {},
        "special": None,
    },
    
    "orc": {
        "name": "an orc warrior",
        "aliases": ["orc", "orc warrior"],
        "level": 7,
        "hp": 75,
        "damage": "2d6+3",
        "exp": 200,
        "gold": (10, 40),
        "spawn_areas": ["dungeon", "mountain", "blackavar"],
        "spawn_rate": 0.15,
        "behavior": "aggressive",
        "loot": [
            {"item": "orc_sword", "chance": 0.1},
            {"item": "leather_armor", "chance": 0.1},
        ],
        "description": "A brutish orc warrior glares at you.",
        "resistances": {},
        "special": None,
    },
    
    "skeleton": {
        "name": "a skeleton",
        "aliases": ["skeleton"],
        "level": 6,
        "hp": 40,
        "damage": "1d6+1",
        "exp": 150,
        "gold": (2, 20),
        "spawn_areas": ["dungeon", "graveyard", "darkcaverns"],
        "spawn_rate": 0.25,
        "behavior": "aggressive",
        "loot": [
            {"item": "bone_fragment", "chance": 0.2},
            {"item": "rusty_sword", "chance": 0.1},
        ],
        "description": "A clattering skeleton advances toward you.",
        "resistances": {"piercing": 25, "cold": 50},
        "special": None,
    },
    
    "zombie": {
        "name": "a zombie",
        "aliases": ["zombie"],
        "level": 4,
        "hp": 55,
        "damage": "1d6+2",
        "exp": 100,
        "gold": (3, 15),
        "spawn_areas": ["dungeon", "graveyard", "swamp", "darkcaverns"],
        "spawn_rate": 0.2,
        "behavior": "aggressive",
        "loot": [
            {"item": "rotting_flesh", "chance": 0.15},
            {"item": "tattered_cloth", "chance": 0.1},
        ],
        "description": "A shambling zombie moans and reaches for you.",
        "resistances": {"slashing": 25, "cold": 50, "poison": 100},
        "special": None,
    },
    
    # High-level monsters (levels 15+)
    "dragon": {
        "name": "a red dragon",
        "aliases": ["dragon", "red dragon"],
        "level": 25,
        "hp": 500,
        "damage": "3d10+10",
        "exp": 5000,
        "gold": (200, 1000),
        "spawn_areas": ["mountain", "volcano", "everrest"],
        "spawn_rate": 0.05,
        "behavior": "aggressive",
        "loot": [
            {"item": "dragon_scale", "chance": 0.5},
            {"item": "dragon_fang", "chance": 0.3},
            {"item": "dragon_hoard", "chance": 0.8},
        ],
        "description": "A massive red dragon fills the cavern with its presence.",
        "resistances": {"fire": 100, "magic": 50},
        "special": "fire_breath",
    },
    
    "lich": {
        "name": "a lich",
        "aliases": ["lich"],
        "level": 20,
        "hp": 300,
        "damage": "2d8+8",
        "exp": 3000,
        "gold": (100, 500),
        "spawn_areas": ["dungeon", "tower", "darkcaverns"],
        "spawn_rate": 0.03,
        "behavior": "aggressive",
        "loot": [
            {"item": "lich_phylactery", "chance": 0.2},
            {"item": "spellbook_dark", "chance": 0.3},
        ],
        "description": "An undead lich radiates dark power.",
        "resistances": {"cold": 75, "poison": 100, "magic": 25},
        "special": "drain_life",
    },
    
    "demon": {
        "name": "a lesser demon",
        "aliases": ["demon", "lesser demon"],
        "level": 15,
        "hp": 200,
        "damage": "2d8+5",
        "exp": 1500,
        "gold": (50, 200),
        "spawn_areas": ["dungeon", "hell", "darkcaverns"],
        "spawn_rate": 0.1,
        "behavior": "aggressive",
        "loot": [
            {"item": "demon_heart", "chance": 0.2},
            {"item": "hellfire_ember", "chance": 0.15},
        ],
        "description": "A twisted demon snarls and lunges at you.",
        "resistances": {"fire": 50, "magic": 25},
        "special": None,
    },
}

# Area-specific spawn tables
AREA_SPAWNS = {
    "lobelands": ["earwig", "bumble_bee", "rat", "spider"],
    "yensid_land": ["earwig", "bumble_bee", "rat"],
    "darkcaverns": ["rat", "spider", "skeleton", "zombie", "goblin"],
    "forest": ["spider", "wolf", "rat"],
    "dungeon": ["rat", "spider", "skeleton", "zombie", "goblin", "orc", "lich", "demon"],
    "mountain": ["wolf", "goblin", "orc", "dragon"],
    "gossamer": ["bumble_bee", "wolf"],
    "sombre": ["wolf", "goblin"],
    "newbie_areas": ["earwig", "rat", "bumble_bee"],
}

def get_monster_data(monster_id):
    """Get monster definition by ID."""
    return MONSTERS.get(monster_id)

def roll_damage(damage_string):
    """
    Roll damage from a dice string like '1d6+2' or '2d8+5'.
    
    Returns:
        int: Total damage
    """
    import re
    match = re.match(r'(\d+)d(\d+)(?:\+(\d+))?', damage_string)
    if not match:
        return 0
    
    num_dice = int(match.group(1))
    dice_size = int(match.group(2))
    bonus = int(match.group(3)) if match.group(3) else 0
    
    total = sum(random.randint(1, dice_size) for _ in range(num_dice))
    return total + bonus

def create_monster(monster_id, location):
    """
    Create a monster instance in a location.
    
    Args:
        monster_id: Key from MONSTERS dict
        location: Room to spawn in
    
    Returns:
        Mob: Created monster object
    """
    data = get_monster_data(monster_id)
    if not data:
        return None
    
    monster = create_object(
        Mob,
        key=data["name"],
        location=location,
        attributes=[
            ("db.level", data["level"]),
            ("db.hp", data["hp"]),
            ("db.max_hp", data["hp"]),
            ("db.damage", data["damage"]),
            ("db.exp_reward", data["exp"]),
            ("db.gold", random.randint(data["gold"][0], data["gold"][1])),
            ("db.behavior", data["behavior"]),
            ("db.loot_table", data["loot"]),
            ("db.resistances", data["resistances"]),
            ("db.special", data["special"]),
        ]
    )
    
    monster.aliases.add(*data["aliases"])
    monster.db.desc = data["description"]
    
    return monster

def spawn_monsters_for_area(area_name, room_list, max_monsters=5):
    """
    Spawn monsters for a given area.
    
    Args:
        area_name: Area identifier
        room_list: List of rooms to spawn in
        max_monsters: Maximum monsters to spawn
    
    Returns:
        list: Spawned monster objects
    """
    spawnable = AREA_SPAWNS.get(area_name, [])
    if not spawnable:
        return []
    
    spawned = []
    for room in room_list:
        # Check each possible monster
        for monster_id in spawnable:
            data = get_monster_data(monster_id)
            if not data:
                continue
            
            # Roll spawn chance
            if random.random() < data["spawn_rate"]:
                monster = create_monster(monster_id, room)
                if monster:
                    spawned.append(monster)
                    
                    if len(spawned) >= max_monsters:
                        return spawned
    
    return spawned

# Boss monsters for special locations
BOSSES = {
    "yensid_overseer": {
        "name": "the Yensid Overseer",
        "level": 10,
        "hp": 150,
        "damage": "2d6+5",
        "exp": 800,
        "gold": (50, 100),
        "location": "yensid_land",
        "loot": [
            {"item": "overseer_ring", "chance": 0.5},
            {"item": "yensid_crystal", "chance": 0.3},
        ],
        "description": "The Overseer of Yensid Land stands before you.",
    },
    "blackavar_guardian": {
        "name": "the Blackavar Guardian",
        "level": 20,
        "hp": 350,
        "damage": "3d8+8",
        "exp": 2500,
        "gold": (100, 300),
        "location": "blackavar_city",
        "loot": [
            {"item": "guardian_shield", "chance": 0.4},
            {"item": "blackavar_key", "chance": 0.2},
        ],
        "description": "The ancient guardian of Blackavar awakens.",
    },
}

def create_boss(boss_id, location):
    """Create a boss monster."""
    data = BOSSES.get(boss_id)
    if not data:
        return None
    
    boss = create_object(
        Mob,
        key=data["name"],
        location=location,
        attributes=[
            ("db.is_boss", True),
            ("db.level", data["level"]),
            ("db.hp", data["hp"]),
            ("db.max_hp", data["hp"]),
            ("db.damage", data["damage"]),
            ("db.exp_reward", data["exp"]),
            ("db.gold", random.randint(data["gold"][0], data["gold"][1])),
            ("db.loot_table", data["loot"]),
        ]
    )
    
    boss.db.desc = data["description"]
    return boss
