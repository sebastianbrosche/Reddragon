"""
Red Dragon MUD - Terrain Builder
Common terrain room builder functions for Map Builder integration
"""

from evennia import create_object
from typeclasses import rooms, exits
import random

# Terrain type configurations
TERRAIN_CONFIG = {
    "water": {
        "name_prefix": "Open Ocean",
        "descs": [
            "Endless waves stretch to the horizon in every direction.",
            "The sea is calm here, with gentle swells rolling past.",
            "Rough waters churn beneath your vessel.",
            "A vast expanse of blue water surrounds you.",
        ],
        "typeclass": rooms.Room,
    },
    "beach": {
        "name_prefix": "Sandy Beach",
        "descs": [
            "Waves lap gently at the white sand.",
            "A long stretch of beach with seashells scattered about.",
            "The shoreline curves gently, bordered by dunes.",
            "Fine golden sand stretches between sea and land.",
        ],
        "typeclass": rooms.Room,
    },
    "forest": {
        "name_prefix": "Forest",
        "descs": [
            "Tall trees surround you, their canopy blocking much of the light.",
            "A quiet forest glade with moss-covered stones.",
            "The forest is thick here, with undergrowth at every turn.",
            "Sunlight filters through leaves, dappling the forest floor.",
        ],
        "typeclass": rooms.Room,
    },
    "deep_forest": {
        "name_prefix": "Deep Forest",
        "descs": [
            "The forest grows dark and oppressive here.",
            "Ancient trees tower overhead, their branches intertwined.",
            "This part of the forest feels primeval and untouched.",
            "Thick vegetation makes travel difficult.",
        ],
        "typeclass": rooms.Room,
    },
    "hills": {
        "name_prefix": "Rolling Hills",
        "descs": [
            "Gentle hills roll across the landscape.",
            "The high ground offers views of the surrounding area.",
            "Rocky outcrops dot these grassy hills.",
            "Wind sweeps across the open hilltops.",
        ],
        "typeclass": rooms.Room,
    },
    "mountains": {
        "name_prefix": "Mountain",
        "descs": [
            "Steep, rocky slopes rise sharply here.",
            "The thin mountain air makes breathing difficult.",
            "Snow-capped peaks are visible in the distance.",
            "A narrow path winds through jagged rocks.",
        ],
        "typeclass": rooms.Room,
    },
    "desert": {
        "name_prefix": "Desert",
        "descs": [
            "Endless sand dunes shift in the wind.",
            "The desert sun beats down mercilessly.",
            "A dry, cracked wasteland stretches in all directions.",
            "Sparse vegetation clings to life in the sand.",
        ],
        "typeclass": rooms.Room,
    },
    "swamp": {
        "name_prefix": "Swamp",
        "descs": [
            "Murky water and rotting vegetation surround you.",
            "The swamp emits a foul odor.",
            "Strange sounds echo from the misty wetlands.",
            "Sinking mud makes every step treacherous.",
        ],
        "typeclass": rooms.Room,
    },
    "marsh": {
        "name_prefix": "Marsh",
        "descs": [
            "Waterlogged ground squelches underfoot.",
            "Tall reeds grow thick in the marshy soil.",
            "The marsh is quiet except for buzzing insects.",
            "Shallow pools reflect the overcast sky.",
        ],
        "typeclass": rooms.Room,
    },
    "road": {
        "name_prefix": "Road",
        "descs": [
            "A well-traveled road stretches before you.",
            "The road is paved with ancient stones.",
            "Dust rises from the beaten path.",
            "Signs of frequent travel are evident here.",
        ],
        "typeclass": rooms.Room,
    },
    "plains": {
        "name_prefix": "Plains",
        "descs": [
            "Open grassland extends to the horizon.",
            "Tall grass sways in the breeze.",
            "The prairie is alive with the sounds of insects.",
            "A vast expanse of flat land surrounds you.",
        ],
        "typeclass": rooms.Room,
    },
    "city": {
        "name_prefix": "City Street",
        "descs": [
            "A busy street with buildings on all sides.",
            "The cobblestones are worn smooth by countless footsteps.",
            "Shops and houses line this thoroughfare.",
            "The sounds of city life fill the air.",
        ],
        "typeclass": rooms.Room,
    },
    "building": {
        "name_prefix": "Building",
        "descs": [
            "A sturdy structure stands here.",
            "The building shows signs of age and wear.",
            "This structure appears well-maintained.",
            "A building of local architecture.",
        ],
        "typeclass": rooms.Room,
    },
    "lake": {
        "name_prefix": "Lake Shore",
        "descs": [
            "Calm waters lap at the shore.",
            "A peaceful lake reflects the sky above.",
            "The lake stretches out before you.",
            "Waterfowl drift across the still surface.",
        ],
        "typeclass": rooms.Room,
    },
    "dungeon": {
        "name_prefix": "Dark Dungeon",
        "descs": [
            "Darkness presses in from all sides.",
            "The dungeon walls are damp and cold.",
            "Faint echoes hint at dangers nearby.",
            "This place has not seen light in ages.",
        ],
        "typeclass": rooms.Room,
    },
    "crossing": {
        "name_prefix": "Crossroads",
        "descs": [
            "Paths meet at this junction.",
            "A well-worn crossroads with weathered signposts.",
            "Several routes converge here.",
            "Travelers have left marks pointing the way.",
        ],
        "typeclass": rooms.Room,
    },
    "valley": {
        "name_prefix": "Valley",
        "descs": [
            "A deep valley stretches between peaks.",
            "The valley floor is lush and green.",
            "Steep walls rise on either side.",
            "A river winds through the valley below.",
        ],
        "typeclass": rooms.Room,
    },
}


