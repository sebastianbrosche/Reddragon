"""
Red Dragon MUD - Equipment System
Based on Islands of Myth equipment data
Decay scale, equipment types, spider silk, SNAFU items, spellbooks, tickets, lodestones.
"""

# =============================================================================
# DECAY SCALE (9 levels from mint to broken)
# =============================================================================

DECAY_SCALE = {
    9: {
        "condition": "mint",
        "desc": "It is in mint condition and is brand new.",
    },
    8: {
        "condition": "near-mint",
        "desc": "It is in near-mint condition and is as good as new.",
    },
    7: {
        "condition": "excellent",
        "desc": "It is in excellent condition and has seen some use.",
    },
    6: {
        "condition": "great",
        "desc": "It is in great condition and has been well repaired.",
    },
    5: {
        "condition": "good",
        "desc": "It is in good shape and has been patched a few times.",
    },
    4: {
        "condition": "scratched",
        "desc": "It is somewhat scratched and has been heavily used.",
    },
    3: {
        "condition": "heavily scratched",
        "desc": "It is heavily scratched and is heavily decayed.",
    },
    2: {
        "condition": "battered",
        "desc": "It is in a battered condition and is nearly worn out.",
    },
    1: {
        "condition": "broken",
        "desc": "It is broken and unusable.",
    },
}

# =============================================================================
# EQUIPMENT TYPES
# =============================================================================

EQUIPMENT_TYPES = {
    "regular": {
        "desc": "Any basic item currently available in-game",
        "saveable": True,
        "magical": False,
    },
    "nosave": {
        "desc": "Any item that will not save on a player's body, in a castle, or on the ground",
        "saveable": False,
        "magical": False,
    },
    "magical": {
        "desc": "Any item that gives some sort of bonus and is currently available in-game",
        "saveable": True,
        "magical": True,
    },
    "unique": {
        "desc": "Special items with only one copy distributed in-game through various methods",
        "saveable": True,
        "magical": True,
    },
    "ungettable": {
        "desc": "Special items that have been changed and the original was not removed, or items that have been removed",
        "saveable": True,
        "magical": True,
    },
    "random_pool": {
        "desc": "Magical items randomly dropped by random smaller EQ monsters",
        "saveable": True,
        "magical": True,
    },
    "random_unique": {
        "desc": "Special magical items dropped by random exp monsters that last about a couple of weeks before disappearing",
        "saveable": True,
        "magical": True,
        "party_bound": True,
    },
    "random_newbie": {
        "desc": "Magical items dropped by random monsters that are only useable by the newbie player or their party",
        "saveable": True,
        "magical": True,
        "newbie_bound": True,
    },
}

# =============================================================================
# SPIDER SILK SYSTEM
# =============================================================================

SPIDER_SILK_DATA = {
    "dropped_by": ["spiders", "driders"],
    "event": "Lloth's Children",
    "specials": [
        "randomly drain the wearer's enemies of sp",
        "randomly damage the wearer's enemies",
        "randomly reduces the wearer's spell casting time",
    ],
    "combine": True,  # Can combine to save inventory space
    "ball_sizes": [
        "miniscule",
        "tiny",
        "small",
        "smaller than average",
        "average",
        "larger than average",
        "large",
        "huge",
        "gigantic",
    ],
}

# =============================================================================
# GUILD CREATED ITEMS
# =============================================================================

GUILD_CREATED_TYPES = {
    "nosave_magical": {
        "desc": "Nosave magical items created by different guilds, tailored to guild stats",
        "saveable": False,
    },
    "lava": {
        "desc": "Nosave magical items created by Lava Mage guild members, with random stat bonuses",
        "saveable": False,
        "creator_guild": "lava_mage",
    },
    "shadow": {
        "desc": "Nosave magical items created by Disciple Of Shadow guild members",
        "saveable": False,
        "creator_guild": "disciple_of_shadow",
    },
}

# =============================================================================
# FORMULAS (Master Enchanter system)
# =============================================================================

FORMULA_DATA = {
    "dropped_by": "random monsters",
    "used_by": "Master Enchanter guild members",
    "effect": "teaches one particular slot and enchantment type",
}

# =============================================================================
# SNAFU ITEMS (animal body parts -> magical newbie items)
# =============================================================================

