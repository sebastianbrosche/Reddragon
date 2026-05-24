"""
Red Dragon MUD - Warrior Guild Action Messages
Based on Islands of Myth warrior data
Complete action messages for all warrior skills and stances.
"""

# =============================================================================
# WARRIOR ACTION MESSAGES
# =============================================================================

WARRIOR_ACTION_MESSAGES = {
    "berserker_stance": {
        "effect_up": "You place yourself in a berserker stance.",
        "effect_down": "You lose your beserker stance.",
        "effect_refresh": "You stay in the berserker stance.",
    },
    "biofeedback": {
        "success": "You focus your strength and heal yourself.",
    },
    "blade_dance": {
        "effect_up": "Suddenly your eyes snap open and you glow slightly.",
        "effect_down": "You gasp as your glowing aura flickers and fades away.",
    },
    "bladed_fury": {
        "success": [
            "You helicopter {target}, cutting into {pronoun} body from both sides. Body parts fall from the sky!",
            "You slice your weapon into {target}, cutting flesh and splattering blood everywhere!",
        ],
    },
    "champion_trance": {
        "effect_up": "You focus your will and enter a Champion trance!",
        "effect_down": "You blink out of your Champion trance.",
    },
    "charge": {
        "success": [
            "You rush at {target} and slam your {weapon} into {pronoun}, crushing {pronoun} with the force of your attack.",
            "You roar a thunderous battlecry as you violently charge {target} launching an incredibly powerful blow straight into {pronoun} chest!",
            "{target} seems frozen with fear as you charge with terrible speed at {pronoun}. Right before reaching {pronoun}, you jump high into the air and hurl down your {weapon} right on {pronoun} head!",
        ],
        "other": "{target} shakes violently as your massive blow sends shivers of pain into {pronoun} body.",
    },
    "cry_of_the_berserker": {
        "success": (
            "Your eyes gleam with utter hatred and revulsion as you bring your {weapon} crashing down on "
            "{target}'s skull! {pronoun} gurgles like a vegetable as {pronoun} head collapses in on "
            "{pronoun} brain. You pound on the bloody remains of {pronoun} head until there is nothing left "
            "but a bloody mass of shattered skull and mulched brains..."
        ),
        "effect_up": "You are filled with the rage of the berserker.",
        "effect_down": "Your rage fades.",
        "effect_refresh": "You are filled with rage once again.",
    },
    "cry_of_the_defender": {
        "effect_up": "You are filled with the spirit of war.",
        "effect_refresh": "You are filled with the spirit of war again.",
    },
    "deathblow": {
        "success": [
            (
                "Your eyes gleam with utter hatred and revulsion as you bring your {weapon} crashing down on "
                "{target}'s skull! {pronoun} gurgles like a vegetable as {pronoun} head collapses in on "
                "{pronoun} brain. You pound on the bloody remains of {pronoun} head until there is nothing left "
                "but a bloody mass of shattered skull and mulched brains..."
            ),
            (
                "You mutilates {target} with your unbelievably cruel deathblow! {pronoun} can only gasp before "
                "a gout of thick, black blood explodes out of {pronoun} mouth!"
            ),
        ],
    },
    "fevered_strength": {
        "effect_up": "You grow stronger.",
        "effect_down": "You grow a bit weaker.",
        "effect_refresh": "Your muscles surge with renewed strength.",
    },
    "impale": {
        "success": [
            "You cruelly tear {target}'s side, impaling {pronoun} with your wicked weapon!",
            "You cruelly slash at {target} making {pronoun} scream in pain!",
            "You make a deadly slash at {target}, and your weapon bites deeply into {pronoun} flesh, badly scarring {pronoun}!",
            "You violently stab your weapon into {target}, tearing through flesh and vital organs, creating terrible inner wounds!",
            "You slam your weapon with terrible force straight into {target}, impaling {pronoun} up to the hilt. You then start to turn your weapon while still inside {pronoun} body, ravaging {pronoun} entrails!",
        ],
    },
    "kick": {
        "success": "You land a hard kick to {target}'s stomach, hurting {pronoun}!",
    },
    "punch": {
        "success": "You punch {target} square in the temple, rocking {pronoun} badly!",
    },
    "resist_pain": {
        "success": "You focuse on your body.",
        "effect_up": "You begin to resist pain.",
        "effect_down": "You stop resisting pain.",
    },
    "singing_blade": {
        "success": "You start to sing in a low and sorrowful voice.",
        "effect_up": "{weapon} vibrates, singing its own song!",
        "effect_down": "{weapon} loses its humming song.",
        "effect_refresh": "{weapon} vibrates strongly again.",
    },
    "strike": {
        "success": "You BLASTs your {weapon} into {target}, incising flesh and splatters blood everywhere.",
        "effect": "{target} stumbles backwards a few feet shocked and disoriented.",
    },
    "unbalancing_blow": {
        "success": [
            "You ram {target} with your shield with extraordinary strength!",
            "You violently slam your shield in {target}'s stomach!",
        ],
        "effect": "{target} fights to maintain {pronoun} balance, but fails!",
        "effect_2": "You strongly slam your shield in {target}, badly hurting {pronoun} and making {pronoun} stumble and lose {pronoun} balance!",
    },
}

