# -*- coding: utf-8 -*-
"""
IOM Complete World Builder v2

Builds the entire Islands of Myth world in Evennia from parsed map data.
Handles multiple entry types: walk, portal, touch, enter, climb.

Usage from Evennia shell or @py:
    from world.iom_complete_builder import build_full_world
    build_full_world()
"""

import json
from pathlib import Path

MAP_DATA_DIR = Path(__file__).parent / "map_data"


def lazy_imports():
    """Lazy imports to avoid issues when module is loaded outside Evennia."""
    global create_object, search_object, IOMRoom, IOMExit
    from evennia import create_object, search_object
    from typeclasses.rooms import IOMRoom
    from typeclasses.exits import IOMExit
    return create_object, search_object, IOMRoom, IOMExit


# ============================================================================
# ENTRY TYPE HANDLERS
# ============================================================================

def create_walk_entry(hub, area_key, entry_room, area_name):
    """Create a normal directional exit from hub to sub-area."""
    create_object, search_object, IOMRoom, IOMExit = lazy_imports()
    
    # Use area name as exit name
    exit_name = area_name.lower()
    
    # Create exit from hub to sub-area
    hub_exit = create_object(IOMExit, key=f"to {area_name}")
    hub_exit.aliases.add(exit_name)
    hub_exit.aliases.add(area_key.replace("_", " "))
    hub_exit.location = hub
    hub_exit.destination = entry_room
    
    # Create return exit
    return_exit = create_object(IOMExit, key="out")
    return_exit.aliases.add("exit")
    return_exit.location = entry_room
    return_exit.destination = hub
    
    return hub_exit


def create_portal_entry(hub, area_key, entry_room, area_name, portal_name=None):
    """Create a portal object that transports players when activated."""
    create_object, search_object, IOMRoom, IOMExit = lazy_imports()
    
    from evennia import DefaultObject
    
    portal = create_object(DefaultObject, key=portal_name or f"portal to {area_name}")
    portal.db.desc = f"A shimmering portal leading to {area_name}."
    portal.db.destination = entry_room
    portal.location = hub
    portal.aliases.add("portal")
    
    # Add portal command to hub room
    hub.cmdset.add(PortalCmdSet)
    
    # Create return exit from sub-area
    return_exit = create_object(IOMExit, key="out")
    return_exit.aliases.add("exit")
    return_exit.location = entry_room
    return_exit.destination = hub
    
    return portal


def create_touch_entry(hub, area_key, entry_room, area_name, object_name="mysterious stone"):
    """Create a touchable object that transports players."""
    create_object, search_object, IOMRoom, IOMExit = lazy_imports()
    
    from evennia import DefaultObject
    
    stone = create_object(DefaultObject, key=object_name)
    stone.db.desc = f"A strange {object_name}. Touching it might transport you somewhere..."
    stone.db.destination = entry_room
    stone.location = hub
    
    # Create return exit
    return_exit = create_object(IOMExit, key="out")
    return_exit.aliases.add("exit")
    return_exit.location = entry_room
    return_exit.destination = hub
    
    return stone


def create_enter_entry(hub, area_key, entry_room, area_name, enter_name="crack"):
    """Create an enterable feature (crack, hole, tunnel, etc)."""
    create_object, search_object, IOMRoom, IOMExit = lazy_imports()
    
    from evennia import DefaultObject
    
    feature = create_object(DefaultObject, key=f"{enter_name}")
    feature.db.desc = f"A {enter_name} leading somewhere. You could enter it."
    feature.db.destination = entry_room
    feature.location = hub
    feature.aliases.add(enter_name)
    
    # Create return exit
    return_exit = create_object(IOMExit, key="out")
    return_exit.aliases.add("exit")
    return_exit.location = entry_room
    return_exit.destination = hub
    
    return feature


def create_climb_entry(hub, area_key, entry_room, area_name, climb_name="ladder"):
    """Create a climbable feature (ladder, rope, tree, etc)."""
    create_object, search_object, IOMRoom, IOMExit = lazy_imports()
    
    from evennia import DefaultObject
    
    feature = create_object(DefaultObject, key=f"{climb_name}")
    feature.db.desc = f"A {climb_name}. You could climb it to reach {area_name}."
    feature.db.destination = entry_room
    feature.location = hub
    feature.aliases.add(climb_name)
    
    # Create return exit
    return_exit = create_object(IOMExit, key="out")
    return_exit.aliases.add("exit")
    return_exit.location = entry_room
    return_exit.destination = hub
    
    return feature


