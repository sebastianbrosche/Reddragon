"""
Red Dragon MUD — Combat Engine with Weapon Mastery
====================================================
A comprehensive combat system that integrates:
  - Weapon Mastery (per-weapon-type skill progression)
  - Race bonuses/penalties to combat
  - Guild bonuses/penalties to combat
  - Damage calculation with multiple modifiers
  - Critical hits, dodging, blocking, parrying
  - Status effects (bleed, poison, burn, etc.)

Weapon Mastery System:
----------------------
Every character tracks mastery for each weapon type:
  0-20   : Novice      (+0% damage, -5% hit chance)
  21-40  : Apprentice  (+5% damage, normal hit)
  41-60  : Journeyman  (+10% damage, +5% crit)
  61-80  : Expert      (+15% damage, +10% crit, +5% parry)
  81-95  : Master      (+20% damage, +15% crit, +10% parry, special move)
  96-100 : Grandmaster (+25% damage, +20% crit, +15% parry, legendary move)

Mastery XP is gained by:
  - Hitting enemies (+1 XP per hit)
  - Killing enemies (+10 XP per kill)
  - Training with guild masters (+20 XP per session)
  - Using racial weapon bonuses (+50% mastery XP)

Damage Formula:
---------------
Base Damage = (Weapon Base + STR modifier) * Mastery multiplier
            * Race multiplier * Guild multiplier
            * Critical multiplier * Position multiplier
            * Random variance (0.9 - 1.1)

Where:
  STR modifier = STR * 0.5 (melee) or DEX * 0.5 (ranged)
  Mastery multiplier = 1.0 + (mastery_level * 0.0025)
  Race multiplier = racial weapon bonus (e.g., Dwarf +10% axe/hammer)
  Guild multiplier = guild weapon proficiency (e.g., Warrior +10% all weapons)
  Critical = 1.5x (normal), 2.0x (master crit), 2.5x (legendary)
  Position = 1.0 (front), 1.5 (flank), 2.0 (behind), 1.2 (stealth opener)

Race Combat Interactions:
-------------------------
  Dwarf     : +10% axe/hammer damage, +15% physical DR
  Elf       : +15% bow damage, +10% dodge
  Giant     : Can wield 2H in 1H, +20% oversized weapon damage
  Minotaur  : Charge deals +50% first attack, horn gore 1d6 bonus
  Troll     : Regen 5% HP/round in combat, immune to normal weapon fear
  Vampire   : Drain 50% of damage as HP on unarmed/magical attacks
  Thrikhren : Extra off-hand attack, +10% polearm damage
  Hobbit    : +10% thrown weapon damage, lucky reroll 1/day
  Goblin    : Pack tactics +5% per ally
  etc.

Guild Combat Interactions:
--------------------------
  Warrior      : +1% weapon damage per guild level
  Martial Artist: +2% unarmed per guild level, chi abilities
  Acrobat      : +1.5% dodge per guild level, tumble past enemies
  Lurker       : +3% stealth damage per guild level, poison mastery
  Woodsman     : +2% bow damage per guild level, tracking
  Evoker       : +2% spell damage per guild level, overcharge
  Necromancer  : +2% life drain per guild level, undead minions
  etc.
"""

import random
from evennia import DefaultCharacter

# ---------------------------------------------------------------------------
# Weapon Types and Base Stats
# ---------------------------------------------------------------------------
WEAPON_TYPES = [
    "sword", "axe", "mace", "dagger", "spear", "polearm", "staff",
    "bow", "crossbow", "throwing", "unarmed", "claws", "whip", "chain",
    "flail", "scythe", "sickle", "club", "garrote", "holy_symbol",
    "wand", "two_handed", "natural", "bone", "poison"
]

