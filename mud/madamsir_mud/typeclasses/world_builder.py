#!/usr/bin/env python3
"""
Evennia Batch Builder for Red Dragon MUD World
Reads maps_daran.json and creates rooms/exits.

Usage (in Evennia):
  @py from typeclasses.world_builder import build_world; build_world()
"""
import json
from evennia import create_object, search_object
from typeclasses.rooms import Room
from typeclasses.exits import Exit

MAPS_FILE = "/root/.openclaw/workspace/mud/maps_daran.json"

# Level ranges for islands (estimated)
ISLAND_LEVELS = {
    "gossamer": (1, 20),
    "emerald": (5, 25),
    "misty": (10, 30),
    "hyboria": (15, 35),
    "blackavar": (20, 40),
    "darkcaverns": (25, 45),
    "sombre": (30, 50),
    "everrest": (35, 55),
    "twin": (40, 60),
    "oddworld": (45, 65),
    "underwater": (50, 70),
    "other": (55, 75),
}

ISLAND_CLIMATES = {
    "gossamer": "temperate",
    "emerald": "tropical",
    "misty": "foggy",
    "hyboria": "varied",
    "blackavar": "dark",
    "darkcaverns": "subterranean",
    "sombre": "shadowy",
    "everrest": "frozen",
    "twin": "coastal",
    "oddworld": "chaotic",
    "underwater": "aquatic",
    "other": "mysterious",
}

ISLAND_DANGERS = {
    "gossamer": "low",
    "emerald": "low-moderate",
    "misty": "moderate",
    "hyboria": "moderate",
    "blackavar": "high",
    "darkcaverns": "high",
    "sombre": "high",
    "everrest": "very high",
    "twin": "high",
    "oddworld": "extreme",
    "underwater": "extreme",
    "other": "legendary",
}

# Track created objects
_created_rooms = {}
_created_exits = {}

def get_or_create_room(key, aliases=None, typeclass=None, **kwargs):
    """Get existing room or create new one."""
    if key in _created_rooms:
        return _created_rooms[key]
    
    existing = search_object(key)
    if existing:
        room = existing[0]
        _created_rooms[key] = room
        return room
    
    room = create_object(typeclass or Room, key=key, **kwargs)
    if aliases:
        room.aliases.add(aliases)
    _created_rooms[key] = room
    return room

def create_exit(from_room, to_room, name, aliases=None):
    """Create a bidirectional exit between rooms."""
    exit_key = f"{from_room.key}_to_{to_room.key}"
    if exit_key in _created_exits:
        return
    
    # Create exit from -> to
    exit_obj = create_object(Exit, key=name, location=from_room, destination=to_room)
    if aliases:
        for alias in aliases:
            exit_obj.aliases.add(alias)
    
    _created_exits[exit_key] = exit_obj

def build_world():
    """Build the entire world from map data."""
    import evennia
    evennia._init()
    
    with open(MAPS_FILE, "r") as f:
        data = json.load(f)
    
    print("=" * 60)
    print("RED DRAGON MUD — World Builder")
    print("=" * 60)
    
    # Create the Nexus (starting point)
    nexus = get_or_create_room(
        "The Nexus",
        aliases=["nexus", "spawn"],
        attributes=[
            ("island", "hub"),
            ("level_range", (1, 75)),
            ("climate", "neutral"),
            ("dangers", "low"),
            ("rest_area", True),
        ]
    )
    nexus.db.desc = (
        "You stand in the Nexus, a swirling vortex of energy where all paths converge.\n"
        "From here, you can travel to any of the Twelve Islands.\n"
        "Type 'look' to see available destinations, or 'help' for assistance."
    )
    print("✓ Created: The Nexus")
    
    # Build each island
    for island_name, island_data in data["islands"].items():
        build_island(island_name, island_data, nexus)
    
    # Summary
    total_rooms = len(_created_rooms)
    total_exits = len(_created_exits)
    print("\n" + "=" * 60)
    print(f"World build complete!")
    print(f"  Total rooms: {total_rooms}")
    print(f"  Total exits: {total_exits}")
    print("=" * 60)
    
    return total_rooms, total_exits