def build_room(x, y, terrain_type, **kwargs):
    """
    Build a room for the given terrain type.
    
    Args:
        x, y: Coordinates on the map
        terrain_type: Key from TERRAIN_CONFIG
        **kwargs: Additional args passed by mapbuilder
    
    Returns:
        Room object
    """
    config = TERRAIN_CONFIG.get(terrain_type, TERRAIN_CONFIG["plains"])
    
    room = create_object(
        config["typeclass"],
        key=f"{config['name_prefix']} {x},{y}"
    )
    
    # Set description
    room.db.desc = random.choice(config["descs"])
    
    # Set terrain tag for reference
    room.db.terrain = terrain_type
    room.db.x_coord = x
    room.db.y_coord = y
    
    # Notify caller
    if "caller" in kwargs:
        kwargs["caller"].msg(f"Created: {room.key}")
    
    return room


# Convenience builders for map legends
def build_water(x, y, **kwargs):
    return build_room(x, y, "water", **kwargs)

def build_beach(x, y, **kwargs):
    """Build a beach room - may become a dock if adjacent to water."""
    room = build_room(x, y, "beach", **kwargs)
    
    # Check if this beach is a potential dock location
    # Docks are at beach locations that face open water
    room.db.is_dock = True
    room.db.dock_name = f"{room.key} Dock"
    
    return room

def build_forest(x, y, **kwargs):
    return build_room(x, y, "forest", **kwargs)

def build_deep_forest(x, y, **kwargs):
    return build_room(x, y, "deep_forest", **kwargs)

def build_hills(x, y, **kwargs):
    return build_room(x, y, "hills", **kwargs)

def build_mountains(x, y, **kwargs):
    return build_room(x, y, "mountains", **kwargs)

def build_desert(x, y, **kwargs):
    return build_room(x, y, "desert", **kwargs)

def build_swamp(x, y, **kwargs):
    return build_room(x, y, "swamp", **kwargs)

def build_marsh(x, y, **kwargs):
    return build_room(x, y, "marsh", **kwargs)

def build_road(x, y, **kwargs):
    return build_room(x, y, "road", **kwargs)

def build_plains(x, y, **kwargs):
    return build_room(x, y, "plains", **kwargs)

def build_city(x, y, **kwargs):
    return build_room(x, y, "city", **kwargs)

def build_building(x, y, **kwargs):
    return build_room(x, y, "building", **kwargs)

def build_lake(x, y, **kwargs):
    return build_room(x, y, "lake", **kwargs)

def build_dungeon(x, y, **kwargs):
    return build_room(x, y, "dungeon", **kwargs)

def build_crossing(x, y, **kwargs):
    return build_room(x, y, "crossing", **kwargs)

def build_valley(x, y, **kwargs):
    return build_room(x, y, "valley", **kwargs)
