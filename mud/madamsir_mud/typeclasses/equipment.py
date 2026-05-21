#!/usr/bin/env python3
"""
Red Dragon MUD — Equipment System
=================================
Based on Daran Madrox's equipment sets.
Equipment slots, stats, and special effects.
"""

# Equipment slot positions
EQUIPMENT_SLOTS = [
    "head", "eyes", "neck", "cloak", "amulet",
    "torso", "left_arm", "right_arm", "left_hand", "right_hand",
    "left_ring", "right_ring", "belt", "left_leg", "right_leg",
    "left_foot", "right_foot", "left_weapon", "right_weapon"
]

# Stat abbreviations mapping
STAT_ABBREVIATIONS = {
    "str": "strength",
    "con": "constitution",
    "dex": "dexterity",
    "sta": "stamina",
    "int": "intelligence",
    "wis": "wisdom",
    "cha": "charisma",
    "spr": "spirit",
    "spmax": "sp_max",
    "epmax": "ep_max",
    "hpmax": "hp_max",
    "ac": "armor_class",
}

# Equipment sets from Daran's guide
EQUIPMENT_DATABASE = {
    # Healer Set
    "red_hydra_hide_headband": {
        "name": "Red Hydra Hide Headband",
        "slot": "head",
        "set": "healer",
        "stats": {"wisdom": 20, "sp_max": 20, "quick_chant": 3},
        "description": "A headband made from red hydra hide. Boosts wisdom and chanting speed.",
        "level_req": 11,
    },
    "opal_tikka_spyefel": {
        "name": "Opal Tikka of Spyefel",
        "slot": "eyes",
        "set": "healer",
        "special": ["heal_boost", "pfeed", "align_shift", "freecast"],
        "enhance": 17,
        "description": "Mystical eyewear that enhances healing abilities.",
        "level_req": 20,
    },
    "holy_ankh": {
        "name": "Holy Ankh",
        "slot": "neck",
        "set": "healer",
        "mastery": "heal_mastery",
        "mastery_bonus": 9,
        "description": "Sacred symbol of life. Grants mastery over healing arts.",
        "level_req": 15,
    },
    "cape_of_sand": {
        "name": "Cape of Sand",
        "slot": "cloak",
        "set": "healer",
        "stats": {"wisdom": 16, "spirit": 9, "quick_chant": 5},
        "description": "A flowing cape that seems made of desert sand.",
        "level_req": 1,
    },
    "scarab_of_life": {
        "name": "Scarab of Life",
        "slot": "amulet",
        "set": "healer",
        "stats": {"wisdom": 8, "spirit": 25, "mastery_of_healing": 5},
        "avatar_soul": 4,
        "description": "Ancient scarab that pulses with life energy.",
        "level_req": 25,
    },
    "golden_hide_breastplate": {
        "name": "Golden Hide Breastplate (E)",
        "slot": "torso",
        "set": "healer",
        "stats": {"wisdom": 30, "enhance_healing": 4, "heal": 4},
        "martyr_strength": 9,
        "description": "Enchanted breastplate of golden hide. Exceptional healer armor.",
        "level_req": 30,
    },
    "ghazis_vambrace": {
        "name": "Ghazi's Vambrace",
        "slot": "left_arm",
        "set": "healer",
        "stats": {"wisdom": 12, "spirit": 14, "quick_chant": 2},
        "holy_cause": 5,
        "description": "Arm guard once worn by the legendary healer Ghazi.",
        "level_req": 20,
    },
    "artems_silvery_bracer": {
        "name": "Artem's Silvery Bracer",
        "slot": "right_arm",
        "set": "healer",
        "stats": {"wisdom": 20, "spirit": 8, "quick_chant": 2},
        "description": "Silver bracer inscribed with healing runes.",
        "level_req": 18,
    },
    "scaled_glove": {
        "name": "Scaled Glove",
        "slot": "left_hand",
        "set": "healer",
        "stats": {"wisdom": 18, "spirit": 9, "mastery_of_healing": 1},
        "description": "Glove covered in dragon scales.",
        "level_req": 15,
    },
    "glove_of_scales": {
        "name": "Glove of Scales",
        "slot": "right_hand",
        "set": "healer",
        "stats": {"wisdom": 22, "spirit": 9, "enhance_healing": 3},
        "description": "Matching scaled glove with healing enchantments.",
        "level_req": 16,
    },
    "kreativs_tear": {
        "name": "Kreativ's Tear",
        "slot": "ring",
        "set": "healer",
        "stats": {"intelligence": 9, "spirit": 15, "enhance": 5, "martyr_strength": 3},
        "description": "A crystallized tear with healing properties.",
        "level_req": 22,
    },
    "sash_of_niobhan": {
        "name": "Sash of Niobhan",
        "slot": "belt",
        "set": "healer",
        "stats": {"wisdom": 15, "spirit": 8, "holy_cause": 5, "soul": 4},
        "description": "Woven sash blessed by the healer Niobhan.",
        "level_req": 20,
    },
    "supple_deerskin_chap": {
        "name": "Supple Deerskin Chap",
        "slot": "leg",
        "set": "healer",
        "stats": {"wisdom": 15, "spirit": 9, "martyr_strength": 3},
        "description": "Light leggings made from deerskin.",
        "level_req": 12,
    },
    "bone_leg_plate": {
        "name": "Bone Leg Plate",
        "slot": "leg",
        "set": "healer",
        "stats": {"wisdom": 18, "soul": 3, "holy_essence": 1, "mastery_of_healing": 2},
        "description": "Armor plate carved from ancient bone.",
        "level_req": 18,
    },
    "left_foot_yeti": {
        "name": "Left Foot of the Yeti",
        "slot": "foot",
        "set": "healer",
        "stats": {"wisdom": 18, "intelligence": 6, "quick_chant": 2},
        "description": "Furry boot made from yeti hide.",
        "level_req": 14,
    },
    "boot_of_cleric": {
        "name": "Boot of the Cleric",
        "slot": "foot",
        "set": "healer",
        "stats": {"wisdom": 18, "spirit": 9, "mastery_of_healing": 1},
        "description": "Holy boots worn by high clerics.",
        "level_req": 16,
    },
    "apocalypse_staff": {
        "name": "Apocalypse Staff",
        "slot": "weapon",
        "set": "healer",
        "stats": {"wisdom": 29, "spirit": 19},
        "special": ["healing_boost"],
        "description": "Staff of legendary healing power.",
        "level_req": 35,
    },
    "holy_shield_light": {
        "name": "Holy Shield of Light",
        "slot": "shield",
        "set": "healer",
        "special": ["heal_boost", "protection"],
        "description": "Radiant shield that boosts healing spells.",
        "level_req": 25,
    },
    
    # Abjurer Set
    "armored_helmet_corruption": {
        "name": "Armored Helmet of Corruption",
        "slot": "head",
        "set": "abjurer",
        "stats": {"wisdom": 24, "spirit": 10, "vuln_mastery": 3},
        "quick_chant": 25,
        "description": "Dark helmet that grants vulnerability mastery.",
        "level_req": 30,
    },
    "flexible_eyewear_xenial": {
        "name": "Flexible Eyewear of Xenial",
        "slot": "eyes",
        "set": "abjurer",
        "stats": {"wisdom": 25, "spirit": 9, "quick_chant": 5, "vuln_mastery": 2},
        "description": "Adaptive lenses for abjuration magic.",
        "level_req": 28,
    },
    "abjurean_necklace": {
        "name": "Abjurean Necklace",
        "slot": "neck",
        "set": "abjurer",
        "stats": {"wisdom": 30, "spirit": 205, "lengthen_abjuration": 5, "strengthen_abjuration": 1},
        "lengthen_abjuration_bonus": 9,
        "description": "Ancient necklace of the Abjurean order.",
        "level_req": 35,
    },
    "bronze_griffen_scale": {
        "name": "Bronze Griffen Scale",
        "slot": "amulet",
        "set": "abjurer",
        "stats": {"spirit": 6, "sp_max": 20, "quick_chant": 4, "hef": 3},
        "protection_ritual": 3,
        "description": "Scale from a bronze griffen. Enhances protection rituals.",
        "level_req": 22,
    },
    "breastplate_darkness": {
        "name": "Breastplate of Darkness",
        "slot": "torso",
        "set": "abjurer",
        "stats": {"wisdom": 30, "spirit": 15},
        "special": ["weaken", "reduce_damage_type"],
        "hef": 5,
        "description": "Dark armor that weakens enemy attacks.",
        "level_req": 32,
    },
    "chromatic_chamo_chlamys": {
        "name": "Chromatic Chamo Chlamys",
        "slot": "left_arm",
        "set": "abjurer",
        "stats": {"wisdom": 15, "spirit": 15, "ritual": 3},
        "special": ["boost_ceb"],  # boost combined elemental blast
        "description": "Color-shifting cloak arm piece.",
        "level_req": 28,
    },
    "arctic_sleeve": {
        "name": "Arctic Sleeve",
        "slot": "right_arm",
        "set": "abjurer",
        "stats": {"wisdom": 15, "vuln_mastery": 2, "cold_vulnerability": 3},
        "description": "Frozen sleeve that enhances cold vulnerabilities.",
        "level_req": 24,
    },
    "ruby_ring_weakening": {
        "name": "Ruby Ring of Weakening",
        "slot": "ring",
        "set": "abjurer",
        "stats": {"wisdom": 19, "spirit": 19},
        "special": ["boost_vulns"],
        "description": "Ruby ring that amplifies vulnerability spells.",
        "level_req": 26,
    },
    "ring_of_disruption": {
        "name": "Ring of Disruption",
        "slot": "ring",
        "set": "abjurer",
        "stats": {"wisdom": 15, "spirit": 25},
        "special": ["boost_vulns", "boost_ruptures"],
        "description": "Ring that disrupts magical defenses.",
        "level_req": 28,
    },
    "tiamat_leggings": {
        "name": "Tiamat Leggings (frayed)",
        "slot": "legs",
        "set": "abjurer",
        "stats": {"wisdom": 8, "intelligence": 8, "spirit": 20, "quick_chant": 5},
        "description": "Leggings worn by the dragon Tiamat's servants.",
        "level_req": 30,
    },
    "blackmons_midnight_boots": {
        "name": "Blackmon's Midnight Boots",
        "slot": "feet",
        "set": "abjurer",
        "stats": {"wisdom": 14, "spirit": 22, "lengthen_abjuration": 4},
        "description": "Boots of the legendary abjurer Blackmon.",
        "level_req": 25,
    },
    "prismatic_shield": {
        "name": "Prismatic Shield",
        "slot": "shield",
        "set": "abjurer",
        "special": ["reflective_shield"],
        "description": "Shield that reflects elemental damage.",
        "level_req": 35,
    },
    "bone_dagger": {
        "name": "Bone Dagger",
        "slot": "weapon",
        "set": "abjurer",
        "stats": {"wisdom": 15, "intelligence": 5, "spirit": 15, "vuln_mastery": 3},
        "description": "Dagger carved from dragon bone.",
        "level_req": 20,
    },
    
    # Harmer Set (shared pieces from other sets)
    "staff_of_death": {
        "name": "Staff of Death",
        "slot": "weapon",
        "set": "harmer",
        "special": ["inflict_harm", "dark_ritual"],
        "description": "Staff that channels dark energies for harming spells.",
        "level_req": 30,
    },
    "black_bag": {
        "name": "Black Bag",
        "slot": "container",
        "set": "harmer",
        "contents": ["globe_of_darkness", "globe_of_light"],
        "description": "Mysterious black bag containing orbs of power.",
        "level_req": 20,
    },
    "featureless_mask": {
        "name": "Featureless Mask",
        "slot": "face",
        "set": "harmer",
        "special": ["hide_alignment", "intimidate"],
        "description": "A blank mask that conceals the wearer's identity.",
        "level_req": 15,
    },
    "spellring_create_food": {
        "name": "Spellring - Create Food",
        "slot": "ring",
        "set": "harmer",
        "spell": "create_food",
        "description": "Ring enchanted with the create food spell.",
        "level_req": 10,
    },
    "spellbook_estimate_worth": {
        "name": "Spellbook - Estimate Worth",
        "slot": "held",
        "set": "harmer",
        "spell": "estimate_worth",
        "description": "Spellbook teaching the estimate worth spell.",
        "level_req": 12,
    },
}