def build_island(island_name, island_data, nexus):
    """Build an island hub and all its areas."""
    areas = island_data.get("areas", [])
    if not areas:
        return
    
    display_name = island_name.title().replace("Darkcaverns", "Dark Caverns")
    levels = ISLAND_LEVELS.get(island_name, (1, 75))
    climate = ISLAND_CLIMATES.get(island_name, "unknown")
    dangers = ISLAND_DANGERS.get(island_name, "unknown")
    
    # Create island hub room
    hub = get_or_create_room(
        f"{display_name} — Dock",
        aliases=[island_name, f"{island_name}_dock"],
        attributes=[
            ("island", island_name),
            ("level_range", levels),
            ("climate", climate),
            ("dangers", dangers),
            ("rest_area", True),
        ]
    )
    hub.db.desc = (
        f"You stand at the dock of {display_name}, a {climate} island "
        f"known for its {dangers} dangers.\n"
        f"Recommended level range: {levels[0]}-{levels[1]}.\n"
        f"The island stretches before you with {len(areas)} areas to explore."
    )
    
    # Connect Nexus to island hub
    create_exit(nexus, hub, display_name, aliases=[island_name])
    create_exit(hub, nexus, "Nexus", aliases=["nexus", "spawn"])
    
    print(f"\n🏝  {display_name} ({len(areas)} areas, levels {levels[0]}-{levels[1]})")
    
    # Build each area
    for area_data in areas:
        build_area(island_name, display_name, hub, area_data, levels, climate, dangers)

def build_area(island_name, island_display, hub, area_data, island_levels, climate, dangers):
    """Build an area entrance and its rooms."""
    area_name = area_data["name"]
    labels = area_data.get("room_labels", {})
    has_map = area_data.get("has_ascii_map", False)
    ascii_map = area_data.get("ascii_map", "")
    
    # Create area entrance
    entrance = get_or_create_room(
        f"{area_name} — Entrance",
        aliases=[area_name.lower().replace(" ", "_"), f"{island_name}_{area_name.lower().replace(' ', '_')}"],
        attributes=[
            ("island", island_name),
            ("area", area_name),
            ("level_range", island_levels),
            ("climate", climate),
            ("dangers", dangers),
            ("rest_area", area_name in ["Illium City", "Slagos City", "Tarantia City"]),
        ]
    )
    
    # Build description
    desc_parts = [f"You stand at the entrance to {area_name}."]
    
    if has_map and ascii_map:
        # Include a compact version of the map
        desc_parts.append("\n{{yA map has been carved into the stone here:{{n")
        desc_parts.append(ascii_map[:1500])  # Truncate very large maps
        if len(ascii_map) > 1500:
            desc_parts.append("... (map continues)")
    
    if labels:
        desc_parts.append(f"\n{{yNotable locations within:{{n")
        for label, desc in sorted(labels.items()):
            desc_parts.append(f"  {label}: {desc}")
    
    entrance.db.desc = "\n".join(desc_parts)
    
    # Connect hub to entrance
    create_exit(hub, entrance, area_name, aliases=[area_name.lower().replace(" ", "_")])
    create_exit(entrance, hub, island_display, aliases=[island_name])
    
    # Build individual rooms for labels
    label_rooms = []
    for label, label_desc in labels.items():
        room_key = f"{area_name} — {label_desc[:40]}"
        room = get_or_create_room(
            room_key,
            aliases=[f"{area_name}_{label}", label],
            attributes=[
                ("island", island_name),
                ("area", area_name),
                ("label", label),
                ("level_range", island_levels),
                ("climate", climate),
                ("dangers", dangers),
            ]
        )
        room.db.desc = f"You are at {label_desc} in {area_name}."
        
        # Connect to entrance
        create_exit(entrance, room, f"to_{label}", aliases=[label.lower()])
        create_exit(room, entrance, "entrance", aliases=["out", "exit"])
        
        label_rooms.append(room)
    
    # Connect label rooms to each other in a simple chain/grid
    if len(label_rooms) > 1:
        for i in range(len(label_rooms) - 1):
            create_exit(label_rooms[i], label_rooms[i+1], "next")
            create_exit(label_rooms[i+1], label_rooms[i], "back")
    
    print(f"  📍 {area_name} ({len(labels)} rooms, map={has_map})")


if __name__ == "__main__":
    build_world()
