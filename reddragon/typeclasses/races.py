"""
Red Dragon MUD - Race System
Based on Islands of Myth 27-race archive
"""

from evennia import DefaultScript

# IOM stat tiers mapped to numeric values for calculation
TIER_MAP = {
    "Terrible": 10, "Bad": 20, "Poor": 30, "Below Ave": 40,
    "Average": 50, "Above Ave": 60, "Good": 70, "Very Good": 80,
    "Excellent": 90, "Extremely": 100  # for special traits
}

RACES = {
    "cromagnon": {
        "name": "Cromagnon",
        "stats": {
            "strength": 70, "dexterity": 60, "constitution": 70,
            "stamina": 60, "intelligence": 20, "wisdom": 20, "charisma": 40
        },
        "hp_max": 50, "ep_max": 50, "sp_max": 10,
        "hp_regen": 60, "ep_regen": 60, "sp_regen": 10,
        "skill_cap": 90, "spell_cap": 70,
        "xp_rate": 1.06,
        "height": "5'5\"", "mass": 184,
        "traits": [
            "learn_skills_fast",
            "learn_spells_slow",
            "resist_physical",
            "vulnerable_magic"
        ],
        "desc": "Living relics from the dawn of humanity. Tougher, stronger, but magically stunted."
    },
    "drow": {
        "name": "Drow",
        "stats": {
            "strength": 50, "dexterity": 70, "constitution": 40,
            "stamina": 40, "intelligence": 60, "wisdom": 70, "charisma": 75
        },
        "hp_max": 50, "ep_max": 40, "sp_max": 50,
        "hp_regen": 40, "ep_regen": 50, "sp_regen": 80,
        "skill_cap": 95, "spell_cap": 100,
        "xp_rate": 0.84,
        "height": "5'4\"", "mass": 133,
        "traits": [
            "learn_skills_slow",
            "learn_spells_normal",
            "see_in_dark"
        ],
        "desc": "Dark Elves of the Underworld. Ruthless killers with spellcasting and fighting ability."
    },
    "dwarf": {
        "name": "Dwarf",
        "stats": {
            "strength": 70, "dexterity": 60, "constitution": 70,
            "stamina": 60, "intelligence": 30, "wisdom": 60, "charisma": 50
        },
        "hp_max": 70, "ep_max": 50, "sp_max": 10,
        "hp_regen": 50, "ep_regen": 60, "sp_regen": 30,
        "skill_cap": 100, "spell_cap": 85,
        "xp_rate": 0.88,
        "height": "4'0\"", "mass": 176,
        "traits": [
            "learn_skills_fast",
            "learn_spells_slow",
            "see_in_dark",
            "resist_poison"
        ],
        "desc": "Small, heavy-set masters of craft and combat. The best weaponsmiths."
    },
    "elf": {
        "name": "Elf",
        "stats": {
            "strength": 40, "dexterity": 60, "constitution": 40,
            "stamina": 30, "intelligence": 50, "wisdom": 80, "charisma": 75
        },
        "hp_max": 50, "ep_max": 30, "sp_max": 50,
        "hp_regen": 50, "ep_regen": 60, "sp_regen": 80,
        "skill_cap": 95, "spell_cap": 95,
        "xp_rate": 0.95,
        "height": "5'2\"", "mass": 113,
        "traits": [
            "learn_skills_slow",
            "learn_spells_normal",
            "see_in_dark",
            "resist_physical"
        ],
        "desc": "Ancient, graceful, nearly immortal. Masters of mystery and magic."
    },
    "ent": {
        "name": "Ent",
        "stats": {
            "strength": 60, "dexterity": 10, "constitution": 70,
            "stamina": 20, "intelligence": 50, "wisdom": 90, "charisma": 70
        },
        "hp_max": 60, "ep_max": 20, "sp_max": 70,
        "hp_regen": 40, "ep_regen": 40, "sp_regen": 80,
        "skill_cap": 90, "spell_cap": 95,
        "xp_rate": 0.90,
        "height": "7'8\"", "mass": 377,
        "traits": [
            "learn_skills_slow",
            "learn_spells_normal",
            "see_in_dark",
            "vulnerable_fire"
        ],
        "desc": "Ancient tree-kin. Slow to act, but wise beyond measure."
    },
    "faerie": {
        "name": "Faerie",
        "stats": {
            "strength": 10, "dexterity": 80, "constitution": 30,
            "stamina": 30, "intelligence": 60, "wisdom": 80, "charisma": 70
        },
        "hp_max": 40, "ep_max": 40, "sp_max": 80,
        "hp_regen": 40, "ep_regen": 30, "sp_regen": 80,
        "skill_cap": 95, "spell_cap": 100,
        "xp_rate": 0.97,
        "height": "2'4\"", "mass": 16,
        "traits": [
            "learn_skills_slow",
            "learn_spells_fast",
            "see_in_dark",
            "resist_psionic",
            "resist_magic",
            "vulnerable_physical"
        ],
        "desc": "Tiny mystical creatures with wings that evolution left unable to fly."
    },
    "gargoyle": {
        "name": "Gargoyle",
        "stats": {
            "strength": 40, "dexterity": 30, "constitution": 70,
            "stamina": 30, "intelligence": 80, "wisdom": 50, "charisma": 35
        },
        "hp_max": 40, "ep_max": 30, "sp_max": 80,
        "hp_regen": 30, "ep_regen": 30, "sp_regen": 90,
        "skill_cap": 90, "spell_cap": 95,
        "xp_rate": 0.90,
        "height": "6'8\"", "mass": 308,
        "traits": [
            "learn_skills_normal",
            "learn_spells_fast",
            "see_in_dark",
            "resist_physical"
        ],
        "desc": "Once stone guardians of holy places, now conscious and highly magical."
    },
    "giant": {
        "name": "Giant",
        "stats": {
            "strength": 90, "dexterity": 50, "constitution": 90,
            "stamina": 60, "intelligence": 20, "wisdom": 10, "charisma": 35
        },
        "hp_max": 90, "ep_max": 60, "sp_max": 10,
        "hp_regen": 70, "ep_regen": 70, "sp_regen": 10,
        "skill_cap": 95, "spell_cap": 20,
        "xp_rate": 0.85,
        "height": "10'0\"", "mass": 519,
        "traits": [
            "learn_skills_slow",
            "learn_spells_very_slow",
            "shout_fee_fie_fo_fum"
        ],
        "desc": "Huge, non-magical brutes. Shout 'Fee, fie, fo, fum!' to break out of shock."
    },
    "gnome": {
        "name": "Gnome",
        "stats": {
            "strength": 30, "dexterity": 40, "constitution": 40,
            "stamina": 30, "intelligence": 60, "wisdom": 90, "charisma": 50
        },
        "hp_max": 40, "ep_max": 40, "sp_max": 80,
        "hp_regen": 40, "ep_regen": 30, "sp_regen": 80,
        "skill_cap": 85, "spell_cap": 95,
        "xp_rate": 1.06,
        "height": "3'6\"", "mass": 122,
        "traits": [
            "learn_skills_slow",
            "learn_spells_fast",
            "see_in_dark",
            "resist_physical"
        ],
        "desc": "Small tinkers with china-blue eyes. Inventors and excellent mages."
    },
    "goblin": {
        "name": "Goblin",
        "stats": {
            "strength": 50, "dexterity": 80, "constitution": 40,
            "stamina": 60, "intelligence": 30, "wisdom": 30, "charisma": 35
        },
        "hp_max": 50, "ep_max": 60, "sp_max": 20,
        "hp_regen": 50, "ep_regen": 70, "sp_regen": 20,
        "skill_cap": 95, "spell_cap": 60,
        "xp_rate": 1.04,
        "height": "4'8\"", "mass": 160,
        "traits": [
            "learn_skills_normal"
        ],
        "desc": "Mischievous little clansmen. Nimble, stealthy, and great at complicated skills."
    },
    "grorrark": {
        "name": "Grorrark",
        "stats": {
            "strength": 70, "dexterity": 90, "constitution": 70,
            "stamina": 60, "intelligence": 30, "wisdom": 30, "charisma": 50
        },
        "hp_max": 60, "ep_max": 40, "sp_max": 20,
        "hp_regen": 50, "ep_regen": 60, "sp_regen": 20,
        "skill_cap": 100, "spell_cap": 80,
        "xp_rate": 0.88,
        "height": "6'8\"", "mass": 267,
        "traits": [
            "learn_skills_fast",
            "learn_spells_very_slow",
            "see_in_dark",
            "eat_corpses",
            "resist_cold",
            "vulnerable_fire",
            "roar",
            "roar_liv"
        ],
        "desc": "Half-human, half-lion. Ferocious fighters who can draw on their beast nature to roar."
    },
    "halfelf": {
        "name": "Halfelf",
        "stats": {
            "strength": 70, "dexterity": 70, "constitution": 60,
            "stamina": 40, "intelligence": 50, "wisdom": 60, "charisma": 65
        },
        "hp_max": 50, "ep_max": 30, "sp_max": 40,
        "hp_regen": 50, "ep_regen": 60, "sp_regen": 50,
        "skill_cap": 95, "spell_cap": 95,
        "xp_rate": 0.90,
        "height": "5'8\"", "mass": 141,
        "traits": [
            "learn_skills_slow",
            "learn_spells_fast",
            "see_in_dark"
        ],
        "desc": "Mixed blood of human and elf. Versatile and balanced."
    },
    "hobbit": {
        "name": "Hobbit",
        "stats": {
            "strength": 40, "dexterity": 90, "constitution": 60,
            "stamina": 60, "intelligence": 40, "wisdom": 30, "charisma": 50
        },
        "hp_max": 50, "ep_max": 60, "sp_max": 20,
        "hp_regen": 40, "ep_regen": 70, "sp_regen": 20,
        "skill_cap": 100, "spell_cap": 75,
        "xp_rate": 0.99,
        "height": "3'2\"", "mass": 81,
        "traits": [
            "learn_skills_fast",
            "learn_spells_very_slow",
            "resist_poison"
        ],
        "desc": "Cheerful fellows who love eating and singing. Surprisingly courageous."
    },
    "human": {
        "name": "Human",
        "stats": {
            "strength": 50, "dexterity": 50, "constitution": 50,
            "stamina": 50, "intelligence": 50, "wisdom": 50, "charisma": 50
        },
        "hp_max": 50, "ep_max": 50, "sp_max": 50,
        "hp_regen": 50, "ep_regen": 50, "sp_regen": 50,
        "skill_cap": 95, "spell_cap": 95,
        "xp_rate": 1.00,
        "height": "5'8\"", "mass": 176,
        "traits": [
            "resist_magic"
        ],
        "desc": "The most common and adaptable race. Jacks of all trades."
    },
    "kobold": {
        "name": "Kobold",
        "stats": {
            "strength": 40, "dexterity": 70, "constitution": 40,
            "stamina": 60, "intelligence": 30, "wisdom": 30, "charisma": 35
        },
        "hp_max": 40, "ep_max": 50, "sp_max": 20,
        "hp_regen": 60, "ep_regen": 60, "sp_regen": 20,
        "skill_cap": 90, "spell_cap": 75,
        "xp_rate": 1.19,
        "height": "3'10\"", "mass": 85,
        "traits": [
            "learn_skills_normal",
            "learn_spells_slow",
            "see_in_dark",
            "eat_corpses",
            "vulnerable_asphyxiation",
            "vulnerable_fire",
            "vulnerable_cold",
            "vulnerable_psionic",
            "flee_combat"
        ],
        "desc": "Small, dog-like, craven creatures. They can often flee combat with no ill effects."
    },
    "leprechaun": {
        "name": "Leprechaun",
        "stats": {
            "strength": 10, "dexterity": 60, "constitution": 30,
            "stamina": 30, "intelligence": 60, "wisdom": 70, "charisma": 65
        },
        "hp_max": 30, "ep_max": 30, "sp_max": 60,
        "hp_regen": 30, "ep_regen": 30, "sp_regen": 60,
        "skill_cap": 80, "spell_cap": 90,
        "xp_rate": 1.18,
        "height": "2'10\"", "mass": 73,
        "traits": [
            "learn_skills_slow",
            "learn_spells_fast",
            "vulnerable_magic",
            "vulnerable_physical"
        ],
        "desc": "Playful, mischievous, quick-minded. Natural at magic but erratic."
    },
    "lizardman": {
        "name": "Lizardman",
        "stats": {
            "strength": 60, "dexterity": 70, "constitution": 60,
            "stamina": 50, "intelligence": 30, "wisdom": 60, "charisma": 65
        },
        "hp_max": 60, "ep_max": 50, "sp_max": 20,
        "hp_regen": 40, "ep_regen": 60, "sp_regen": 50,
        "skill_cap": 95, "spell_cap": 90,
        "xp_rate": 0.87,
        "height": "6'4\"", "mass": 254,
        "traits": [],
        "desc": "Savage semi-aquatic reptilian humanoids. Scavengers and raiders."
    },
    "mindflayer": {
        "name": "Mindflayer",
        "stats": {
            "strength": 30, "dexterity": 40, "constitution": 30,
            "stamina": 30, "intelligence": 90, "wisdom": 90, "charisma": 20
        },
        "hp_max": 30, "ep_max": 20, "sp_max": 90,
        "hp_regen": 30, "ep_regen": 30, "sp_regen": 90,
        "skill_cap": 90, "spell_cap": 100,
        "xp_rate": 0.89,
        "height": "5'4\"", "mass": 100,
        "traits": [
            "learn_skills_slow",
            "learn_spells_very_slow",
            "eat_corpses"
        ],
        "desc": "Tentacled evil genius from the Underworld. Feed on brains to gain psionic power."
    },
    "minotaur": {
        "name": "Minotaur",
        "stats": {
            "strength": 90, "dexterity": 70, "constitution": 90,
            "stamina": 60, "intelligence": 20, "wisdom": 20, "charisma": 35
        },
        "hp_max": 80, "ep_max": 50, "sp_max": 10,
        "hp_regen": 60, "ep_regen": 60, "sp_regen": 10,
        "skill_cap": 100, "spell_cap": 50,
        "xp_rate": 0.92,
        "height": "6'11\"", "mass": 276,
        "traits": [
            "learn_skills_normal"
        ],
        "desc": "Bull-headed heavy hitters. Fearsome combatants, famously stupid."
    },
    "ogier": {
        "name": "Ogier",
        "stats": {
            "strength": 70, "dexterity": 90, "constitution": 80,
            "stamina": 60, "intelligence": 20, "wisdom": 30, "charisma": 65
        },
        "hp_max": 70, "ep_max": 60, "sp_max": 20,
        "hp_regen": 50, "ep_regen": 60, "sp_regen": 20,
        "skill_cap": 95, "spell_cap": 60,
        "xp_rate": 0.91,
        "height": "7'2\"", "mass": 331,
        "traits": [
            "learn_spells_very_slow",
            "vulnerable_psionic",
            "resist_physical"
        ],
        "desc": "Expert stonemasons from the Stedding. Once fierce warriors, now withdrawn."
    },
    "phoenix": {
        "name": "Phoenix",
        "stats": {
            "strength": 40, "dexterity": 50, "constitution": 40,
            "stamina": 40, "intelligence": 70, "wisdom": 60, "charisma": 65
        },
        "hp_max": 40, "ep_max": 30, "sp_max": 60,
        "hp_regen": 40, "ep_regen": 30, "sp_regen": 70,
        "skill_cap": 90, "spell_cap": 95,
        "xp_rate": 1.02,
        "height": "5'0\"", "mass": 109,
        "traits": [
            "learn_skills_slow"
        ],
        "desc": "Legendary birds of fire that return from beyond the grave."
    },
    "snakeman": {
        "name": "Snakeman",
        "stats": {
            "strength": 30, "dexterity": 40, "constitution": 30,
            "stamina": 30, "intelligence": 90, "wisdom": 50, "charisma": 35
        },
        "hp_max": 30, "ep_max": 30, "sp_max": 80,
        "hp_regen": 40, "ep_regen": 40, "sp_regen": 90,
        "skill_cap": 95, "spell_cap": 100,
        "xp_rate": 0.98,
        "height": "4'4\"", "mass": 109,
        "traits": [
            "learn_skills_slow",
            "learn_spells_fast",
            "see_in_dark",
            "resist_poison",
            "vulnerable_physical",
            "fly",
            "vulnerable_cold",
            "resist_fire"
        ],
        "desc": "Created by a mage, killed him, became the best mages. Cold-blooded and proud."
    },
    "thrikhren": {
        "name": "Thrikhren",
        "stats": {
            "strength": 40, "dexterity": 60, "constitution": 50,
            "stamina": 30, "intelligence": 90, "wisdom": 60, "charisma": 50
        },
        "hp_max": 50, "ep_max": 30, "sp_max": 60,
        "hp_regen": 30, "ep_regen": 30, "sp_regen": 70,
        "skill_cap": 95, "spell_cap": 95,
        "xp_rate": 0.87,
        "height": "4'7\"", "mass": 114,
        "traits": [
            "learn_skills_slow",
            "learn_spells_normal",
            "see_in_dark",
            "eat_corpses"
        ],
        "desc": "Ancient Mantis warriors. Proficient psionic mages with strong shells."
    },
    "troll": {
        "name": "Troll",
        "stats": {
            "strength": 90, "dexterity": 70, "constitution": 90,
            "stamina": 50, "intelligence": 20, "wisdom": 20, "charisma": 35
        },
        "hp_max": 80, "ep_max": 50, "sp_max": 20,
        "hp_regen": 70, "ep_regen": 60, "sp_regen": 10,
        "skill_cap": 95, "spell_cap": 50,
        "xp_rate": 0.92,
        "height": "7'0\"", "mass": 300,
        "traits": [
            "learn_skills_slow",
            "vulnerable_fire"
        ],
        "desc": "Massive regenerating brutes. Fire is their bane."
    },
    "vampire": {
        "name": "Vampire",
        "stats": {
            "strength": 50, "dexterity": 50, "constitution": 50,
            "stamina": 50, "intelligence": 70, "wisdom": 60, "charisma": 70
        },
        "hp_max": 50, "ep_max": 50, "sp_max": 60,
        "hp_regen": 50, "ep_regen": 50, "sp_regen": 70,
        "skill_cap": 95, "spell_cap": 95,
        "xp_rate": 1.02,
        "height": "5'8\"", "mass": 160,
        "traits": [
            "learn_skills_slow",
            "learn_spells_fast",
            "see_in_dark",
            "heal_in_dark"
        ],
        "desc": "Children of the night. Only heal in dark places."
    },
    "vinnipier": {
        "name": "Vinnipier",
        "stats": {
            "strength": 60, "dexterity": 90, "constitution": 50,
            "stamina": 60, "intelligence": 30, "wisdom": 50, "charisma": 50
        },
        "hp_max": 50, "ep_max": 50, "sp_max": 20,
        "hp_regen": 50, "ep_regen": 50, "sp_regen": 20,
        "skill_cap": 95, "spell_cap": 60,
        "xp_rate": 0.92,
        "height": "5'4\"", "mass": 140,
        "traits": [
            "learn_spells_very_slow"
        ],
        "desc": "A genetic mistake in an elf offbreed. They stagger constantly."
    },
    "xorn": {
        "name": "Xorn",
        "stats": {
            "strength": 80, "dexterity": 60, "constitution": 80,
            "stamina": 50, "intelligence": 40, "wisdom": 40, "charisma": 40
        },
        "hp_max": 70, "ep_max": 50, "sp_max": 20,
        "hp_regen": 60, "ep_regen": 50, "sp_regen": 20,
        "skill_cap": 95, "spell_cap": 50,
        "xp_rate": 0.95,
        "height": "5'0\"", "mass": 200,
        "traits": [
            "learn_skills_normal",
            "learn_spells_slow",
            "see_in_dark",
            "dig",
            "eat_rocks"
        ],
        "desc": "Stone-eating earth elementals. Can dig through solid rock to places."
    }
}


