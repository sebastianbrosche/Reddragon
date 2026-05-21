"""
Red Dragon MUD — Complete Race System
=====================================
All 27 playable races from Islands of Myth, with full stat modifiers,
racial traits, XP rates, and skill/spell caps.

Stat scale (numeric mapping):
  Terrible = -3, Bad = -2, Below Ave = -1, Average = 0,
  Above Ave = 1, Good = 2, Very Good = 3, Excellent = 4

Each race defines:
  - Base stat modifiers (applied at creation)
  - Racial traits (passive abilities)
  - XP rate modifier (affects leveling speed)
  - Skill cap / Spell cap (maximum training percentages)
  - Special abilities (active racial powers)
"""

from evennia import DefaultCharacter

# ---------------------------------------------------------------------------
# Stat tier mapping
# ---------------------------------------------------------------------------
TIER_MAP = {
    "terrible": -3, "bad": -2, "below ave": -1, "average": 0,
    "above ave": 1, "good": 2, "very good": 3, "excellent": 4,
}

# ---------------------------------------------------------------------------
# Complete Race Database (27 races)
# ---------------------------------------------------------------------------
RACES = {
    "cromagnon": {
        "name": "Cromagnon",
        "desc": "Living relics from the dawn of humanity. Stronger and tougher than modern humans, but completely unable to use magic. They learn skills with brutal efficiency.",
        "stats": {
            "strength": 2, "constitution": 2, "dexterity": 1, "stamina": 1,
            "intelligence": -2, "wisdom": -2,
            "hp_max": 0, "hp_regen": 1, "ep_max": 0, "ep_regen": 1,
            "sp_max": -3, "sp_regen": -3,
        },
        "traits": [
            "Extremely resistant to physical damage (+25% DR)",
            "Vulnerable to magical damage (-20% MR)",
            "Cannot cast spells or use magical items",
            "Learn physical skills 30% faster",
            "Unattractive — social penalties with refined races",
        ],
        "xp_rate": 1.06,
        "skill_cap": 0.90,
        "spell_cap": 0.00,
        "height": "5'5\"",
        "mass": 184,
        "special": "berserker_rage",
    },
    "drow": {
        "name": "Drow",
        "desc": "Dark Elves of the Underworld — indigo-skinned, white-haired killers with red or golden eyes. Ruthless, precise, and feared.",
        "stats": {
            "strength": 0, "constitution": -1, "dexterity": 2, "stamina": -1,
            "intelligence": 1, "wisdom": 2,
            "hp_max": 0, "hp_regen": -1, "ep_max": -1, "ep_regen": 0,
            "sp_max": 0, "sp_regen": 3,
        },
        "traits": [
            "See perfectly in complete darkness",
            "Only regenerate HP/SP in dark places (sunlight halts regen)",
            "Extremely vulnerable to holy damage (-30%)",
            "Resistant to unholy damage (+20%)",
            "Resistant to magical damage (+15%)",
            "Fascinating aura — +10% persuasion vs opposite gender",
        ],
        "xp_rate": 0.84,
        "skill_cap": 0.95,
        "spell_cap": 1.00,
        "height": "5'4\"",
        "mass": 133,
        "special": "shadow_dance",
    },
    "dwarf": {
        "name": "Dwarf",
        "desc": "Stout, stocky masters of stone and metal. Thick beards, fierce loyalty, and an unmatched ability to hold a line.",
        "stats": {
            "strength": 2, "constitution": 3, "dexterity": -1, "stamina": 2,
            "intelligence": 0, "wisdom": 1,
            "hp_max": 1, "hp_regen": 1, "ep_max": 0, "ep_regen": 0,
            "sp_max": -2, "sp_regen": -2,
        },
        "traits": [
            "See in the dark (infravision)",
            "Resistant to poison (+25%)",
            "Resistant to physical damage (+15% DR)",
            "Cannot ride mounts larger than ponies",
            "Bonus to all crafting skills (+15%)",
            "Bonus to axe and hammer weapon mastery (+10%)",
        ],
        "xp_rate": 0.98,
        "skill_cap": 0.95,
        "spell_cap": 0.85,
        "height": "4'6\"",
        "mass": 160,
        "special": "stoneform",
    },
    "elf": {
        "name": "Elf",
        "desc": "Slender, graceful, long-lived beings with pointed ears and an ancient connection to magic and nature.",
        "stats": {
            "strength": -1, "constitution": -1, "dexterity": 1, "stamina": -2,
            "intelligence": 0, "wisdom": 3,
            "hp_max": -1, "hp_regen": 0, "ep_max": -1, "ep_regen": 1,
            "sp_max": 0, "sp_regen": 3,
        },
        "traits": [
            "See in low light (twilight vision)",
            "Resistant to charm and sleep effects (+20%)",
            "Learn spells at normal speed, physical skills slower (-10%)",
            "Cannot be resurrected by necromancy (soul passes to afterlife)",
            "Bonus to bow weapon mastery (+15%)",
        ],
        "xp_rate": 0.95,
        "skill_cap": 0.95,
        "spell_cap": 0.95,
        "height": "5'8\"",
        "mass": 130,
        "special": "nature_walk",
    },
    "ent": {
        "name": "Ent",
        "desc": "Ancient tree-shepherds, slow to anger but terrible in wrath. Massive wooden beings that speak in long, deliberate sentences.",
        "stats": {
            "strength": 3, "constitution": 4, "dexterity": -3, "stamina": -1,
            "intelligence": 1, "wisdom": 3,
            "hp_max": 2, "hp_regen": 1, "ep_max": 1, "ep_regen": 1,
            "sp_max": 1, "sp_regen": 2,
        },
        "traits": [
            "Immune to charm, fear, and mental domination",
            "Resistant to nature magic (+30%)",
            "Extremely slow movement (50% normal speed)",
            "Can commune with trees for information",
            "Vulnerable to fire (-25% fire resistance)",
            "Regenerate HP slowly while in forest areas",
        ],
        "xp_rate": 0.85,
        "skill_cap": 0.90,
        "spell_cap": 0.90,
        "height": "12'0\"",
        "mass": 800,
        "special": "ent_root",
    },
    "faerie": {
        "name": "Faerie",
        "desc": "Tiny winged humanoids with iridescent bodies and a penchant for mischief. Powerful in magic despite their size.",
        "stats": {
            "strength": -3, "constitution": -2, "dexterity": 3, "stamina": -2,
            "intelligence": 2, "wisdom": 2,
            "hp_max": -2, "hp_regen": 0, "ep_max": -1, "ep_regen": 1,
            "sp_max": 2, "sp_regen": 3,
        },
        "traits": [
            "Can fly (bypass terrain obstacles)",
            "Can turn invisible at will (drains SP)",
            "Vulnerable to iron weapons (+50% damage from iron)",
            "Can cast minor spells without components",
            "Extremely hard to hit (+20% dodge vs large opponents)",
        ],
        "xp_rate": 0.90,
        "skill_cap": 0.85,
        "spell_cap": 0.95,
        "height": "1'0\"",
        "mass": 8,
        "special": "pixie_dust",
    },
    "gargoyle": {
        "name": "Gargoyle",
        "desc": "Stone-skinned winged guardians created by ancient magics. Cold, patient, and nearly impervious to harm.",
        "stats": {
            "strength": 2, "constitution": 3, "dexterity": 0, "stamina": 1,
            "intelligence": -1, "wisdom": 0,
            "hp_max": 1, "hp_regen": 0, "ep_max": 1, "ep_regen": 0,
            "sp_max": -2, "sp_regen": -1,
        },
        "traits": [
            "Can fly (limited duration, must rest on stone)",
            "Resistant to all physical damage (+30% DR)",
            "Immune to petrification and paralysis",
            "Cannot heal naturally — must rest on stone surfaces",
            "Vulnerable to sonic damage (-20%)",
        ],
        "xp_rate": 0.92,
        "skill_cap": 0.90,
        "spell_cap": 0.75,
        "height": "6'0\"",
        "mass": 300,
        "special": "stone_skin",
    },
    "giant": {
        "name": "Giant",
        "desc": "Massive humanoids whose strength is legendary. Simple-minded but capable of shattering castle walls with their bare hands.",
        "stats": {
            "strength": 4, "constitution": 3, "dexterity": -2, "stamina": 2,
            "intelligence": -2, "wisdom": -1,
            "hp_max": 2, "hp_regen": 1, "ep_max": 2, "ep_regen": 1,
            "sp_max": -3, "sp_regen": -2,
        },
        "traits": [
            "Can wield two-handed weapons in one hand",
            "Resistant to knockback and being moved against will",
            "Vulnerable to mental magic (-20% MR)",
            "Eat 3x normal food rations",
            "Can throw boulders as ranged attacks",
            "Intimidation bonus (+25%)",
        ],
        "xp_rate": 1.10,
        "skill_cap": 0.85,
        "spell_cap": 0.60,
        "height": "10'0\"",
        "mass": 600,
        "special": "colossal_slam",
    },
    "gnome": {
        "name": "Gnome",
        "desc": "Small, clever humanoids with a natural affinity for illusion magic and mechanical invention.",
        "stats": {
            "strength": -2, "constitution": -1, "dexterity": 1, "stamina": 0,
            "intelligence": 3, "wisdom": 1,
            "hp_max": -1, "hp_regen": 0, "ep_max": 0, "ep_regen": 0,
            "sp_max": 1, "sp_regen": 1,
        },
        "traits": [
            "Can see through all illusions automatically",
            "Bonus to crafting and tinkering (+20%)",
            "Resistant to mental magic (+15%)",
            "Can fit through spaces as small as 1 foot wide",
            "Bonus to dagger and crossbow weapon mastery (+10%)",
        ],
        "xp_rate": 0.95,
        "skill_cap": 0.90,
        "spell_cap": 0.95,
        "height": "3'6\"",
        "mass": 50,
        "special": "illusion_break",
    },
    "goblin": {
        "name": "Goblin",
        "desc": "Small, green-skinned tricksters with sharp teeth and a society built on theft, cunning, and survival.",
        "stats": {
            "strength": -2, "constitution": -1, "dexterity": 2, "stamina": 1,
            "intelligence": 0, "wisdom": -1,
            "hp_max": -1, "hp_regen": 0, "ep_max": 0, "ep_regen": 1,
            "sp_max": -1, "sp_regen": 0,
        },
        "traits": [
            "Can pickpocket NPCs (success chance = dex + level)",
            "Bonus to hiding and sneaking (+20%)",
            "Resistant to disease and poison (+15%)",
            "Start with extra gold (+50 coins)",
            "Pack tactics — +5% damage per allied goblin in room (max +25%)",
        ],
        "xp_rate": 1.05,
        "skill_cap": 0.90,
        "spell_cap": 0.80,
        "height": "3'8\"",
        "mass": 55,
        "special": "sneak_attack",
    },
    "grorrark": {
        "name": "Grorrark",
        "desc": "Reptilian humanoids with tough scales and a savage, primitive fighting style. Devastating in close combat.",
        "stats": {
            "strength": 2, "constitution": 2, "dexterity": 1, "stamina": 1,
            "intelligence": -2, "wisdom": -1,
            "hp_max": 1, "hp_regen": 0, "ep_max": 1, "ep_regen": 0,
            "sp_max": -2, "sp_regen": -1,
        },
        "traits": [
            "Natural armor — scales provide +15% DR",
            "Carnivore only — cannot eat plant-based food",
            "Resistant to fire (+20%)",
            "Bite attack deals bonus poison damage (1d4/round for 3 rounds)",
            "Cold-blooded — move slower in cold environments",
        ],
        "xp_rate": 1.08,
        "skill_cap": 0.90,
        "spell_cap": 0.70,
        "height": "6'2\"",
        "mass": 220,
        "special": "savage_bite",
    },
    "halfelf": {
        "name": "Half-Elf",
        "desc": "Born of human and elf unions. They blend human adaptability with elven grace and a touch of magic.",
        "stats": {
            "strength": 0, "constitution": 0, "dexterity": 1, "stamina": 0,
            "intelligence": 0, "wisdom": 1,
            "hp_max": 0, "hp_regen": 0, "ep_max": 0, "ep_regen": 0,
            "sp_max": 0, "sp_regen": 1,
        },
        "traits": [
            "See in low light (twilight vision)",
            "Resistant to charm (+10%)",
            "Can pass as human or elf in social situations",
            "Learn all skills 5% faster than humans",
            "No racial penalties to any guild",
        ],
        "xp_rate": 1.00,
        "skill_cap": 0.95,
        "spell_cap": 0.95,
        "height": "5'7\"",
        "mass": 140,
        "special": "adaptability",
    },
    "hobbit": {
        "name": "Hobbit",
        "desc": "Small, cheerful folk with hairy feet and a love of food, comfort, and simple pleasures. Surprisingly resilient.",
        "stats": {
            "strength": -2, "constitution": 1, "dexterity": 1, "stamina": 0,
            "intelligence": 0, "wisdom": 1,
            "hp_max": 0, "hp_regen": 1, "ep_max": 0, "ep_regen": 0,
            "sp_max": -1, "sp_regen": 0,
        },
        "traits": [
            "Resistant to fear (+25% — impossible to panic)",
            "Bonus to cooking and foraging (+20%)",
            "Can hide effectively even in poor cover (+15%)",
            "Lucky — once per day, reroll any failed save",
            "Resistant to poison (+10%)",
            "Bonus to thrown weapon mastery (+10%)",
        ],
        "xp_rate": 1.00,
        "skill_cap": 0.95,
        "spell_cap": 0.85,
        "height": "3'6\"",
        "mass": 60,
        "special": "second_breakfast",
    },
    "human": {
        "name": "Human",
        "desc": "The most common race — adaptable, ambitious, and capable of mastering any path they choose.",
        "stats": {
            "strength": 0, "constitution": 0, "dexterity": 0, "stamina": 0,
            "intelligence": 0, "wisdom": 0,
            "hp_max": 0, "hp_regen": 0, "ep_max": 0, "ep_regen": 0,
            "sp_max": 0, "sp_regen": 0,
        },
        "traits": [
            "No racial penalties of any kind",
            "Choose one bonus trait at character creation",
            "Fast learners — 5% XP bonus to all guilds",
            "Average in all things, exceptional in none",
            "Can multiclass without penalties",
        ],
        "xp_rate": 1.00,
        "skill_cap": 0.95,
        "spell_cap": 0.95,
        "height": "5'8\"",
        "mass": 150,
        "special": "versatility",
    },
    "kobold": {
        "name": "Kobold",
        "desc": "Small, reptilian creatures that dwell in darkness. Cowardly alone, deadly in swarms. Masters of trap-making.",
        "stats": {
            "strength": -2, "constitution": -1, "dexterity": 2, "stamina": 1,
            "intelligence": 0, "wisdom": -1,
            "hp_max": -1, "hp_regen": 0, "ep_max": 0, "ep_regen": 1,
            "sp_max": -1, "sp_regen": 0,
        },
        "traits": [
            "See in complete darkness",
            "Bonus to trap-making and detecting traps (+25%)",
            "Pack tactics — +5% damage per ally in room (max +25%)",
            "Can craft crude explosives (level-dependent)",
            "Resistant to disease (+15%)",
        ],
        "xp_rate": 1.05,
        "skill_cap": 0.90,
        "spell_cap": 0.80,
        "height": "3'4\"",
        "mass": 45,
        "special": "trap_sense",
    },
    "leprechaun": {
        "name": "Leprechaun",
        "desc": "Tiny tricksters with a pot of gold and a rainbow of illusions. Master manipulators of luck and perception.",
        "stats": {
            "strength": -3, "constitution": -2, "dexterity": 3, "stamina": -2,
            "intelligence": 2, "wisdom": 1,
            "hp_max": -2, "hp_regen": 0, "ep_max": -1, "ep_regen": 0,
            "sp_max": 1, "sp_regen": 2,
        },
        "traits": [
            "Can teleport short distances (line of sight, costs SP)",
            "Luck manipulation — force one reroll per combat",
            "Resistant to illusions (+20%)",
            "Vulnerable to being captured or bound (+50% escape penalty)",
            "Can turn invisible for 1 round (once per combat)",
        ],
        "xp_rate": 0.88,
        "skill_cap": 0.85,
        "spell_cap": 0.95,
        "height": "1'6\"",
        "mass": 15,
        "special": "rainbow_step",
    },
    "lizardman": {
        "name": "Lizardman",
        "desc": "Cold-blooded reptilian warriors with thick scales and a tribal society. Fierce defenders of their swamp homes.",
        "stats": {
            "strength": 1, "constitution": 2, "dexterity": 1, "stamina": 1,
            "intelligence": -1, "wisdom": 0,
            "hp_max": 1, "hp_regen": 0, "ep_max": 1, "ep_regen": 0,
            "sp_max": -2, "sp_regen": -1,
        },
        "traits": [
            "Natural armor — scales provide +10% DR",
            "Can hold breath underwater for 10 minutes",
            "Resistant to poison (+20%)",
            "Regenerate lost limbs over 1 week (HP regen doubled)",
            "Cold-blooded — slowed by cold, boosted by heat",
        ],
        "xp_rate": 1.02,
        "skill_cap": 0.90,
        "spell_cap": 0.75,
        "height": "6'0\"",
        "mass": 200,
        "special": "swamp_dweller",
    },
    "mindflayer": {
        "name": "Mindflayer",
        "desc": "Alien, octopus-headed humanoids that feed on brains. Masters of psionics and mental domination. Feared by all.",
        "stats": {
            "strength": -1, "constitution": -1, "dexterity": 0, "stamina": -1,
            "intelligence": 4, "wisdom": 3,
            "hp_max": -1, "hp_regen": -1, "ep_max": -1, "ep_regen": -1,
            "sp_max": 3, "sp_regen": 3,
        },
        "traits": [
            "Psionic powers — cast mind spells without verbal components",
            "Can read surface thoughts of nearby enemies (passive)",
            "Must consume brains periodically (or lose 1 INT/day)",
            "Vulnerable to head damage (+50% crit chance vs them)",
            "Immune to charm and mental domination",
        ],
        "xp_rate": 0.80,
        "skill_cap": 0.95,
        "spell_cap": 0.95,
        "height": "5'8\"",
        "mass": 140,
        "special": "mind_blast",
    },
    "minotaur": {
        "name": "Minotaur",
        "desc": "Bull-headed humanoids of immense strength and ferocity. They charge first and ask questions never.",
        "stats": {
            "strength": 3, "constitution": 2, "dexterity": -1, "stamina": 2,
            "intelligence": -2, "wisdom": -1,
            "hp_max": 1, "hp_regen": 1, "ep_max": 1, "ep_regen": 1,
            "sp_max": -3, "sp_regen": -2,
        },
        "traits": [
            "Charge attack — first attack in combat deals +50% damage",
            "Can gore with horns (bonus 1d6 piercing, no weapon needed)",
            "Resistant to maze and confusion spells (+20%)",
            "Vulnerable to confusion effects when actually hit (-10%)",
            "Cannot wear helmets (horns)",
            "Bonus to axe and spear weapon mastery (+10%)",
        ],
        "xp_rate": 1.08,
        "skill_cap": 0.90,
        "spell_cap": 0.65,
        "height": "7'0\"",
        "mass": 350,
        "special": "bull_rush",
    },
    "ogier": {
        "name": "Ogier",
        "desc": "Gentle giants with a love of trees, books, and stonework. Fierce when provoked but prefer peace.",
        "stats": {
            "strength": 3, "constitution": 2, "dexterity": -2, "stamina": 1,
            "intelligence": 1, "wisdom": 2,
            "hp_max": 1, "hp_regen": 0, "ep_max": 1, "ep_regen": 0,
            "sp_max": -1, "sp_regen": 0,
        },
        "traits": [
            "Can sense stonework traps and hidden doors (passive)",
            "Resistant to fear (+20%)",
            "Bonus to crafting, especially stone and wood (+20%)",
            "Slow to anger — +10% resistance to taunt/provoke",
            "When HP drops below 25%, enter 'Oath-Rage' (+2 STR, +1 CON)",
        ],
        "xp_rate": 0.95,
        "skill_cap": 0.90,
        "spell_cap": 0.80,
        "height": "8'0\"",
        "mass": 400,
        "special": "stonewright",
    },
    "phoenix": {
        "name": "Phoenix",
        "desc": "Immortal fire-birds that can take humanoid form. They burn with inner flame and rise from their own ashes.",
        "stats": {
            "strength": 1, "constitution": 1, "dexterity": 2, "stamina": 1,
            "intelligence": 2, "wisdom": 2,
            "hp_max": 0, "hp_regen": 1, "ep_max": 0, "ep_regen": 1,
            "sp_max": 2, "sp_regen": 2,
        },
        "traits": [
            "Immune to fire damage",
            "Can resurrect once per day (return at 25% HP, costs all SP)",
            "Aura of warmth — allies within 10 feet resist cold (+10%)",
            "Vulnerable to water and ice damage (-20%)",
            "Leave burning footprints (minor fire DOT on ground)",
        ],
        "xp_rate": 0.85,
        "skill_cap": 0.90,
        "spell_cap": 0.95,
        "height": "5'10\"",
        "mass": 140,
        "special": "rebirth",
    },
    "snakeman": {
        "name": "Snakeman",
        "desc": "Serpentine humanoids with venomous fangs and hypnotic gazes. Cold, calculating, and patient hunters.",
        "stats": {
            "strength": 0, "constitution": 1, "dexterity": 2, "stamina": 0,
            "intelligence": 1, "wisdom": 0,
            "hp_max": 0, "hp_regen": 0, "ep_max": 0, "ep_regen": 0,
            "sp_max": 0, "sp_regen": 1,
        },
        "traits": [
            "Venomous bite — unarmed attacks apply poison (1d6/round, 3 rounds)",
            "Hypnotic gaze — chance to stun enemy for 1 round (WIS vs WIS)",
            "Can constrict grappled enemies (bonus crushing damage)",
            "Resistant to poison (+25%)",
            "Can sense heat signatures (see warm creatures in darkness)",
        ],
        "xp_rate": 1.00,
        "skill_cap": 0.95,
        "spell_cap": 0.90,
        "height": "5'10\"",
        "mass": 160,
        "special": "serpent_strike",
    },
    "thrikhren": {
        "name": "Thrikhren",
        "desc": "Insectoid humanoids with multiple limbs and a hive mentality. Alien in thought but loyal to the collective.",
        "stats": {
            "strength": 0, "constitution": 1, "dexterity": 2, "stamina": 1,
            "intelligence": 1, "wisdom": 0,
            "hp_max": 0, "hp_regen": 0, "ep_max": 0, "ep_regen": 1,
            "sp_max": 0, "sp_regen": 1,
        },
        "traits": [
            "Multiple arms — can wield an off-hand weapon without penalty",
            "Resistant to mind control (+20%)",
            "Can communicate with all insects (information gathering)",
            "Vulnerable to insecticide and poison gas (-20%)",
            "Bonus to polearm weapon mastery (+10% — extra reach)",
        ],
        "xp_rate": 1.00,
        "skill_cap": 0.95,
        "spell_cap": 0.90,
        "height": "5'6\"",
        "mass": 140,
        "special": "hive_link",
    },
    "troll": {
        "name": "Troll",
        "desc": "Hulking regenerating brutes that are nearly impossible to kill. Dumb as rocks but tougher than them.",
        "stats": {
            "strength": 3, "constitution": 3, "dexterity": -2, "stamina": 2,
            "intelligence": -3, "wisdom": -2,
            "hp_max": 2, "hp_regen": 3, "ep_max": 2, "ep_regen": 2,
            "sp_max": -3, "sp_regen": -3,
        },
        "traits": [
            "Regenerate HP at 5% max HP per round in combat",
            "Regenerate HP at 15% max HP per round out of combat",
            "Resistant to fire (fire does NOT stop regeneration)",
            "Vulnerable to acid damage (-25%, acid prevents regen for 3 rounds)",
            "Can eat anything — no food poisoning, can consume corpses",
            "Cannot wear metal armor (allergic — -1 CON while wearing)",
        ],
        "xp_rate": 1.15,
        "skill_cap": 0.80,
        "spell_cap": 0.50,
        "height": "8'6\"",
        "mass": 450,
        "special": "regeneration",
    },
    "vampire": {
        "name": "Vampire",
        "desc": "Undead aristocrats that feed on blood. Immortal, powerful, and bound by ancient rules and weaknesses.",
        "stats": {
            "strength": 2, "constitution": 2, "dexterity": 2, "stamina": 2,
            "intelligence": 1, "wisdom": 1,
            "hp_max": 1, "hp_regen": 1, "ep_max": 1, "ep_regen": 1,
            "sp_max": 1, "sp_regen": 2,
        },
        "traits": [
            "Immune to poison, disease, and normal aging",
            "Can drain HP from enemies (unarmed attack heals 50% of damage)",
            "Vulnerable to sunlight (-5 HP/round in direct sun)",
            "Vulnerable to holy damage (-25%)",
            "Can turn into mist (become ethereal, move through walls, costs SP)",
            "Cannot enter homes uninvited",
        ],
        "xp_rate": 0.90,
        "skill_cap": 0.95,
        "spell_cap": 0.95,
        "height": "5'10\"",
        "mass": 150,
        "special": "blood_drain",
    },
    "vinnipier": {
        "name": "Vinnipier",
        "desc": "Mysterious aquatic humanoids from the deep ocean. They walk among land-dwellers but never forget the sea.",
        "stats": {
            "strength": 1, "constitution": 1, "dexterity": 1, "stamina": 2,
            "intelligence": 0, "wisdom": 1,
            "hp_max": 0, "hp_regen": 0, "ep_max": 1, "ep_regen": 0,
            "sp_max": 0, "sp_regen": 1,
        },
        "traits": [
            "Can breathe underwater indefinitely",
            "Resistant to cold damage (+20%)",
            "Can communicate with sea creatures",
            "Dry out slowly on land (-1 HP/hour away from water)",
            "Move 50% faster in water, 10% slower on land",
            "Bonus to spear and trident weapon mastery (+10%)",
        ],
        "xp_rate": 0.98,
        "skill_cap": 0.95,
        "spell_cap": 0.90,
        "height": "5'8\"",
        "mass": 145,
        "special": "tidal_surge",
    },
    "xorn": {
        "name": "Xorn",
        "desc": "Alien earth-elementals that phase through stone. They devour gems and minerals, ignoring most physical harm.",
        "stats": {
            "strength": 2, "constitution": 3, "dexterity": -1, "stamina": 2,
            "intelligence": 0, "wisdom": 0,
            "hp_max": 1, "hp_regen": 0, "ep_max": 1, "ep_regen": 0,
            "sp_max": -2, "sp_regen": -1,
        },
        "traits": [
            "Can phase through stone and earth (move through walls, costs SP)",
            "Immune to normal (non-magical) weapon damage",
            "Devour gems and minerals for sustenance (no normal food)",
            "Vulnerable to magical weapons (+50% damage from magic weapons)",
            "Resistant to crushing damage (+20%)",
        ],
        "xp_rate": 1.00,
        "skill_cap": 0.90,
        "spell_cap": 0.75,
        "height": "5'0\"",
        "mass": 250,
        "special": "earth Glide",
    },
}