# ============================================================================
# DOMAIN CONFIGURATION
# ============================================================================

# Maps domain names to their hub settings and sub-area entry types
DOMAIN_CONFIG = {
    "gossamer": {
        "title": "Gossamer Island",
        "sub_areas": {
            "illium_city": {"type": "walk"},
            "yensidland": {"type": "portal", "portal_name": "mystical portal"},
            "newbie_ocean": {"type": "walk"},
            "undercity": {"type": "enter", "enter_name": "dark crack"},
            "forest_trail": {"type": "walk"},
            "thieves_network": {"type": "climb", "climb_name": "rope"},
            "troll_cave": {"type": "walk"},
            "goblin_mounds": {"type": "walk"},
            "kobold_village": {"type": "walk"},
            "north_forest": {"type": "walk"},
            "aviary": {"type": "climb", "climb_name": "tree"},
            "beanstalk": {"type": "climb", "climb_name": "beanstalk"},
            "cat_world": {"type": "portal", "portal_name": "whiskers portal"},
            "chucks_bait_shop": {"type": "walk"},
            "crystal_dragon_cave": {"type": "enter", "enter_name": "crystal cave"},
            "evoker_tower": {"type": "walk"},
            "forest_grove": {"type": "walk"},
            "kreativs_pool_memorial_park": {"type": "walk"},
            "larssis_island": {"type": "portal", "portal_name": "ferry"},
            "peaceful_wood": {"type": "walk"},
            "player_castles": {"type": "walk"},
            "prima_market": {"type": "walk"},
            "private_beach": {"type": "walk"},
            "red_dragon_city_ruins": {"type": "walk"},
            "small_clearing": {"type": "walk"},
            "small_glade": {"type": "walk"},
            "small_village": {"type": "walk"},
            "spidranox_swamp": {"type": "walk"},
            "swamp_mansion": {"type": "enter", "enter_name": "mansion gate"},
            "tidy_farm": {"type": "walk"},
            "zun_zoo": {"type": "walk"},
        }
    },
    "blackavar": {
        "title": "Blackavar Island",
        "sub_areas": {
            "blackavar_city": {"type": "walk"},
            "ankh-morpork_city": {"type": "walk"},
            "city_of_bakhgrul": {"type": "walk"},
            "newbie_valley": {"type": "walk"},
            "abandoned_tower": {"type": "enter", "enter_name": "tower"},
            "curly_grubb_inn": {"type": "walk"},
            "desert_storm": {"type": "walk"},
            "draculas_castle": {"type": "enter", "enter_name": "castle gate"},
            "draejars_tower": {"type": "climb", "climb_name": "spiral stairs"},
            "dryad_forest": {"type": "walk"},
            "forlorn_forest": {"type": "walk"},
            "goodwin_castle": {"type": "enter", "enter_name": "castle gate"},
            "highland_keep": {"type": "climb", "climb_name": "stone steps"},
            "insect_mound": {"type": "enter", "enter_name": "mound"},
            "lynne_mine": {"type": "enter", "enter_name": "mine shaft"},
            "merlins_keep": {"type": "walk"},
            "mindflayer_city": {"type": "walk"},
            "mountain_dungeon": {"type": "enter", "enter_name": "dungeon entrance"},
            "mountain_path": {"type": "walk"},
            "mt_nevermind": {"type": "climb", "climb_name": "mountain path"},
            "mt_olympus": {"type": "climb", "climb_name": "divine stairs"},
            "old_church": {"type": "enter", "enter_name": "church door"},
            "ruo_gen_city": {"type": "walk"},
            "spirit_temple": {"type": "enter", "enter_name": "temple gate"},
            "stony_brook_forest": {"type": "walk"},
            "tavern": {"type": "walk"},
            "tower_of_arabidopsis": {"type": "climb", "climb_name": "tower"},
            "tower_ruins": {"type": "enter", "enter_name": "ruined tower"},
            "underworld": {"type": "enter", "enter_name": "dark gate"},
            "valley_of_giants": {"type": "walk"},
            "valley_of_magic": {"type": "walk"},
        }
    },
    "emerald": {
        "title": "Emerald Island",
        "sub_areas": {
            "newbie_forest": {"type": "walk"},
            "ogre_villages": {"type": "walk"},
            "spamalot": {"type": "portal", "portal_name": "laughing portal"},
            "celtica": {"type": "walk"},
            "small_manor": {"type": "walk"},
            "coramonde": {"type": "walk"},
            "bugbear_forest": {"type": "walk"},
            "crystal_caverns": {"type": "enter", "enter_name": "crystal cave"},
            "emerald_mines": {"type": "enter", "enter_name": "mine entrance"},
            "forest_of_a_thousand_dreams": {"type": "walk"},
            "hags_forest": {"type": "walk"},
            "ice_mountain": {"type": "climb", "climb_name": "icy slope"},
            "kobold_village": {"type": "walk"},
            "minotaur_temple": {"type": "enter", "enter_name": "temple gate"},
            "mossflower_forest": {"type": "walk"},
            "mountain_of_flowers_and_fruits": {"type": "climb", "climb_name": "flowery path"},
            "passage": {"type": "enter", "enter_name": "dark tunnel"},
            "princess_bride": {"type": "walk"},
            "small_farm": {"type": "walk"},
            "small_grove": {"type": "walk"},
            "swamp_castle": {"type": "enter", "enter_name": "castle gate"},
        }
    },
    "darkcaverns": {
        "title": "Darkcaverns Island",
        "sub_areas": {
            "newbie_area": {"type": "walk"},
            "dragon_caves": {"type": "enter", "enter_name": "dragon cave"},
            "kobold_cave": {"type": "enter", "enter_name": "kobold cave"},
            "netherworld": {"type": "portal", "portal_name": "dark portal"},
            "slith_cave": {"type": "enter", "enter_name": "slith cave"},
            "underground_city": {"type": "enter", "enter_name": "underground gate"},
        }
    },
    "everrest": {
        "title": "Everrest Island",
        "sub_areas": {
            "everrest_city": {"type": "walk"},
            "newbie_valley": {"type": "walk"},
            "castle_everrest": {"type": "enter", "enter_name": "castle gate"},
            "dantes_inferno": {"type": "portal", "portal_name": "inferno portal"},
            "elven_forest": {"type": "walk"},
            "frozen_lake": {"type": "walk"},
            "graveyard": {"type": "walk"},
            "ice_palace": {"type": "enter", "enter_name": "ice palace"},
            "naraku": {"type": "portal", "portal_name": "dark portal"},
            "thieves_guild": {"type": "enter", "enter_name": "hidden door"},
            "trading_post": {"type": "walk"},
            "yeti_cave": {"type": "enter", "enter_name": "icy cave"},
        }
    },
    "hyboria": {
        "title": "Hyboria Island",
        "sub_areas": {
            "hyboria_city": {"type": "walk"},
            "newbie_area": {"type": "walk"},
            "aquilonia": {"type": "walk"},
            "fire_world": {"type": "portal", "portal_name": "fire portal"},
            "ice_world": {"type": "portal", "portal_name": "ice portal"},
            "mordulaks_realm": {"type": "enter", "enter_name": "dark realm"},
            "stygia": {"type": "walk"},
            "troll_cave": {"type": "enter", "enter_name": "cave"},
            "vanaheim": {"type": "walk"},
        }
    },
    "mists": {
        "title": "Mists Island",
        "sub_areas": {
            "mists_city": {"type": "walk"},
            "newbie_area": {"type": "walk"},
            "cathedral": {"type": "enter", "enter_name": "cathedral door"},
            "foggy_forest": {"type": "walk"},
            "graveyard": {"type": "walk"},
            "haunted_house": {"type": "enter", "enter_name": "creaky door"},
            "maze": {"type": "enter", "enter_name": "maze entrance"},
            "swamp": {"type": "walk"},
            "werewolf_den": {"type": "enter", "enter_name": "den"},
        }
    },
    "oddworld": {
        "title": "Oddworld Island",
        "sub_areas": {
            "oddworld_city": {"type": "walk"},
            "newbie_area": {"type": "walk"},
            "mudokon_village": {"type": "walk"},
            "raisin_cave": {"type": "enter", "enter_name": "cave"},
            "scarab_cave": {"type": "enter", "enter_name": "scarab nest"},
            "slig_barracks": {"type": "enter", "enter_name": "barracks"},
        }
    },
    "sombre": {
        "title": "Sombre Island",
        "sub_areas": {
            "sombre_city": {"type": "walk"},
            "newbie_area": {"type": "walk"},
            "grakhna_city": {"type": "walk"},
            "icarus_kingdom": {"type": "enter", "enter_name": "kingdom gate"},
            "valmoria_city": {"type": "walk"},
            "dark_forest": {"type": "walk"},
            "shadow_dungeon": {"type": "enter", "enter_name": "dungeon gate"},
        }
    },
    "southcape": {
        "title": "Southcape Island",
        "sub_areas": {
            "southcape_city": {"type": "walk"},
            "newbie_area": {"type": "walk"},
            "heracleion": {"type": "walk"},
            "pygmy_tribe": {"type": "walk"},
            "shifting_sands": {"type": "walk"},
            "sunken_temple": {"type": "enter", "enter_name": "temple gate"},
        }
    },
    "twin_islands": {
        "title": "Twin Islands",
        "sub_areas": {
            "twin_city": {"type": "walk"},
            "newbie_area": {"type": "walk"},
            "east_island": {"type": "walk"},
            "west_island": {"type": "walk"},
            "pirate_cove": {"type": "enter", "enter_name": "cove"},
            "volcano": {"type": "climb", "climb_name": "volcano path"},
        }
    },
}


