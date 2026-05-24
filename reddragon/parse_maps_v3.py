#!/usr/bin/env python3
"""
IOM Map Parser v3 - Robust path-tracing for walkable worlds.

This parser traces connections between + rooms through valid path chars,
handling variable spacing and complex ASCII art.
"""

import json
import re
from pathlib import Path

VALID_PATH_CHARS = set('-|/~=\\,\'` ')
DIRECTIONS = {
    'north': (-1, 0),
    'south': (1, 0),
    'west': (0, -1),
    'east': (0, 1),
    'northwest': (-1, -1),
    'northeast': (-1, 1),
    'southwest': (1, -1),
    'southeast': (1, 1),
}

def extract_map_data(html_content):
    """Extract pre-formatted ASCII map from HTML."""
    pattern = re.compile(r'<pre[^>]*>(.*?)</pre>', re.DOTALL | re.IGNORECASE)
    matches = pattern.findall(html_content)
    if not matches:
        return None, None, None, []
    
    raw = matches[0]
    # Clean HTML entities
    raw = raw.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
    lines = raw.split('\n')
    
    # Extract header info from first 10 lines
    area_name, island, coder = "Unknown", "Unknown", "Unknown"
    for line in lines[:15]:
        if 'Area' in line and ':' in line:
            area_name = line.split(':', 1)[1].strip()
        elif 'Island' in line and ':' in line:
            island = line.split(':', 1)[1].strip()
        elif 'Coder' in line and ':' in line:
            coder = line.split(':', 1)[1].strip()
    
    # Find all + positions (rooms)
    rooms = {}  # (row, col) -> room_id
    for row_idx, line in enumerate(lines):
        for col_idx, char in enumerate(line):
            if char == '+':
                rooms[(row_idx, col_idx)] = len(rooms)
    
    return area_name, island, coder, lines, rooms


def trace_path(lines, start_row, start_col, dr, dc, room_positions):
    """
    Trace from a room in direction (dr, dc) looking for another room.
    Returns the target room position if found, None otherwise.
    """
    row, col = start_row + dr, start_col + dc
    max_dist = 20  # Maximum distance to search
    
    for dist in range(1, max_dist + 1):
        if row < 0 or row >= len(lines) or col < 0:
            return None
        
        line = lines[row] if row < len(lines) else ""
        
        if col >= len(line):
            return None
        
        char = line[col]
        
        # Found a room!
        if char == '+' and (row, col) in room_positions:
            # Verify the path between is valid
            if is_valid_path(lines, start_row, start_col, row, col, dr, dc):
                return (row, col)
            return None
        
        # Path must only contain valid chars
        if char not in VALID_PATH_CHARS and char != '+':
            # Hit a wall/invalid char
            return None
        
        row += dr
        col += dc
    
    return None


def is_valid_path(lines, r1, c1, r2, c2, dr, dc):
    """Verify all chars between two points are valid path chars."""
    row, col = r1 + dr, c1 + dc
    while (row, col) != (r2, c2):
        if row < 0 or row >= len(lines):
            return False
        line = lines[row] if row < len(lines) else ""
        if col < 0 or col >= len(line):
            return False
        char = line[col]
        if char not in VALID_PATH_CHARS:
            return False
        row += dr
        col += dc
    return True


def find_room_name(lines, row, col, room_positions):
    """
    Find the name for a room by looking at nearby text.
    Strategy:
    1. Look for legend abbreviations (single/two letters near room)
    2. Look for text in the room's row
    3. Look for text nearby
    """
    # First, check if there's a single letter abbreviation near the room
    # These are usually 1-3 chars, placed right next to the room
    
    # Search in a small radius
    best_name = None
    best_score = 0
    
    for r in range(max(0, row - 3), min(len(lines), row + 4)):
        line = lines[r] if r < len(lines) else ""
        for c in range(max(0, col - 6), min(len(line), col + 7)):
            if (r, c) in room_positions and (r, c) != (row, col):
                continue  # Skip other rooms
            
            # Extract word at this position
            if c >= len(line):
                continue
            ch = line[c]
            if not (ch.isalpha() or ch in " '-_"):
                continue
            
            # Get the word
            start, end = c, c
            while start > 0 and (line[start - 1].isalpha() or line[start - 1] in " '-_"):
                start -= 1
            while end < len(line) and (line[end].isalpha() or line[end] in " '-_"):
                end += 1
            
            word = line[start:end].strip()
            if not word or len(word) < 2 or len(word) > 20:
                continue
            
            # Skip common non-name words
            lower = word.lower()
            if lower in ('out', 'portal', 'and', 'the', 'of', 'to', 'area', 'island', 'coder'):
                continue
            
            # Skip path-like text
            if set(word) <= set('-=~|'):
                continue
            
            # Calculate distance score
            dist = abs(r - row) + abs(c - col)
            
            # Prefer shorter words closer to room (likely abbreviations)
            # But also accept longer descriptive names
            if len(word) <= 3 and dist <= 3:
                score = 100 - dist * 10 + 50  # High score for abbreviations
            elif dist <= 4:
                score = 100 - dist * 15
            else:
                score = 0
            
            # Don't pick text that's between two rooms (it's a path label)
            if r == row:
                left_room = any((r, x) in room_positions for x in range(start, col))
                right_room = any((r, x) in room_positions for x in range(col + 1, end + 1))
                if left_room and right_room:
                    score = 0  # This is a path label, not a room name
            
            if score > best_score:
                best_name = word
                best_score = score
    
    return best_name


