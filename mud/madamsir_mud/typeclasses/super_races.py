"""
Red Dragon MUD — Super Races
==============================
Three "Super" races from Islands of Myth:
- Celestial Mage
- Ghyrdon
- Gnoll

These are advanced races with powerful abilities.
"""

SUPER_RACES = {
    "celestial_mage": {
        "name": "Celestial Mage",
        "desc": "Ascended beings of pure starlight and cosmic energy. Once mortal mages who transcended flesh through mastery of the Celestial Weave.",
        "stats": {
            "strength": -1,
            "dexterity": 0,
            "constitution": -2,
            "stamina": 3,
            "intelligence": 4,
            "wisdom": 3,
            "charisma": 2,
        },
        "height_range": (70, 85),  # inches
        "mass_range": (140, 180),  # lbs
        "special": "Celestial Form",
        "special_desc": "Can shift into pure starlight for 3 rounds, becoming immune to physical damage.",
        "passives": [
            "Starlight Aura — innate light source, +10% spell damage",
            "Cosmic Attunement — +25% spell point regeneration",
            "Astral Resistance — +50% resistance to magic damage",
        ],
        "skills": {
            "max": 45,
            "bonus": 25,
            "spells": {
                "max": 65,
                "bonus": 30,
            },
        },
        "xp_rate": 120,  # 20% slower than standard
        "combat_bonuses": {
            "spell_damage": 0.25,  # +25%
            "magic_resistance": 0.50,
            "physical_damage": -0.15,  # -15% (frail)
        },
        "abilities": {
            11: "Starfire Bolt — ranged cosmic damage",
            21: "Nebula Shield — magic barrier absorbs 100 damage",
            31: "Astral Projection — scout distant areas mentally",
            41: "Supernova — massive AoE celestial damage, 5 min cooldown",
            51: "Celestial Ascension — +50% all stats for 30 seconds, 10 min cooldown",
        },
    },
    "ghyrdon": {
        "name": "Ghyrdon",
        "desc": "Living weapons born of war itself. Ghyrdon are constructs of living metal and battle-fury, forged in ancient wars and given consciousness.",
        "stats": {
            "strength": 4,
            "dexterity": 2,
            "constitution": 3,
            "stamina": 2,
            "intelligence": -2,
            "wisdom": -1,
            "charisma": -3,
        },
        "height_range": (80, 95),
        "mass_range": (280, 400),
        "special": "Living Weapon",
        "special_desc": "Transform any held weapon into a Ghyrdon-forged blade for 5 rounds, doubling base damage.",
        "passives": [
            "Living Metal — regenerate 2% HP per round when holding metal",
            "Battle Fury — +1% damage per consecutive round in combat (max +20%)",
            "Weapon Bond — cannot be disarmed, +15% weapon mastery XP",
        ],
        "skills": {
            "max": 65,
            "bonus": 35,
            "spells": {
                "max": 15,
                "bonus": 5,
            },
        },
        "xp_rate": 140,  # 40% slower
        "combat_bonuses": {
            "weapon_damage": 0.20,
            "unarmed_damage": 0.15,
            "magic_resistance": -0.20,  # vulnerable to magic
            "physical_resistance": 0.15,
        },
        "abilities": {
            11: "Iron Skin — +25 AC for 30 seconds",
            21: "Bladestorm — attack all enemies in room",
            31: "Weapon Mastery Surge — +50 weapon mastery for 60 seconds",
            41: "Living Arsenal — summon phantom weapons, +3 attacks/round",
            51: "Avatar of War — transform into pure battle-form, +100% damage, 10 min cooldown",
        },
    },
    "gnoll": {
        "name": "Gnoll",
        "desc": "Hyena-like pack hunters of the Dark Caverns. Gnolls possess primal pack instincts and can unlock secret creation magic.",
        "stats": {
            "strength": 2,
            "dexterity": 3,
            "constitution": 1,
            "stamina": 2,
            "intelligence": -1,
            "wisdom": 0,
            "charisma": -2,
        },
        "height_range": (68, 78),
        "mass_range": (160, 220),
        "special": "Pack Hunt",
        "special_desc": "When fighting alongside another Gnoll, both gain +25% damage and +15% crit chance.",
        "passives": [
            "Pack Tactics — +10% damage per allied Gnoll in room (max +50%)",
            "Laughing Resilience — 50% chance to ignore fear effects",
            "Scavenger's Nose — detect hidden items and exits in room",
        ],
        "skills": {
            "max": 55,
            "bonus": 25,
            "spells": {
                "max": 30,
                "bonus": 10,
            },
        },
        "xp_rate": 110,  # 10% slower
        "combat_bonuses": {
            "bite_damage": 0.30,
            "stealth": 0.15,
            "group_damage": 0.25,
        },
        "abilities": {
            11: "Hyena's Bite — savage bite attack, causes bleed",
            21: "Pack Call — summon 2 spectral hyenas to fight for 30 seconds",
            31: "Feral Sprint — +50% movement speed for 30 seconds",
            41: "Alpha's Howl — buff all allies +20% damage, +10% crit",
            51: "Gnoll Creation Magic — unlock the secret magic (one-time quest reward)",
        },
    },
}


def apply_super_race(character, race_key):
    """Apply a super race to a character."""
    race = SUPER_RACES.get(race_key)
    if not race:
        return False
    
    character.db.race = race["name"]
    character.db.race_type = "super"
    character.db.race_key = race_key
    
    # Apply stat modifiers
    for stat, mod in race["stats"].items():
        current = getattr(character.db, stat, 10)
        setattr(character.db, stat, current + mod)
    
    # Apply limits
    character.db.max_skill = race["skills"]["max"]
    character.db.max_spell = race["skills"]["spells"]["max"]
    character.db.xp_rate = race["xp_rate"]
    
    # Combat bonuses
    character.db.race_bonuses = race.get("combat_bonuses", {})
    
    # Special
    character.db.racial_special = race["special"]
    character.db.racial_special_desc = race["special_desc"]
    character.db.racial_passives = race["passives"]
    character.db.racial_abilities = race["abilities"]
    
    return True
