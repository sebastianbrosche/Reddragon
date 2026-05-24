"""
Red Dragon MUD - Armor Class System
Based on Islands of Myth armor class data
Scale from None to BEST.
"""

# =============================================================================
# ARMOR CLASS SCALE
# =============================================================================

ARMOR_CLASS_SCALE = [
    "None",
    "Low",
    "Average",
    "High",
    "VHigh",
    "Great",
    "Super",
    "BEST",
]

# =============================================================================
# ARMOR CLASS RATINGS (numeric for calculations)
# =============================================================================

ARMOR_CLASS_RATINGS = {
    "None": 0,
    "Low": 1,
    "Average": 2,
    "High": 3,
    "VHigh": 4,
    "Great": 5,
    "Super": 6,
    "BEST": 7,
}

# =============================================================================
# ARMOR CLASS MESSAGES
# =============================================================================

ARMOR_CLASS_MESSAGES = {
    "None": "You are completely unprotected.",
    "Low": "You have minimal protection.",
    "Average": "You have average protection.",
    "High": "You have good protection.",
    "VHigh": "You have very high protection.",
    "Great": "You have great protection.",
    "Super": "You have superb protection.",
    "BEST": "You have the best possible protection.",
}

# =============================================================================
# DAMAGE REDUCTION MULTIPLIERS (by armor class)
# =============================================================================
# Higher armor class = less damage taken

DAMAGE_REDUCTION = {
    "None": 1.0,      # 100% damage taken
    "Low": 0.85,      # 85% damage taken
    "Average": 0.70,  # 70% damage taken
    "High": 0.55,     # 55% damage taken
    "VHigh": 0.45,    # 45% damage taken
    "Great": 0.35,    # 35% damage taken
    "Super": 0.25,    # 25% damage taken
    "BEST": 0.15,     # 15% damage taken
}

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_armor_class_rating(ac_name):
    """Get numeric rating for an armor class name."""
    return ARMOR_CLASS_RATINGS.get(ac_name, 0)

def get_armor_class_name(rating):
    """Get armor class name from numeric rating."""
    for name, val in ARMOR_CLASS_RATINGS.items():
        if val == rating:
            return name
    return "None"

def get_damage_reduction(ac_name):
    """Get damage reduction multiplier for an armor class."""
    return DAMAGE_REDUCTION.get(ac_name, 1.0)

def get_armor_message(ac_name):
    """Get the status message for an armor class."""
    return ARMOR_CLASS_MESSAGES.get(ac_name, "Unknown protection level.")

def calculate_mitigated_damage(raw_damage, ac_name):
    """Calculate damage after armor mitigation."""
    reduction = get_damage_reduction(ac_name)
    return int(raw_damage * reduction)
