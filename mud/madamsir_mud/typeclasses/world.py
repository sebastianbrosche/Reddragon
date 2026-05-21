#!/usr/bin/env python3
"""
Red Dragon MUD — World Builder
==============================
Creates the 11 islands and their key areas based on Islands of Myth content.
"""

from evennia import create_object
from typeclasses.rooms import Room
from typeclasses.exits import Exit

ISLANDS = {
    "blackavar": {
        "desc": "A dark, forested island shrouded in perpetual twilight. The elves of Blackavar guard ancient secrets beneath their ancient trees.",
        "key_areas": ["Queen Vrille's Court", "Castle Goodwin", "Elven Forest", "Wandering Ghost Woods"],
        "level_range": (20, 50),
        "climate": "temperate",
        "dangers": ["cursed undead", "elven sentinels", "shadow beasts"],
    },
    "gossamer": {
        "desc": "A delicate island of floating gardens and crystalline structures. Reality feels thin here, as if the world itself were spun from silk.",
        "key_areas": ["Floating Gardens", "Crystal Spires", "Silk Weaver's Loom"],
        "level_range": (30, 70),
        "climate": "ethereal",
        "dangers": ["silk spiders", "reality tears", "mirror doppelgangers"],
    },
    "sombre": {
        "desc": "A grey, rainswept island where the sun never shines. Its people are as dour as the weather, but their secrets are worth the gloom.",
        "key_areas": ["Grey Harbor", "Rainwashed Catacombs", "Sombre Keep"],
        "level_range": (15, 45),
        "climate": "cold_wet",
        "dangers": ["drowned spirits", "grey wolves", "melancholy specters"],
    },
    "darkcaverns": {
        "desc": "Not an island but an underworld — vast caverns beneath the islands where orcs, gnolls, and darker things dwell in eternal night.",
        "key_areas": ["Orc Castle", "The Pales", "Gnoll Warrens", "Main Path"],
        "level_range": (25, 80),
        "climate": "underground",
        "dangers": ["orc warbands", "gnoll packs", "cave trolls", "shadow demons"],
    },
    "hyboria": {
        "desc": "A savage land of jungles and prehistoric beasts. The cave people of Hyboria worship ancient spirits and guard powerful artifacts.",
        "key_areas": ["Tarantia", "Prehistoric Caves", "Lothlorien Forest", "Aquilonia Library"],
        "level_range": (10, 60),
        "climate": "tropical",
        "dangers": ["sabretooth cats", "cave bears", "cannibal tribes"],
    },
    "southcape": {
        "desc": "The southernmost tip of civilization, where trade winds meet pirate coves. A bustling port with a dangerous underbelly.",
        "key_areas": ["Southcape Docks", "Pirate Cove", "Merchant Quarter", "Sewers"],
        "level_range": (5, 40),
        "climate": "warm",
        "dangers": ["pirates", "smugglers", "drowned sailors"],
    },
    "emerald": {
        "desc": "A lush green island covered in emerald forests and haunted by the hag who rules its heart. Ancient magic lingers in every glade.",
        "key_areas": ["Emerald Forest", "The Hag's Hut", "Old Man's Cottage"],
        "level_range": (20, 55),
        "climate": "temperate",
        "dangers": ["the hag", "forest wraiths", "thorn walkers"],
    },
    "mists": {
        "desc": "An island perpetually shrouded in fog. Sslaath the demonologist makes his home here, and the plague-ravaged world of Uforia bleeds through.",
        "key_areas": ["Mist Shores", "Sslaath's Tower", "Uforia Gates", "Mermaid Waters"],
        "level_range": (30, 75),
        "climate": "misty",
        "dangers": ["demonologists", "plague zombies", "mist serpents"],
    },
    "twin_islands": {
        "desc": "Two islands joined by a narrow bridge. The north has a crumbling lighthouse; the south hosts Lord Jesrael's demon army.",
        "key_areas": ["North Lighthouse", "South Twin Docks", "Lord Jesrael's Fortress", "Safari Camp"],
        "level_range": (15, 50),
        "climate": "temperate",
        "dangers": ["demon army", "shipwrecks", "lion prides"],
    },
    "everrest": {
        "desc": "A frozen peak rising from the sea, home to Chilperic the Biomancer and Breeder Bob's exotic menagerie. Dangerous at any level.",
        "key_areas": ["Chilperic's Menagerie", "Breeder Bob's Caves", "Frozen Summit", "Dangerous Castle"],
        "level_range": (25, 80),
        "climate": "frozen",
        "dangers": ["biomantic horrors", "exotic beasts", "ice wraiths"],
    },
    "oddworld": {
        "desc": "A strange, alien island where nothing works as it should. The ancient burial grounds below host a war that has raged for centuries.",
        "key_areas": ["Anker Village", "Ancient Burial Ground", "The Dig", "Oddworld Caverns"],
        "level_range": (20, 70),
        "climate": "alien",
        "dangers": ["undead armies", "reality distortions", "alien parasites"],
    },
}

