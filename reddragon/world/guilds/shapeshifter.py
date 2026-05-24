"""
Red Dragon MUD - Shapeshifter Guild
Based on Islands of Myth shapeshifter data
Complete implementation with forms, skills, commands, and guild tree.
"""

# =============================================================================
# SHAPESHIFTER FORMS DATA
# =============================================================================

# Player forms: 18 total
# Wizard forms: 2 total (gryphon, gold dragon)

PLAYER_FORMS = {
    # Canine forms
    "dog": {
        "category": "canine",
        "skills": ["track"],
        "can_hold_inventory": False,
        "stat_bonuses": {},
        "stat_penalties": {},
        "resistances": {},
        "height_mod": 0,
        "weight_mod": 0,
        "hunger_mod": 0,
    },
    "wolf": {
        "category": "canine",
        "skills": ["track"],
        "can_hold_inventory": True,
        "stat_bonuses": {},
        "stat_penalties": {},
        "resistances": {},
        "height_mod": 0,
        "weight_mod": 0,
        "hunger_mod": 0,
    },
    "timber wolf": {
        "category": "canine",
        "skills": ["track"],
        "can_hold_inventory": True,
        "stat_bonuses": {},
        "stat_penalties": {},
        "resistances": {},
        "height_mod": 0,
        "weight_mod": 0,
        "hunger_mod": 0,
    },
    # Feline forms
    "cat": {
        "category": "feline",
        "skills": ["hide", "stealth", "hunting"],
        "can_hold_inventory": False,
        "stat_bonuses": {"str": 1, "dex": 1, "con": 1, "sta": 1},
        "stat_penalties": {},
        "resistances": {
            "acid": 1, "asphyxiation": 1, "cold": 1, "electric": 1,
            "fire": 1, "holy": 1, "magical": 1, "physical": 1,
            "poison": 1, "psionic": 1, "unholy": 1,
        },
        "height_mod": -10,
        "weight_mod": -10,
        "hunger_mod": -10,
    },
    "leopard": {
        "category": "feline",
        "skills": ["hunting"],
        "can_hold_inventory": True,
        "stat_bonuses": {"str": 1, "dex": 1, "con": 1, "sta": 1},
        "stat_penalties": {},
        "resistances": {
            "acid": 1, "asphyxiation": 1, "cold": 1, "electric": 1,
            "fire": 1, "holy": 1, "magical": 1, "physical": 1,
            "poison": 1, "psionic": 1, "unholy": 1,
        },
        "height_mod": 5,
        "weight_mod": 5,
        "hunger_mod": 5,
    },
    "tiger": {
        "category": "feline",
        "skills": ["hunting"],
        "can_hold_inventory": True,
        "stat_bonuses": {"str": 1, "dex": 1, "con": 1, "sta": 1},
        "stat_penalties": {},
        "resistances": {
            "acid": 1, "asphyxiation": 1, "cold": 1, "electric": 1,
            "fire": 1, "holy": 1, "magical": 1, "physical": 1,
            "poison": 1, "psionic": 1, "unholy": 1,
        },
        "height_mod": 5,
        "weight_mod": 5,
        "hunger_mod": 5,
    },
    # Avian forms
    "falcon": {
        "category": "avian",
        "skills": [],
        "skill_bonuses": {"motion_control": 1},
        "can_hold_inventory": False,
        "stat_bonuses": {},
        "stat_penalties": {},
        "resistances": {},
        "height_mod": 0,
        "weight_mod": 0,
        "hunger_mod": 0,
    },
    "vulture": {
        "category": "avian",
        "skills": ["eat_corpses"],
        "skill_bonuses": {"motion_control": 1},
        "can_hold_inventory": True,
        "stat_bonuses": {},
        "stat_penalties": {},
        "resistances": {},
        "height_mod": 0,
        "weight_mod": 0,
        "hunger_mod": 0,
    },
    "owl": {
        "category": "avian",
        "skills": ["hide", "stealth"],
        "skill_bonuses": {"motion_control": 1},
        "can_hold_inventory": False,
        "stat_bonuses": {},
        "stat_penalties": {},
        "resistances": {},
        "height_mod": 0,
        "weight_mod": 0,
        "hunger_mod": 0,
    },
    "eagle": {
        "category": "avian",
        "skills": [],
        "skill_bonuses": {"motion_control": 1},
        "can_hold_inventory": False,
        "stat_bonuses": {},
        "stat_penalties": {},
        "resistances": {},
        "height_mod": 0,
        "weight_mod": 0,
        "hunger_mod": 0,
    },
    # Ursine forms
    "black bear": {
        "category": "ursine",
        "skills": [],
        "can_hold_inventory": False,
        "stat_bonuses": {},
        "stat_penalties": {},
        "resistances": {},
        "height_mod": 0,
        "weight_mod": 0,
        "hunger_mod": 0,
    },
    "grizzly bear": {
        "category": "ursine",
        "skills": [],
        "can_hold_inventory": True,
        "stat_bonuses": {},
        "stat_penalties": {},
        "resistances": {},
        "height_mod": 0,
        "weight_mod": 0,
        "hunger_mod": 0,
    },
    "polar bear": {
        "category": "ursine",
        "skills": [],
        "can_hold_inventory": True,
        "stat_bonuses": {},
        "stat_penalties": {},
        "resistances": {},
        "height_mod": 0,
        "weight_mod": 0,
        "hunger_mod": 0,
    },
    # Dragon forms (all need avian + feline + ursine + canine prerequisites)
    "white dragon": {
        "category": "dragon",
        "skills": [],
        "can_hold_inventory": True,
        "stat_bonuses": {},
        "stat_penalties": {},
        "resistances": {},
        "height_mod": 0,
        "weight_mod": 0,
        "hunger_mod": 0,
        "prerequisites": ["avian", "feline", "ursine", "canine"],
    },
    "green dragon": {
        "category": "dragon",
        "skills": [],
        "can_hold_inventory": True,
        "stat_bonuses": {},
        "stat_penalties": {},
        "resistances": {},
        "height_mod": 0,
        "weight_mod": 0,
        "hunger_mod": 0,
        "prerequisites": ["avian", "feline", "ursine", "canine"],
    },
    "blue dragon": {
        "category": "dragon",
        "skills": ["voltaic_venting"],
        "can_hold_inventory": True,
        "stat_bonuses": {},
        "stat_penalties": {},
        "resistances": {},
        "height_mod": 0,
        "weight_mod": 0,
        "hunger_mod": 0,
        "prerequisites": ["avian", "feline", "ursine", "canine"],
    },
    "black dragon": {
        "category": "dragon",
        "skills": ["caustic_cyclone"],
        "can_hold_inventory": True,
        "stat_bonuses": {},
        "stat_penalties": {},
        "resistances": {},
        "height_mod": 0,
        "weight_mod": 0,
        "hunger_mod": 0,
        "prerequisites": ["avian", "feline", "ursine", "canine"],
    },
    "red dragon": {
        "category": "dragon",
        "skills": [],
        "can_hold_inventory": True,
        "stat_bonuses": {},
        "stat_penalties": {},
        "resistances": {},
        "height_mod": 0,
        "weight_mod": 0,
        "hunger_mod": 0,
        "prerequisites": ["avian", "feline", "ursine", "canine"],
    },
}

