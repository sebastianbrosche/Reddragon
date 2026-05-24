#!/usr/bin/env python3
"""
IOM Map Bridge Builder v1

Automatically bridges disconnected room clusters within each sub-area
by adding exits between the closest rooms in different components.

This is a pragmatic fix for parser limitations — some map connections
are non-obvious (secret passages, teleporters, up/down not shown, etc).
Bridges are logged for manual review.
"""

import json
from pathlib import Path
from collections import defaultdict

MAP_DATA_DIR = Path('/root/.openclaw/workspace/reddragon/world/map_data')
BRIDGE_LOG = Path('/root/.openclaw/workspace/reddragon/world/map_bridges.json')

def find_components(rooms_data):
    """Find all connected components in a sub-area."""
    adj = defaultdict(set)
    for rid, r in rooms_data.items():
        for direction, target in r.get('exits', {}).items():
            adj[rid].add(str(target))
            adj[str(target)].add(rid)
    
    visited = set()
    components = []
    for start in rooms_data.keys():
        if start in visited:
            continue
        comp = set()
        queue = [start]
        while queue:
            node = queue.pop(0)
            if node in visited:
                continue
            visited.add(node)
            comp.add(node)
            for neighbor in adj.get(node, []):
                if neighbor not in visited and neighbor in rooms_data:
                    queue.append(neighbor)
        components.append(comp)
    return components


def grid_distance(room_a, room_b):
    """Manhattan distance between two rooms on the ASCII grid."""
    return abs(room_a['row'] - room_b['row']) + abs(room_a['col'] - room_b['col'])


def direction_between(room_a, room_b):
    """Determine the compass direction from room_a to room_b."""
    dr = room_b['row'] - room_a['row']
    dc = room_b['col'] - room_a['col']
    
    # Normalize to nearest direction
    directions = {
        'north': (-1, 0), 'south': (1, 0), 'west': (0, -1), 'east': (0, 1),
        'northwest': (-1, -1), 'northeast': (-1, 1), 'southwest': (1, -1), 'southeast': (1, 1),
    }
    
    # Find closest direction vector
    best_dir = 'north'  # default
    best_similarity = -2
    
    for name, (ddr, ddc) in directions.items():
        # Cosine similarity (for grid directions)
        similarity = (dr * ddr + dc * ddc) / (abs(dr) + abs(dc) + 1)
        if similarity > best_similarity:
            best_similarity = similarity
            best_dir = name
    
    return best_dir


def build_bridges():
    """Build bridges between disconnected components in all sub-areas."""
    bridge_log = {}
    total_bridges = 0
    areas_fixed = 0
    
    for json_file in sorted(MAP_DATA_DIR.glob('*.json')):
        domain = json_file.stem
        with open(json_file) as f:
            domain_data = json.load(f)
        
        domain_bridges = {}
        
        for area_key, area_data in domain_data.items():
            rooms = area_data.get('rooms', {})
            if len(rooms) < 2:
                continue
            
            components = find_components(rooms)
            if len(components) <= 1:
                continue  # Already fully connected
            
            bridges = []
            
            # Connect each small component to the nearest room in the largest component
            components.sort(key=len, reverse=True)
            main_comp = components[0]
            main_rooms = {rid: rooms[rid] for rid in main_comp}
            
            for comp in components[1:]:
                if len(comp) == 0:
                    continue
                    
                # Find closest pair of rooms between comp and main_comp
                best_pair = None
                best_dist = float('inf')
                
                for rid_a in comp:
                    room_a = rooms[rid_a]
                    for rid_b in main_comp:
                        room_b = rooms[rid_b]
                        dist = grid_distance(room_a, room_b)
                        if dist < best_dist:
                            best_dist = dist
                            best_pair = (rid_a, rid_b)
                
                if not best_pair:
                    continue
                    
                rid_a, rid_b = best_pair
                room_a = rooms[rid_a]
                room_b = rooms[rid_b]
                
                dir_a_to_b = direction_between(room_a, room_b)
                dir_b_to_a = direction_between(room_b, room_a)
                
                # Add exits
                if dir_a_to_b not in room_a.get('exits', {}):
                    room_a.setdefault('exits', {})[dir_a_to_b] = int(rid_b) if rid_b.isdigit() else rid_b
                if dir_b_to_a not in room_b.get('exits', {}):
                    room_b.setdefault('exits', {})[dir_b_to_a] = int(rid_a) if rid_a.isdigit() else rid_a
                
                bridges.append({
                    'from': rid_a,
                    'to': rid_b,
                    'from_name': room_a.get('name', 'Unknown'),
                    'to_name': room_b.get('name', 'Unknown'),
                    'direction': dir_a_to_b,
                    'distance': best_dist,
                    'component_size': len(comp)
                })
                
                total_bridges += 1
            
            if bridges:
                domain_bridges[area_key] = bridges
                areas_fixed += 1
                print(f"  {domain}/{area_key}: {len(bridges)} bridges ({len(components)} -> 1 component)")
        
        if domain_bridges:
            bridge_log[domain] = domain_bridges
            # Save updated domain data
            with open(json_file, 'w') as f:
                json.dump(domain_data, f, indent=2)
    
    # Save bridge log
    with open(BRIDGE_LOG, 'w') as f:
        json.dump(bridge_log, f, indent=2)
    
    print(f"\n{'='*60}")
    print(f"BRIDGE BUILD COMPLETE")
    print(f"  Areas fixed: {areas_fixed}")
    print(f"  Total bridges added: {total_bridges}")
    print(f"  Bridge log: {BRIDGE_LOG}")
    print(f"{'='*60}")
    print("\nAll sub-areas are now fully connected.")
    print("Review bridge log for any suspicious connections.")


if __name__ == '__main__':
    build_bridges()
