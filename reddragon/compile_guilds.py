#!/usr/bin/env python3
"""
Compile all IOM guild pages into a structured guild_database.py
"""

import os
import re
import glob

GUILDS_DIR = "/root/.openclaw/workspace/reddragon/docs/guilds"
OUTPUT_FILE = "/root/.openclaw/workspace/reddragon/world/guild_database.py"

# Define guild trees structure
GUILD_TREES = {
    "warrior": {
        "alpha": ["warrior"],
        "beta": ["knight", "defender_of_the_crown", "berserker", "traveler"],
        "gamma": ["blade_dancer", "barbarian", "shield_master", "flogger", "thruster", "champion_of_the_crown"]
    },
    "martial_artist": {
        "alpha": ["martial_artist"],
        "beta": ["dragonfist", "mystic", "traveler", "fighter", "warriors"],
        "gamma": ["toad_master", "tiger_master", "crane_master", "snake_master", "order_of_the_crescent_moon", "dragon_master"]
    },
    "acrobat": {
        "alpha": ["acrobat"],
        "beta": ["street_brawler", "juggler", "bard", "traveler"],
        "gamma": ["minstrel", "bartender", "bannerman", "gleeman", "troubadour"]
    },
    "abjurer": {
        "alpha": ["abjurer"],
        "beta": ["protector_of_the_earth", "masters_of_energy", "irrifletta", "navigator", "traveler"],
        "gamma": ["master_abjurer", "harbinger_of_anguish", "enchanter", "master_navigators", "master_of_disruption", "guardians"]
    },
    "psychics": {
        "alpha": ["psychics"],
        "beta": ["mystics", "witch", "telekinetics", "traveler", "navigator"],
        "gamma": ["cauldron_magic", "oneiromancers", "watchers_of_the_night", "psionists", "enchanter", "master_navigators"],
        "delta": ["talisman_magic"]
    },
    "elemental": {
        "alpha": ["elemental"],
        "beta": ["fire_mage", "earth_mage", "air_mage", "water_mage", "navigator", "traveler"],
        "gamma": ["lava_mage", "mist_mage", "enchanter", "master_navigators", "nether_mage"]
    },
    "necromancer": {
        "alpha": ["necromancer"],
        "beta": ["traveler", "necroscope", "voodooist", "bone_mage", "navigator"],
        "gamma": ["stygian_sorcerer", "embalmer", "dreadlord", "scourge", "enchanter", "master_navigators"],
        "delta": ["lords_of_undeath", "blood_brother"]
    },
    "evoker": {
        "alpha": ["evoker"],
        "beta": ["evoker_of_elements", "evoker_of_ether", "traveler", "navigator"],
        "gamma": ["evoker_of_magic", "evoker_of_vacuum", "evoker_of_flames", "evoker_of_force"],
        "delta": ["evoker_of_poison", "evoker_of_acid", "evoker_of_lightning", "evoker_of_ice"],
        "epsilon": ["enchanter", "master_navigators", "sorcerer"]
    },
    "weaver": {
        "alpha": ["weaver"],
        "beta": ["healer", "martyr", "confessor", "navigator", "traveler"],
        "gamma": ["avatar", "exorcist", "templar", "shields_of_faith", "enchanter", "master_navigators"],
        "delta": ["high_priest"]
    },
    "unraveller": {
        "alpha": ["unraveller"],
        "beta": ["harmer", "sacrificer", "magical_torturer", "traveler", "navigator"],
        "gamma": ["servant_of_mordulak", "servant_of_shirija", "servant_of_talakh", "servant_of_lloth"],
        "delta": ["enchanter", "master_navigator"],
        "epsilon": ["elder_of_mordulak", "patriarch_of_shirija", "sword_of_talakh", "primate_of_lloth", "master_enchanter"]
    },
    "druid": {
        "alpha": ["druid"],
        "beta": ["weather_watcher", "animal_tamer", "herbalist", "traveler"],
        "gamma": ["adept_of_the_stones", "enchanter", "shaman_of_soil"],
        "delta": ["chanter_of_deep_earth"]
    },
    "shapeshifter": {
        "alpha": ["shapeshifter"],
        "beta": ["bestial_seccedaneum", "savager", "animal_tamer", "traveler"],
        "gamma": ["animal_healer", "animal_trainer", "beast_lord", "dragon_lord"]
    },
    "woodsman": {
        "alpha": ["woodsman"],
        "beta": ["sylvan_guard", "sylvan_ward", "animal_tamer", "herbalist", "traveler"],
        "gamma": ["sylvan_scout", "sylvan_protector", "sylvan_woodlord"]
    },
    "lurker": {
        "alpha": ["lurker"],
        "beta": ["street_brawler", "poison_brewer", "trickster", "traveler"],
        "gamma": ["assassin", "bartender", "master_assassin", "disciple_of_shadow"],
        "delta": ["silent_hand"]
    }
}


