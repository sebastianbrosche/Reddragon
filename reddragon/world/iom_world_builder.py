# -*- coding: utf-8 -*-
"""
IOM World Builder - Batch command for Evennia

Reads parsed map data from world/map_data/*.json and builds the entire IOM world.

Usage from within Evennia:
    @batchcommand iom_world_builder

Or as a standalone script that generates batch command files.
"""

import json
import os
from pathlib import Path
from evennia import DefaultRoom, DefaultExit, create_object
from typeclasses.rooms import IOMRoom
from typeclasses.exits import IOMExit

# Map data directory
MAP_DATA_DIR = Path(__file__).parent / "map_data"

# Domain configuration - how sub-areas connect to parent domain
# Entry methods: "walk", "portal", "touch", "enter", "climb", "jump"
DOMAIN_CONFIG = {
    "gossamer": {
        "name": "Gossamer Island",
        "description": "A vast island with diverse landscapes ranging from peaceful forests to dangerous dungeons.",
        "sub_areas": {
            "newbie_garden": {"entry": "walk", "from": "central_square", "direction": "south"},
            "newbie_ocean": {"entry": "walk", "from": "central_square", "direction": "east"},
            "yensidland": {"entry": "portal", "from": "adventurer_guild", "portal_name": "mystical portal"},
            "illium_city": {"entry": "walk", "from": "central_square", "direction": "north"},
            "undercity": {"entry": "enter", "from": "illium_city_well", "command": "well"},
            "forest_trail": {"entry": "walk", "from": "central_square", "direction": "west"},
            "thieves_network": {"entry": "climb", "from": "illium_city", "command": "ladder"},
            "troll_cave": {"entry": "walk", "from": "forest_trail", "direction": "north"},
            "goblin_mounds": {"entry": "walk", "from": "north_forest", "direction": "east"},
            "kobold_village": {"entry": "walk", "from": "north_forest", "direction": "northeast"},
            "north_forest": {"entry": "walk", "from": "illium_city", "direction": "northwest"},
            "aviary": {"entry": "climb", "from": "illium_city", "command": "tree"},
            "beanstalk": {"entry": "climb", "from": "forest_trail", "command": "beanstalk"},
            "cat_world": {"entry": "portal", "from": "illium_city", "portal_name": "whiskers portal"},
            "chucks_bait_shop": {"entry": "walk", "from": "illium_city", "direction": "southwest"},
            "crystal_dragon_cave": {"entry": "walk", "from": "north_forest", "direction": "west"},
            "evoker_tower": {"entry": "walk", "from": "illium_city", "direction": "northeast"},
            "forest_grove": {"entry": "walk", "from": "forest_trail", "direction": "south"},
            "kreativs_pool_memorial_park": {"entry": "walk", "from": "illium_city", "direction": "southeast"},
            "larssis_island": {"entry": "portal", "from": "newbie_ocean", "portal_name": "ferry"},
            "peaceful_wood": {"entry": "walk", "from": "forest_trail", "direction": "east"},
            "player_castles": {"entry": "walk", "from": "illium_city", "direction": "east"},
            "prima_market": {"entry": "walk", "from": "illium_city", "direction": "south"},
            "private_beach": {"entry": "walk", "from": "illium_city", "direction": "southeast"},
            "red_dragon_city_ruins": {"entry": "walk", "from": "illium_city", "direction": "west"},
            "small_clearing": {"entry": "walk", "from": "forest_trail", "direction": "north"},
            "small_glade": {"entry": "walk", "from": "forest_trail", "direction": "northeast"},
            "small_village": {"entry": "walk", "from": "forest_trail", "direction": "southwest"},
            "spidranox_swamp": {"entry": "walk", "from": "illium_city", "direction": "south"},
            "swamp_mansion": {"entry": "walk", "from": "spidranox_swamp", "direction": "east"},
            "tidy_farm": {"entry": "walk", "from": "forest_trail", "direction": "southeast"},
            "zun_zoo": {"entry": "walk", "from": "illium_city", "direction": "east"},
        }
    },
    "emerald": {
        "name": "Emerald Island",
        "description": "A lush green island filled with forests, swamps, and ancient ruins.",
        "sub_areas": {
            "newbie_forest": {"entry": "walk", "from": "central", "direction": "north"},
            "ogre_villages": {"entry": "walk", "from": "central", "direction": "east"},
            "spamalot": {"entry": "portal", "from": "central", "portal_name": "laughing portal"},
            "celtica": {"entry": "walk", "from": "central", "direction": "west"},
            "small_manor": {"entry": "walk", "from": "central", "direction": "south"},
            "coramonde": {"entry": "walk", "from": "central", "direction": "southeast"},
            "bugbear_forest": {"entry": "walk", "from": "newbie_forest", "direction": "north"},
            "crystal_caverns": {"entry": "enter", "from": "newbie_forest", "command": "cave"},
            "emerald_mines": {"entry": "enter", "from": "coramonde", "command": "mine"},
            "forest_of_a_thousand_dreams": {"entry": "walk", "from": "central", "direction": "northeast"},
            "hags_forest": {"entry": "walk", "from": "central", "direction": "northwest"},
            "ice_mountain": {"entry": "climb", "from": "central", "command": "mountain"},
            "kobold_village": {"entry": "walk", "from": "newbie_forest", "direction": "west"},
            "minotaur_temple": {"entry": "walk", "from": "coramonde", "direction": "east"},
            "mossflower_forest": {"entry": "walk", "from": "central", "direction": "southwest"},
            "mountain_of_flowers_and_fruits": {"entry": "climb", "from": "central", "command": "path"},
            "passage": {"entry": "enter", "from": "coramonde", "command": "tunnel"},
            "princess_bride": {"entry": "walk", "from": "central", "direction": "south"},
            "small_farm": {"entry": "walk", "from": "newbie_forest", "direction": "south"},
            "small_grove": {"entry": "walk", "from": "newbie_forest", "direction": "east"},
            "swamp_castle": {"entry": "walk", "from": "spidranox_swamp", "direction": "south"},
        }
    }
}


