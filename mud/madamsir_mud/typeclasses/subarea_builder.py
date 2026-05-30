#!/usr/bin/env python3
"""
Red Dragon MUD — Detailed Sub-Area Builder
==========================================
Builds the Hall of Races, Adventurer's Guild, and key detailed sub-areas
beyond the hub+entrance approach of the main world builder.

Usage (in Evennia):
  @py from typeclasses.subarea_builder import build_subareas; build_subareas()
"""

from evennia import create_object, search_object
from typeclasses.rooms import Room
from typeclasses.exits import Exit


def get_or_create_room(key, aliases=None, typeclass=None, **kwargs):
    """Get existing room or create new one."""
    existing = search_object(key, typeclass=typeclass or "typeclasses.rooms.Room")
    if existing:
        room = existing[0]
        if aliases:
            for a in aliases:
                room.aliases.add(a)
        return room
    
    room = create_object(typeclass or Room, key=key, **kwargs)
    if aliases:
        for a in aliases:
            room.aliases.add(a)
    return room


def create_exit(from_room, to_room, name, aliases=None):
    """Create a one-way exit. Creates bidirectional if needed."""
    exit_obj = create_object(Exit, key=name, location=from_room, destination=to_room)
    if aliases:
        for a in aliases:
            exit_obj.aliases.add(a)
    return exit_obj


def create_bidirectional_exit(room_a, room_b, name_a, name_b, aliases_a=None, aliases_b=None):
    """Create exits in both directions."""
    create_exit(room_a, room_b, name_a, aliases_a)
    create_exit(room_b, room_a, name_b, aliases_b)