def parse_guild_file(filepath):
    """Parse a single guild HTML file and extract structured data."""
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    guild_id = os.path.basename(filepath).replace('.md', '')
    
    # Extract guild name and level from header
    header_match = re.search(
        r'Guild info on ([^.]+)\.\s+A\s+(\w+) level',
        content,
        re.IGNORECASE
    )
    guild_name = header_match.group(1).strip() if header_match else guild_id.replace('_', ' ')
    guild_level = header_match.group(2).lower() if header_match else "unknown"
    
    # Extract description (the <p> tag after the header table)
    desc_match = re.search(r'</pre>\s*<p>\s*(.*?)\s*</p>', content, re.DOTALL | re.IGNORECASE)
    description = re.sub(r'<[^>]+>', '', desc_match.group(1)) if desc_match else ""
    description = re.sub(r'\s+', ' ', description).strip()
    
    # Extract level progression table
    progression = []
    prog_pattern = re.findall(
        r'\[Level\s+(\d+)\]\s*\n\s*New\s+(Skills?|Spells?):\s*(.*?)\s*\n',
        content
    )
    for level, kind, items in prog_pattern:
        # Split multiple skills/spells on "and"
        item_names = re.findall(r'<a[^>]*>(.*?)</a>', items)
        if not item_names:
            item_names = [items.strip()]
        for name in item_names:
            clean_name = re.sub(r'<[^>]+>', '', name).strip()
            if clean_name:
                progression.append({
                    "guild_level": int(level),
                    "kind": "skill" if "skill" in kind.lower() else "spell",
                    "name": clean_name
                })
    
    # Extract detailed skill/spell entries
    entries = []
    entry_blocks = re.findall(
        r'={60,}\s*Help on\s+(skill|spell)\s+:\s+(.+?)\s*'
        r'Guild Level\s+:\s+(\w+)\s*'
        r'(?:Skill|Spell) type\s+:\s+(.+?)\s*'
        r'Base Experience Cost\s+:\s+(\d+)'
        r'={60,}\s*'
        r'(.*?)(?=={60,}|\Z)',
        content,
        re.DOTALL | re.IGNORECASE
    )
    
    for kind, name, entry_level, entry_type, cost, desc in entry_blocks:
        clean_desc = re.sub(r'<[^>]+>', '', desc)
        clean_desc = re.sub(r'\s+', ' ', clean_desc).strip()
        entries.append({
            "kind": kind.lower(),
            "name": name.strip(),
            "guild_level": entry_level.lower(),
            "type": entry_type.strip(),
            "cost": int(cost),
            "description": clean_desc
        })
    
    return {
        "id": guild_id,
        "name": guild_name,
        "level": guild_level,
        "description": description,
        "progression": progression,
        "entries": entries
    }


