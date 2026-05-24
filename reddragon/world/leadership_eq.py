"""
Red Dragon MUD - Race Leadership Equipment
Based on Islands of Myth leadership EQ data
All 27 races with their leadership equipment piece and stats.
"""

# =============================================================================
# RACE LEADERSHIP EQ TABLE
# =============================================================================

RACE_LEADERSHIP_EQ = {
    "Cromagnon": {
        "item": "Magical nosebone of gam'ba'la",
        "stats": {},  # Unknown bonuses
        "notes": "Unknown stats",
    },
    "Drow": {
        "item": "Sleek black scabbard of darkness",
        "stats": {"str": 4, "dex": 8, "wis": 4},
    },
    "Dwarf": {
        "item": "Glowing sacred symbol of aule",
        "stats": {"con": 6, "wis": 4, "hpr": 6},
    },
    "Elf": {
        "item": "Elvania's platinum ear",
        "stats": {"con": 5, "wis": 7, "spr": 4},
    },
    "Ent": {
        "item": "Mallorn headband",
        "stats": {"con": 5, "wis": 7, "fire_res": 1},
    },
    "Faerie": {
        "item": "Tiny magical dust pouch of faeries",
        "stats": {"dex": 3, "int": 5, "spr": 7},
    },
    "Gargoyle": {
        "item": "Krishin's stone earrings",
        "stats": {"int": 6, "spr": 6, "con": 4},
    },
    "Giant": {
        "item": "Blue drudge-beast collar",
        "stats": {"str": 3, "con": 4, "hpr": 10},
    },
    "Gnome": {
        "item": "Thinking cap",
        "stats": {"int": 4, "wis": 6, "spr": 6},
    },
    "Goblin": {
        "item": "Abraxas's earring",
        "stats": {},  # Unknown bonuses
        "notes": "Unknown stats",
    },
    "Grorrark": {
        "item": "Mystical teeth pendant of morak",
        "stats": {"str": 6, "dex": 5},
    },
    "Halfelf": {
        "item": "Tiara of duality",
        "stats": {"dex": 8, "wis": 4, "cha": 10},
    },
    "Hobbit": {
        "item": "Old toby's briar pipe",
        "stats": {"dex": 8, "sta": 4, "phys_res": 1},
    },
    "Human": {
        "item": "Imperial great seal",
        "stats": {"str": 3, "dex": 3, "con": 3, "sta": 3, "int": 3, "wis": 3, "cha": 3},
    },
    "Kobold": {
        "item": "Kobold's magical slime ball",
        "stats": {},  # Unknown bonuses
        "notes": "Unknown stats",
    },
    "Leprechaun": {
        "item": "Leprechaun bright feather",
        "stats": {"dex": 3, "int": 5, "spr": 8},
    },
    "Lizardman": {
        "item": "Adamantium tailspike of lizard king",
        "stats": {"str": 6, "dex": 4, "hpr": 6},
    },
    "Mindflayer": {
        "item": "Dark eye of the underworld",
        "stats": {"int": 7, "wis": 5, "sp": 4},  # sp in original, likely spr
    },
    "Minotaur": {
        "item": "Morantha's nosering",
        "stats": {"str": 6, "con": 10},
    },
    "Ogier": {
        "item": "Talisman of growing",
        "stats": {"str": 7, "dex": 5, "sta": 4},
    },
    "Phoenix": {
        "item": "Firedrake's fire opal",
        "stats": {"int": 5, "spr": 7, "fire_res": 1},
    },
    "Snakeman": {
        "item": "Selene's magical scale",
        "stats": {"int": 6, "spr": 6, "poison_res": 1},
    },
    "Thrikhren": {
        "item": "Powerful golden mandibles of g'Tak",
        "stats": {"str": 4, "int": 6, "spr": 6},
    },
    "Troll": {
        "item": "Quicksilver eye",
        "stats": {"con": 10, "fire_res": 1, "acid_res": 1},
    },
    "Vampire": {
        "item": "Fang of nosferatu",
        "stats": {"int": 8, "wis": 4, "holy_res": 1},
    },
    "Vinnipier": {
        "item": "Glowing armband of deirdre",
        "stats": {"str": 4, "dex": 7, "hpr": 5},
    },
    "Xorn": {
        "item": "Xorzan's red scale hide",
        "stats": {},  # Unknown bonuses
        "notes": "Unknown stats",
    },
}

# =============================================================================
# CELESTIAL MAGE VARIANTS
# =============================================================================

CELESTIAL_MAGE_EQ = {
    "Archangel": {
        "item": "Golden tipped wings",
        "stats": {},
        "special": "allows wearer to avoid area spell damage",
    },
    "Archdemon": {
        "item": "Jesrael's demon horns",
        "stats": {},
        "special": "boosts damage on blast spells",
    },
    "Ghyrdon": {
        "item": "Silver spile of syrah",
        "stats": {},
        "special": "Creates small vials of sap that heal a small amount of drinker's endurance points",
    },
    "Gnoll": {
        "item": "Ear stud",
        "stats": {"wis": 6, "dex": 6, "epr": 1},
    },
}

# =============================================================================
# ALL RACES WITH LEADERSHIP EQ
# =============================================================================

ALL_RACE_LEADERSHIP_EQ = {**RACE_LEADERSHIP_EQ, **CELESTIAL_MAGE_EQ}

# =============================================================================
# RACES WITH UNKNOWN STATS
# =============================================================================

UNKNOWN_STAT_RACES = [
    "Cromagnon",
    "Goblin",
    "Kobold",
    "Xorn",
]

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_leadership_eq(race):
    """Get the leadership equipment for a race."""
    return ALL_RACE_LEADERSHIP_EQ.get(race, None)

def get_leadership_eq_stats(race):
    """Get the stats for a race's leadership equipment."""
    eq = ALL_RACE_LEADERSHIP_EQ.get(race, {})
    return eq.get("stats", {})

def get_leadership_eq_item_name(race):
    """Get the item name for a race's leadership equipment."""
    eq = ALL_RACE_LEADERSHIP_EQ.get(race, {})
    return eq.get("item", "Unknown")

def race_has_known_stats(race):
    """Check if a race has known leadership EQ stats."""
    return race not in UNKNOWN_STAT_RACES
