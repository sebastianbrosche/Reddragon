"""
Red Dragon MUD - Master World Builder
Orchestrates creation of all world areas
"""

from world.ilium import create_ilium_adventurers_guild
from world.yensidland import create_yensidland
from world.newbie_areas import (
    create_newbie_garden, create_spider_cave, create_circus,
    create_monster_daycare, create_church, create_ocean,
    create_strawberry_fields, create_fire_world, create_ice_world,
    create_cat_world, create_kobold_village, create_zoo,
    create_newbie_forest, create_ancient_tree, create_animal_nursery,
    create_swallow_moors, create_bee_hive, create_valley_new_adventurers
)
from world.detention import create_detention_facility

def _count(result):
    """Helper to count rooms from a function that may return single object or list."""
    if result is None:
        return 0
    if isinstance(result, (list, tuple)):
        return len(result)
    return 1

def build_world():
    """
    Build the entire Red Dragon world.
    Call this from at_server_start or a management command.
    """
    print("Building Red Dragon world...")
    
    # Create Ilium City (central hub)
    ilium_rooms = create_ilium_adventurers_guild()
    print(f"Created Ilium City: {_count(ilium_rooms)} rooms")
    
    # Create Yensid Land (newbie grinding area)
    yensid_rooms = create_yensidland()
    print(f"Created Yensid Land: {_count(yensid_rooms)} rooms")
    
    # Create all 19 newbie areas
    newbie_areas = {
        "Newbie Garden": create_newbie_garden(),
        "Spider Cave": create_spider_cave(),
        "The Circus": create_circus(),
        "Monster Daycare": create_monster_daycare(),
        "Church": create_church(),
        "Ocean": create_ocean(),
        "Strawberry Fields": create_strawberry_fields(),
        "Fire World": create_fire_world(),
        "Ice World": create_ice_world(),
        "Cat World": create_cat_world(),
        "Kobold Village": create_kobold_village(),
        "Zoo": create_zoo(),
        "Newbie Forest": create_newbie_forest(),
        "Ancient Tree": create_ancient_tree(),
        "Animal Nursery": create_animal_nursery(),
        "Swallow Moors": create_swallow_moors(),
        "Bee Hive": create_bee_hive(),
        "Valley of New Adventurers": create_valley_new_adventurers(),
    }
    print(f"Created {len(newbie_areas)} newbie areas")
    
    # Create admin areas
    detention = create_detention_facility()
    print("Created Detention Facility")
    
    # Link newbie areas to Ilium via portal in Newbie Guild
    # This would be done via the Sisong teleport system
    
    print("Red Dragon world build complete!")
    return {
        "ilium": ilium_rooms,
        "yensidland": yensid_rooms,
        "newbie_areas": newbie_areas,
        "detention": detention,
    }

if __name__ == "__main__":
    build_world()