# ============================================================================
# MAIN BUILDER
# ============================================================================

def build_full_world():
    """Build the complete IOM world."""
    create_object, search_object, IOMRoom, IOMExit = lazy_imports()
    
    print("=" * 60)
    print("IOM COMPLETE WORLD BUILDER v2")
    print("=" * 60)
    
    grand_total_rooms = 0
    grand_total_exits = 0
    
    for domain_name, config in sorted(DOMAIN_CONFIG.items()):
        json_path = MAP_DATA_DIR / f"{domain_name}.json"
        if not json_path.exists():
            print(f"  ✗ No map data for {domain_name}")
            continue
        
        with open(json_path) as f:
            map_data = json.load(f)
        
        # Create domain hub
        hub = create_object(IOMRoom, key=config["title"])
        hub.db.desc = f"The central hub of {config['title']}. From here you can reach many destinations."
        hub.db.domain = domain_name
        hub.db.is_domain_hub = True
        
        print(f"\n  Building {config['title']} ({len(config['sub_areas'])} sub-areas)...")
        
        domain_rooms = 0
        domain_exits = 0
        
        for area_key, entry_config in sorted(config["sub_areas"].items()):
            area_data = map_data.get(area_key)
            if not area_data:
                print(f"    ✗ {area_key}: Not found in map data")
                continue
            
            # Build sub-area
            entry_room, rcount, ecount = build_sub_area(area_key, area_data, domain_name, IOMRoom, IOMExit, create_object)
            
            if not entry_room:
                print(f"    ✗ {area_key}: Failed to build")
                continue
            
            domain_rooms += rcount
            domain_exits += ecount
            
            # Create entry to sub-area
            area_name = area_data.get("area_name", area_key.replace("_", " ").title())
            entry_type = entry_config.get("type", "walk")
            
            if entry_type == "walk":
                create_walk_entry(hub, area_key, entry_room, area_name)
            elif entry_type == "portal":
                create_portal_entry(hub, area_key, entry_room, area_name, 
                                   entry_config.get("portal_name"))
            elif entry_type == "touch":
                create_touch_entry(hub, area_key, entry_room, area_name,
                                  entry_config.get("object_name", "mysterious stone"))
            elif entry_type == "enter":
                create_enter_entry(hub, area_key, entry_room, area_name,
                                  entry_config.get("enter_name", "crack"))
            elif entry_type == "climb":
                create_climb_entry(hub, area_key, entry_room, area_name,
                                  entry_config.get("climb_name", "ladder"))
            
            print(f"    ✓ {area_key} [{entry_type}]: {rcount} rooms, {ecount} exits")
        
        grand_total_rooms += domain_rooms
        grand_total_exits += domain_exits
        print(f"  → {config['title']}: {domain_rooms} rooms, {domain_exits} exits")
    
    # Create inter-domain ferry connections
    print("\n  Creating ferry connections...")
    create_ferry_network(IOMRoom, IOMExit, create_object, search_object)
    
    print(f"\n{'='*60}")
    print(f"WORLD BUILD COMPLETE")
    print(f"  Total Rooms: {grand_total_rooms}")
    print(f"  Total Exits: {grand_total_exits}")
    print(f"{'='*60}")
    print("\nExplore with: @tel #<room_id>, look, north/east/etc")


