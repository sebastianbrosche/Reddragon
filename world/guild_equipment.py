"""
Red Dragon MUD - Guild Equipment Database
Parsed from IOM guild equipment data
"""

GUILD_EQUIPMENT = {
    "abjurer": {
        "name": "mystical shield",
        "type": "shield",
        "class": 16,
        "handed": 1,
        "stat_bonuses": {
            "int": None,  # variable
            "wis": None,
            "spr": None,
        },
        "skill_bonuses": [
            "enhance abjuration",
            "lengthen abjuration",
            "strengthen abjuration",
        ],
        "ranks": [
            (1, "Novice abjurer"),
            (2, "Apprentice abjurer"),
            (3, "Abjurer trainee"),
            (5, "Expert abjurer"),
            (6, "Master abjurer"),
        ],
    },
    "acrobat": {
        "name": "bard feathered hat",
        "type": "head",
        "class": 2,
        "slots": ["head"],
        "stat_bonuses": {
            "dex": None,
            "wis": None,
            "cha": None,
            "spr": None,
            "epr": None,
            "avoid_hits": None,
        },
        "skill_bonuses": [
            "storytelling",
            "please audience",
        ],
        "ranks": [
            (5, "Master bard"),
            (6, "Master composer"),
        ],
    },
    "druid": {
        "name": "druidic staff",
        "type": "blunt",
        "class": 56,
        "stat_bonuses": {
            "wis": 46,
            "int": 37,
            "con": 18,
            "sp_regen": 56,
            "hp_regen": 9,
        },
        "resistances": {
            "electric": 14,
            "physical": 9,
        },
        "skill_bonuses": {
            "quick chant": 4,
            "crystal efficiency": 4,
            "lore of the soil sha": 4,
        },
        "ranks": [
            (1, "Novice"),
            (2, "Initiate of Gaia"),
            (3, "Affiliate of Gaia"),
            (4, "Druid of Gaia"),
            (5, "Priest of Gaia"),
            (6, "Master Druid"),
            (7, "Druid Lord"),
        ],
    },
    "elemental": {
        "name": "ring of the elements",
        "class": 4,
        "slots": ["finger"],
        "stat_bonuses": {
            "wis": 14,
            "sp_regen": 43,
            "int": 38,
        },
        "resistances": {
            "physical": 9,
            "cold": 9,
            "fire": 9,
            "asphyxiation": 9,
        },
        "skill_bonuses": {
            "quick chant": 4,
            "mastery of elements": 4,
        },
        "ranks": [
            (1, "Apprentice elemental mage"),
            (2, "Student of elemental lore"),
            (3, "Elemental mage"),
            (4, "Senior elemental mage"),
            (5, "Master elemental mage"),
            (6, ""),
            (7, "Lord of Elements"),
        ],
    },
    "evoker": {
        "name": "prismatic amulet",
        "armor_class": 4,
        "slots": ["amulet"],
        "stat_bonuses": {
            "int": 35,
            "wis": 25,
            "spr": 40,
        },
        "resistances": {
            "poison": 5,
            "acid": 5,
            "magic": 5,
            "physical": 5,
            "cold": 5,
            "fire": 5,
            "asphyxiation": 5,
            "electric": 5,
        },
        "skill_bonuses": {
            "mastery of evocation": "5%",
        },
        "ranks": [
            (1, "Initiate evoker"),
            (3, "Evoker"),
            (7, "Grandmaster of evocation"),
        ],
    },
    "inquisitor": {
        "name": "ceremonial robe",
        "class": 11,
        "slots": ["torso"],
        "stat_bonuses": {
            "int": None,
            "wis": None,
            "spr": None,
        },
        "resistances": {
            "unholy": None,
        },
        "ranks": [
            (1, "Believer"),
            (2, "Initiate"),
            (3, "Follower"),
            (4, ""),
            (5, "Priest"),
            (6, "High Priest"),
            (7, ""),
        ],
    },
    "martial_artist": {
        "name": "black leather gloves",
        "class": 6,
        "stat_bonuses": {
            "str": None,
            "dex": None,
            "hpr": None,
            "epr": None,
            "damage": None,
        },
        "skill_bonuses": [
            "fists of fury",
            "dragonfist",
        ],
        "ranks": [
            (1, "Student"),
            (2, "Novice"),
            (3, "Subadult"),
            (4, "Martial artist"),
            (5, "Old"),
            (6, "Ancient"),
        ],
    },
    "necromancer": {
        "name": "Wooden staff of the necromancer",
        "armor_class": 40,
        "stat_bonuses": {
            "con": 12,
            "int": 33,
            "wis": 28,
            "hp_regen": 12,
            "sp_regen": 39,
        },
        "skill_bonuses": {
            "anatomy": 2,
            "dead speak": 2,
            "hematology": 3,
            "mastery of mummificati": 3,
            "mind power": 3,
            "minion control": 2,
            "osteology": 2,
            "voodooism": 2,
        },
        "ranks": [
            (1, ""),
            (2, ""),
            (3, ""),
            (4, "Master necromancer"),
            (5, ""),
            (6, ""),
            (7, ""),
        ],
    },
    "shapeshifter": {
        "name": "Shapeshifters' Collar",
        "armor_class": 22,
        "slots": ["neck"],
        "stat_bonuses": {
            "dex": 10,
            "hp_regen": 10,
            "con": 15,
            "str": 15,
            "int": 25,
            "sta": 15,
            "ep_regen": 10,
        },
        "skill_bonuses": {
            "avian lore": 6,
            "canine lore": 6,
            "draconian lore": 6,
            "feline lore": 6,
            "ursine lore": 6,
        },
        "ranks": [
            (1, "Imitator"),
            (2, "Impersonator"),
            (3, "Shapeshifter"),
            (4, "Practiced Shapeshifter"),
            (5, "Changeling"),
            (6, "Metamorphe"),
            (7, ""),
        ],
    },
    "warrior": {
        "name": "ornamented warrior belt",
        "class": 7,
        "slots": ["belt"],
        "stat_bonuses": {
            "hpr": None,
            "str": None,
            "con": None,
        },
        "skill_bonuses": [
            "dodge",
            "weaponmaster",
        ],
        "resistances": {
            "physical": None,
        },
        "ranks": [
            (1, "Warrior trainee"),
            (2, "Warrior"),
            (3, "Veteran warrior"),
            (4, ""),
            (5, "Warrior of the crown"),
            (6, ""),
            (7, ""),
        ],
    },
    "weaver": {
        "name": "holy ankh",
        "armor_class": 4,
        "slots": ["neck"],
        "stat_bonuses": {
            "wis": 35,
            "con": 25,
            "spr": 40,
        },
        "resistances": {
            "holy": 20,
        },
        "skill_bonuses": {
            "mastery fo healing": "5%",
            "enhance healing": "5%",
        },
        "ranks": [
            (1, "Apprentice nurse"),
            (2, "Medic helper"),
            (3, "Apprentice healer"),
            (4, "Journeyman healer"),
            (5, "Trained healer"),
            (6, "Expert healer"),
            (7, "Master healer"),
        ],
    },
    "woodsman": {
        "name": "magical woodsman cloak",
        "armor_class": 24,
        "slots": ["cloak"],
        "stat_bonuses": {
            "hp_regen": 14,
            "str": 24,
            "dex": 33,
            "ep_regen": 14,
            "con": 9,
        },
        "resistances": {
            "physical": 9,
            "cold": 14,
        },
        "skill_bonuses": {
            "harmony with nature": 4,
            "natural weapon lore": 4,
        },
        "ranks": [
            (1, "Novice woodsman"),
            (2, ""),
            (3, "Trained woodsman"),
            (4, "Expert woodsman"),
            (5, "Ranger"),
            (6, "Master ranger"),
            (7, "Ranger lord"),
        ],
    },
    "witch": {
        "name": "wooden broom",
        "type": "blunt",
        "handed": "both",
        "weapon_class": 45,
        "stat_bonuses": {
            "int": 45,
            "wis": 40,
            "con": 20,
            "spr": 55,
            "hpr": 20,
        },
        "resistances": {
            "magic": 10,
            "electric": 10,
            "physical": 10,
            "psi": 10,
        },
        "skill_bonuses": {
            "brewing lore": "5%",
            "lore of the elders": "5%",
            "talisman ceremonies": "5%",
            "mental tide": "5%",
            "dreamweaving lore": "5%",
            "lore of the watchers": "5%",
        },
        "ranks": [
            (1, "Servant to the Coven"),
            (2, "Apprentice warlock"),
            (3, "Learning Warlock"),
            (4, "Hex brother"),
            (6, "Master of the Coven"),
            (7, "Elder warlock"),
        ],
    },
}

# Guild hierarchy from IOM
GUILD_HIERARCHY = {
    "beta": {
        "animist": ["druid", "shapeshifter", "woodsman"],
        "cleric": ["inquisitor", "weaver"],
        "fighter": ["martial artist", "warrior"],
        "mage": ["abjurer", "elemental", "evoker", "necromancer"],
        "rogue": ["acrobat", "thief"],
    },
    "gamma": {
        "mage": ["witch"],
    },
}

# All guild names
ALL_GUILDS = [
    "abjurer", "acrobat", "druid", "elemental", "evoker",
    "inquisitor", "martial artist", "necromancer", "shapeshifter",
    "warrior", "weaver", "woodsman", "witch", "thief",
]

# Guild base classes
GUILD_BASE_CLASSES = {
    "abjurer": "mage",
    "elemental": "mage",
    "evoker": "mage",
    "necromancer": "mage",
    "witch": "mage",
    "druid": "animist",
    "shapeshifter": "animist",
    "woodsman": "animist",
    "inquisitor": "cleric",
    "weaver": "cleric",
    "martial artist": "fighter",
    "warrior": "fighter",
    "acrobat": "rogue",
    "thief": "rogue",
}