# Equipment rarity levels
RARITY_COLORS = {
    "common": "white",
    "uncommon": "green",
    "rare": "blue",
    "epic": "purple",
    "legendary": "orange",
    "artifact": "red",
    "mythic": "cyan",
}

# Condition system (from mechanics.py)
def get_equipment_stats(item_key):
    """Return stats for an equipment piece."""
    item = EQUIPMENT_DATABASE.get(item_key)
    if not item:
        return None
    return {
        "name": item["name"],
        "slot": item["slot"],
        "stats": item.get("stats", {}),
        "special": item.get("special", []),
        "level_req": item.get("level_req", 1),
        "set": item.get("set", None),
        "description": item.get("description", ""),
    }

def get_set_bonus(set_name, num_pieces):
    """Return set bonus for wearing multiple pieces of a set."""
    set_bonuses = {
        "healer": {
            3: {"healing_boost": 0.05, "spirit": 10},
            5: {"healing_boost": 0.10, "spirit": 20, "quick_chant": 2},
            8: {"healing_boost": 0.15, "spirit": 35, "quick_chant": 5, "mastery_of_healing": 3},
            12: {"healing_boost": 0.25, "spirit": 50, "quick_chant": 8, "mastery_of_healing": 5, "enhance_healing": 3},
        },
        "abjurer": {
            3: {"vuln_mastery": 2, "wisdom": 10},
            5: {"vuln_mastery": 5, "wisdom": 20, "quick_chant": 2},
            8: {"vuln_mastery": 8, "wisdom": 35, "quick_chant": 5, "lengthen_abjuration": 3},
        },
        "harmer": {
            3: {"dark_damage": 0.05, "intelligence": 10},
            5: {"dark_damage": 0.10, "intelligence": 20, "inflict_harm": 2},
        },
    }
    bonuses = set_bonuses.get(set_name, {})
    # Return highest applicable bonus
    result = {}
    for count in sorted(bonuses.keys()):
        if num_pieces >= count:
            result = bonuses[count]
    return result

# Weapon types
WEAPON_TYPES = {
    "sword": {"damage_type": "physical", "mastery": "sword"},
    "axe": {"damage_type": "physical", "mastery": "axe"},
    "mace": {"damage_type": "physical", "mastery": "mace"},
    "dagger": {"damage_type": "physical", "mastery": "dagger"},
    "staff": {"damage_type": "physical", "mastery": "staff"},
    "spear": {"damage_type": "physical", "mastery": "spear"},
    "bow": {"damage_type": "physical", "mastery": "bow"},
    "unarmed": {"damage_type": "physical", "mastery": "unarmed"},
    "wand": {"damage_type": "magic", "mastery": "wand"},
}