# =============================================================================
# WARRIOR NOTES / GAMEPLAY TIPS
# =============================================================================

WARRIOR_NOTES = {
    "parry_command": (
        "You must use the command 'parry #' to put yourself into a defensive mode. "
        "'Parry 100' will put you in full defensive mode and 'Parry 0' will put you in full offensive mode."
    ),
    "trobbit_relocator": (
        "Blocking the way to Stone Hedge Tower on Blackavar, is a trobbit that has a berserker guild "
        "relocator that can only be used by a berserker, but it relocates you to the guild."
    ),
    "ignore_resist_pain_combo": (
        "The skills 'ignore pain' and 'resist pain' can be used together."
    ),
}

# =============================================================================
# WARRIOR GUILD PREREQUISITE TREE
# =============================================================================

WARRIOR_GUILD_TREE = {
    "warrior": {
        "prerequisites": [],
        "location": ("Gossamer Island", "A Shack Among Ruins"),
    },
    "berserker": {
        "prerequisites": [("warrior", 20)],
        "location": ("Blackavar Island", "Blackavar City's Royal Palace"),
    },
    "defender_of_the_crown": {
        "prerequisites": [("warrior", 20)],
        "location": ("Blackavar Island", "Blackavar City's Royal Palace"),
    },
    "knight": {
        "prerequisites": [("warrior", 20)],
        "location": ("Blackavar Island", "Blackavar City"),
    },
    "barbarian": {
        "prerequisites": [
            ("berserker", 10),
            ("defender_of_the_crown", 10),  # OR knight 10
        ],
        "location": ("Hyboria Island", "Turanian Camp"),
    },
    "blade_dancer": {
        "prerequisites": [
            ("knight", 10),
            ("berserker", 10),  # OR defender_of_the_crown 10
        ],
        "location": ("Hyboria Island", "Aquilonia Wastelands"),
    },
    "flogger": {
        "prerequisites": [
            ("berserker", 10),
            ("defender_of_the_crown", 10),  # OR knight 10
        ],
        "location": ("Misty Island", "Misty Castle"),
    },
    "shield_master": {
        "prerequisites": [
            ("defender_of_the_crown", 10),
            ("berserker", 10),  # OR knight 10
        ],
        "location": ("Sombre Islands", "Sombre City"),
    },
    "thruster": {
        "prerequisites": [
            ("knight", 10),
            ("berserker", 10),  # OR defender_of_the_crown 10
        ],
        "location": ("Sombre Islands", "Stronglight Castle"),
    },
    "champion_of_the_crown": {
        "prerequisites": [
            # 10 levels in ANY 3 of the 5 warrior bravo guilds
            ("bravo_guilds_any_3", 10),
        ],
        "location": ("Sombre Islands", "Stronglight Castle"),
    },
}

# The 5 warrior bravo guilds for Champion requirement
WARRIOR_BRAVO_GUILDS = [
    "barbarian",
    "blade_dancer",
    "flogger",
    "shield_master",
    "thruster",
]

# =============================================================================
# WARRIOR SKILLS (extended with action message keys)
# =============================================================================

WARRIOR_EXTENDED_SKILLS = {
    "berserker_stance": {"cost": 300, "max": 100, "desc": "Enter a berserker stance.", "messages": "berserker_stance"},
    "biofeedback": {"cost": 250, "max": 100, "desc": "Focus your strength to heal.", "messages": "biofeedback"},
    "blade_dance": {"cost": 400, "max": 100, "desc": "Dance with your blade.", "messages": "blade_dance"},
    "bladed_fury": {"cost": 350, "max": 100, "desc": "A furious bladed assault.", "messages": "bladed_fury"},
    "champion_trance": {"cost": 500, "max": 100, "desc": "Enter a champion trance.", "messages": "champion_trance"},
    "charge": {"cost": 200, "max": 100, "desc": "Charge at your enemy.", "messages": "charge"},
    "cry_of_the_berserker": {"cost": 400, "max": 100, "desc": "Unleash berserker rage.", "messages": "cry_of_the_berserker"},
    "cry_of_the_defender": {"cost": 400, "max": 100, "desc": "Call the spirit of war.", "messages": "cry_of_the_defender"},
    "deathblow": {"cost": 450, "max": 100, "desc": "A devastating killing strike.", "messages": "deathblow"},
    "fevered_strength": {"cost": 250, "max": 100, "desc": "Surge with fevered strength.", "messages": "fevered_strength"},
    "impale": {"cost": 300, "max": 100, "desc": "Impale your enemy.", "messages": "impale"},
    "kick": {"cost": 100, "max": 100, "desc": "A powerful kick.", "messages": "kick"},
    "punch": {"cost": 100, "max": 100, "desc": "A solid punch.", "messages": "punch"},
    "resist_pain": {"cost": 200, "max": 100, "desc": "Resist incoming pain.", "messages": "resist_pain"},
    "singing_blade": {"cost": 300, "max": 100, "desc": "Make your blade sing.", "messages": "singing_blade"},
    "strike": {"cost": 150, "max": 100, "desc": "A powerful strike.", "messages": "strike"},
    "unbalancing_blow": {"cost": 250, "max": 100, "desc": "Throw enemy off balance.", "messages": "unbalancing_blow"},
}