def apply_race(character, race_key):
    """Apply race stats and traits to a character."""
    race_data = RACES.get(race_key.lower())
    if not race_data:
        return False
    
    character.db.race = race_data["name"]
    
    # Apply base stats
    for stat, value in race_data["stats"].items():
        setattr(character.db, stat, value)
    
    # Apply resource maxima
    character.db.hp_max = race_data["hp_max"] * 10  # Scale up
    character.db.sp_max = race_data["sp_max"] * 10
    character.db.ep_max = race_data["ep_max"] * 10
    character.db.hp = character.db.hp_max
    character.db.sp = character.db.sp_max
    character.db.ep = character.db.ep_max
    
    # Apply physical attributes
    character.db.height = race_data["height"]
    character.db.weight = race_data["mass"]
    
    # Store traits
    character.db.traits = race_data["traits"]
    character.db.skill_cap = race_data["skill_cap"]
    character.db.spell_cap = race_data["spell_cap"]
    character.db.xp_rate = race_data["xp_rate"]
    
    return True


class RaceSelectionRoom:
    """Mixin for race selection area (Hall of Races equivalent)."""
    
    def at_object_creation(self):
        super().at_object_creation()
        self.db.is_race_selection = True
        
    def at_desc(self, looker=None, **kwargs):
        """Show race selection info."""
        if not looker:
            return super().at_desc(looker, **kwargs)
        
        desc = """
This is the Hall of Races in the space outside the world. The only way out of
this void is to select the race you wish to represent in the world of Red Dragon.
In this hall, every race has a statue, and you feel that you can do these things:

-------------------------------------------------------------------------
      TYPE THIS    : TO RECEIVE
-------------------------------------------------------------------------
      all races    : To get a list of available races
      touch <race> : To touch the statue of <race> and enter the world
      la <race>    : To examine <race>'s statue and learn more info
      read poster  : To see which races are best for which guilds
      read sign    : You're lost and need additional help
-------------------------------------------------------------------------
"""
        return desc