def build_sub_area(area_key, area_data, domain_name, IOMRoom, IOMExit, create_object):
    """Build a single sub-area from JSON data."""
    area_name = area_data.get("area_name", area_key.replace("_", " ").title())
    rooms_data = area_data.get("rooms", {})
    
    if not rooms_data:
        return None, 0, 0
    
    # Create all rooms
    room_map = {}  # original_id -> room_object
    created_rooms = 0
    
    for orig_id, rdata in rooms_data.items():
        name = rdata.get("name", "Chamber")
        
        # Clean bad names
        if name.startswith("Room_") or name in ["----", "-----", "---", "-U-D-", "====", "~~~~", " "]:
            name = area_name
        if not name or name.strip() == "":
            name = area_name
            
        name = name.strip().title()
        if len(name) < 2:
            name = f"{area_name} Chamber"
        
        # Build description
        desc = f"You are in {area_name}."
        if rdata.get("is_exit"):
            desc += " There is a way leading out of this area."
        if rdata.get("has_portal"):
            desc += " A strange portal shimmers nearby."
            
        room = create_object(IOMRoom, key=name)
        room.db.desc = desc
        room.db.area = area_name
        room.db.domain = domain_name
        room.db.subarea = area_key
        room_map[orig_id] = room
        created_rooms += 1
    
    # Create exits between rooms
    exits_created = 0
    for orig_id, rdata in rooms_data.items():
        orig_id = int(orig_id) if isinstance(orig_id, str) else orig_id
        source = room_map.get(orig_id)
        if not source:
            continue
            
        for direction, target_id in rdata.get("exits", {}).items():
            target_id = int(target_id) if isinstance(target_id, (str, int)) else target_id
            target = room_map.get(target_id)
            if not target:
                continue
            
            # Check if exit already exists in this direction
            if any(ex.key == direction for ex in source.exits):
                continue
                
            ex = create_object(IOMExit, key=direction)
            ex.aliases.add(direction)
            ex.location = source
            ex.destination = target
            exits_created += 1
    
    # Determine entry room (first room, or room marked as entry/exit)
    entry_room = None
    for orig_id, rdata in rooms_data.items():
        if rdata.get("is_entry") or rdata.get("is_exit"):
            room_id = int(orig_id) if isinstance(orig_id, str) else orig_id
            entry_room = room_map.get(room_id)
            break
    
    if not entry_room and room_map:
        # Find edge room (lowest row/col)
        first_id = min(rooms_data.keys(), 
                      key=lambda k: (rooms_data[k]["row"], rooms_data[k]["col"]))
        room_id = int(first_id) if isinstance(first_id, str) else first_id
        entry_room = room_map.get(room_id)
    
    return entry_room, created_rooms, exits_created


