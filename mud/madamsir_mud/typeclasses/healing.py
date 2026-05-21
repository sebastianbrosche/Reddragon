#!/usr/bin/env python3
"""
Red Dragon MUD — Healing & Party Mechanics
==========================================
Based on bempire.demon.nl/healmyth.txt — party healing guide.
"""

# Healer Guild Progression (from healmyth guide)
HEALER_PROGRESSION = {
    "weaver": {
        "level": 1,
        "required_spells": ["cure serious wounds", "minor refresh"],
        "optional": ["holy essence", "know alignment", "essence eye", "minor cleric staff", "remove scar", "create food"],
        "passives": [],
    },
    "healer": {
        "level": 2,
        "required_spells": ["heal", "major refresh", "mastery of healing", "enhance healing"],
        "optional": ["estimate worth", "reincarnate"],
        "passives": [],
    },
    "martyr": {
        "level": 3,
        "branch": "martyr",
        "required_spells": ["martyric presence", "heal companions", "refresh companions", "holy cause"],
        "optional": ["restore companions", "invigorate companions", "sacrifice life force"],
        "passives": ["party refresh", "party heal"],
        "why": "Martyric presence and party refresh for big parties",
    },
    "confessor": {
        "level": 3,
        "branch": "confessor",
        "required_spells": ["prayer for healing", "prayer for refreshment", "prayer for mankind", "pious words"],
        "optional": [],
        "passives": ["goodwill", "name recognition"],
        "why": "Goodwill and name recognition for getting picked in parties",
    },
    "avatar": {
        "level": 4,
        "required_spells": ["encourage regeneration", "soul of the avatar", "quick chant"],
        "optional": ["cleanse soul", "feed companions", "revive dead", "avatar regeneration"],
        "passives": [],
        "why": "Encourage regeneration is the game-changer for big party healing",
    },
    "lotus": {
        "level": 5,
        "optional": [],
        "passives": [],
        "why": "Additional healing options",
    },
}

# Healing Spell Database
HEALING_SPELLS = {
    # Weaver spells
    "cure serious wounds": {
        "guild": "weaver",
        "type": "heal",
        "target": "single",
        "base_heal": 50,
        "sp_cost": 15,
        "mastery": "holy essence",
        "description": "Heal moderate wounds on a single target.",
    },
    "cure critical wounds": {
        "guild": "weaver",
        "type": "heal",
        "target": "single",
        "base_heal": 100,
        "sp_cost": 25,
        "mastery": "holy essence",
        "description": "Heal severe wounds on a single target.",
    },
    "minor refresh": {
        "guild": "weaver",
        "type": "refresh",
        "target": "single",
        "base_refresh": 20,
        "sp_cost": 10,
        "description": "Restore a small amount of EP to target.",
    },
    "holy essence": {
        "guild": "weaver",
        "type": "passive",
        "effect": "boost_healing",
        "per_rank": 0.02,  # +2% per rank
        "description": "Passively boosts all healing spells.",
    },
    
    # Healer spells
    "heal": {
        "guild": "healer",
        "type": "heal",
        "target": "single",
        "base_heal": 200,
        "sp_cost": 40,
        "mastery": "mastery of healing",
        "description": "Powerful single-target heal. Must be at 100% for party healing.",
    },
    "major refresh": {
        "guild": "healer",
        "type": "refresh",
        "target": "single",
        "base_refresh": 60,
        "sp_cost": 25,
        "description": "Restore a large amount of EP to target.",
    },
    "mastery of healing": {
        "guild": "healer",
        "type": "passive",
        "effect": "boost_healing",
        "per_rank": 0.03,  # +3% per rank
        "description": "Significantly boosts all healing spells.",
    },
    "enhance healing": {
        "guild": "healer",
        "type": "passive",
        "effect": "boost_healing",
        "per_rank": 0.02,
        "description": "Further enhances healing output.",
    },
    
    # Martyr spells
    "martyric presence": {
        "guild": "martyr",
        "type": "aura",
        "target": "party",
        "effect": "hp_regen",
        "base_regen": 5,
        "sp_cost": 30,
        "duration": 300,
        "description": "Party-wide HP regeneration aura. MUST max first at level 5.",
    },
    "heal companions": {
        "guild": "martyr",
        "type": "heal",
        "target": "party",
        "base_heal": 80,
        "sp_cost": 50,
        "description": "Heal all party members moderately.",
    },
    "refresh companions": {
        "guild": "martyr",
        "type": "refresh",
        "target": "party",
        "base_refresh": 30,
        "sp_cost": 35,
        "description": "Restore EP to all party members.",
    },
    "holy cause": {
        "guild": "martyr",
        "type": "passive",
        "effect": "sp_regen",
        "per_rank": 0.01,
        "description": "Slight increase in SP regeneration for the party.",
    },
    
    # Confessor spells
    "prayer for healing": {
        "guild": "confessor",
        "type": "heal",
        "target": "single",
        "base_heal": 150,
        "sp_cost": 35,
        "description": "Divine healing through prayer.",
    },
    "prayer for refreshment": {
        "guild": "confessor",
        "type": "refresh",
        "target": "single",
        "base_refresh": 45,
        "sp_cost": 20,
        "description": "Restore EP through divine blessing.",
    },
    "prayer for mankind": {
        "guild": "confessor",
        "type": "buff",
        "target": "party",
        "effect": "hp_max_boost",
        "boost": 0.10,
        "sp_cost": 40,
        "duration": 180,
        "description": "Boost max HP for all party members.",
    },
    "pious words": {
        "guild": "confessor",
        "type": "passive",
        "effect": "reputation",
        "description": "Improves reputation with NPCs and other players.",
    },
    
    # Avatar spells
    "encourage regeneration": {
        "guild": "avatar",
        "type": "buff",
        "target": "single",
        "effect": "sp_regen",
        "base_regen": 15,
        "sp_cost": 45,
        "duration": 600,
        "description": "THE game-changer. Massive SP regen for one target. Cast once, lasts long.",
    },
    "soul of the avatar": {
        "guild": "avatar",
        "type": "passive",
        "effect": "all_stats",
        "per_rank": 0.02,
        "description": "Boost all stats slightly.",
    },
    "quick chant": {
        "guild": "avatar",
        "type": "passive",
        "effect": "cast_speed",
        "per_rank": 0.05,
        "description": "Reduce casting time for all spells.",
    },
    "cleanse soul": {
        "guild": "avatar",
        "type": "heal",
        "target": "single",
        "effect": "remove_scars",
        "sp_cost": 30,
        "description": "Remove all scars in one cast.",
    },
    "feed companions": {
        "guild": "avatar",
        "type": "buff",
        "target": "party",
        "effect": "hunger_reset",
        "sp_cost": 20,
        "description": "Reset hunger levels for entire party. WAY more useful than create food.",
    },
    "revive dead": {
        "guild": "avatar",
        "type": "resurrect",
        "target": "single",
        "sp_cost": 100,
        "description": "Resurrect a fallen party member.",
    },
    "avatar regeneration": {
        "guild": "avatar",
        "type": "self_buff",
        "effect": "hp_regen",
        "base_regen": 25,
        "sp_cost": 50,
        "duration": 300,
        "description": "Personal, better form of encourage regeneration. Most effective with good alignment.",
    },
}

