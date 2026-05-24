#!/usr/bin/env python3
"""
Generate Map Builder modules for all IOM domains
"""

import os

def generate_domain_module(domain_name, map_content):
    """Generate a Python module with MAP and LEGEND for a domain."""
    
    # Clean up the map content
    lines = map_content.strip().split('\n')
    # Remove title lines if present
    cleaned_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped and not stripped.startswith('IoM') and not stripped.startswith(domain_name.title()):
            cleaned_lines.append(line.rstrip())
    
    map_string = '\n'.join(cleaned_lines)
    
    # Standard IOM terrain legend
    legend = """from world.maps.terrain import (
    build_water, build_beach, build_forest, build_deep_forest,
    build_hills, build_mountains, build_desert, build_swamp,
    build_marsh, build_road, build_plains, build_city,
    build_building, build_lake, build_dungeon, build_crossing,
    build_valley
)

# Terrain character mapping for IOM ASCII maps
{domain_upper}_LEGEND = {{
    "W": build_water,       # Ocean
    "~": build_water,       # Ocean (alternative)
    "b": build_beach,       # Beach/Coast
    "f": build_forest,      # Forest
    "F": build_deep_forest, # Deep Forest
    "h": build_hills,       # Hills
    "H": build_hills,       # Hills (alternative)
    "M": build_mountains,   # Mountains
    "d": build_desert,      # Desert
    "s": build_swamp,       # Swamp
    "S": build_swamp,       # Swamp (alternative)
    "m": build_marsh,       # Marsh
    "R": build_road,        # Road
    "p": build_plains,      # Plains/Path
    "P": build_plains,      # Plains (alternative)
    "c": build_city,        # City
    "C": build_city,        # City (alternative)
    "B": build_building,    # Building/Castle
    "L": build_lake,        # Lake
    "#": build_dungeon,     # Dungeon/Tower
    "+": build_crossing,    # Crossing/Intersection
    "|": build_road,        # Road vertical
    "-": build_road,        # Road horizontal
    "=": build_road,        # Bridge/Road special
    "\\\\": build_road,      # Road diagonal
    "/": build_road,        # Road diagonal
    "^": build_mountains,  # Mountain peak
    "v": build_valley,     # Valley
    "V": build_valley,     # Valley (alternative)
}}
""".format(domain_upper=domain_name.upper())
    
    module_content = f'"""\nRed Dragon MUD - {domain_name.title()} Domain Map\nGenerated from IOM ASCII map\n\nUsage:\n    @mapbuilder world.maps.{domain_name}.{domain_name.upper()}_MAP world.maps.{domain_name}.{domain_name.upper()}_LEGEND\n"""\n\n{domain_name.upper()}_MAP = r\'\'\'\n{map_string}\n\'\'\'\n\n{legend}\n'
    
    return module_content

# Process all maps
map_dir = "/root/.openclaw/workspace/reddragon/world/maps"
iom_map_dir = "/root/.openclaw/workspace/reddragon/world/maps"

for domain in ["blackavar", "gossamer", "sombre", "darkcaverns", "hyboria",
               "southcape", "emerald", "mists", "twin_islands", "everrest", "oddworld"]:
    map_file = os.path.join(iom_map_dir, f"{domain}_map.txt")
    if os.path.exists(map_file):
        with open(map_file, 'r') as f:
            content = f.read()
        
        module_content = generate_domain_module(domain, content)
        
        output_file = os.path.join(map_dir, f"{domain}.py")
        with open(output_file, 'w') as f:
            f.write(module_content)
        
        print(f"Generated {domain}.py ({len(content)} chars)")
    else:
        print(f"Missing: {map_file}")

print("\nAll domain modules generated!")
print(f"Location: {map_dir}")
