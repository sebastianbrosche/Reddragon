# -*- coding: utf-8 -*-
"""
IOM Complete World Builder

Run from Evennia with:
    @py from world.iom_complete_builder import build_full_world; build_full_world()

Or add to server/conf/at_server_startstop.py to auto-build on first start.
"""

import json
from pathlib import Path
from evennia import create_object
from typeclasses.rooms import IOMRoom
from typeclasses.exits import IOMExit

MAP_DATA_DIR = Path(__file__).parent / "map_data"

# Domain hubs - central connection points
def get_or_create_domain_hub(domain_name, domain_title):
    """Get or create the central hub room for a domain."""
    # Search for existing hub
    from evennia import search_object
    hubs = search_object(domain_title, typeclass=IOMRoom)
    if hubs:
        return hubs[0]
    
    hub = create_object(IOMRoom, key=domain_title)
    hub.db.desc = f"The central hub of {domain_title}. Paths lead to many destinations."
    hub.db.domain = domain_name
    hub.db.is_domain_hub = True
    return hub


def build_sub_area(area_key, area_data, domain_name):
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
        if name.startswith("Room_") or name in ["----", "-----", "---", "-U-D-", "====", "~~~~"]:
            name = area_name
        if not name or name.strip() == "":
            name = area_name
            
        name = name.strip().title()
        
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
    
    # Create exits
    exits_created = 0
    for orig_id, rdata in rooms_data.items():
        source = room_map.get(orig_id)
        if not source:
            continue
            
        for direction, target_id in rdata.get("exits", {}).items():
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
            entry_room = room_map.get(orig_id)
            break
    
    if not entry_room and room_map:
        # Find edge room (lowest row, or first in dict)
        first_id = min(rooms_data.keys(), key=lambda k: (rooms_data[k]["row"], rooms_data[k]["col"]))
        entry_room = room_map.get(first_id)
    
    return entry_room, created_rooms, exits_created


def build_domain(domain_name):
    """Build all sub-areas for a domain and link them."""
    json_path = MAP_DATA_DIR / f"{domain_name}.json"
    if not json_path.exists():
        print(f"  ✗ No data file for {domain_name}")
        return 0, 0
    
    with open(json_path) as f:
        domain_data = json.load(f)
    
    domain_title = domain_name.replace("_", " ").title() + " Island"
    hub = get_or_create_domain_hub(domain_name, domain_title)
    
    total_rooms = 0
    total_exits = 0
    linked_areas = 0
    
    print(f"\n  Building {domain_title} ({len(domain_data)} sub-areas)...")
    
    for area_key, area_data in domain_data.items():
        entry_room, rcount, ecount = build_sub_area(area_key, area_data, domain_name)
        
        if entry_room:
            total_rooms += rcount
            total_exits += ecount
            
            # Link sub-area entry to domain hub
            area_name = area_data.get("area_name", area_key.replace("_", " ").title())
            
            # Create exit from hub to sub-area
            if not any(ex.key == area_key for ex in hub.exits):
                hub_exit = create_object(IOMExit, key=area_key)
                hub_exit.aliases.add(area_key.replace("_", " "))
                hub_exit.location = hub
                hub_exit.destination = entry_room
                
            # Create return exit from sub-area to hub
            if not any(ex.key == domain_name for ex in entry_room.exits):
                return_exit = create_object(IOMExit, key=domain_name)
                return_exit.aliases.add("out")
                return_exit.location = entry_room
                return_exit.destination = hub
                
            linked_areas += 1
            print(f"    ✓ {area_key}: {rcount} rooms, {ecount} exits")
        else:
            print(f"    ✗ {area_key}: Failed to build")
    
    print(f"  → {domain_title}: {linked_areas} areas, {total_rooms} rooms, {total_exits} exits")
    return total_rooms, total_exits


def build_full_world():
    """Build the complete IOM world."""
    print("=" * 60)
    print("IOM COMPLETE WORLD BUILDER")
    print("=" * 60)
    
    grand_total_rooms = 0
    grand_total_exits = 0
    
    # Process all domains
    for json_file in sorted(MAP_DATA_DIR.glob("*.json")):
        domain_name = json_file.stem
        rooms, exits = build_domain(domain_name)
        grand_total_rooms += rooms
        grand_total_exits += exits
    
    # Create inter-domain ferry connections
    print("\n  Creating inter-domain ferry connections...")
    create_ferry_connections()
    
    print(f"\n{'='*60}")
    print(f"WORLD BUILD COMPLETE")
    print(f"  Total Rooms: {grand_total_rooms}")
    print(f"  Total Exits: {grand_total_exits}")
    print(f"{'='*60}")
    print("\nTo explore:")
    print("  @tel #<room_id>  (teleport to any room)")
    print("  look            (examine your surroundings)")
    print("  north/east/etc  (move around)")


def create_ferry_connections():
    """Create ferry connections between domain hubs."""
    from evennia import search_object
    
    ferry_routes = [
        ("Gossamer Island", ["Blackavar Island", "Emerald Island", "Sombre Island", 
                             "Mists Island", "Twin Islands", "Everrest Island", 
                             "Oddworld Island", "Hyboria Island", "Southcape Island",
                             "Darkcaverns Island"]),
    ]
    
    for hub_name, destinations in ferry_routes:
        hubs = search_object(hub_name, typeclass=IOMRoom)
        if not hubs:
            continue
        hub = hubs[0]
        
        for dest_name in destinations:
            dests = search_object(dest_name, typeclass=IOMRoom)
            if not dests:
                continue
            dest = dests[0]
            
            # Create ferry exit
            ferry_key = f"ferry_to_{dest_name.replace(' ', '_').lower()}"
            if not any(ex.key == ferry_key for ex in hub.exits):
                ferry = create_object(IOMExit, key=f"ferry to {dest_name}")
                ferry.aliases.add("ferry")
                ferry.location = hub
                ferry.destination = dest
                print(f"    Ferry: {hub_name} -> {dest_name}")


if __name__ == "__main__":
    print("Run this from within Evennia with:")
    print("  @py from world.iom_complete_builder import build_full_world; build_full_world()")