def build_subareas():
    """Build all detailed sub-areas."""
    import evennia
    evennia._init()
    
    print("=" * 60)
    print("RED DRAGON MUD — Sub-Area Builder")
    print("=" * 60)
    
    # ── 1. HALL OF RACES ──
    print("\n🏛  Hall of Races")
    hall = get_or_create_room(
        "Hall of Races",
        aliases=["hall", "races", "chargen"],
        attributes=[
            ("island", "chargen"),
            ("level_range", (1, 1)),
            ("climate", "ethereal"),
            ("dangers", "none"),
            ("rest_area", True),
        ]
    )
    hall.db.desc = (
        "|cHall of Races|n\n\n"
        "This is the Hall of Races in the space outside the world. The only way out of\n"
        "this void is to select the race you wish to represent in the world of Islands\n"
        "of Myth. In this hall, every race has a statue, and you feel that you can do\n"
        "these things:\n"
        "|c-------------------------------------------------------------------------|n\n"
        "      |gTYPE THIS|n    |y:|n |gTO RECEIVE|n\n"
        "|c-------------------------------------------------------------------------|n\n"
        "      |yall races|n    — To get a list of available races\n"
        "      |ytouch <race>|n — To touch the statue of <race> and roll your stats\n"
        "      |yla <race>|n    — To examine <race>'s statue and learn more info\n"
        "      |yread poster|n  — To see which races are best for which guilds\n"
        "      |yread sign|n   — You're lost and need additional help\n"
        "|c-------------------------------------------------------------------------|n\n"
        "An interesting looking poster.\n\n"
        "An important sign stands here.\n"
    )
    print("  ✓ Hall of Races created/updated")
    
    # ── 2. ADVENTURER'S GUILD OF ILLIUM ──
    print("\n⚔  Adventurer's Guild of Illium")
    adv_guild = get_or_create_room(
        "Adventurer's Guild of Illium",
        aliases=["adventurer guild", "guild", "illium guild"],
        attributes=[
            ("island", "gossamer"),
            ("area", "Illium City"),
            ("level_range", (1, 20)),
            ("climate", "temperate"),
            ("dangers", "low"),
            ("rest_area", True),
        ]
    )
    adv_guild.db.desc = (
        "|cThe Adventurer's Guild of Illium|n\n\n"
        "A warm, well-lit hall filled with the buzz of conversation and\n"
        "the clink of gold coins. Notice boards cover every wall, covered\n"
        "in quests, bounties, and desperate pleas for help.\n\n"
        "A |ychubby clerk|n sits behind a desk, ready to assist new adventurers.\n"
        "A |ystaircase|n leads up to the guildmasters' chambers.\n\n"
        "|gAvailable exits:|n\n"
        "  |ynorth|n  — Illium City Central Square\n"
        "  |ywest|n   — The Training Grounds\n"
        "  |yeast|n   — Guild Shops\n"
    )
    print("  ✓ Adventurer's Guild created/updated")
    
    # ── 3. STARTING ROOM (before Hall of Races) ──
    print("\n🏠  New Player Starting Room")
    start_room = get_or_create_room(
        "Welcome Room",
        aliases=["start", "welcome"],
        attributes=[
            ("island", "chargen"),
            ("level_range", (1, 1)),
            ("climate", "ethereal"),
            ("dangers", "none"),
            ("rest_area", True),
        ]
    )
    start_room.db.desc = (
        "|cWelcome to Islands of Myth!|n\n\n"
        "This is the starting room. In this room are 2 exits: |yrace-select|n, and |ytour|n.\n\n"
        "If you are new to mudding, or new to Islands of Myth, and wish to take the tour\n"
        "please type |ytour|n. This will take approximately 15-30 minutes, but is well\n"
        "worth the time, particularly if you have not played this type of mud\n"
        "before. It will guide you through character creation, as well as choosing\n"
        "a guild.\n\n"
        "If you have played here, or another mud before, you may type |yrace-select|n to go\n"
        "right to the character creation process.\n"
    )
    print("  ✓ Welcome Room created")
    
    # ── 4. CONNECT STARTING ROOM ↔ HALL OF RACES (IOM-style) ──
    print("\n🌀  Connecting Welcome Room ↔ Hall of Races")
    create_bidirectional_exit(
        start_room, hall,
        "north", "south",
        aliases_a=["race-select", "races"], aliases_b=["welcome", "start"]
    )
    print("  ✓ Welcome Room ↔ Hall of Races connected")
    # ── 4. ILLIUM CITY CENTRAL SQUARE ──
    print("\n🏙  Illium City Central Square")
    central = get_or_create_room(
        "Illium City — Central Square",
        aliases=["central square", "square", "illium center"],
        attributes=[
            ("island", "gossamer"),
            ("area", "Illium City"),
            ("level_range", (1, 20)),
            ("climate", "temperate"),
            ("dangers", "low"),
            ("rest_area", True),
        ]
    )
    central.db.desc = (
        "|cIllium City — Central Square|n\n\n"
        "The bustling heart of Illium, where merchants hawk their wares,\n"
        "bards play for coin, and adventurers gather before venturing forth.\n"
        "A grand fountain in the center depicts a dragon coiled around the world.\n\n"
        "|gNotable locations:|n\n"
        "  |ynorth|n  — The Fiery Flagon (tavern)\n"
        "  |ysouth|n  — City Gates\n"
        "  |yeast|n   — Market District\n"
        "  |ywest|n   — Residential Quarter\n"
        "  |ydown|n   — Sewers (dangerous)\n"
    )
    print("  ✓ Central Square created/updated")
    
    # ── 5. CONNECT KEY LOCATIONS ──
    print("\n🔗  Connecting key locations")
    
    # Guild ↔ Central Square
    create_bidirectional_exit(
        adv_guild, central,
        "north", "south",
        aliases_a=["square", "out"], aliases_b=["guild", "adventurer guild"]
    )
    print("  ✓ Guild ↔ Central Square")
    
    # ── 6. FIERY FLAGON TAVERN ──
    print("\n🍺  Fiery Flagon Tavern")
    tavern = get_or_create_room(
        "The Fiery Flagon",
        aliases=["tavern", "flagon", "fiery flagon"],
        attributes=[
            ("island", "gossamer"),
            ("area", "Illium City"),
            ("level_range", (1, 20)),
            ("climate", "temperate"),
            ("dangers", "low"),
            ("rest_area", True),
            ("shop_type", "tavern"),
        ]
    )
    tavern.db.desc = (
        "|cThe Fiery Flagon|n\n\n"
        "A cozy tavern that smells of ale, roasted meat, and adventurer sweat.\n"
        "The barkeep, a burly dwarf named |yThorin|n, wipes mugs and eyes newcomers.\n"
        "A bard in the corner plays a mournful tune on a lute.\n\n"
        "|gAvailable exits:|n\n"
        "  |ysouth|n  — Central Square\n"
        "  |yup|n     — Private Rooms (rentable)\n"
    )
    create_bidirectional_exit(
        central, tavern,
        "north", "south",
        aliases_a=["tavern"], aliases_b=["square"]
    )
    print("  ✓ Fiery Flagon connected")
    
    # ── 7. ILLIUM CITY BANK ──
    print("\n🏦  Illium City Bank")
    bank = get_or_create_room(
        "Illium City Bank",
        aliases=["bank", "illium bank"],
        attributes=[
            ("island", "gossamer"),
            ("area", "Illium City"),
            ("level_range", (1, 20)),
            ("climate", "temperate"),
            ("dangers", "low"),
            ("rest_area", True),
            ("shop_type", "bank"),
        ]
    )
    bank.db.desc = (
        "|cIllium City Bank|n\n\n"
        "A grand marble building with iron bars on every window.\n"
        "A |ysterling golem|n stands guard, its eyes glowing with magical wards.\n"
        "Behind the counter, a |ygoblin banker|n counts coins with manic speed.\n\n"
        "|yServices:|n deposit, withdraw, balance, transfer\n\n"
        "|gAvailable exits:|n\n"
        "  |yeast|n  — Market District\n"
    )
    create_bidirectional_exit(
        central, bank,
        "west", "east",
        aliases_a=["bank", "west"], aliases_b=["square"]
    )
    print("  ✓ Bank connected")
    
    # ── 8. TRAINING GROUNDS ──
    print("\n🎯  Training Grounds")
    training = get_or_create_room(
        "Training Grounds",
        aliases=["training", "practice", "grounds"],
        attributes=[
            ("island", "gossamer"),
            ("area", "Illium City"),
            ("level_range", (1, 20)),
            ("climate", "temperate"),
            ("dangers", "low"),
            ("rest_area", False),
        ]
    )
    training.db.desc = (
        "|cTraining Grounds|n\n\n"
        "A wide sand pit surrounded by wooden dummies and target stands.\n"
        "The clashing of steel and the thud of practice arrows fills the air.\n"
        "A |yweathered veteran|n watches trainees, shouting corrections.\n\n"
        "|gAvailable exits:|n\n"
        "  |yeast|n  — Adventurer's Guild\n"
        "  |ysouth|n — Sparring Arena\n"
    )
    create_bidirectional_exit(
        adv_guild, training,
        "west", "east",
        aliases_a=["training", "grounds"], aliases_b=["guild"]
    )
    print("  ✓ Training Grounds connected")
    
    # ── 9. CITY GATES ──
    print("\n🚪  City Gates")
    gates = get_or_create_room(
        "Illium City Gates",
        aliases=["gates", "city gates", "exit"],
        attributes=[
            ("island", "gossamer"),
            ("area", "Illium City"),
            ("level_range", (1, 20)),
            ("climate", "temperate"),
            ("dangers", "moderate"),
            ("rest_area", False),
        ]
    )
    gates.db.desc = (
        "|cIllium City Gates|n\n\n"
        "Massive iron gates that have stood for centuries, guarding the city\n"
        "from the wilderness beyond. Two |ycity guards|n watch everyone who passes.\n"
        "Beyond the gates, the road splits toward different regions of Gossamer.\n\n"
        "|gAvailable exits:|n\n"
        "  |ynorth|n  — Central Square\n"
        "  |yeast|n   — Eastern Road (to Sandy Beach)\n"
        "  |ysouth|n  — Southern Road (to Ghastly Swamp)\n"
        "  |ywest|n   — Western Road (to Badlands)\n"
    )
    create_bidirectional_exit(
        central, gates,
        "south", "north",
        aliases_a=["gates", "exit"], aliases_b=["square"]
    )
    print("  ✓ City Gates connected")
    
    # ── 10. WILDERNESS CONNECTIONS FROM GATES ──
    print("\n🌲  Wilderness connections")
    
    # Sandy Beach
    beach = get_or_create_room(
        "Sandy Beach",
        aliases=["beach", "shore", "sandy"],
        attributes=[
            ("island", "gossamer"),
            ("area", "Wilderness"),
            ("level_range", (1, 10)),
            ("climate", "coastal"),
            ("dangers", "low"),
            ("rest_area", False),
        ]
    )
    beach.db.desc = (
        "|cSandy Beach|n\n\n"
        "Golden sand stretches along the coastline, lapped by gentle waves.\n"
        "Seagulls cry overhead. A few |ycrabs|n scuttle along the waterline.\n\n"
        "|gAvailable exits:|n\n"
        "  |ywest|n  — City Gates\n"
        "  |yeast|n  — Rocky Coastline\n"
    )
    create_bidirectional_exit(
        gates, beach,
        "east", "west",
        aliases_a=["beach"], aliases_b=["gates"]
    )
    print("  ✓ Sandy Beach connected")
    
    # Ghastly Swamp
    swamp = get_or_create_room(
        "Ghastly Swamp",
        aliases=["swamp", "ghastly", "bog"],
        attributes=[
            ("island", "gossamer"),
            ("area", "Wilderness"),
            ("level_range", (5, 15)),
            ("climate", "humid"),
            ("dangers", "moderate"),
            ("rest_area", False),
        ]
    )
    swamp.db.desc = (
        "|cGhastly Swamp|n\n\n"
        "Thick mist coils between twisted trees and stagnant pools.\n"
        "The air smells of decay. Strange |yeyes|n watch from the darkness.\n\n"
        "|gAvailable exits:|n\n"
        "  |ynorth|n — City Gates\n"
        "  |ydown|n  — Deeper Swamp (dangerous)\n"
    )
    create_bidirectional_exit(
        gates, swamp,
        "south", "north",
        aliases_a=["swamp"], aliases_b=["gates"]
    )
    print("  ✓ Ghastly Swamp connected")
    
    # Badlands
    badlands = get_or_create_room(
        "The Badlands",
        aliases=["badlands", "wasteland", "desert"],
        attributes=[
            ("island", "gossamer"),
            ("area", "Wilderness"),
            ("level_range", (5, 15)),
            ("climate", "arid"),
            ("dangers", "moderate"),
            ("rest_area", False),
        ]
    )
    badlands.db.desc = (
        "|cThe Badlands|n\n\n"
        "A harsh, rocky landscape where little grows. The sun beats down mercilessly.\n"
        "Vultures circle overhead. |yBandits|n are rumored to hide in the canyons.\n\n"
        "|gAvailable exits:|n\n"
        "  |yeast|n  — City Gates\n"
        "  |ysouth|n — Canyon Depths\n"
    )
    create_bidirectional_exit(
        gates, badlands,
        "west", "east",
        aliases_a=["badlands"], aliases_b=["gates"]
    )
    print("  ✓ Badlands connected")
    
    # ── 11. FOREST AND PLAINS ──
    print("\n🌳  Forest and Plains")
    
    forest = get_or_create_room(
        "Gossamer Forest",
        aliases=["forest", "woods", "trees"],
        attributes=[
            ("island", "gossamer"),
            ("area", "Wilderness"),
            ("level_range", (3, 12)),
            ("climate", "temperate"),
            ("dangers", "low-moderate"),
            ("rest_area", False),
        ]
    )
    forest.db.desc = (
        "|cGossamer Forest|n\n\n"
        "Tall oaks and pines form a dense canopy overhead. Sunlight filters\n"
        "through in golden shafts. |yForest creatures|n rustle in the undergrowth.\n\n"
        "|gAvailable exits:|n\n"
        "  |ysouth|n — Rocky Coastline\n"
        "  |ywest|n  — Open Plains\n"
    )
    print("  ✓ Forest created")
    
    plains = get_or_create_room(
        "Open Plains",
        aliases=["plains", "grasslands", "field"],
        attributes=[
            ("island", "gossamer"),
            ("area", "Wilderness"),
            ("level_range", (2, 10)),
            ("climate", "temperate"),
            ("dangers", "low"),
            ("rest_area", False),
        ]
    )
    plains.db.desc = (
        "|cOpen Plains|n\n\n"
        "Endless grasslands stretch to the horizon. Wildflowers sway in the breeze.\n"
        "A herd of |ywild horses|n gallops in the distance.\n\n"
        "|gAvailable exits:|n\n"
        "  |yeast|n  — Forest\n"
        "  |ysouth|n — Badlands\n"
    )
    print("  ✓ Plains created")
    
    # Connect wilderness internally
    create_bidirectional_exit(
        beach, forest,
        "south", "north",
        aliases_a=["forest"], aliases_b=["beach"]
    )
    create_bidirectional_exit(
        forest, plains,
        "west", "east",
        aliases_a=["plains"], aliases_b=["forest"]
    )
    create_bidirectional_exit(
        plains, badlands,
        "south", "north",
        aliases_a=["badlands"], aliases_b=["plains"]
    )
    print("  ✓ Wilderness internally connected")
    
    # ── ADDITIONAL CITY LOCATIONS ──
    print("\n🏙  Additional City Locations")
    
    # Market District
    market = get_or_create_room(
        "Market District",
        aliases=["market", "bazaar", "shops"],
        attributes=[
            ("island", "gossamer"),
            ("area", "Illium City"),
            ("level_range", (1, 20)),
            ("climate", "temperate"),
            ("dangers", "low"),
            ("rest_area", False),
        ]
    )
    market.db.desc = (
        "|cMarket District|n\n\n"
        "A bustling marketplace where merchants from across the Twelve Islands\n"
        "display their wares. The air is thick with the smell of spices, leather,\n"
        "and fresh baked bread.\n\n"
        "|gAvailable exits:|n\n"
        "  |ywest|n  — Central Square\n"
        "  |ynorth|n — Weapon Smith\n"
        "  |yeast|n  — Armor Shop\n"
        "  |ysouth|n — General Store\n"
    )
    create_bidirectional_exit(
        central, market,
        "east", "west",
        aliases_a=["market"], aliases_b=["square"]
    )
    print("  ✓ Market District")
    
    # Weapon Smith
    weapon_shop = get_or_create_room(
        "Weapon Smith",
        aliases=["weapons", "smith", "sword"],
        attributes=[
            ("island", "gossamer"),
            ("area", "Illium City"),
            ("level_range", (1, 20)),
            ("climate", "temperate"),
            ("dangers", "low"),
            ("rest_area", False),
            ("shop_type", "weapon"),
        ]
    )
    weapon_shop.db.desc = (
        "|cThe Weapon Smith|n\n\n"
        "A forge burns brightly at the back of the shop. The smith, a burly\n"
        "dwarf with soot-stained arms, hammers away at a glowing blade.\n"
        "Racks of swords, axes, and spears line the walls.\n\n"
        "|yWeapons for sale: sword (50g), axe (45g), spear (40g), dagger (25g)|n\n"
        "|gAvailable exits:|n\n"
        "  |ysouth|n — Market District\n"
    )
    create_bidirectional_exit(
        market, weapon_shop,
        "north", "south",
        aliases_a=["smith"], aliases_b=["market"]
    )
    print("  ✓ Weapon Smith")
    
    # Armor Shop
    armor_shop = get_or_create_room(
        "Armor Shop",
        aliases=["armor", "armour", "plate"],
        attributes=[
            ("island", "gossamer"),
            ("area", "Illium City"),
            ("level_range", (1, 20)),
            ("climate", "temperate"),
            ("dangers", "low"),
            ("rest_area", False),
            ("shop_type", "armor"),
        ]
    )
    armor_shop.db.desc = (
        "|cThe Armor Shop|n\n\n"
        "Mannequins display various suits of armor: leather, chainmail, and plate.\n"
        "A |ygoblin armorer|n measures a customer for a custom fit.\n\n"
        "|yArmor for sale: leather (30g), chainmail (80g), plate (150g), shield (40g)|n\n"
        "|gAvailable exits:|n\n"
        "  |ywest|n — Market District\n"
    )
    create_bidirectional_exit(
        market, armor_shop,
        "east", "west",
        aliases_a=["armor"], aliases_b=["market"]
    )
    print("  ✓ Armor Shop")
    
    # General Store
    general_store = get_or_create_room(
        "General Store",
        aliases=["store", "general", "supplies"],
        attributes=[
            ("island", "gossamer"),
            ("area", "Illium City"),
            ("level_range", (1, 20)),
            ("climate", "temperate"),
            ("dangers", "low"),
            ("rest_area", False),
            ("shop_type", "general"),
        ]
    )
    general_store.db.desc = (
        "|cGeneral Store|n\n\n"
        "Shelves groan under the weight of supplies: rope, torches, rations,\n"
        "waterskins, and healing potions. The shopkeeper, a |yhalfling|n,\n"
        "greets you with a smile.\n\n"
        "|ySupplies: torch (2g), ration (5g), potion (25g), rope (10g)|n\n"
        "|gAvailable exits:|n\n"
        "  |ynorth|n — Market District\n"
    )
    create_bidirectional_exit(
        market, general_store,
        "south", "north",
        aliases_a=["store"], aliases_b=["market"]
    )
    print("  ✓ General Store")
    
    # Residential Quarter
    residential = get_or_create_room(
        "Residential Quarter",
        aliases=["residential", "homes", "housing"],
        attributes=[
            ("island", "gossamer"),
            ("area", "Illium City"),
            ("level_range", (1, 20)),
            ("climate", "temperate"),
            ("dangers", "low"),
            ("rest_area", True),
        ]
    )
    residential.db.desc = (
        "|cResidential Quarter|n\n\n"
        "Quiet cobblestone streets lined with modest homes. Children play\n"
        "in the alleys while old folks sit on porches, watching the world go by.\n"
        "The smell of cooking drifts from open windows.\n\n"
        "|gAvailable exits:|n\n"
        "  |yeast|n  — Central Square\n"
        "  |ysouth|n — City Park\n"
    )
    create_bidirectional_exit(
        central, residential,
        "west", "east",
        aliases_a=["residential", "homes"], aliases_b=["square"]
    )
    print("  ✓ Residential Quarter")
    
    # City Park
    park = get_or_create_room(
        "City Park",
        aliases=["park", "gardens"],
        attributes=[
            ("island", "gossamer"),
            ("area", "Illium City"),
            ("level_range", (1, 20)),
            ("climate", "temperate"),
            ("dangers", "low"),
            ("rest_area", True),
        ]
    )
    park.db.desc = (
        "|cCity Park|n\n\n"
        "A peaceful green space in the heart of Illium. Flower beds burst\n"
        "with color, and a small pond reflects the sky. Benches offer rest\n"
        "for weary travelers. A |ywise old druid|n tends the gardens.\n\n"
        "|gAvailable exits:|n\n"
        "  |ynorth|n — Residential Quarter\n"
        "  |yeast|n  — Training Grounds\n"
    )
    create_bidirectional_exit(
        residential, park,
        "south", "north",
        aliases_a=["park"], aliases_b=["residential"]
    )
    create_bidirectional_exit(
        training, park,
        "south", "west",
        aliases_a=["park"], aliases_b=["training"]
    )
    print("  ✓ City Park")
    
    # ── DEEPER WILDERNESS ──
    print("\n🌲  Deeper Wilderness")
    
    # Rocky Coastline
    coastline = get_or_create_room(
        "Rocky Coastline",
        aliases=["coastline", "rocks", "cliffs"],
        attributes=[
            ("island", "gossamer"),
            ("area", "Wilderness"),
            ("level_range", (3, 12)),
            ("climate", "coastal"),
            ("dangers", "moderate"),
            ("rest_area", False),
        ]
    )
    coastline.db.desc = (
        "|cRocky Coastline|n\n\n"
        "Jagged rocks jut from the surf, making footing treacherous.\n"
        "|ySeals|n bask on the flat stones, watching you with curious eyes.\n"
        "The tide pools contain strange sea creatures.\n\n"
        "|gAvailable exits:|n\n"
        "  |ywest|n  — Sandy Beach\n"
        "  |yeast|n  — Shipwreck Cove\n"
        "  |ysouth|n — Gossamer Forest\n"
    )
    create_bidirectional_exit(
        beach, coastline,
        "east", "west",
        aliases_a=["coastline"], aliases_b=["beach"]
    )
    print("  ✓ Rocky Coastline")
    
    # Deeper Swamp
    deep_swamp = get_or_create_room(
        "Deeper Swamp",
        aliases=["deep swamp", "bog depths", "murk"],
        attributes=[
            ("island", "gossamer"),
            ("area", "Wilderness"),
            ("level_range", (8, 18)),
            ("climate", "humid"),
            ("dangers", "high"),
            ("rest_area", False),
        ]
    )
    deep_swamp.db.desc = (
        "|cDeeper Swamp|n\n\n"
        "The mist thickens into a suffocating fog. Ancient trees twist\n"
        "like screaming figures half-submerged in black water.\n"
        "|yGlowing eyes|n watch from the murk. The air reeks of decay.\n\n"
        "|rWarning: High-level monsters inhabit this area.|n\n"
        "|gAvailable exits:|n\n"
        "  |ynorth|n — Ghastly Swamp\n"
        "  |ydown|n  — Swamp Caverns (very dangerous)\n"
    )
    create_bidirectional_exit(
        swamp, deep_swamp,
        "down", "up",
        aliases_a=["deep"], aliases_b=["swamp"]
    )
    print("  ✓ Deeper Swamp")
    
    # Canyon Depths
    canyon = get_or_create_room(
        "Canyon Depths",
        aliases=["canyon", "depths", "ravine"],
        attributes=[
            ("island", "gossamer"),
            ("area", "Wilderness"),
            ("level_range", (8, 18)),
            ("climate", "arid"),
            ("dangers", "high"),
            ("rest_area", False),
        ]
    )
    canyon.db.desc = (
        "|cCanyon Depths|n\n\n"
        "Sheer rock walls rise on either side, casting the canyon floor\n"
        "in perpetual shadow. The bones of ancient beasts litter the sand.\n"
        "|yScavengers|n circle overhead, waiting for the weak to falter.\n\n"
        "|rWarning: High-level monsters inhabit this area.|n\n"
        "|gAvailable exits:|n\n"
        "  |ynorth|n — The Badlands\n"
        "  |ywest|n  — Bandit Camp\n"
    )
    create_bidirectional_exit(
        badlands, canyon,
        "south", "north",
        aliases_a=["canyon"], aliases_b=["badlands"]
    )
    print("  ✓ Canyon Depths")
    
    # Shipwreck Cove
    shipwreck = get_or_create_room(
        "Shipwreck Cove",
        aliases=["shipwreck", "cove", "wreck"],
        attributes=[
            ("island", "gossamer"),
            ("area", "Wilderness"),
            ("level_range", (5, 15)),
            ("climate", "coastal"),
            ("dangers", "moderate"),
            ("rest_area", False),
        ]
    )
    shipwreck.db.desc = (
        "|cShipwreck Cove|n\n\n"
        "The splintered remains of a great galleon rest half-submerged\n"
        "in the shallows. |yTreasure hunters|n have picked it clean, but\n"
        "rumor says the captain's cabin still holds secrets.\n\n"
        "|gAvailable exits:|n\n"
        "  |ywest|n  — Rocky Coastline\n"
        "  |ysouth|n — Sunken Ruins (underwater)\n"
    )
    create_bidirectional_exit(
        coastline, shipwreck,
        "east", "west",
        aliases_a=["shipwreck", "cove"], aliases_b=["coastline"]
    )
    print("  ✓ Shipwreck Cove")
    
    # Sparring Arena
    arena = get_or_create_room(
        "Sparring Arena",
        aliases=["arena", "sparring", "fight"],
        attributes=[
            ("island", "gossamer"),
            ("area", "Illium City"),
            ("level_range", (1, 20)),
            ("climate", "temperate"),
            ("dangers", "low"),
            ("rest_area", False),
        ]
    )
    arena.db.desc = (
        "|cSparring Arena|n\n\n"
        "A circular sand pit surrounded by wooden bleachers. Fighters\n"
        "spar here without risk of death — magical wards prevent fatal blows.\n"
        "A |ytournament board|n lists upcoming matches.\n\n"
        "|gAvailable exits:|n\n"
        "  |ynorth|n — Training Grounds\n"
    )
    create_bidirectional_exit(
        training, arena,
        "south", "north",
        aliases_a=["arena"], aliases_b=["training"]
    )
    print("  ✓ Sparring Arena")
    
    # ── HALL OF RACES → WORLD EXIT ──
    print("\n🌀  Hall of Races → World connection")
    create_bidirectional_exit(
        hall, adv_guild,
        "north", "south",
        aliases_a=["world", "guild"], aliases_b=["hall", "races"]
    )
    print("  ✓ Hall of Races ↔ Adventurer's Guild (north/south)")

    # ── SUMMARY ──
    print("\n" + "=" * 60)
    print("Sub-Area Build Complete!")
    print("=" * 60)
    print("  Hall of Races          → chargen spawn point")
    print("  Adventurer's Guild     → guild hub, rest area")
    print("  Central Square         → city hub")
    print("  Fiery Flagon           → tavern, rest area")
    print("  Illium City Bank       → banking services")
    print("  Training Grounds       → practice area")
    print("  City Gates             → wilderness access")
    print("  Sandy Beach            → coastal (Lv 1-10)")
    print("  Ghastly Swamp          → swamp (Lv 5-15)")
    print("  Badlands               → arid (Lv 5-15)")
    print("  Gossamer Forest        → forest (Lv 3-12)")
    print("  Open Plains            → grasslands (Lv 2-10)")
    print("=" * 60)


if __name__ == "__main__":
    build_subareas()
