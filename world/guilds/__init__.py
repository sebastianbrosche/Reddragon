"""
Red Dragon MUD - Complete Guild Data
All 14 IOM guild trees with prerequisites, skills, and locations.
Based on Daran Madrox's Guide and Wildchild's Archive.
"""

# =============================================================================
# GUILD PREREQUISITES
# =============================================================================

# Format: guild_key: {prerequisites}
# Prerequisites can be:
#   - guild: "guild_name", level: X
#   - alt_guild: "guild_name", alt_level: X (OR condition)
#   - any_of: N, bravo_guilds: [list] (need N levels across any of these)

GUILD_PREREQUISITES = {
    # === WARRIOR TREE ===
    "warrior": None,
    "berserker": {"guild": "warrior", "level": 20},
    "defender": {"guild": "warrior", "level": 20},
    "knight": {"guild": "warrior", "level": 20},
    "barbarian": {"guild": "berserker", "level": 10},
    "blade_dancer": {"guild": "berserker", "level": 10, "alt_guild": "knight", "alt_level": 10},
    "flogger": {"guild": "knight", "level": 10},
    "shield_master": {"guild": "defender", "level": 10, "alt_guild": "berserker", "alt_level": 10},
    "thruster": {"guild": "defender", "level": 10, "alt_guild": "knight", "alt_level": 10},
    "champion": {"any_of": 3, "bravo_guilds": ["barbarian", "blade_dancer", "flogger", "shield_master", "thruster"]},
    
    # === MARTIAL ARTIST TREE ===
    "martial_artist": None,
    "dragonfist_fighter": {"guild": "martial_artist", "level": 20},
    "mystic_warrior": {"guild": "martial_artist", "level": 20},
    "crane_master": {"guild": "dragonfist_fighter", "level": 10},
    "snake_master": {"guild": "dragonfist_fighter", "level": 10, "alt_guild": "mystic_warrior", "alt_level": 10},
    "tiger_master": {"guild": "mystic_warrior", "level": 10},
    "toad_master": {"guild": "mystic_warrior", "level": 10, "alt_guild": "dragonfist_fighter", "alt_level": 10},
    "order_of_the_crescent_moon": {"any_of": 3, "bravo_guilds": ["crane_master", "snake_master", "tiger_master", "toad_master"]},
    "dragon_master": {"guild": "order_of_the_crescent_moon", "level": 10},
    
    # === WEAVER (HEALER) TREE ===
    "weaver": None,
    "confessor": {"guild": "weaver", "level": 20},
    "healer": {"guild": "weaver", "level": 20},
    "martyr": {"guild": "weaver", "level": 20},
    "avatar": {"guild": "confessor", "level": 10, "alt_guild": "healer", "alt_level": 10},
    "exorcist": {"guild": "confessor", "level": 10, "alt_guild": "martyr", "alt_level": 10},
    "shields_of_faith": {"guild": "healer", "level": 10, "alt_guild": "martyr", "alt_level": 10},
    "templar": {"guild": "healer", "level": 10, "alt_guild": "confessor", "alt_level": 10},
    "high_priest": {"any_of": 3, "bravo_guilds": ["avatar", "exorcist", "shields_of_faith", "templar"]},
    
    # === UNRAVELLER TREE ===
    "unraveller": None,
    "harmer": {"guild": "unraveller", "level": 20},
    "magical_torturer": {"guild": "unraveller", "level": 20},
    "sacrificer": {"guild": "unraveller", "level": 20},
    "servant_of_lloth": {"guild": "harmer", "level": 10},
    "servant_of_mordulak": {"guild": "harmer", "level": 10, "alt_guild": "magical_torturer", "alt_level": 10},
    "servant_of_shirija": {"guild": "magical_torturer", "level": 10, "alt_guild": "sacrificer", "alt_level": 10},
    "servant_of_talakh": {"guild": "sacrificer", "level": 10, "alt_guild": "harmer", "alt_level": 10},
    "elder": {"any_of": 3, "bravo_guilds": ["servant_of_lloth", "servant_of_mordulak", "servant_of_shirija", "servant_of_talakh"]},
    "patriarch": {"guild": "elder", "level": 10},
    "primate": {"guild": "elder", "level": 10, "alt_guild": "patriarch", "alt_level": 10},
    "sword": {"guild": "elder", "level": 10, "alt_guild": "patriarch", "alt_level": 10},
    
    # === ELEMENTAL TREE ===
    "elemental": None,
    "air_mage": {"guild": "elemental", "level": 20},
    "earth_mage": {"guild": "elemental", "level": 20},
    "fire_mage": {"guild": "elemental", "level": 20},
    "water_mage": {"guild": "elemental", "level": 20},
    "lava_mage": {"any_of": 2, "bravo_guilds": ["fire_mage", "earth_mage"]},
    "mist_mage": {"any_of": 2, "bravo_guilds": ["air_mage", "water_mage"]},
    "nether_mage": {"any_of": 2, "bravo_guilds": ["lava_mage", "mist_mage"]},
    
    # === EVOKER TREE ===
    "evoker": None,
    "evoker_of_elements": {"guild": "evoker", "level": 20},
    "evoker_of_ether": {"guild": "evoker", "level": 20},
    "acid_evoker": {"guild": "evoker_of_elements", "level": 10},
    "flames_evoker": {"guild": "evoker_of_elements", "level": 10},
    "force_evoker": {"guild": "evoker_of_elements", "level": 10},
    "ice_evoker": {"guild": "evoker_of_elements", "level": 10},
    "lightning_evoker": {"guild": "evoker_of_ether", "level": 10},
    "magic_evoker": {"guild": "evoker_of_ether", "level": 10},
    "poison_evoker": {"guild": "evoker_of_ether", "level": 10},
    "vacuum_evoker": {"guild": "evoker_of_ether", "level": 10},
    "sorcerer": {"any_of": 4, "bravo_guilds": ["acid_evoker", "flames_evoker", "force_evoker", "ice_evoker", "lightning_evoker", "magic_evoker", "poison_evoker", "vacuum_evoker"]},
    
    # === NECROMANCER TREE ===
    "necromancer": None,
    "undead": {"guild": "necromancer", "level": 20},
    "shadow": {"guild": "necromancer", "level": 20},
    "death": {"guild": "necromancer", "level": 20},
    "lich": {"guild": "undead", "level": 10, "alt_guild": "shadow", "alt_level": 10},
    "vampire_lord": {"guild": "shadow", "level": 10, "alt_guild": "death", "alt_level": 10},
    "dark_lord": {"any_of": 2, "bravo_guilds": ["lich", "vampire_lord"]},
    
    # === PSYCHICS TREE ===
    "psychics": None,
    "telepath": {"guild": "psychics", "level": 20},
    "telekinetic": {"guild": "psychics", "level": 20},
    "psionic": {"guild": "telepath", "level": 10, "alt_guild": "telekinetic", "alt_level": 10},
    "mentalist": {"guild": "telekinetic", "level": 10, "alt_guild": "telepath", "alt_level": 10},
    "grandmaster": {"any_of": 2, "bravo_guilds": ["psionic", "mentalist"]},
    
    # === ACROBAT TREE ===
    "acrobat": None,
    "juggler": {"guild": "acrobat", "level": 20},
    "tightrope": {"guild": "acrobat", "level": 20},
    "trapeze": {"guild": "juggler", "level": 10, "alt_guild": "tightrope", "alt_level": 10},
    "fire_eater": {"guild": "juggler", "level": 10, "alt_guild": "tightrope", "alt_level": 10},
    "ringmaster": {"any_of": 2, "bravo_guilds": ["trapeze", "fire_eater"]},
    
    # === LURKER (THIEF) TREE ===
    "lurker": None,
    "scout": {"guild": "lurker", "level": 20},
    "thief": {"guild": "lurker", "level": 20},
    "assassin": {"guild": "scout", "level": 10, "alt_guild": "thief", "alt_level": 10},
    "rogue": {"guild": "thief", "level": 10, "alt_guild": "scout", "alt_level": 10},
    "shadow_master": {"any_of": 2, "bravo_guilds": ["assassin", "rogue"]},
    
    # === DRUID TREE ===
    "druid": None,
    "shaman": {"guild": "druid", "level": 20},
    "witch": {"guild": "druid", "level": 20},
    "elder_druid": {"guild": "shaman", "level": 10, "alt_guild": "witch", "alt_level": 10},
    "archdruid": {"guild": "elder_druid", "level": 10},
    
    # === WOODSMAN (RANGER) TREE ===
    "woodsman": None,
    "ranger": {"guild": "woodsman", "level": 20},
    "tracker": {"guild": "woodsman", "level": 20},
    "beast_master": {"guild": "ranger", "level": 10, "alt_guild": "tracker", "alt_level": 10},
    "forest_lord": {"guild": "beast_master", "level": 10},
    
    # === SHAPESHIFTER TREE ===
    "shapeshifter": None,
    "animal_tamer": {"guild": "shapeshifter", "level": 20},
    "bestial_seccedaneum": {"guild": "shapeshifter", "level": 20},
    "savager": {"guild": "shapeshifter", "level": 20},
    "animal_healer": {"guild": "animal_tamer", "level": 10, "alt_guild": "bestial_seccedaneum", "alt_level": 10},
    "animal_trainer": {"guild": "animal_tamer", "level": 10, "alt_guild": "savager", "alt_level": 10},
    "beast_lord": {"guild": "bestial_seccedaneum", "level": 10, "alt_guild": "savager", "alt_level": 10},
    "dragon_lord": {"any_of": 3, "bravo_guilds": ["animal_healer", "animal_trainer", "beast_lord"]},
}