WEAPON_BASE_DAMAGE = {
    "dagger": (1, 4), "unarmed": (1, 3), "claws": (1, 6),
    "whip": (1, 4), "chain": (1, 6), "garrote": (1, 4),
    "sword": (1, 8), "mace": (1, 8), "club": (1, 6),
    "axe": (1, 8), "spear": (1, 8), "staff": (1, 6),
    "polearm": (1, 10), "flail": (1, 8), "scythe": (1, 10),
    "sickle": (1, 6), "bone": (1, 6), "holy_symbol": (1, 4),
    "bow": (1, 8), "crossbow": (1, 10), "throwing": (1, 6),
    "wand": (1, 4), "two_handed": (2, 6), "natural": (1, 6),
    "poison": (1, 4),
}

# Mastery tiers
MASTERY_TIERS = [
    (0, 20, "Novice", 0.0, -0.05, 0.0, 0.0, None),
    (21, 40, "Apprentice", 0.05, 0.0, 0.0, 0.0, None),
    (41, 60, "Journeyman", 0.10, 0.0, 0.05, 0.0, None),
    (61, 80, "Expert", 0.15, 0.0, 0.10, 0.05, None),
    (81, 95, "Master", 0.20, 0.0, 0.15, 0.10, "special_move"),
    (96, 100, "Grandmaster", 0.25, 0.0, 0.20, 0.15, "legendary_move"),
]

# Race weapon bonuses
RACE_WEAPON_BONUSES = {
    "dwarf": {"axe": 0.10, "hammer": 0.10, "mace": 0.05},
    "elf": {"bow": 0.15, "sword": 0.05},
    "giant": {"two_handed": 0.20, "polearm": 0.10, "mace": 0.10},
    "minotaur": {"axe": 0.10, "spear": 0.10},
    "gnome": {"dagger": 0.10, "crossbow": 0.10},
    "thrikhren": {"polearm": 0.10, "spear": 0.05},
    "hobbit": {"throwing": 0.10, "dagger": 0.05},
    "vinnipier": {"spear": 0.10, "trident": 0.10, "polearm": 0.05},
    "grorrark": {"claws": 0.15, "unarmed": 0.10},
    "snakeman": {"unarmed": 0.10, "dagger": 0.05},
    "mindflayer": {"staff": 0.10, "wand": 0.05},
    "faerie": {"dagger": 0.10, "wand": 0.05},
    "leprechaun": {"dagger": 0.10, "throwing": 0.05},
    "goblin": {"dagger": 0.10, "short_sword": 0.05},
    "kobold": {"dagger": 0.10, "crossbow": 0.05},
    "martialartist": {"unarmed": 0.15, "staff": 0.10},
    "woodsman": {"bow": 0.15, "spear": 0.05},
}

# Damage type resistances/vulnerabilities by race
RACE_DAMAGE_MODIFIERS = {
    "cromagnon": {"physical": 0.75, "magical": 1.20},
    "drow": {"holy": 1.30, "unholy": 0.80, "magical": 0.85},
    "dwarf": {"poison": 0.75, "physical": 0.85},
    "elf": {"charm": 0.80, "sleep": 0.80},
    "ent": {"nature": 0.70, "fire": 1.25},
    "faerie": {"iron": 1.50, "magical": 0.90},
    "gargoyle": {"physical": 0.70, "sonic": 1.20, "petrification": 0.0},
    "giant": {"mental": 1.20, "physical": 0.90},
    "gnome": {"mental": 0.85, "illusion": 0.50},
    "goblin": {"disease": 0.85, "poison": 0.85},
    "grorrark": {"fire": 0.80, "cold": 1.15},
    "halfelf": {"charm": 0.90},
    "hobbit": {"fear": 0.0, "poison": 0.90},
    "human": {},
    "kobold": {"disease": 0.85},
    "leprechaun": {},
    "lizardman": {"poison": 0.80, "cold": 1.10},
    "mindflayer": {"mental": 0.0, "head_crit": 1.50},
    "minotaur": {"confusion": 0.80},
    "ogier": {"fear": 0.80},
    "phoenix": {"fire": 0.0, "water": 1.20, "ice": 1.20},
    "snakeman": {"poison": 0.75},
    "thrikhren": {"mind_control": 0.80, "gas": 1.20},
    "troll": {"acid": 1.25, "fire": 0.90},
    "vampire": {"holy": 1.25, "sunlight": 1.50, "poison": 0.0, "disease": 0.0},
    "vinnipier": {"cold": 0.80, "water": 0.90},
    "xorn": {"physical_normal": 0.0, "magical_weapon": 1.50, "crushing": 0.80},
}