def parse_map(lines, room_positions):
    """Parse exits and names for all rooms."""
    rooms_data = {}
    
    for (row, col), room_id in room_positions.items():
        room_info = {
            'row': row,
            'col': col,
            'name': None,
            'exits': {},
            'is_entry': False,
            'is_exit': False,
            'has_portal': False,
        }
        
        # Find exits
        for direction, (dr, dc) in DIRECTIONS.items():
            target = trace_path(lines, row, col, dr, dc, room_positions)
            if target:
                target_id = room_positions[target]
                room_info['exits'][direction] = target_id
        
        # Find name
        name = find_room_name(lines, row, col, room_positions)
        if name:
            room_info['name'] = name
        else:
            room_info['name'] = f"Room_{row}_{col}"
        
        # Check for special markers
        for r in range(max(0, row - 2), min(len(lines), row + 3)):
            line = lines[r] if r < len(lines) else ""
            lower_line = line.lower()
            if 'out' in lower_line:
                pos = lower_line.find('out')
                if abs(pos - col) < 5 and abs(r - row) < 3:
                    room_info['is_exit'] = True
            if 'portal' in lower_line or ' p ' in lower_line:
                for i in range(len(line)):
                    if line[i:i+3] == ' P ' or line[i:i+2] == '-P':
                        if abs(i - col) < 5 and abs(r - row) < 3:
                            room_info['has_portal'] = True
        
        rooms_data[room_id] = room_info
    
    return rooms_data


def process_all_maps():
    maps_dir = Path('/root/.openclaw/workspace/reddragon/docs/maps')
    output_dir = Path('/root/.openclaw/workspace/reddragon/world/map_data')
    output_dir.mkdir(exist_ok=True)
    
    total_areas, total_rooms = 0, 0
    failed = []
    
    for domain_dir in sorted(maps_dir.iterdir()):
        if not domain_dir.is_dir() or domain_dir.name.startswith('.'):
            continue
        
        domain_name = domain_dir.name
        domain_data = {}
        
        for html_file in sorted(domain_dir.glob('*.html')):
            if html_file.name == 'index.html':
                continue
            
            with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
                html = f.read()
            
            result = extract_map_data(html)
            if not result or not result[3]:
                failed.append(f"{domain_name}/{html_file.name}")
                continue
            
            area_name, island, coder, lines, room_positions = result
            
            if not room_positions:
                failed.append(f"{domain_name}/{html_file.name}")
                continue
            
            rooms_data = parse_map(lines, room_positions)
            
            # Count rooms with exits
            rooms_with_exits = sum(1 for r in rooms_data.values() if r['exits'])
            
            domain_data[html_file.stem] = {
                'area_name': area_name,
                'island': island,
                'coder': coder,
                'rooms': rooms_data,
                'stats': {
                    'total_rooms': len(rooms_data),
                    'rooms_with_exits': rooms_with_exits,
                    'rooms_without_exits': len(rooms_data) - rooms_with_exits,
                }
            }
            
            total_areas += 1
            total_rooms += len(rooms_data)
        
        # Save
        json_path = output_dir / f"{domain_name}.json"
        with open(json_path, 'w') as f:
            json.dump(domain_data, f, indent=2)
        
        areas_with_exits = sum(1 for a in domain_data.values() if a['stats']['rooms_with_exits'] > 0)
        print(f"  ✓ {domain_name}: {len(domain_data)} areas, {total_rooms} rooms, {areas_with_exits} areas with exits")
    
    print(f"\n{'='*60}")
    print(f"TOTAL: {total_areas} areas, {total_rooms} rooms")
    if failed:
        print(f"FAILED ({len(failed)}): {', '.join(failed[:10])}")
    print(f"{'='*60}")


if __name__ == '__main__':
    process_all_maps()