# =============================================================================
# GUILD STARTING SKILLS
# =============================================================================

GUILD_STARTING_SKILLS = {
    # Warrior tree
    "warrior": {"attack": 20, "parry": 10, "weapon skill blunt": 20},
    "berserker": {"berserker stance": 10, "charge": 10},
    "defender": {"defend": 10, "shield block": 10},
    "knight": {"honor": 10, "charge": 10},
    "barbarian": {"cry of the berserker": 10, "bladed fury": 10},
    "blade_dancer": {"blade dance": 10},
    "flogger": {"flog": 10},
    "shield_master": {"shield bash": 10},
    "thruster": {"thrust": 10},
    "champion": {"champion trance": 10},
    
    # Martial Artist
    "martial_artist": {"punch": 20, "kick": 10},
    "dragonfist_fighter": {"dragon punch": 10},
    "mystic_warrior": {"mystic bolt": 10},
    
    # Weaver
    "weaver": {"heal": 20, "refresh": 10},
    "confessor": {"confess": 10},
    "healer": {"major heal": 10},
    "martyr": {"martyric presence": 10},
    
    # Unraveller
    "unraveller": {"harm": 20, "curse": 10},
    "harmer": {"major harm": 10},
    
    # Elemental
    "elemental": {"magic missile": 20, "shield": 10},
    "air_mage": {"lightning bolt": 10},
    "earth_mage": {"stone skin": 10},
    "fire_mage": {"fireball": 10},
    "water_mage": {"healing stream": 10},
    
    # Evoker
    "evoker": {"evoke": 20, "channel": 10},
    "evoker_of_elements": {"elemental blast": 10},
    "evoker_of_ether": {"ether bolt": 10},
    
    # Necromancer
    "necromancer": {"animate dead": 20, "drain life": 10},
    "undead": {"summon skeleton": 10},
    "shadow": {"shadow bolt": 10},
    
    # Psychics
    "psychics": {"mind blast": 20, "telepathy": 10},
    "telepath": {"mind read": 10},
    "telekinetic": {"telekinetic blast": 10},
    
    # Acrobat
    "acrobat": {"tumble": 20, "balance": 10},
    "juggler": {"juggle": 10},
    "tightrope": {"walk tightrope": 10},
    
    # Lurker
    "lurker": {"hide": 20, "sneak": 10, "backstab": 10},
    "scout": {"track": 10},
    "thief": {"pick pocket": 10},
    "assassin": {"assassinate": 10},
    "rogue": {"dodge": 10},
    
    # Druid
    "druid": {"nature's touch": 20, "entangle": 10},
    "shaman": {"spirit call": 10},
    "witch": {"hex": 10},
    
    # Woodsman
    "woodsman": {"chop": 20, "track": 10},
    "ranger": {"bow shot": 10},
    "tracker": {"find path": 10},
    "beast_master": {"tame beast": 10},
    
    # Shapeshifter
    "shapeshifter": {"shape shift": 10, "reverse transformation": 10},
    "animal_tamer": {"tame animal": 10},
    "bestial_seccedaneum": {"beast form": 10},
    "savager": {"savage attack": 10},
    "animal_healer": {"heal beast": 10},
    "animal_trainer": {"train beast": 10},
    "beast_lord": {"beast lord command": 10},
    "dragon_lord": {"dragon breath": 10},
}