def main():
    files = sorted(glob.glob(os.path.join(GUILDS_DIR, "*.md")))
    print(f"Found {len(files)} guild files to process")
    
    all_guilds = {}
    total_skills = 0
    total_spells = 0
    
    for filepath in files:
        guild_id = os.path.basename(filepath).replace('.md', '')
        try:
            data = parse_guild_file(filepath)
            all_guilds[guild_id] = data
            total_skills += len([e for e in data["entries"] if e["kind"] == "skill"])
            total_spells += len([e for e in data["entries"] if e["kind"] == "spell"])
        except Exception as e:
            print(f"ERROR parsing {guild_id}: {e}")
            continue
    
    # Build the output
    lines = [
        '#!/usr/bin/env python3',
        '"""',
        'Islands of Myth - Complete Guild Database',
        'Auto-generated from http://www.islandsofmyth.org/3k/cgi/guildtree.c',
        f'Generated: 2026-05-24',
        f'Total guilds: {len(all_guilds)}',
        f'Total skills documented: {total_skills}',
        f'Total spells documented: {total_spells}',
        '"""',
        '',
        'GUILD_TREES = {',
    ]
    
    for tree_name, tiers in GUILD_TREES.items():
        lines.append(f'    "{tree_name}": {{')
        for tier, guilds in tiers.items():
            glist = ', '.join(f'"{g}"' for g in guilds)
            lines.append(f'        "{tier}": [{glist}],')
        lines.append('    },')
    lines.append('}')
    lines.append('')
    
    lines.append('GUILD_DATA = {')
    for gid, data in sorted(all_guilds.items()):
        lines.append(f'    "{gid}": {{')
        lines.append(f'        "name": "{data["name"]}",')
        lines.append(f'        "level": "{data["level"]}",')
        lines.append(f'        "description": """{data["description"]}""",')
        
        # Progression
        lines.append('        "progression": [')
        for p in data["progression"]:
            lines.append(f'            {{"guild_level": {p["guild_level"]}, "kind": "{p["kind"]}", "name": "{p["name"]}"}},')
        lines.append('        ],')
        
        # Entries
        lines.append('        "entries": [')
        for e in data["entries"]:
            desc = e["description"].replace('"', '\\"').replace('\n', ' ')
            lines.append(f'            {{')
            lines.append(f'                "kind": "{e["kind"]}",')
            lines.append(f'                "name": "{e["name"]}",')
            lines.append(f'                "guild_level": "{e["guild_level"]}",')
            lines.append(f'                "type": "{e["type"]}",')
            lines.append(f'                "cost": {e["cost"]},')
            lines.append(f'                "description": "{desc}",')
            lines.append(f'            }},')
        lines.append('        ],')
        lines.append('    },')
    lines.append('}')
    lines.append('')
    
    # Add helper functions
    lines.extend([
        '',
        'def get_guild(guild_id):',
        '    """Get guild data by ID."""',
        '    return GUILD_DATA.get(guild_id)',
        '',
        'def get_tree(tree_name):',
        '    """Get all guilds in a tree."""',
        '    tree = GUILD_TREES.get(tree_name, {})',
        '    result = []',
        '    for tier, guilds in tree.items():',
        '        for gid in guilds:',
        '            data = GUILD_DATA.get(gid)',
        '            if data:',
        '                result.append({"id": gid, "tier": tier, **data})',
        '    return result',
        '',
        'def get_skill(spell_name, guild_id=None):',
        '    """Search for a skill/spell by name across all guilds."""',
        '    results = []',
        '    for gid, data in GUILD_DATA.items():',
        '        if guild_id and gid != guild_id:',
        '            continue',
        '        for entry in data.get("entries", []):',
        '            if entry["name"].lower() == spell_name.lower():',
        '                results.append({"guild": gid, **entry})',
        '    return results',
        '',
        'def list_all_skills():',
        '    """Return a flat list of all skills/spells with guild info."""',
        '    results = []',
        '    for gid, data in GUILD_DATA.items():',
        '        for entry in data.get("entries", []):',
        '            results.append({"guild": gid, "guild_name": data["name"], **entry})',
        '    return results',
        '',
        'if __name__ == "__main__":',
        '    print(f"Loaded {len(GUILD_DATA)} guilds from {len(GUILD_TREES)} trees")',
    ])
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    print(f"\nDone! Compiled {len(all_guilds)} guilds into {OUTPUT_FILE}")
    print(f"  Skills: {total_skills}")
    print(f"  Spells: {total_spells}")
    print(f"  Total entries: {total_skills + total_spells}")


if __name__ == "__main__":
    main()