class IOMWorldBuilder:
    """Builds the entire IOM world from parsed map data."""
    
    def __init__(self):
        self.rooms = {}  # domain -> area -> room_id -> room_obj
        self.exits_created = 0
        self.rooms_created = 0
        
    def build_domain(self, domain_name):
        """Build all sub-areas for a domain."""
        config = DOMAIN_CONFIG.get(domain_name)
        if not config:
            print(f"No config for domain: {domain_name}")
            return
            
        json_path = MAP_DATA_DIR / f"{domain_name}.json"
        if not json_path.exists():
            print(f"No map data for domain: {domain_name}")
            return
            
        with open(json_path) as f:
            map_data = json.load(f)
        
        print(f"\n{'='*60}")
        print(f"Building domain: {config['name']}")
        print(f"{'='*60}")
        
        # Build each sub-area
        for area_key, area_data in map_data.items():
            if area_key not in config.get("sub_areas", {}):
                print(f"  Skipping {area_key} (no config)")
                continue
                
            self.build_sub_area(domain_name, area_key, area_data, config["sub_areas"][area_key])
            
        print(f"Domain complete: {self.rooms_created} rooms, {self.exits_created} exits")
        
    def build_sub_area(self, domain_name, area_key, area_data, entry_config):
        """Build a single sub-area from parsed map data."""
        area_name = area_data.get("area_name", area_key.replace("_", " ").title())
        rooms_data = area_data.get("rooms", {})
        
        if not rooms_data:
            print(f"  ✗ {area_key}: No rooms")
            return
            
        print(f"  → {area_key}: {len(rooms_data)} rooms")
        
        # Create rooms
        area_rooms = {}
        for room_id, room_data in rooms_data.items():
            room_name = room_data.get("name", f"{area_name} - Room")
            if room_name.startswith("Room_") or room_name in ["----", "-----", "---", "-U-D-"]:
                room_name = f"{area_name}"
            
            # Clean up room name
            room_name = room_name.strip().title()
            if not room_name or room_name == area_name:
                room_name = f"{area_name} - Chamber"
                
            desc = f"You are in {area_name}."
            if room_data.get("is_exit"):
                desc += " There appears to be a way out of this area."
            if room_data.get("has_portal"):
                desc += " A mystical portal shimmers nearby."
                
            room = create_object(IOMRoom, key=room_name)
            room.db.desc = desc
            room.db.area = area_name
            room.db.domain = domain_name
            room.db.is_entry = room_data.get("is_entry", False)
            room.db.is_exit = room_data.get("is_exit", False)
            
            area_rooms[room_id] = room
            self.rooms_created += 1
            
        # Create exits between rooms
        for room_id, room_data in rooms_data.items():
            source_room = area_rooms.get(room_id)
            if not source_room:
                continue
                
            for direction, target_id in room_data.get("exits", {}).items():
                target_room = area_rooms.get(target_id)
                if not target_room:
                    continue
                    
                # Check if exit already exists
                existing = [ex for ex in source_room.exits if ex.key == direction]
                if existing:
                    continue
                    
                exit_obj = create_object(IOMExit, key=direction)
                exit_obj.aliases.add(direction)
                exit_obj.location = source_room
                exit_obj.destination = target_room
                
                self.exits_created += 1
                
        # Mark entry room
        if area_rooms:
            # Use first room as entry, or room with is_entry flag
            entry_room = None
            for room_id, room_data in rooms_data.items():
                if room_data.get("is_entry"):
                    entry_room = area_rooms.get(room_id)
                    break
            if not entry_room:
                entry_room = list(area_rooms.values())[0]
                
            entry_room.db.is_subarea_entry = True
            entry_room.db.subarea_key = area_key
            
        # Store for later linking
        if domain_name not in self.rooms:
            self.rooms[domain_name] = {}
        self.rooms[domain_name][area_key] = area_rooms
        
    def link_sub_areas(self, domain_name):
        """Create entry points from parent domain to sub-areas."""
        config = DOMAIN_CONFIG.get(domain_name)
        if not config:
            return
            
        print(f"\n  Linking sub-areas for {domain_name}...")
        
        for area_key, entry_config in config.get("sub_areas", {}).items():
            area_rooms = self.rooms.get(domain_name, {}).get(area_key, {})
            if not area_rooms:
                continue
                
            # Find entry room in sub-area
            entry_room = None
            for room in area_rooms.values():
                if getattr(room.db, "is_subarea_entry", False):
                    entry_room = room
                    break
            if not entry_room:
                entry_room = list(area_rooms.values())[0]
                
            # Create entry method
            entry_type = entry_config.get("entry", "walk")
            
            if entry_type == "walk":
                # Create exit from parent room to sub-area entry
                parent_area = entry_config.get("from", "central")
                direction = entry_config.get("direction", "north")
                
                # Find parent room (would need to be built already)
                print(f"    {area_key}: Walk {direction} from {parent_area}")
                
            elif entry_type == "portal":
                print(f"    {area_key}: Portal '{entry_config.get('portal_name')}' from {entry_config.get('from')}")
                
            elif entry_type == "enter":
                print(f"    {area_key}: Enter {entry_config.get('command')} from {entry_config.get('from')}")
                
            elif entry_type == "climb":
                print(f"    {area_key}: Climb {entry_config.get('command')} from {entry_config.get('from')}")
                
    def build_all(self):
        """Build all configured domains."""
        for domain_name in DOMAIN_CONFIG:
            self.build_domain(domain_name)
            self.link_sub_areas(domain_name)
            
        print(f"\n{'='*60}")
        print(f"WORLD BUILD COMPLETE")
        print(f"Total rooms: {self.rooms_created}")
        print(f"Total exits: {self.exits_created}")
        print(f"{'='*60}")


def build_world(caller=None):
    """Main entry point for batch building."""
    builder = IOMWorldBuilder()
    builder.build_all()
    return builder


if __name__ == "__main__":
    # When run as standalone, just show what would be built
    print("IOM World Builder")
    print("=" * 60)
    print("\nConfigured domains:")
    for domain_name, config in DOMAIN_CONFIG.items():
        print(f"  {config['name']}: {len(config.get('sub_areas', {}))} sub-areas")
        
    print("\nTo build, run this from within Evennia:")
    print("  @py from world.iom_world_builder import build_world; build_world()")