# =============================================================================
# GUILD LOCATIONS (Island + Area)
# =============================================================================

GUILD_LOCATIONS = {
    # Warrior
    "warrior": {"island": "Blackavar", "area": "Stone Hedge Tower"},
    "berserker": {"island": "Blackavar", "area": "Berserker Shrine"},
    "defender": {"island": "Sombre", "area": "Defender's Fort"},
    "knight": {"island": "Sombre", "area": "Knight's Keep"},
    "champion": {"island": "Sombre", "area": "Stronglight Castle"},
    
    # Martial Artist
    "martial_artist": {"island": "Gossamer", "area": "Dojo"},
    "dragon_master": {"island": "Oddworld", "area": "Dragon Temple"},
    
    # Weaver
    "weaver": {"island": "Gossamer", "area": "Weaver's Hut"},
    "high_priest": {"island": "Misty", "area": "High Temple"},
    
    # Unraveller
    "unraveller": {"island": "Darkcaverns", "area": "Unraveller's Pit"},
    
    # Elemental
    "elemental": {"island": "Emerald", "area": "Elemental Tower"},
    "nether_mage": {"island": "Darkcaverns", "area": "Nether Chamber"},
    
    # Evoker
    "evoker": {"island": "Gossamer", "area": "Evoker Tower"},
    "sorcerer": {"island": "Misty", "area": "Sorcerer's Spire"},
    
    # Necromancer
    "necromancer": {"island": "Darkcaverns", "area": "Necromancer's Lair"},
    "dark_lord": {"island": "Darkcaverns", "area": "Throne of Shadows"},
    
    # Psychics
    "psychics": {"island": "Hyboria", "area": "Psionic Academy"},
    
    # Acrobat
    "acrobat": {"island": "Gossamer", "area": "Circus Tent"},
    "ringmaster": {"island": "Oddworld", "area": "Big Top"},
    
    # Lurker
    "lurker": {"island": "Blackavar", "area": "Thieves' Den"},
    "shadow_master": {"island": "Misty", "area": "Shadow Hall"},
    
    # Druid
    "druid": {"island": "Gossamer", "area": "Druid Grove"},
    "archdruid": {"island": "Gossamer", "area": "Ancient Oak"},
    
    # Woodsman
    "woodsman": {"island": "Gossamer", "area": "Hunter's Lodge"},
    "forest_lord": {"island": "Everrest", "area": "Forest Heart"},
    
    # Shapeshifter
    "shapeshifter": {"island": "Gossamer", "area": "Ancient Forest"},
    "dragon_lord": {"island": "Darkcaverns", "area": "High Ledge On A Cliff"},
}

