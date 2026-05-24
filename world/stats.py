"""
Red Dragon MUD - Stats System
Based on Islands of Myth stat data
All stat effects, increase/decrease messages, resistance messages, height/weight.
"""

# =============================================================================
# STAT EFFECTS
# =============================================================================

STAT_EFFECTS = {
    "str": {
        "hp_bonus": 0.5,  # .5hp per +1 str
        "effects": [
            "melee hit power",
            "size of weapons that are wieldable",
            "inventory size",
        ],
    },
    "dex": {
        "ep_bonus": 0.5,  # .5ep per 1 dex
        "effects": [
            "most defensive abilities",
            "amount of melee hits",
        ],
    },
    "con": {
        "hp_bonus": 2.5,  # 2.5hp per 1 con
        "effects": [],
    },
    "sta": {
        "ep_bonus": 2.5,  # +2.5ep per 1 sta
        "effects": [],
    },
    "int": {
        "sp_bonus": 2.0,  # +2sp per 1 int
        "effects": [
            "most attack spells' damage",
        ],
    },
    "wis": {
        "sp_bonus": 2.0,  # +2sp per 1 wis
        "effects": [
            "most healing spell power",
        ],
    },
    "cha": {
        "effects": [
            "influences how much you can buy/sell items in shops",
        ],
    },
    "hpr": {
        "hp_bonus": 5.0,  # +5hp per 1 hpmax
        "effects": [],
    },
    "spr": {
        "sp_bonus": 5.0,  # +5sp per 1 spmax
        "effects": [],
    },
    "epr": {
        "ep_bonus": 5.0,  # +5ep per 1 epmax (note: doc says hpmax typo)
        "effects": [],
    },
}

# =============================================================================
# STAT INCREASE/DECREASE MESSAGES
# =============================================================================

STAT_MESSAGES = {
    "str": {
        "increase": "You feel stronger",
        "decrease": "You feel weaker",
    },
    "dex": {
        "increase": "You feel agile.",
        "decrease": "You feel slower.",
    },
    "con": {
        "increase": "Your muscles swell.",
        "decrease": "Your muscles shrink.",
    },
    "sta": {
        "increase": "You feel more endurant.",
        "decrease": "You feel a bit drained.",
    },
    "int": {
        "increase": "Your brain feels like a sponge.",
        "decrease": "You are a little confused.",
    },
    "wis": {
        "increase": "You feel witty.",
        "decrease": "You feel less witty.",
    },
    "cha": {
        "increase": "You feel more charismatic.",
        "decrease": "You seem less of a leader.",
    },
    "hpr": {
        "increase": "Your heart beats an extra beat.",
        "decrease": "Your heart skips a beat.",
    },
    "spr": {
        "increase": "Your brain pulses.",
        "decrease": "Your brain slows down.",
    },
    "epr": {
        "increase": "You feel refreshed.",
        "decrease": "You feel tired.",
    },
    "all_spells": {
        "increase": "Your spell knowledge increases.",
        "decrease": "Your spell knowledge decreases.",
    },
    "all_skills": {
        "increase": "Your skill knowledge increases.",
        "decrease": "Your skill knowledge decreases.",
    },
}

# =============================================================================
# RESISTANCE MESSAGES (increase/decrease)
# =============================================================================

RESISTANCE_MESSAGES = {
    "acid": {
        "increase": "Your skin becomes resistant.",
        "decrease": "Your skin becomes less resistant.",
    },
    "asphyxiation": {
        "increase": "Your throat clears.",
        "decrease": "Your throat clogs back up.",
    },
    "cold": {
        "increase": "You feel warm.",
        "decrease": "You feel less resistant to cold.",
    },
    "electric": {
        "increase": "You feel less conductive.",
        "decrease": "You feel more conductive.",
    },
    "fire": {
        "increase": "You feel cool.",
        "decrease": "You feel less resistant to fire.",
    },
    "holy": {
        "increase": "You feel closer to the good gods.",
        "decrease": "You feel further from the good gods.",
    },
    "magical": {
        "increase": "You feel arcane power.",
        "decrease": "You feel a loss of arcane power.",
    },
    "physical": {
        "increase": "You feel resistant.",
        "decrease": "You feel less resistant.",
    },
    "poison": {
        "increase": "You feel your internals strengthen.",
        "decrease": "You feel your internals weaken.",
    },
    "psionic": {
        "increase": "You feel your brain structure align.",
        "decrease": "You feel your brain lose focus.",
    },
    "unholy": {
        "increase": "You feel closer to the evil gods.",
        "decrease": "You feel further from the evil gods.",
    },
}

# =============================================================================
# HEIGHT / WEIGHT MESSAGES
# =============================================================================

HEIGHT_WEIGHT_MESSAGES = {
    "height_increase": "Your body grows.",
    "height_decrease": "Your body shrinks.",
    "weight_increase": "You feel heavier than air.",
    "weight_decrease": "You feel lighter than air.",
}

# =============================================================================
# ALL RESISTANCE TYPES
# =============================================================================

ALL_RESISTANCES = [
    "acid",
    "asphyxiation",
    "cold",
    "electric",
    "fire",
    "holy",
    "magical",
    "physical",
    "poison",
    "psionic",
    "unholy",
]

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_stat_increase_message(stat):
    """Get the increase message for a stat."""
    return STAT_MESSAGES.get(stat, {}).get("increase", "You feel different.")

def get_stat_decrease_message(stat):
    """Get the decrease message for a stat."""
    return STAT_MESSAGES.get(stat, {}).get("decrease", "You feel different.")

def get_resistance_increase_message(resistance):
    """Get the increase message for a resistance."""
    return RESISTANCE_MESSAGES.get(resistance, {}).get("increase", "You feel more resistant.")

def get_resistance_decrease_message(resistance):
    """Get the decrease message for a resistance."""
    return RESISTANCE_MESSAGES.get(resistance, {}).get("decrease", "You feel less resistant.")

def get_stat_effect_description(stat):
    """Get the gameplay effects of a stat."""
    data = STAT_EFFECTS.get(stat, {})
    effects = data.get("effects", [])
    bonuses = []
    if "hp_bonus" in data:
        bonuses.append(f"+{data['hp_bonus']} HP per point")
    if "ep_bonus" in data:
        bonuses.append(f"+{data['ep_bonus']} EP per point")
    if "sp_bonus" in data:
        bonuses.append(f"+{data['sp_bonus']} SP per point")
    return {
        "bonuses": bonuses,
        "effects": effects,
    }
