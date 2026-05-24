"""
Red Dragon MUD - Hunger System
Based on Islands of Myth hunger data
Scale and HP/SP/EP regeneration effects.
"""

# =============================================================================
# HUNGER SCALE
# =============================================================================

HUNGER_SCALE = {
    "starved": {
        "min": 0,
        "max": 2,
        "desc": "Starved",
        "regen_penalty": 0.0,  # No regeneration
    },
    "craving": {
        "min": 3,
        "max": 10,
        "desc": "Craving",
        "regen_penalty": 0.25,  # 25% regeneration
    },
    "hungry": {
        "min": 11,
        "max": 20,
        "desc": "Hungry",
        "regen_penalty": 0.50,  # 50% regeneration
    },
    "peckish": {
        "min": 21,
        "max": 50,
        "desc": "Peckish",
        "regen_penalty": 0.75,  # 75% regeneration
    },
    "content": {
        "min": 51,
        "max": 75,
        "desc": "Content",
        "regen_penalty": 1.0,  # 100% regeneration
    },
    "full": {
        "min": 76,
        "max": 95,
        "desc": "Full",
        "regen_penalty": 1.0,  # 100% regeneration
    },
    "stuffed": {
        "min": 96,
        "max": 100,
        "desc": "Stuffed",
        "regen_penalty": 0.80,  # 80% regeneration (slight penalty for overeating)
    },
}

# =============================================================================
# HUNGER MESSAGES
# =============================================================================

HUNGER_MESSAGES = {
    "starved": "You are starving! You need food immediately!",
    "craving": "Your stomach rumbles loudly. You crave food.",
    "hungry": "You feel hungry.",
    "peckish": "You could use a snack.",
    "content": "You feel content.",
    "full": "You feel full.",
    "stuffed": "You are stuffed! You can barely move.",
}

# =============================================================================
# HUNGER EFFECTS ON REGENERATION
# =============================================================================
# HP, SP, and EP regeneration are all affected by hunger level

def get_hunger_state(hunger_percent):
    """
    Get the hunger state name and regen multiplier for a given hunger percentage.
    """
    if hunger_percent < 0:
        hunger_percent = 0
    if hunger_percent > 100:
        hunger_percent = 100

    for state_name, data in HUNGER_SCALE.items():
        if data["min"] <= hunger_percent <= data["max"]:
            return {
                "state": state_name,
                "desc": data["desc"],
                "regen_multiplier": data["regen_penalty"],
                "message": HUNGER_MESSAGES.get(state_name, ""),
            }

    # Fallback
    return {
        "state": "content",
        "desc": "Content",
        "regen_multiplier": 1.0,
        "message": HUNGER_MESSAGES["content"],
    }

def get_regen_multiplier(hunger_percent):
    """Get the HP/SP/EP regeneration multiplier based on hunger."""
    state = get_hunger_state(hunger_percent)
    return state["regen_multiplier"]

def get_hunger_message(hunger_percent):
    """Get the appropriate hunger message."""
    state = get_hunger_state(hunger_percent)
    return state["message"]

# =============================================================================
# FOOD CONSUMPTION
# =============================================================================

# Food items restore hunger by reducing hunger percentage
# (lower hunger % = more full)

FOOD_RESTORE_AMOUNT = {
    "small_snack": 5,
    "light_meal": 15,
    "standard_meal": 25,
    "hearty_meal": 40,
    "feast": 60,
}

# =============================================================================
# HUNGER TICKS (natural hunger increase over time)
# =============================================================================

HUNGER_INCREASE_PER_TICK = 1  # Hunger increases by 1% per tick
HUNGER_TICK_INTERVAL = 60  # Seconds between hunger ticks

# =============================================================================
# DEATH FROM STARVATION
# =============================================================================

STARVATION_DAMAGE = 5  # HP lost per tick when starved (0-2%)
STARVATION_WARNING = "You are starving! Your body begins to weaken!"