SNAFU_STAT_ANIMAL_KEY = {
    "str": "Termite",
    "dex": "Weasel",
    "con": "Moose",
    "sta": "Stallion",
    "int": "Hedgehog",
    "wis": "Turtle",
    "cha": "Kangaroo",
    "hpr": "Rabbit",
    "spr": "Dragon",
    "epr": "Wombat",
}

# Reverse lookup
SNAFU_ANIMAL_STAT_KEY = {v.lower(): k for k, v in SNAFU_STAT_ANIMAL_KEY.items()}

SNAFU_DATA = {
    "source": "SNAFU Forest animal body parts",
    "target": "magical items for newbies only",
    "stat_animal_key": SNAFU_STAT_ANIMAL_KEY,
}

# =============================================================================
# SPELLBOOKS / RINGS OF KNOWLEDGE
# =============================================================================

GETTABLE_SPELLBOOKS = [
    "Barkskin",
    "Clairvoyance",
    "Condition Orbit",
    "Create Food",
    "Create Navigation Stone",
    "Diagnose",
    "Distant Sell",
    "Enlarge Weapon",
    "Estimate Worth",
    "Heavy Weight",
    "Identify",
    "Know Alignment",
    "Magical Void",
    "Remove Poison",
    "Remove Scar",
    "Shrink Weapon",
]

UNGETTABLE_SPELLBOOKS = [
    "Carrier Pigeon",
    "Continual Darkness",
    "Continual Light",
    "Cure Light Wounds",
    "Heal All In Mud",
    "Prayer For Mankind",
]

GETTABLE_RINGS = [
    "Air Shield",
    "Darkness",
    "Flame Blade",
    "Guild Portal",
    "Identify",
    "Light",
]

SPELLBOOK_DATA = {
    "cast_level": 0.75,  # Cast spell at ~75% studied level
    "usage": "You must look at the book/ring to determine what spell it allows",
    "gettable_books": GETTABLE_SPELLBOOKS,
    "ungettable_books": UNGETTABLE_SPELLBOOKS,
    "gettable_rings": GETTABLE_RINGS,
}

# =============================================================================
# TICKETS
# =============================================================================

GETTABLE_TICKETS = [
    "Free Resurrect",
    "Free Reinc",
    "Free Exp",
    "Equipment Repair",
    "Random Event",
    "Battle Royale Event",
    "Berserking Lessons Event",
    "Dhrugs' Rage Event",
    "Escape From Hell Event",
    "Feast Of Fools Event",
    "Lloth's Children Event",
    "Nosuck Event",
    "Time Of Life Event",
    "Personal Nosuck",
    "Personal Time Of Life",
    "Time Of Life Event",  # Listed twice in original
]

TICKET_DATA = {
    "desc": "Tickets are general items for special abilities or effects, given out for various reasons",
    "gettable": GETTABLE_TICKETS,
}

# =============================================================================
# LODESTONES (Navigation Stones)
# =============================================================================

LODESTONE_DATA = {
    "desc": "Navigation stones that transport you to preset or chosen locations",
    "creation": "Created via the spell 'Create Navigation Stone'",
    "usage": "You must look at the lodestone to determine its teleport destination",
    "types": [
        "random preset location",
        "owner-chosen location",
    ],
}

# =============================================================================
# RACE LEADERSHIP EQ
# =============================================================================

RACE_LEADERSHIP_EQ_DATA = {
    "desc": "Magical items given to the current race leader when they are the highest guild level of their race logged in",
    "distribution": "One piece per race leader",
}

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_decay_desc(decay_level):
    """Get the description for a given decay level (1-9)."""
    data = DECAY_SCALE.get(decay_level, {})
    return data.get("desc", "Unknown condition.")

def get_equipment_type_desc(eq_type):
    """Get the description for an equipment type."""
    data = EQUIPMENT_TYPES.get(eq_type, {})
    return data.get("desc", "Unknown equipment type.")

def get_snafu_animal_for_stat(stat):
    """Get the SNAFU animal name for a stat."""
    return SNAFU_STAT_ANIMAL_KEY.get(stat.lower(), "Unknown")

def get_snafu_stat_for_animal(animal):
    """Get the stat for a SNAFU animal name."""
    return SNAFU_ANIMAL_STAT_KEY.get(animal.lower(), "Unknown")
