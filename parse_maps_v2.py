#!/usr/bin/env python3
"""
IOM Map Parser v2 - Produces clean structured data for Evennia integration.
"""

import os
import re
import json
from pathlib import Path

def extract_pre_text(html_content):
    pattern = re.compile(r'<pre[^>]*>(.*?)</pre>', re.DOTALL | re.IGNORECASE)
    matches = pattern.findall(html_content)
    return max(matches, key=len) if matches else ""

def clean_html(text):
    clean = re.sub(r'<[^>]+>', '', text)
    clean = clean.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
    return clean

def parse_ascii_map(raw_text):
    lines = raw_text.split('\n')
    
    # Header
    area_name, island, coder = "Unknown", "Unknown", "Unknown"
    for line in lines[:10]:
        if 'Area' in line and ':' in line:
            area_name = line.split(':', 1)[1].strip()
        elif 'Island' in line and ':' in line:
            island = line.split(':', 1)[1].strip()
        elif 'Coder' in line and ':' in line:
            coder = line.split(':', 1)[1].strip()
    
    # Find grid lines (lines containing + and connections)
    grid_lines = []
    for i, line in enumerate(lines):
        if '+' in line and any(c in line for c in '-|/~=\\'):
            grid_lines.append((i, line))
    
    if not grid_lines:
        return None
    
    # Parse rooms
    rooms = {}  # (row, col) -> room_data
    for row_idx, line in grid_lines:
        for col_idx, char in enumerate(line):
            if char == '+':
                rooms[(row_idx, col_idx)] = {
                    'row': row_idx, 'col': col_idx,
                    'name': None, 'exits': {},
                    'is_entry': False, 'is_exit': False,
                    'has_portal': False
                }
    
    # Parse connections
    directions = {
        (-1, 0): 'north', (1, 0): 'south',
        (0, -1): 'west', (0, 1): 'east',
        (-1, -1): 'northwest', (-1, 1): 'northeast',
        (1, -1): 'southwest', (1, 1): 'southeast',
    }
    
    for key, room in rooms.items():
        row, col = room['row'], room['col']
        for (dr, dc), direction in directions.items():
            target = f"{row + dr},{col + dc}"
            if target in rooms:
                room['exits'][direction] = target
                continue
            target2 = f"{row + dr * 2},{col + dc * 2}"
            if target2 in rooms:
                mid = (row + dr, col + dc)
                if mid[0] < len(lines) and mid[1] < len(lines[mid[0]]):
                    mid_char = lines[mid[0]][mid[1]]
                    if mid_char in '-|/~=\\' or mid_char.isspace():
                        room['exits'][direction] = target2
    
    # Extract room names from nearby text
    for (row, col), room in rooms.items():
        best_name, best_dist = None, float('inf')
        
        for r in range(max(0, row-3), min(len(lines), row+4)):
            for c in range(max(0, col-8), min(len(lines[r]), col+9)):
                if (r, c) in rooms and (r, c) != (row, col):
                    continue
                
                dist = abs(r - row) + abs(c - col)
                if dist >= best_dist:
                    continue
                
                ch = lines[r][c] if c < len(lines[r]) else ' '
                if not (ch.isalpha() or ch in " '-_"):
                    continue
                
                # Extract word
                start, end = c, c
                line = lines[r]
                while start > 0 and (line[start-1].isalpha() or line[start-1] in " '-_"):
                    start -= 1
                while end < len(line) and (line[end].isalpha() or line[end] in " '-_"):
                    end += 1
                
                word = line[start:end].strip()
                if not word or len(word) < 2:
                    continue
                if word.lower() in ('out', 'p', 'portal', 'and', 'the', 'of'):
                    continue
                
                # Skip if text is between two rooms (it's a path label)
                is_path = False
                if r == row:
                    left_room = any((r, x) in rooms for x in range(start, col))
                    right_room = any((r, x) in rooms for x in range(col+1, end+1))
                    if left_room and right_room:
                        is_path = True
                
                if not is_path:
                    best_name = word
                    best_dist = dist
        
        room['name'] = best_name.title() if best_name else f"Room_{row}_{col}"
    
    # Detect special markers
    for key, room in rooms.items():
        row, col = room['row'], room['col']
        for r in range(max(0, row-2), min(len(lines), row+3)):
            line = lines[r] if r < len(lines) else ""
            # Exit marker
            if 'out' in line.lower():
                pos = line.lower().find('out')
                if abs(pos - col) < 4 and abs(r - row) < 3:
                    room['is_exit'] = True
            # Portal marker
            if 'portal' in line.lower() or ('P' in line and 'P' in raw_text):
                for i, ch in enumerate(line):
                    if ch == 'P':
                        if abs(i - col) < 4 and abs(r - row) < 3:
                            room['has_portal'] = True
    
    return {
        'area_name': area_name,
        'island': island,
        'coder': coder,
        'rooms': {f"{k[0]},{k[1]}": v for k, v in rooms.items()},
        'grid_lines': len(grid_lines)
    }

def process_all_maps():
    maps_dir = Path('/root/.openclaw/workspace/reddragon/docs/maps')
    output_dir = Path('/root/.openclaw/workspace/reddragon/world/map_data')
    output_dir.mkdir(exist_ok=True)
    
    total_areas, total_rooms = 0, 0
    failed = []
    
    for domain_dir in sorted(maps_dir.iterdir()):
        if not domain_dir.is_dir() or domain_dir.name.startswith('.'):
            continue
        
        domain_data = {}
        domain_name = domain_dir.name
        
        for html_file in sorted(domain_dir.glob('*.html')):
            if html_file.name == 'index.html':
                continue
            
            with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
                html = f.read()
            
            pre_text = extract_pre_text(html)
            raw = clean_html(pre_text)
            result = parse_ascii_map(raw)
            
            if not result or not result['rooms']:
                failed.append(f"{domain_name}/{html_file.name}")
                continue
            
            area_key = html_file.stem
            domain_data[area_key] = result
            total_areas += 1
            total_rooms += len(result['rooms'])
        
        # Save per-domain JSON
        json_path = output_dir / f"{domain_name}.json"
        with open(json_path, 'w') as f:
            json.dump(domain_data, f, indent=2)
        print(f"  ✓ {domain_name}: {len(domain_data)} areas saved to {json_path}")
    
    print(f"\n{'='*60}")
    print(f"TOTAL: {total_areas} areas, {total_rooms} rooms")
    if failed:
        print(f"FAILED ({len(failed)}): {', '.join(failed[:5])}")
    print(f"{'='*60}")

if __name__ == '__main__':
    process_all_maps()