def apply_race(character, race_key):
    """Apply a race to a character, setting all racial attributes."""
    race = RACES.get(race_key.lower())
    if not race:
        return False

    character.db.race = race_key.lower()
    character.db.race_name = race["name"]
    character.db.race_desc = race["desc"]
    character.db.race_traits = race["traits"]
    character.db.xp_rate = race.get("xp_rate", 1.0)
    character.db.skill_cap = race.get("skill_cap", 0.95)
    character.db.spell_cap = race.get("spell_cap", 0.95)
    character.db.race_special = race.get("special")
    character.db.height = race.get("height", "5'8\"")
    character.db.mass = race.get("mass", 150)

    # Apply base stat modifiers
    for stat, mod in race.get("stats", {}).items():
        current = character.attributes.get(stat, 10)
        character.attributes.add(stat, max(1, current + mod))

    # Set base stats if not already set
    base_stats = ["strength", "constitution", "dexterity", "stamina",
                  "intelligence", "wisdom", "hp_max", "hp_regen",
                  "ep_max", "ep_regen", "sp_max", "sp_regen"]
    for stat in base_stats:
        if character.attributes.get(stat) is None:
            character.attributes.add(stat, 10)

    # Initialize HP/EP/SP to max
    character.db.hp = character.attributes.get("hp_max", 10)
    character.db.ep = character.attributes.get("ep_max", 10)
    character.db.sp = character.attributes.get("sp_max", 10)

    return True