def get_mastery_tier(mastery_level):
    """Return mastery tier info for a given mastery level (0-100)."""
    for low, high, name, dmg, hit, crit, parry, special in MASTERY_TIERS:
        if low <= mastery_level <= high:
            return {
                "name": name, "dmg_bonus": dmg, "hit_bonus": hit,
                "crit_bonus": crit, "parry_bonus": parry, "special": special
            }
    return MASTERY_TIERS[-1]  # Grandmaster


def get_weapon_mastery(character, weapon_type):
    """Get a character's mastery level for a weapon type."""
    if not character.db.weapon_mastery:
        character.db.weapon_mastery = {}
    return character.db.weapon_mastery.get(weapon_type, 0)


def gain_weapon_mastery_xp(character, weapon_type, amount=1):
    """Award weapon mastery XP to a character."""
    if not character.db.weapon_mastery:
        character.db.weapon_mastery = {}
    current = character.db.weapon_mastery.get(weapon_type, 0)

    # Racial bonus to mastery XP
    race = character.db.race
    if race in RACE_WEAPON_BONUSES and weapon_type in RACE_WEAPON_BONUSES.get(race, {}):
        amount = int(amount * 1.5)

    new = min(100, current + amount)
    character.db.weapon_mastery[weapon_type] = new

    # Check for tier advancement
    old_tier = get_mastery_tier(current)["name"]
    new_tier = get_mastery_tier(new)["name"]
    if old_tier != new_tier:
        return new_tier
    return None