WIZARD_FORMS = {
    "gryphon": {
        "category": "wizard",
        "skills": [],
        "can_hold_inventory": True,
        "stat_bonuses": {},
        "stat_penalties": {},
        "resistances": {},
        "height_mod": 0,
        "weight_mod": 0,
        "hunger_mod": 0,
    },
    "gold dragon": {
        "category": "wizard",
        "skills": [],
        "can_hold_inventory": True,
        "stat_bonuses": {},
        "stat_penalties": {},
        "resistances": {},
        "height_mod": 0,
        "weight_mod": 0,
        "hunger_mod": 0,
    },
}

ALL_FORMS = {**PLAYER_FORMS, **WIZARD_FORMS}

# =============================================================================
# GUILD PREREQUISITE TREE
# =============================================================================

SHAPESHIFTER_GUILD_TREE = {
    "shapeshifter": {
        "prerequisites": [],
        "location": ("Gossamer Island", "Ancient Forest"),
    },
    "animal_tamer": {
        "prerequisites": [("shapeshifter", 20)],
        "location": ("Emerald Island", "Small Grove"),
        "familiar_limit": {"major": 1, "minor": 1},
    },
    "bestial_seccedaneum": {
        "prerequisites": [("shapeshifter", 20)],
        "location": ("Gossamer Island", "Ancient Forest"),
    },
    "savager": {
        "prerequisites": [("shapeshifter", 20)],
        "location": ("Gossamer Island", "Ancient Forest"),
    },
    "animal_healer": {
        "prerequisites": [("animal_tamer", 10), ("bestial_seccedaneum", 1)],
        "location": ("Emerald Island", "Small Grove"),
    },
    "animal_trainer": {
        "prerequisites": [
            ("animal_tamer", 10),
            ("bestial_seccedaneum", 10),  # OR savager 10
        ],
        "location": ("Emerald Island", "Small Grove"),
        "familiar_bonus": {"major": 1},  # Up to 2 major + 1 minor
    },
    "beast_lord": {
        "prerequisites": [("bestial_seccedaneum", 10), ("savager", 10)],
        "location": ("Gossamer Island", "Ancient Forest"),
    },
    "dragon_lord": {
        "prerequisites": [
            ("animal_healer", 10),
            ("animal_trainer", 10),
            ("beast_lord", 10),
        ],
        "location": ("Dark Caverns Island", "High Ledge On A Cliff"),
        "familiar_bonus": {"major": 1},  # Up to 3 major + 1 minor
    },
}