def create_ferry_network(IOMRoom, IOMExit, create_object, search_object):
    """Create ferry connections between all domain hubs."""
    # Get all domain hubs
    from evennia import DefaultRoom
    
    # Find all hub rooms
    all_rooms = search_object("Island", typeclass=IOMRoom)
    hubs = [r for r in all_rooms if getattr(r.db, "is_domain_hub", False)]
    
    if not hubs:
        print("    No domain hubs found for ferry network")
        return
    
    # Create ferry connections between all hubs
    ferry_count = 0
    for i, hub_a in enumerate(hubs):
        for hub_b in hubs[i+1:]:
            # Create ferry exit from A to B
            ferry_key = f"ferry_to_{hub_b.key.replace(' ', '_').lower()}"
            if not any(ex.key == ferry_key for ex in hub_a.exits):
                ferry = create_object(IOMExit, key=f"ferry to {hub_b.key}")
                ferry.aliases.add("ferry")
                ferry.location = hub_a
                ferry.destination = hub_b
                ferry_count += 1
            
            # Create ferry exit from B to A
            ferry_key = f"ferry_to_{hub_a.key.replace(' ', '_').lower()}"
            if not any(ex.key == ferry_key for ex in hub_b.exits):
                ferry = create_object(IOMExit, key=f"ferry to {hub_a.key}")
                ferry.aliases.add("ferry")
                ferry.location = hub_b
                ferry.destination = hub_a
                ferry_count += 1
    
    print(f"    Created {ferry_count} ferry connections between {len(hubs)} islands")


if __name__ == "__main__":
    print("Run this from within Evennia with:")
    print("  @py from world.iom_complete_builder import build_full_world; build_full_world()")
