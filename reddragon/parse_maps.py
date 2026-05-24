#!/usr/bin/env python3
"""
IOM Map Parser - Extracts rooms and exits from ASCII map HTML files
and generates Evennia build scripts.

Map format:
- '+' = room node
- '-', '|', '/', '\\', '~', '=' = connections (exits)
- Text near rooms = room names
- Special: 'out' = exit to parent area, '@' = special room, 'P' = portal
"""

import os
import re
import sys
from pathlib import Path
from html.parser import HTMLParser

class SimpleHTMLExtractor(HTMLParser):
    """Extract text content from HTML, preserving whitespace."""
    def __init__(self):
        super().__init__()
        self.text = []
        self.in_pre = False
        
    def handle_starttag(self, tag, attrs):
        if tag == 'pre':
            self.in_pre = True
            
    def handle_endtag(self, tag):
        if tag == 'pre':
            self.in_pre = False
            
    def handle_data(self, data):
        if self.in_pre:
            self.text.append(data)
            
    def get_text(self):
        return ''.join(self.text)


def extract_pre_text(html_content):
    """Extract text from <pre> tags in HTML."""
    # Find all <pre>...</pre> content
    pattern = re.compile(r'<pre>(.*?)</pre>', re.DOTALL | re.IGNORECASE)
    matches = pattern.findall(html_content)
    if matches:
        # Return the longest pre block (usually the map)
        return max(matches, key=len)
    return ""


def clean_html_tags(text):
    """Remove HTML tags from text."""
    # Remove all HTML tags
    clean = re.sub(r'<[^>]+>', '', text)
    # Decode common HTML entities
    clean = clean.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
    return clean