# =============================================================================
# MIGRATE DESTINATIONS (bird/dragon teleport)
# =============================================================================

MIGRATE_DESTINATIONS = {
    "Gossamer": "bittern",
    "Oddworld": "warbler",
    "Misty": "duck",
    "Hyboria": "goose",
    "Blackavar": "owl",
    "Emerald": "sandpiper",
    "Dark Caverns": "kingfisher",
    "Everrest": "thrush",
    "Sombre": "sparrow",
}

# =============================================================================
# ANIMAL HUSBANDRY UPGRADES
# =============================================================================

FAMILIAR_UPGRADES = {
    "eagle": "golden eagle",
    "bear": "polar bear",
    "wolf": "timber wolf",
    "falcon": "peregrine falcon",
}

# =============================================================================
# MAJOR/MINOR FAMILIAR CLASSIFICATION
# =============================================================================

MAJOR_FAMILIARS = ["bear", "eagle", "wolf"]
MINOR_FAMILIARS = ["falcon"]

# Familiar CHA values
FAMILIAR_CHA = {
    "eagle": 100,
    "golden eagle": 120,
}

# =============================================================================
# HERB GATHERING
# =============================================================================

HERB_TYPES = [
    "small healing herb",
    "medium healing herb",
    "large healing herb",
    "restorative herb",
]

# =============================================================================
# MAGICAL GROWTH PLANTS
# =============================================================================

MAGICAL_GROWTH_PLANTS = {
    "green": {"hunger_restore": 1, "desc": "a small green plant"},
    "red_and_green": {"hunger_restore": 2, "desc": "a red and green plant"},
    "brown": {"hunger_restore": 3, "desc": "a brown plant"},
}

# =============================================================================
# ACTION MESSAGES
# =============================================================================

