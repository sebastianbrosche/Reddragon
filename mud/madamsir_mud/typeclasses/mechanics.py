"""
Red Dragon MUD — Game Mechanics
=================================
Damage types, equipment conditions, alignment, hunger, AC scales.
All based on Islands of Myth content.
"""

# ── Damage Types ──────────────────────────────────────────
DAMAGE_TYPES = {
    "acid": {
        "desc": "Corrosive damage that melts armor and flesh.",
        "resistance_stat": None,
        "effects": ["armor degradation", "continued burning"],
    },
    "asphyxiation": {
        "desc": "Damage from lack of air or constriction.",
        "resistance_stat": "constitution",
        "effects": ["suffocation", "stun"],
    },
    "cold": {
        "desc": "Freezing damage that chills to the bone.",
        "resistance_stat": None,
        "effects": ["slow movement", "frostbite"],
    },
    "electric": {
        "desc": "Shocking damage that arcs through targets.",
        "resistance_stat": None,
        "effects": ["stun", "chain damage"],
    },
    "fire": {
        "desc": "Burning damage that ignites targets.",
        "resistance_stat": None,
        "effects": ["ignite", "continued burning"],
    },
    "holy": {
        "desc": "Divine damage that purges evil.",
        "resistance_stat": None,
        "effects": ["extra vs undead", "extra vs evil"],
    },
    "magic": {
        "desc": "Arcane energy damage.",
        "resistance_stat": "wisdom",
        "effects": ["spell disruption"],
    },
    "physical": {
        "desc": "Standard weapon and impact damage.",
        "resistance_stat": "strength",
        "effects": ["bleed", "knockback"],
    },
    "poison": {
        "desc": "Toxic damage that weakens over time.",
        "resistance_stat": "constitution",
        "effects": ["continued damage", "stat drain"],
    },
    "psi": {
        "desc": "Mental damage that attacks the mind.",
        "resistance_stat": "intelligence",
        "effects": ["confusion", "stun", "fear"],
    },
    "unholy": {
        "desc": "Dark damage that corrupts the soul.",
        "resistance_stat": None,
        "effects": ["curse", "life drain"],
    },
}

# ── Damage Scale ────────────────────────────────────────────
DAMAGE_SCALE = {
    0: ("None", "No damage"),
    1: ("Negligible", "Barely a scratch"),
    2: ("Very Light", "A small wound"),
    3: ("Light", "A noticeable wound"),
    4: ("Moderate", "A solid hit"),
    5: ("Heavy", "A deep wound"),
    6: ("Very Heavy", "A severe wound"),
    7: ("Extreme", "A devastating blow"),
    8: ("Incredible", "A near-fatal strike"),
}

# ── Equipment Condition ───────────────────────────────────
CONDITION_LEVELS = {
    0: ("Broken", "red", "Equipment is destroyed and unusable."),
    1: ("Ruined", "red", "Barely holding together. -50% stats."),
    2: ("Shattered", "red", "Severely damaged. -40% stats."),
    3: ("Dented", "yellow", "Noticeable damage. -30% stats."),
    4: ("Scratched", "yellow", "Light damage. -20% stats."),
    5: ("Worn", "yellow", "Well used. -10% stats."),
    6: ("Good", "green", "Standard condition."),
    7: ("Pristine", "green", "Like new. +10% stats."),
    8: ("Flawless", "green", "Perfect condition. +20% stats."),
    9: ("Legendary", "cyan", "Blessed by the gods. +30% stats."),
    10: ("Mythic", "cyan", "Reality itself preserves this item. +40% stats."),
    11: ("Divine", "magenta", "Touched by divinity. +50% stats."),
    12: ("Eternal", "magenta", "Transcends time. +60% stats, cannot break."),
}

# ── Alignment Scale ───────────────────────────────────────
ALIGNMENT_SCALE = {
    -5: ("Pure Evil", -1000),
    -4: ("Evil", -500),
    -3: ("Wicked", -250),
    -2: ("Mean", -100),
    -1: ("Selfish", -25),
    0: ("Neutral", 0),
    1: ("Kind", 25),
    2: ("Good", 100),
    3: ("Honorable", 250),
    4: ("Heroic", 500),
    5: ("Saintly", 1000),
}

# ── Hunger Scale ────────────────────────────────────────────
HUNGER_LEVELS = {
    0: ("Starving", "You are starving! Find food immediately!"),
    1: ("Famished", "Your stomach groans with emptiness."),
    2: ("Hungry", "You feel hungry."),
    3: ("Peckish", "You could use a snack."),
    4: ("Satisfied", "You feel content."),
    5: ("Full", "You are well fed."),
    6: ("Stuffed", "You are completely stuffed."),
}

# ── Armor Class Scale ─────────────────────────────────────
AC_SCALE = {
    0: ("Naked", "No armor at all."),
    1: ("Cloth", "Basic cloth protection."),
    2: ("Leather", "Light leather armor."),
    3: ("Studded", "Studded leather armor."),
    4: ("Scale", "Scale mail armor."),
    5: ("Chain", "Chain mail armor."),
    6: ("Splint", "Splint mail armor."),
    7: ("Plate", "Full plate armor."),
    8: ("Mythic Plate", "Armor blessed by the gods."),
}

# ── Lodestone System ──────────────────────────────────────
LODESTONE_DESTINATIONS = {
    "illium": "The great city of Illium — heart of civilization.",
    "newbie": "Newbie Garden and Valley — starting area for new adventurers.",
    "blackavar": "Blackavar Docks — dark forested island of secrets.",
    "darkcaverns": "Darkcaverns — the underworld beneath the islands.",
    "everrest": "Everrest — frozen peak home to Chilperic.",
    "hyboria": "Hyboria — savage jungles and prehistoric caves.",
    "mists": "Mists — fog-shrouded island of demons and Uforia.",
    "twin_islands": "Twin Islands — north lighthouse and demon army.",
    "emerald": "Emerald — lush forests haunted by the hag.",
    "gossamer": "Gossamer — floating gardens and crystalline spires.",
    "southcape": "Southcape — bustling port with a dangerous underbelly.",
    "sombre": "Sombre — grey rainswept island of gloom.",
    "oddworld": "Oddworld — strange alien island of ancient wars.",
}


def get_condition_info(level):
    """Return formatted condition info."""
    info = CONDITION_LEVELS.get(level, ("Unknown", "white", "Unknown condition."))
    return f"{info[0]} ({info[2]})"


def get_alignment_info(score):
    """Return alignment name for score."""
    for tier, (name, threshold) in sorted(ALIGNMENT_SCALE.items()):
        if score <= threshold:
            return name
    return "Saintly"


def get_hunger_info(level):
    """Return hunger status."""
    info = HUNGER_LEVELS.get(level, ("Unknown", "???"))
    return f"{info[0]}: {info[1]}"


def get_damage_type_info(dtype):
    """Return damage type description."""
    info = DAMAGE_TYPES.get(dtype)
    if not info:
        return "Unknown damage type."
    lines = [f"{dtype.title()}: {info['desc']}"]
    if info['resistance_stat']:
        lines.append(f"  Resisted by: {info['resistance_stat'].title()}")
    lines.append(f"  Effects: {', '.join(info['effects'])}")
    return "\n".join(lines)


def get_lodestone_info():
    """Return all lodestone destinations."""
    lines = ["{cLodestone Destinations{n", "-" * 40]
    for dest, desc in LODESTONE_DESTINATIONS.items():
        lines.append(f"  {{g{dest:<15}{n} {desc}")
    lines.append("-" * 40)
    lines.append("Use {glodestone <destination>{n to teleport.")
    return "\n".join(lines)