def get_race_detail(race_key):
    """Return formatted detailed info about a race."""
    race = RACES.get(race_key.lower())
    if not race:
        return "Unknown race."

    lines = []
    lines.append(f"{{c{'='*60}{{n")
    lines.append(f"{{G{race['name']}{{n")
    lines.append(f"{{c{'='*60}{{n")
    lines.append("")
    lines.append(race["desc"])
    lines.append("")
    lines.append("{yBase Stats:{n")
    stats = race.get("stats", {})
    for stat in ["strength", "constitution", "dexterity", "stamina",
                   "intelligence", "wisdom"]:
        val = stats.get(stat, 0)
        sign = "+" if val > 0 else ""
        lines.append(f"  {stat.capitalize():12} {sign}{val}")
    lines.append("")
    lines.append("{yResource Stats:{n")
    for stat in ["hp_max", "hp_regen", "ep_max", "ep_regen", "sp_max", "sp_regen"]:
        val = stats.get(stat, 0)
        sign = "+" if val > 0 else ""
        lines.append(f"  {stat.upper():12} {sign}{val}")
    lines.append("")
    lines.append("{yRacial Traits:{n")
    for trait in race["traits"]:
        lines.append(f"  • {trait}")
    lines.append("")
    lines.append(f"{{yXP Rate:{{n {race['xp_rate']*100:.0f}%  |  "
                 f"{{ySkill Cap:{{n {race['skill_cap']*100:.0f}%  |  "
                 f"{{ySpell Cap:{{n {race['spell_cap']*100:.0f}%")
    lines.append(f"{{yHeight:{{n {race.get('height', '?')}  |  "
                 f"{{yMass:{{n {race.get('mass', '?')} lbs")
    lines.append(f"{{ySpecial Ability:{{n {race.get('special', 'None')}")
    lines.append(f"{{c{'='*60}{{n")
    return "\n".join(lines)


def get_race_list():
    """Return a formatted summary list of all races."""
    lines = []
    lines.append("{cAvailable Races (27){n")
    lines.append("-" * 50)
    for key, data in RACES.items():
        xp = data['xp_rate']
        xp_color = "G" if xp <= 1.0 else "r"
        lines.append(f"  {{g{data['name']:<14}{{n — "
                     f"{{y{data['desc'][:45]}...{{n  "
                     f"[{{xp {xp*100:.0f}%{{n]")
    lines.append("-" * 50)
    lines.append("Use {grace <race>{n to view details or select.")
    return "\n".join(lines)