def parse_map(html_content):
    """
    Parse an ASCII map and extract rooms with their coordinates.
    Returns: (area_name, island, coder, rooms, connections)
    """
    pre_text = extract_pre_text(html_content)
    if not pre_text:
        return None, None, None, [], []
    
    # Clean HTML tags
    raw_text = clean_html_tags(pre_text)
    lines = raw_text.split('\n')
    
    # Extract header info
    area_name = "Unknown"
    island = "Unknown"
    coder = "Unknown"
    
    for line in lines[:10]:
        if 'Area' in line and ':' in line:
            area_name = line.split(':', 1)[1].strip()
        elif 'Island' in line and ':' in line:
            island = line.split(':', 1)[1].strip()
        elif 'Coder' in line and ':' in line:
            coder = line.split(':', 1)[1].strip()
    
    # Find the map grid (lines with + and connection characters)
    grid_lines = []
    header_end = 0
    for i, line in enumerate(lines):
        if '+' in line and ('-' in line or '|' in line):
            if header_end == 0:
                header_end = i
            grid_lines.append((i, line))
    
    if not grid_lines:
        return area_name, island, coder, [], []
    
    # Find room positions (each '+' is a room)
    rooms = {}  # (row, col) -> room_info
    room_chars = set('+-|/\\~=@PabcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ')
    
    for row_idx, line in grid_lines:
        for col_idx, char in enumerate(line):
            if char == '+':
                rooms[(row_idx, col_idx)] = {
                    'name': None,
                    'row': row_idx,
                    'col': col_idx,
                    'exits': {}
                }
    
    # Find connections between rooms
    # Check each room's neighbors for connection chars
    connection_chars = set('-|/\\~=')
    exit_directions = {
        (-1, 0): 'north',
        (1, 0): 'south',
        (0, -1): 'west',
        (0, 1): 'east',
        (-1, -1): 'northwest',
        (-1, 1): 'northeast',
        (1, -1): 'southwest',
        (1, 1): 'southeast',
    }
    
    for (row, col), room in rooms.items():
        for (drow, dcol), direction in exit_directions.items():
            # Check midpoint for connection character
            mid_row = row + drow
            mid_col = col + dcol
            
            # Look at the connecting line
            # For cardinal directions, check adjacent cell
            if (drow, dcol) in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                # Check if there's a connection char between rooms
                # For north/south: check character at (row + drow/2, col) if drow != 0
                # Actually, check the cell adjacent to this room
                check_row = row + drow
                check_col = col + dcol
                
                # Find the target room
                target = None
                # Search in the direction for another room
                search_row = check_row
                search_col = check_col
                
                # For direct neighbors, check if target room exists
                if (search_row, search_col) in rooms:
                    target = (search_row, search_col)
                else:
                    # Might be a room 2 cells away (for lines with chars in between)
                    search_row = row + drow * 2
                    search_col = col + dcol * 2
                    if (search_row, search_col) in rooms:
                        target = (search_row, search_col)
                
                if target:
                    room['exits'][direction] = target
    
    # For diagonal connections
    for (row, col), room in rooms.items():
        for drow, dcol, direction in [(-1, -1, 'northwest'), (-1, 1, 'northeast'), 
                                         (1, -1, 'southwest'), (1, 1, 'southeast')]:
            target = (row + drow, col + dcol)
            if target in rooms:
                room['exits'][direction] = target
    
    # Extract room names from text near rooms
    # Look for text labels that are adjacent to or near room nodes
    for (row, col), room in rooms.items():
        # Check surrounding area for text labels
        best_name = None
        best_distance = float('inf')
        
        for search_row in range(max(0, row-2), min(len(lines), row+3)):
            for search_col in range(max(0, col-10), min(len(lines[search_row]) if search_row < len(lines) else 0, col+10)):
                # Skip if this is another room node
                if (search_row, search_col) in rooms and (search_row, search_col) != (row, col):
                    continue
                
                # Calculate distance
                distance = abs(search_row - row) + abs(search_col - col)
                
                # Look for text at this position
                if search_row < len(lines):
                    line = lines[search_row]
                    if search_col < len(line):
                        # Extract word at this position
                        char = line[search_col]
                        if char.isalpha() or char in ' \'-':
                            # Extract word
                            start = search_col
                            while start > 0 and (line[start-1].isalpha() or line[start-1] in ' \'-_'):
                                start -= 1
                            end = search_col
                            while end < len(line) and (line[end].isalpha() or line[end] in ' \'-_'):
                                end += 1
                            word = line[start:end].strip()
                            
                            # Skip connection characters used as labels
                            if word and word not in ['out', 'P'] and len(word) > 1:
                                if distance < best_distance:
                                    # Check if this text is not between two rooms (i.e., it's a label, not a path)
                                    is_between_rooms = False
                                    # Simple check: if the text is on the same row and between two + chars
                                    if search_row == row:
                                        left_room = False
                                        right_room = False
                                        for c in range(start, col):
                                            if (row, c) in rooms:
                                                left_room = True
                                                break
                                        for c in range(col+1, end+1):
                                            if (row, c) in rooms:
                                                right_room = True
                                                break
                                        if left_room and right_room:
                                            is_between_rooms = True
                                    
                                    if not is_between_rooms:
                                        best_name = word
                                        best_distance = distance
        
        if best_name:
            room['name'] = best_name.title()
    
    # Handle special markers
    for (row, col), room in rooms.items():
        # Check for 'out' text near room
        for search_row in range(max(0, row-2), min(len(lines), row+3)):
            line = lines[search_row] if search_row < len(lines) else ""
            if 'out' in line.lower():
                # Check if 'out' is near this room
                out_pos = line.lower().find('out')
                if abs(out_pos - col) < 5 and abs(search_row - row) < 3:
                    room['is_exit'] = True
                    room['exit_target'] = 'parent'
        
        # Check for 'P' or 'Portal' near room
        for search_row in range(max(0, row-2), min(len(lines), row+3)):
            line = lines[search_row] if search_row < len(lines) else ""
            if 'portal' in line.lower() or ('P' in line and 'portal' in raw_text.lower()):
                portal_pos = line.find('P') if 'P' in line else line.lower().find('portal')
                if portal_pos >= 0 and abs(portal_pos - col) < 5 and abs(search_row - row) < 3:
                    room['has_portal'] = True
    
    return area_name, island, coder, list(rooms.values()), lines


