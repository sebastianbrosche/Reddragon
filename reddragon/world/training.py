"""
Red Dragon MUD - Training Cost System
Based on Islands of Myth training data
Exact cost tables and Mount Olympus god training key.
"""

# =============================================================================
# COST PER LEVEL (1-31)
# =============================================================================
# Formula: costs increase by 1.25x each level for exp, ~1.15x for gold

TRAINING_COST_PER_LEVEL = {
    1: {"exp": 200000, "gold": 30000},
    2: {"exp": 250000, "gold": 34500},
    3: {"exp": 312500, "gold": 39675},
    4: {"exp": 390625, "gold": 45626},
    5: {"exp": 488281, "gold": 52470},
    6: {"exp": 610351, "gold": 60340},
    7: {"exp": 762939, "gold": 69391},
    8: {"exp": 953674, "gold": 79800},
    9: {"exp": 1192092, "gold": 91770},
    10: {"exp": 1490116, "gold": 105536},
    11: {"exp": 1862645, "gold": 121366},
    12: {"exp": 2328306, "gold": 139571},
    13: {"exp": 2910383, "gold": 160507},
    14: {"exp": 3637978, "gold": 184583},
    15: {"exp": 4547473, "gold": 212271},
    16: {"exp": 5684342, "gold": 244111},
    17: {"exp": 7105427, "gold": 280728},
    18: {"exp": 8811784, "gold": 322837},
    19: {"exp": 11102230, "gold": 371263},
    20: {"exp": 13877788, "gold": 426952},
    21: {"exp": 17347236, "gold": 490995},
    22: {"exp": 21684044, "gold": 564645},
    23: {"exp": 27105054, "gold": 649342},
    24: {"exp": 33881316, "gold": 746743},
    25: {"exp": 42351648, "gold": 858754},
    26: {"exp": 52939556, "gold": 987568},
    27: {"exp": 66174452, "gold": 1135703},
    28: {"exp": 82718064, "gold": 1306058},
    29: {"exp": 103397568, "gold": 1501967},
    30: {"exp": 129246976, "gold": 1727262},
    31: {"exp": 161558720, "gold": 1986351},
}

# =============================================================================
# CUMULATIVE COST TOTALS (1-31)
# =============================================================================

TRAINING_COST_TOTALS = {
    1: {"exp": 200000, "gold": 30000},
    2: {"exp": 450000, "gold": 64500},
    3: {"exp": 762500, "gold": 104175},
    4: {"exp": 1153125, "gold": 149801},
    5: {"exp": 1641406, "gold": 202271},
    6: {"exp": 2251757, "gold": 262611},
    7: {"exp": 3014696, "gold": 332002},
    8: {"exp": 3968370, "gold": 411802},
    9: {"exp": 5160462, "gold": 503572},
    10: {"exp": 6650578, "gold": 609108},
    11: {"exp": 8513223, "gold": 730474},
    12: {"exp": 10841529, "gold": 870045},
    13: {"exp": 13751912, "gold": 1030552},
    14: {"exp": 17389890, "gold": 1215135},
    15: {"exp": 21937363, "gold": 1427406},
    16: {"exp": 27621705, "gold": 1671517},
    17: {"exp": 34727132, "gold": 1952245},
    18: {"exp": 43608916, "gold": 2275082},
    19: {"exp": 54711146, "gold": 2646345},
    20: {"exp": 68588934, "gold": 3073297},
    21: {"exp": 85936170, "gold": 3564292},
    22: {"exp": 107620214, "gold": 4128937},
    23: {"exp": 134725268, "gold": 4778279},
    24: {"exp": 168606584, "gold": 5525022},
    25: {"exp": 210958232, "gold": 6383776},
    26: {"exp": 263897788, "gold": 7391344},
    27: {"exp": 330072240, "gold": 8507047},
    28: {"exp": 412790304, "gold": 9813105},
    29: {"exp": 516187872, "gold": 11315072},
    30: {"exp": 645434848, "gold": 13042334},
    31: {"exp": 806993568, "gold": 15028685},
}

# =============================================================================
# MOUNT OLYMPUS GOD TRAINING KEY
# =============================================================================
# Each stat has a patron god at Mount Olympus

MOUNT_OLYMPUS_GODS = {
    "str": "Heracles",
    "dex": "Artemis",
    "con": "Achilles",
    "sta": "Hermes",
    "int": "Apollo",
    "wis": "Athena",
    "cha": "Aphrodite",
    "hpr": "Euphrosyne",
    "spr": "Agalaia",
    "epr": "Thalia",
}

# =============================================================================
# COST FORMULAS
# =============================================================================

def get_exp_cost(level):
    """Get experience cost for a specific training level."""
    return TRAINING_COST_PER_LEVEL.get(level, {}).get("exp", 0)

def get_gold_cost(level):
    """Get gold cost for a specific training level."""
    return TRAINING_COST_PER_LEVEL.get(level, {}).get("gold", 0)

def get_cumulative_exp(level):
    """Get cumulative experience cost up to a level."""
    return TRAINING_COST_TOTALS.get(level, {}).get("exp", 0)

def get_cumulative_gold(level):
    """Get cumulative gold cost up to a level."""
    return TRAINING_COST_TOTALS.get(level, {}).get("gold", 0)

def calculate_exp_cost_formula(level):
    """
    Calculate exp cost using the 1.25x multiplier formula.
    Base: 200,000 at level 1
    """
    if level < 1:
        return 0
    return int(200000 * (1.25 ** (level - 1)))

def calculate_gold_cost_formula(level):
    """
    Calculate gold cost using the ~1.15x multiplier formula.
    Base: 30,000 at level 1
    """
    if level < 1:
        return 0
    return int(30000 * (1.15 ** (level - 1)))

def get_god_for_stat(stat):
    """Get the Mount Olympus god name for a given stat."""
    return MOUNT_OLYMPUS_GODS.get(stat.lower(), "Unknown")

# =============================================================================
# TRAINING COMMAND DATA
# =============================================================================

TRAINING_LOCATIONS = {
    "mount_olympus": {
        "name": "Mount Olympus",
        "desc": "The home of the gods. Train your stats here.",
        "gods": MOUNT_OLYMPUS_GODS,
    },
}