def calculate_damage(attacker, defender, weapon_type, damage_type="physical",
                      attack_position="front", is_stealth=False, spell_name=None):
    """
    Calculate damage for an attack.

    Args:
        attacker: The attacking character
        defender: The defending character (can be NPC)
        weapon_type: Type of weapon being used
        damage_type: Type of damage (physical, fire, cold, etc.)
        attack_position: front, flank, behind
        is_stealth: Whether attack is from stealth
        spell_name: If this is a spell attack

    Returns:
        dict with damage, crit, messages, effects
    """
    result = {
        "damage": 0, "is_crit": False, "is_hit": True,
        "messages": [], "effects": [], "mastery_xp": 0
    }

    # Get weapon base damage
    base_dmg = WEAPON_BASE_DAMAGE.get(weapon_type, (1, 6))
    base = random.randint(base_dmg[0], base_dmg[1])

    # Stat modifier
    str_val = attacker.attributes.get("strength", 10)
    dex_val = attacker.attributes.get("dexterity", 10)
    if weapon_type in ["bow", "crossbow", "throwing"]:
        stat_mod = dex_val * 0.3
    else:
        stat_mod = str_val * 0.5

    # Mastery multiplier
    mastery = get_weapon_mastery(attacker, weapon_type)
    tier = get_mastery_tier(mastery)
    mastery_mult = 1.0 + tier["dmg_bonus"]

    # Race multiplier
    race = attacker.db.race
    race_mult = 1.0
    if race in RACE_WEAPON_BONUSES:
        race_mult += RACE_WEAPON_BONUSES[race].get(weapon_type, 0.0)

    # Guild multiplier
    guild = attacker.db.guild
    guild_mult = 1.0
    if guild == "warrior":
        guild_mult += attacker.db.guild_level * 0.01 if attacker.db.guild_level else 0
    elif guild == "martialartist" and weapon_type == "unarmed":
        guild_mult += attacker.db.guild_level * 0.02 if attacker.db.guild_level else 0
    elif guild == "lurker" and is_stealth:
        guild_mult += (attacker.db.guild_level * 0.03 if attacker.db.guild_level else 0)
    elif guild == "woodsman" and weapon_type == "bow":
        guild_mult += attacker.db.guild_level * 0.02 if attacker.db.guild_level else 0

    # Critical hit check
    crit_chance = 0.05 + tier["crit_bonus"]
    # Race crit bonuses
    if race == "minotaur":
        crit_chance += 0.05  # Horns find weak spots
    if race == "hobbit":
        # Lucky — once per day reroll
        pass

    is_crit = random.random() < crit_chance
    crit_mult = 2.0 if is_crit else 1.0

    # Position multiplier
    pos_mult = {"front": 1.0, "flank": 1.5, "behind": 2.0}.get(attack_position, 1.0)
    if is_stealth:
        pos_mult *= 1.5

    # Stealth opener bonus
    if is_stealth and guild == "lurker":
        pos_mult *= 1.25

    # Random variance
    variance = random.uniform(0.9, 1.1)

    # Calculate final damage
    damage = (base + stat_mod) * mastery_mult * race_mult * guild_mult * crit_mult * pos_mult * variance
    damage = max(1, int(damage))

    # Defender damage reduction
    defender_race = getattr(defender.db, 'race', None)
    if defender_race and defender_race in RACE_DAMAGE_MODIFIERS:
        mod = RACE_DAMAGE_MODIFIERS[defender_race].get(damage_type, 1.0)
        damage = int(damage * mod)

    # Defender armor/con reduction
    con_val = defender.attributes.get("constitution", 10)
    armor_dr = getattr(defender.db, 'armor_rating', 0) * 0.02
    damage = max(1, int(damage * (1.0 - armor_dr)))

    # Special race effects on damage dealt
    if race == "vampire" and weapon_type in ["unarmed", "claws", "natural"]:
        heal = int(damage * 0.5)
        result["effects"].append({"type": "life_drain", "amount": heal, "target": "self"})
        result["messages"].append(f"You drain {heal} HP from {defender.name}!")

    if race == "grorrark" and weapon_type in ["unarmed", "claws", "natural"]:
        result["effects"].append({"type": "poison", "amount": random.randint(1, 4), "duration": 3})
        result["messages"].append(f"Your venomous bite poisons {defender.name}!")

    if race == "snakeman" and weapon_type in ["unarmed", "claws", "natural"]:
        result["effects"].append({"type": "poison", "amount": random.randint(1, 6), "duration": 3})
        result["messages"].append(f"Your fangs inject venom into {defender.name}!")

    if race == "phoenix" and damage_type == "fire":
        damage = int(damage * 1.2)  # Phoenix fire is stronger
        result["effects"].append({"type": "burn", "amount": random.randint(1, 4), "duration": 2})

    # Guild special effects
    if guild == "evoker" and spell_name:
        overcharge = getattr(attacker.db, 'overcharge', False)
        if overcharge:
            damage = int(damage * 1.3)
            result["messages"].append("Your spell overcharges with raw power!")

    if guild == "necromancer":
        sp_gain = int(damage * 0.05)
        result["effects"].append({"type": "sp_restore", "amount": sp_gain, "target": "self"})

    # Minotaur charge bonus
    if race == "minotaur" and getattr(attacker.db, 'first_attack_round', False):
        damage = int(damage * 1.5)
        result["messages"].append("Your charge slams into the enemy with devastating force!")
        attacker.db.first_attack_round = False

    # Build result
    result["damage"] = damage
    result["is_crit"] = is_crit
    result["mastery_xp"] = 1 if not is_crit else 3  # Bonus XP for crits

    if is_crit:
        result["messages"].append(f"CRITICAL HIT! You deal {damage} damage!")
    else:
        result["messages"].append(f"You deal {damage} damage.")

    return result