# Party role definitions
PARTY_ROLES = {
    "tank": {
        "description": "Main responsibility: being there, providing HP, taking hits for the party.",
        "consumes": "HP",
        "needs": ["heal", "martyric presence"],
    },
    "blaster": {
        "description": "Uses spells to deal damage. Mainly consumes SP.",
        "consumes": "SP",
        "needs": ["encourage regeneration", "martyric presence"],
    },
    "damager": {
        "description": "Uses skills to deal damage. Mainly consumes EP.",
        "consumes": "EP",
        "needs": ["refresh", "minor refresh", "major refresh"],
    },
    "abjurer": {
        "description": "Provides magical protection and vulnerabilities.",
        "consumes": "SP",
        "needs": ["encourage regeneration"],
    },
    "healer": {
        "description": "Keeps everyone alive and resources flowing.",
        "consumes": "SP",
        "needs": ["quick chant", "essence eye"],
    },
}

def get_heal_amount(spell_name, caster_level, mastery_percent=100):
    """Calculate actual heal amount based on spell and mastery."""
    spell = HEALING_SPELLS.get(spell_name)
    if not spell or spell["type"] not in ["heal", "refresh"]:
        return 0
    
    base = spell.get("base_heal", spell.get("base_refresh", 0))
    
    # Apply mastery bonuses
    mastery_bonus = 1.0
    if "mastery" in spell:
        mastery_name = spell["mastery"]
        mastery_spell = HEALING_SPELLS.get(mastery_name)
        if mastery_spell and mastery_spell["type"] == "passive":
            mastery_bonus += mastery_spell.get("per_rank", 0) * (mastery_percent / 100)
    
    # Apply holy essence
    holy_essence = HEALING_SPELLS.get("holy essence")
    if holy_essence:
        mastery_bonus += holy_essence.get("per_rank", 0) * (mastery_percent / 100)
    
    # Apply enhance healing
    enhance = HEALING_SPELLS.get("enhance healing")
    if enhance:
        mastery_bonus += enhance.get("per_rank", 0) * (mastery_percent / 100)
    
    return int(base * mastery_bonus)

def get_party_heal_priority():
    """Return the priority order for party healing."""
    return [
        "encourage regeneration on blasters first (they do most damage)",
        "martyric presence always active",
        "heal tank when HP drops below 50%",
        "refresh damagers when EP low",
        "re-cast enreg immediately when it falls",
    ]
