"""
Red Dragon MUD - Reincarnation System
Based on Islands of Myth reincarnation data
Reinc tax reduction, item sacrifice, gold sacrifice formula.
"""

# =============================================================================
# REINCARNATION TAX REDUCTION
# =============================================================================

REINCARNATION_DATA = {
    "natural_daily_decrease": True,  # Tax goes down on an in-game daily basis
    "not_logged_in_based": True,     # Not based on logged-in time
    "sacrifice_npc": "Eje",          # NPC in Illium's Church who accepts sacrifices
    "sacrifice_location": "Illium Church",
}

# =============================================================================
# ITEM REQUIREMENTS FOR SACRIFICE
# =============================================================================
# Eje accepts items meeting at least ONE of these criteria

ITEM_SACRIFICE_REQUIREMENTS = {
    "stat_bonus": 8,          # +8 to at least one basic stat
    "resistance": 3,          # +3 to at least one resistance
    "alpha_spell_skill": 5,   # +5% to at least one alpha type spell/skill
    "bravo_spell_skill": 3,   # +3% to at least one bravo type spell/skill
}

# =============================================================================
# GOLD SACRIFICE FORMULA
# =============================================================================
# A = B * 2^(-G/1000000)
# A: Tax after saccing gold
# B: Tax before saccing gold
# G: Gold amount

def calculate_gold_sacrifice_tax_reduction(tax_before, gold_amount):
    """
    Calculate new tax after sacrificing gold.
    
    Args:
        tax_before: Current reincarnation tax (percentage, e.g., 5.0 for 5%)
        gold_amount: Amount of gold sacrificed
    
    Returns:
        New tax percentage after sacrifice
    """
    if gold_amount <= 0:
        return tax_before
    import math
    tax_after = tax_before * (2 ** (-gold_amount / 1000000))
    return tax_after

# =============================================================================
# GOLD SACRIFICE REFERENCE TABLE
# =============================================================================

GOLD_SACRIFICE_EFFECTS = {
    50000: {
        "desc": "Natural daily reduction",
        "effect": "Equivalent to one day of natural decay",
    },
    1000000: {
        "desc": "Major reduction",
        "effect_high_tax": "Reduces your tax by half (if tax > 0.5%)",
        "effect_low_tax": "Reduces your tax by about 0.1% (if tax < 0.5%)",
    },
}

# =============================================================================
# ITEM WORTH TO GOLD CONVERSION
# =============================================================================
# Item task points (tps) worth to gold sacrifice equivalent

ITEM_WORTH_GOLD_TABLE = {
    0: 100000,      # 0 tps = 100,000 gold equivalent
    1: 250000,      # 1 tp = 250,000 gold equivalent
    2: 500000,      # 2 tps = 500,000 gold equivalent
    3: 800000,      # 3 tps = 800,000 gold equivalent
    5: 1600000,     # 5 tps = 1,600,000 gold equivalent
    7: 3000000,     # 7 tps = 3,000,000 gold equivalent
    10: 4000000,    # 10 tps = 4,000,000 gold equivalent
}

def get_item_worth_gold(task_points):
    """
    Get gold equivalent for an item's task point worth.
    """
    # Find closest match
    if task_points in ITEM_WORTH_GOLD_TABLE:
        return ITEM_WORTH_GOLD_TABLE[task_points]
    
    # Interpolate for values not in table
    sorted_tps = sorted(ITEM_WORTH_GOLD_TABLE.keys())
    for i, tp in enumerate(sorted_tps):
        if task_points < tp:
            if i == 0:
                return ITEM_WORTH_GOLD_TABLE[tp]
            lower_tp = sorted_tps[i - 1]
            # Linear interpolation
            lower_gold = ITEM_WORTH_GOLD_TABLE[lower_tp]
            upper_gold = ITEM_WORTH_GOLD_TABLE[tp]
            ratio = (task_points - lower_tp) / (tp - lower_tp)
            return int(lower_gold + (upper_gold - lower_gold) * ratio)
    
    # Above highest known value - extrapolate
    highest_tp = sorted_tps[-1]
    highest_gold = ITEM_WORTH_GOLD_TABLE[highest_tp]
    return int(highest_gold * (task_points / highest_tp))

# =============================================================================
# REINCARNATION NOTES
# =============================================================================

REINCARNATION_NOTES = {
    "daily_natural": "Tax naturally goes down on an in-game daily basis (not based on logged-in time).",
    "eje_sacrifice": "Eje in Illium's Church accepts equipment and gold sacrifices to reduce reincarnation tax.",
    "item_requirements": "Items must have +8 stat, +3 resistance, +5% alpha, or +3% bravo to be accepted.",
    "formula": "A = B * 2^(-G/1000000) where A=new tax, B=old tax, G=gold sacrificed.",
}