def check_hit(attacker, defender, weapon_type, attack_position="front"):
    """
    Check if an attack hits.

    Returns:
        dict with is_hit, dodge, block, messages
    """
    result = {"is_hit": True, "dodged": False, "blocked": False, "parried": False, "messages": []}

    # Base hit chance
    attacker_dex = attacker.attributes.get("dexterity", 10)
    defender_dex = defender.attributes.get("dexterity", 10)

    base_hit = 75  # 75% base hit chance
    hit_bonus = (attacker_dex - 10) * 2
    dodge_bonus = (defender_dex - 10) * 2

    # Mastery hit bonus
    mastery = get_weapon_mastery(attacker, weapon_type)
    tier = get_mastery_tier(mastery)
    hit_bonus += int(tier["hit_bonus"] * 100)

    # Guild bonuses
    guild = attacker.db.guild
    if guild == "acrobat":
        hit_bonus += attacker.db.guild_level if attacker.db.guild_level else 0
    if guild == "martialartist":
        hit_bonus += (attacker.db.guild_level // 2) if attacker.db.guild_level else 0

    # Defender dodge
    defender_race = getattr(defender.db, 'race', None)
    dodge_chance = 5 + dodge_bonus
    if defender_race == "elf":
        dodge_chance += 10
    if defender_race == "faerie":
        dodge_chance += 20
    if defender_race == "drow":
        dodge_chance += 5
    if defender_race == "martialartist":
        dodge_chance += (defender.db.guild_level * 0.5) if defender.db.guild_level else 0

    # Position affects dodge
    if attack_position == "behind":
        dodge_chance = max(0, dodge_chance - 20)

    # Roll for dodge
    if random.randint(1, 100) <= dodge_chance:
        result["dodged"] = True
        result["is_hit"] = False
        result["messages"].append(f"{defender.name} dodges your attack!")
        return result

    # Roll for hit
    final_hit = base_hit + hit_bonus
    if random.randint(1, 100) > final_hit:
        result["is_hit"] = False
        result["messages"].append(f"You miss {defender.name}!")
        return result

    return result


def get_combat_summary(character):
    """Return a formatted combat summary for a character."""
    lines = []
    lines.append("{cCombat Profile{n")
    lines.append("-" * 40)

    # Stats
    str_v = character.attributes.get("strength", 10)
    dex_v = character.attributes.get("dexterity", 10)
    con_v = character.attributes.get("constitution", 10)
    lines.append(f"  STR: {str_v}  DEX: {dex_v}  CON: {con_v}")

    # Race combat bonuses
    race = character.db.race
    if race and race in RACE_WEAPON_BONUSES:
        lines.append(f"  {{yRace bonuses:{{n")
        for wpn, bonus in RACE_WEAPON_BONUSES[race].items():
            lines.append(f"    {wpn}: +{int(bonus*100)}%")

    # Damage resistances
    if race and race in RACE_DAMAGE_MODIFIERS:
        lines.append(f"  {{yDamage resistances:{{n")
        for dtype, mod in RACE_DAMAGE_MODIFIERS[race].items():
            pct = int((1.0 - mod) * 100)
            if pct > 0:
                lines.append(f"    {dtype}: {pct}% resistant")
            elif pct < 0:
                lines.append(f"    {dtype}: {abs(pct)}% vulnerable")

    # Weapon masteries
    if character.db.weapon_mastery:
        lines.append(f"  {{yWeapon Mastery:{{n")
        for wpn, val in sorted(character.db.weapon_mastery.items(), key=lambda x: -x[1]):
            tier = get_mastery_tier(val)
            lines.append(f"    {wpn:15} {val:3}/100  [{tier['name']}]")

    # Guild combat info
    guild = character.db.guild
    if guild:
        lines.append(f"  {{yGuild:{n} {character.db.guild_name} (Lv{character.db.guild_level or 1})")

    lines.append("-" * 40)
    return "\n".join(lines)


def format_mastery_progress(weapon_type, mastery_level):
    """Format a mastery progress bar."""
    tier = get_mastery_tier(mastery_level)
    bar_len = 20
    filled = int((mastery_level / 100) * bar_len)
    bar = "█" * filled + "░" * (bar_len - filled)
    return f"{weapon_type:15} [{bar}] {mastery_level}/100 {tier['name']}"