SHAPE_SHIFTER_MESSAGES = {
    "bite_success": (
        "You decide {target} would look better as a fountain, and immediately "
        "turn your desire to reality. Blood sprays everywhere."
    ),
    "claw_success": [
        "You rip a hole in {target}'s side.",
        "You tear {target}'s belly. Blood and guts scatter everywhere.",
    ],
    "call_for_bear_success": (
        "You fall into a dreamy trance and summon a bear spirit, begging it for help. "
        "Suddenly, a huge {bear_type} bear arrives from somewhere up north, "
        "greeting you as {pronoun} companion!"
    ),
    "call_for_bear_fail": (
        "You pray to the bear spirits for help, but receives no answer."
    ),
    "call_for_bear_effect_down": (
        "{familiar} wanders off, returning to the wilderness it came from."
    ),
    "call_for_eagle_success": (
        "You raise your hands to the sky and calls for help. A few moments later, "
        "coming at an amazing speed, a large eagle comes down from the sky to land near to you."
    ),
    "call_for_eagle_fail": (
        "You pray to the eagle spirits for help, but receives no answer."
    ),
    "call_for_eagle_effect_down": (
        "{familiar} flies off, returning to the wilderness it came from."
    ),
    "call_for_falcon_success": (
        "You look intensely at the sky, and seem to concentrate on a tiny black dot "
        "high in the sky. Suddenly, the dot starts moving and growing very fast, "
        "and a grey-blue falcon comes down from the skies and lands on your shoulder."
    ),
    "call_for_falcon_fail": (
        "You pray to the falcon spirits for help, but receives no answer."
    ),
    "call_for_falcon_effect_down": (
        "{familiar} flies away, returning to the wilderness it came from."
    ),
    "call_for_wolf_fail": (
        "You pray to the wolf spirits for help, but receives no answer."
    ),
    "caustic_cyclone_success": (
        "You breathe, and everything around melts in the resultant spray of acid!"
    ),
    "caustic_cyclone_effect": (
        "You retch, and {target} starts to dissolve in a shower of acid!"
    ),
    "voltaic_venting_success": (
        "You unleash a burst of electrical energy!"
    ),
    "voltaic_venting_effect": (
        "{target} is stunned by the electrical discharge and seems to forget what they were doing!"
    ),
    "herb_gathering_success": (
        "You spend some time examining the floor and finally pick up a {herb}."
    ),
    "herb_gathering_fail": (
        "You search around but fail to find any useful herb."
    ),
    "herb_gathering_outdoor_required": (
        "You need to be outside to gather herbs."
    ),
    "magical_growth_success": (
        "You chant a simple incantation and bring your hands up slowly. "
        "Suddenly a small plant sprouts and grows beside your feet!"
    ),
    "magical_growth_fail": (
        "You chant the words to the spell and make lifting motions with your hands, "
        "but nothing happens."
    ),
    "magical_growth_outdoor_required": (
        "You must be outdoors to magically grow plants."
    ),
    "reverse_transformation_success": (
        "You revert to your natural form."
    ),
    "scavenge_wood_success": (
        "You find some firewood."
    ),
    "scavenge_wood_fail": (
        "You search around but disappointingly find absolutely nothing."
    ),
    "shape_shift_start": (
        "You concentrate really, really hard, and begin to change shape."
    ),
    "shape_shift_other": (
        "You begin to change before your very eyes."
    ),
    "shape_shift_pain_1": (
        "You scream in pain as your transformation continues."
    ),
    "shape_shift_pain_2": (
        "You scream in agony, as your transformation turns you into a quivering blob of goo."
    ),
    "shape_shift_pain_3": (
        "You whimper, and go silent as you black out from the pain."
    ),
    "shape_shift_reform": (
        "You lie there, slowly forming into a new form from the pile of goo you currently is."
    ),
    "shape_shift_complete": (
        "You finish your transformation."
    ),
}

# =============================================================================
# COLLAR INFO TEXT
# =============================================================================

COLLAR_INFO = """
You touch your collar and feel the shapeshifter guild's magic flow through you.

Current Form: {current_form}
Available Forms: {forms}
Abilities: {abilities}

Guild Level: {guild_level}
Prerequisites Met: {prereqs}
"""

# =============================================================================
# SHAPESHIFTER SKILLS DATA (for guilds.py integration)
# =============================================================================

SHAPESHIFTER_SKILLS = {
    "shape_shift": {"cost": 100, "max": 100, "desc": "Transform into a beast form."},
    "reverse_transformation": {"cost": 50, "max": 100, "desc": "Return to natural form."},
    "bite": {"cost": 150, "max": 100, "desc": "A powerful bite attack."},
    "claw": {"cost": 150, "max": 100, "desc": "A rending claw attack."},
    "migrate": {"cost": 200, "max": 100, "desc": "Teleport to another island (bird/dragon forms only)."},
    "herb_gathering": {"cost": 100, "max": 100, "desc": "Find healing herbs outdoors."},
    "magical_growth": {"cost": 150, "max": 100, "desc": "Grow plants to restore hunger."},
    "animal_husbandry": {"cost": 300, "max": 100, "desc": "Upgrade your familiars."},
    "call_for_bear": {"cost": 250, "max": 100, "desc": "Summon a bear familiar."},
    "call_for_eagle": {"cost": 250, "max": 100, "desc": "Summon an eagle familiar."},
    "call_for_falcon": {"cost": 200, "max": 100, "desc": "Summon a falcon familiar."},
    "call_for_wolf": {"cost": 250, "max": 100, "desc": "Summon a wolf familiar."},
    "scavenge_wood": {"cost": 50, "max": 100, "desc": "Find firewood."},
    "caustic_cyclone": {"cost": 500, "max": 100, "desc": "Breathe acid (black dragon only)."},
    "voltaic_venting": {"cost": 500, "max": 100, "desc": "Unleash lightning (blue dragon only)."},
}