def generate_evennia_script(area_name, island, coder, rooms, all_lines, domain_name, area_key):
    """Generate an Evennia batch build script from parsed map data."""
    
    # Create a clean Python identifier
    clean_name = re.sub(r'[^a-zA-Z0-9_]', '_', area_name.lower())
    if clean_name.endswith('_'):
        clean_name = clean_name[:-1]
    
    script = f'''# -*- coding: utf-8 -*-
"""
{area_name} - {island} Domain
Coded by: {coder}
Auto-generated from IOM map archive
"""

from evennia import create_object
from typeclasses.rooms import IOMRoom
from typeclasses.exits import IOMExit

# Room storage for linking exits
rooms = {{}}

'''
    
    # Create rooms
    for i, room in enumerate(rooms):
        room_id = f"room_{i}"
        room_name = room.get('name') or f"Room {i+1}"
        # Clean up room name
        room_name = room_name.strip().title()
        if not room_name or room_name == 'Room':
            room_name = f"{area_name} - Room {i+1}"
        
        desc = f"This is a room in {area_name}."
        
        script += f'''
# {room_name}
{room_id} = create_object(IOMRoom, key="{room_name}")
{room_id}.db.desc = "{desc}"
{room_id}.db.area = "{area_name}"
{room_id}.db.domain = "{domain_name}"
rooms["{room_id}"] = {room_id}
'''
    
    # Create exits
    for i, room in enumerate(rooms):
        room_id = f"room_{i}"
        for direction, target in room.get('exits', {}).items():
            target_idx = None
            for j, r in enumerate(rooms):
                if r['row'] == target[0] and r['col'] == target[1]:
                    target_idx = j
                    break
            
            if target_idx is not None:
                target_id = f"room_{target_idx}"
                script += f'''
# Exit from {room_id} to {target_id} ({direction})
exit_{i}_{direction} = create_object(IOMExit, key="{direction}")
exit_{i}_{direction}.aliases.add("{direction}")
exit_{i}_{direction}.location = {room_id}
exit_{i}_{direction}.destination = {target_id}
'''
    
    # Add entry/exit points
    for i, room in enumerate(rooms):
        if room.get('is_exit'):
            script += f'''
# Exit to parent domain
exit_parent = create_object(IOMExit, key="out")
exit_parent.aliases.add("out")
exit_parent.location = room_{i}
exit_parent.destination = None  # Link to parent area room
'''
    
    script += f'''
print("Created {{len(rooms)}} rooms in {area_name}")
'''
    
    return script


def process_map_file(filepath, domain_name):
    """Process a single map HTML file."""
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()
    
    area_name, island, coder, rooms, lines = parse_map(html)
    if not rooms:
        return None
    
    area_key = Path(filepath).stem
    script = generate_evennia_script(area_name, island, coder, rooms, lines, domain_name, area_key)
    
    return {
        'area_name': area_name,
        'island': island,
        'coder': coder,
        'room_count': len(rooms),
        'rooms': rooms,
        'script': script,
        'area_key': area_key,
    }


def process_domain(domain_dir):
    """Process all maps in a domain directory."""
    domain_path = Path(domain_dir)
    domain_name = domain_path.name
    
    results = []
    for html_file in sorted(domain_path.glob('*.html')):
        if html_file.name == 'index.html':
            continue
        
        result = process_map_file(str(html_file), domain_name)
        if result:
            results.append(result)
            print(f"  ✓ {html_file.name}: {result['area_name']} ({result['room_count']} rooms)")
        else:
            print(f"  ✗ {html_file.name}: No rooms found")
    
    return results


def main():
    maps_dir = Path('/root/.openclaw/workspace/reddragon/docs/maps')
    output_dir = Path('/root/.openclaw/workspace/reddragon/world/maps_generated')
    output_dir.mkdir(exist_ok=True)
    
    total_rooms = 0
    total_areas = 0
    
    # Process each domain
    for domain_dir in sorted(maps_dir.iterdir()):
        if not domain_dir.is_dir():
            continue
        if domain_dir.name.startswith('.'):
            continue
        
        print(f"\n{'='*60}")
        print(f"Processing: {domain_dir.name}")
        print(f"{'='*60}")
        
        results = process_domain(str(domain_dir))
        
        # Generate build script for this domain
        if results:
            domain_script = f'''# -*- coding: utf-8 -*-
"""
{domain_dir.name.upper()} Domain - Auto-generated build script
Generated from IOM map archive
"""

'''
            for result in results:
                domain_script += f"# === {result['area_name']} ===\n"
                domain_script += result['script']
                domain_script += "\n\n"
                total_rooms += result['room_count']
                total_areas += 1
            
            output_file = output_dir / f"{domain_dir.name}.py"
            with open(output_file, 'w') as f:
                f.write(domain_script)
            
            print(f"  → Generated: {output_file}")
    
    print(f"\n{'='*60}")
    print(f"SUMMARY: {total_areas} areas, {total_rooms} rooms")
    print(f"{'='*60}")


if __name__ == '__main__':
    main()