CITY_OF_ILLIUM = {
    "desc": "The great city of Illium, heart of civilization. Here adventurers gather, guilds recruit, and the Adventurer's Guild welcomes all.",
    "key_areas": [
        "Adventurer Guild Entrance",
        "Newbie Garden",
        "Newbie Valley",
        "Free Equipment Machine",
        "Toy Shop",
        "Heavenly Smiles Hotel",
        "The Fountain",
        "Valmoria District",
        "Nuvo City",
        "Hefnoin",
    ],
    "services": [
        "bank", "healer", "shop", "guild_master", "inn", "trainer", "lodestone_merchant"
    ],
}


def build_world(caller=None):
    """Build the entire world — islands, cities, and connections."""
    
    # Create Illium (central hub)
    illium = create_object(Room, key="Illium City", 
                           attributes={"desc": CITY_OF_ILLIUM["desc"]})
    illium.db.island = "illium"
    illium.db.level_range = (1, 10)
    
    # Create sub-rooms in Illium
    illium_areas = {}
    for area in CITY_OF_ILLIUM["key_areas"]:
        room = create_object(Room, key=area, location=illium)
        room.db.island = "illium"
        illium_areas[area] = room
    
    # Create islands and their dock areas
    islands = {}
    for island_key, data in ISLANDS.items():
        # Dock room
        dock = create_object(Room, key=f"{island_key.title()} Docks",
                             attributes={"desc": f"The docks of {island_key.title()}. {data['desc'][:100]}..."})
        dock.db.island = island_key
        dock.db.level_range = data["level_range"]
        dock.db.climate = data["climate"]
        dock.db.dangers = data["dangers"]
        
        # Key areas
        areas = {}
        for area in data["key_areas"]:
            room = create_object(Room, key=f"{area} ({island_key.title()})",
                                 location=dock)
            room.db.island = island_key
            room.db.level_range = data["level_range"]
            areas[area] = room
        
        islands[island_key] = {"dock": dock, "areas": areas}
    
    # Create connections from Illium to each island dock
    for island_key, data in islands.items():
        dock = data["dock"]
        # Create exits both ways
        exit_to = create_object(Exit, key=f"sail to {island_key}",
                               location=illium, destination=dock)
        exit_back = create_object(Exit, key=f"sail to illium",
                                  location=dock, destination=illium)
    
    # Create inter-island connections where logical
    connections = [
        ("twin_islands", "mists", "bridge"),
        ("darkcaverns", "hyboria", "hidden tunnel"),
        ("emerald", "blackavar", "forest path"),
        ("southcape", "twin_islands", "coastal route"),
    ]
    
    for from_key, to_key, route_name in connections:
        if from_key in islands and to_key in islands:
            from_dock = islands[from_key]["dock"]
            to_dock = islands[to_key]["dock"]
            create_object(Exit, key=route_name, location=from_dock, destination=to_dock)
            create_object(Exit, key=f"return {route_name}", location=to_dock, destination=from_dock)
    
    msg = f"World built: 1 city (Illium), {len(ISLANDS)} islands, {sum(len(i['areas']) for i in islands.values())} key areas."
    if caller:
        caller.msg(msg)
    return msg