# =============================================================================
# GUILD CATEGORIES (for display)
# =============================================================================

GUILD_CATEGORIES = {
    "warrior": "Combat",
    "martial_artist": "Combat",
    "weaver": "Healing",
    "unraveller": "Dark",
    "elemental": "Magic",
    "evoker": "Magic",
    "necromancer": "Dark",
    "psychics": "Mental",
    "acrobat": "Utility",
    "lurker": "Stealth",
    "druid": "Nature",
    "woodsman": "Nature",
    "shapeshifter": "Transformation",
}

# =============================================================================
# GUILD DESCRIPTIONS
# =============================================================================

GUILD_DESCRIPTIONS = {
    "warrior": "Master of weapons and combat. The foundation of all fighting guilds.",
    "berserker": "Rage-fueled warrior dealing devastating damage at the cost of defense.",
    "defender": "Stalwart protector who shields allies and absorbs damage.",
    "knight": "Honorable warrior combining offense with divine protection.",
    "barbarian": "Untamed warrior wielding massive weapons with brutal force.",
    "blade_dancer": "Graceful fighter who turns combat into a deadly art form.",
    "flogger": "Whip-wielding specialist who dominates the battlefield.",
    "shield_master": "Ultimate defender who turns shields into weapons.",
    "thruster": "Spear specialist who strikes with precision and reach.",
    "champion": "The pinnacle of warrior training. A true master of combat.",
    "martial_artist": "Disciplined fighter using body and mind as weapons.",
    "dragonfist_fighter": "Martial artist channeling dragon energy into punches.",
    "mystic_warrior": "Warrior blending physical combat with mystical forces.",
    "crane_master": "Graceful master of the crane fighting style.",
    "snake_master": "Deceptive master of the snake fighting style.",
    "tiger_master": "Fierce master of the tiger fighting style.",
    "toad_master": "Resilient master of the toad fighting style.",
    "order_of_the_crescent_moon": "Elite martial artist order.",
    "dragon_master": "Ultimate martial artist who commands dragon power.",
    "weaver": "Healer who mends wounds and restores allies.",
    "confessor": "Healer who extracts truth and purifies souls.",
    "healer": "Master physician capable of curing any ailment.",
    "martyr": "Self-sacrificing healer who shields others with their life.",
    "avatar": "Living vessel of divine healing power.",
    "exorcist": "Healer who drives out corruption and evil.",
    "shields_of_faith": "Healer who manifests divine barriers.",
    "templar": "Holy warrior blending healing with combat.",
    "high_priest": "Supreme healer commanding the full power of faith.",
    "unraveller": "Dark mage who tears apart enemies with raw power.",
    "harmer": "Specialist in inflicting pain and suffering.",
    "magical_torturer": "Expert in magical agony and interrogation.",
    "sacrificer": "Dark mage who sacrifices life for power.",
    "servant_of_lloth": "Devoted to the spider queen.",
    "servant_of_mordulak": "Bound to the demon lord Mordulak.",
    "servant_of_shirija": "Follower of the death goddess Shirija.",
    "servant_of_talakh": "Worshipper of the chaos entity Talakh.",
    "elder": "Ancient unraveller commanding multiple dark powers.",
    "patriarch": "Male leader of the unraveller cult.",
    "primate": "Highest unraveller in the dark hierarchy.",
    "sword": "Unraveller who channels darkness through blades.",
    "elemental": "Mage commanding the four basic elements.",
    "air_mage": "Master of wind, lightning, and storms.",
    "earth_mage": "Master of stone, metal, and terrain.",
    "fire_mage": "Master of flames, heat, and combustion.",
    "water_mage": "Master of water, ice, and healing streams.",
    "lava_mage": "Master of fire and earth combined.",
    "mist_mage": "Master of air and water combined.",
    "nether_mage": "Master of the void between elements.",
    "evoker": "Mage who channels raw magical energy.",
    "evoker_of_elements": "Evoker specializing in elemental energy.",
    "evoker_of_ether": "Evoker specializing in pure magical force.",
    "acid_evoker": "Evoker of corrosive destruction.",
    "flames_evoker": "Evoker of burning devastation.",
    "force_evoker": "Evoker of kinetic impact.",
    "ice_evoker": "Evoker of freezing death.",
    "lightning_evoker": "Evoker of electric destruction.",
    "magic_evoker": "Evoker of pure arcane force.",
    "poison_evoker": "Evoker of toxic corruption.",
    "vacuum_evoker": "Evoker of void and pressure.",
    "sorcerer": "Master of all evocation paths.",
    "necromancer": "Mage commanding death and undeath.",
    "undead": "Necromancer specializing in zombie and skeleton armies.",
    "shadow": "Necromancer specializing in darkness and fear.",
    "death": "Necromancer specializing in direct death magic.",
    "lich": "Undead necromancer of terrible power.",
    "vampire_lord": "Master of blood and shadow.",
    "dark_lord": "Supreme necromancer commanding death itself.",
    "psychics": "Mentalist using mind powers.",
    "telepath": "Psychic who reads and manipulates thoughts.",
    "telekinetic": "Psychic who moves objects with mind alone.",
    "psionic": "Psychic who weaponizes mental energy.",
    "mentalist": "Psychic who controls minds completely.",
    "grandmaster": "Ultimate psychic of limitless mental power.",
    "acrobat": "Performer using agility and dexterity.",
    "juggler": "Acrobat specializing in throwing weapons.",
    "tightrope": "Acrobat specializing in balance and evasion.",
    "trapeze": "High-flying acrobat.",
    "fire_eater": "Acrobat who consumes and breathes fire.",
    "ringmaster": "Leader of the acrobat troupe.",
    "lurker": "Stealth specialist who hides in shadows.",
    "scout": "Lurker specializing in tracking and reconnaissance.",
    "thief": "Lurker specializing in theft and traps.",
    "assassin": "Master of silent, instant kills.",
    "rogue": "Jack of all stealth trades.",
    "shadow_master": "Ultimate lurker who is one with darkness.",
    "druid": "Nature mage commanding plants and animals.",
    "shaman": "Druid who communes with spirits.",
    "witch": "Druid who uses potions and curses.",
    "elder_druid": "Ancient druid of immense natural power.",
    "archdruid": "Supreme master of all nature.",
    "woodsman": "Expert in forests and tracking.",
    "ranger": "Woodsman specializing in ranged combat.",
    "tracker": "Woodsman specializing in finding anything.",
    "beast_master": "Master of animal companions.",
    "forest_lord": "Supreme woodsman commanding the wilderness.",
    "shapeshifter": "Mage who transforms into animal and dragon forms.",
    "animal_tamer": "Shapeshifter who befriends animals.",
    "bestial_seccedaneum": "Shapeshifter who commands beast power.",
    "savager": "Shapeshifter who fights with animal fury.",
    "animal_healer": "Shapeshifter who heals animals.",
    "animal_trainer": "Shapeshifter who trains animal companions.",
    "beast_lord": "Master of all beast forms.",
    "dragon_lord": "Ultimate shapeshifter commanding dragon forms.",
}

# =============================================================================
# ALPHA GUILD LIST (Base guilds you can join first)
# =============================================================================

ALPHA_GUILDS = [
    "warrior", "martial_artist", "weaver", "unraveller",
    "elemental", "evoker", "necromancer", "psychics",
    "acrobat", "lurker", "druid", "woodsman", "shapeshifter"
]
