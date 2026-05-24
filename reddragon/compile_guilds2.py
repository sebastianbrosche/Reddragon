#!/usr/bin/env python3
"""
Compile all IOM guild pages into guild_database.py
Writes directly to file to avoid memory issues.
"""

import os
import re
import glob

GUILDS_DIR = "/root/.openclaw/workspace/reddragon/docs/guilds"
OUTPUT_FILE = "/root/.openclaw/workspace/reddragon/world/guild_database.py"

def parse_guild_file(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    guild_id = os.path.basename(filepath).replace('.md', '')
    
    # Extract guild name and level
    header_match = re.search(
        r'Guild info on ([^.]+)\.\s+A\s+(\w+) level',
        content,
        re.IGNORECASE
    )
    guild_name = header_match.group(1).strip() if header_match else guild_id.replace('_', ' ')
    guild_level = header_match.group(2).lower() if header_match else "unknown"
    
    # Extract description
    desc_match = re.search(r'\<\/pre\>\s*\<p\>\s*(.*?)\s*\<\/p\>', content, re.DOTALL | re.IGNORECASE)
    description = re.sub(r'\<[^\>]+\>', '', desc_match.group(1)) if desc_match else ""
    description = re.sub(r'\s+', ' ', description).strip()
    description = description.replace('\\', '\\\\').replace('"', '\\"').replace("'", "\\'")
    
    # Extract level progression
    progression = []
    prog_pattern = re.findall(
        r'\[Level\s+(\d+)\]\s*\n\s*New\s+(Skills?|Spells?):\s*(.*?)\s*\n',
        content
    )
    for level, kind, items in prog_pattern:
        item_names = re.findall(r'\<a[^\>]*\>(.*?)\<\/a\>', items)
        if not item_names:
            item_names = [items.strip()]
        for name in item_names:
            clean_name = re.sub(r'\<[^\>]+\>', '', name).strip()
            clean_name = clean_name.replace('"', '\\"')
            if clean_name:
                progression.append({
                    "guild_level": int(level),
                    "kind": "skill" if "skill" in kind.lower() else "spell",
                    "name": clean_name
                })
    
    # Extract detailed entries
    entries = []
    entry_blocks = re.findall(
        r'={40,}\s*Help on\s+(skill|spell)\s+:\s+(.+?)\s*'
        r'Guild Level\s+:\s+(\w+)\s*'
        r'(?:Skill|Spell) type\s+:\s+(.+?)\s*'
        r'Base Experience Cost\s+:\s+(\d+)'
        r'={40,}\s*'
        r'(.*?)(?=={40,}|\Z)',
        content,
        re.DOTALL | re.IGNORECASE
    )
    
    for kind, name, entry_level, entry_type, cost, desc in entry_blocks:
        clean_desc = re.sub(r'\<[^\>]+\>', '', desc)
        clean_desc = re.sub(r'\s+', ' ', clean_desc).strip()
        clean_desc = clean_desc.replace('\\', '\\\\').replace('"', '\\"').replace("'", "\\'")
        entries.append({
            "kind": kind.lower(),
            "name": name.strip().replace('"', '\\"'),
            "guild_level": entry_level.lower(),
            "type": entry_type.strip().replace('"', '\\"'),
            "cost": int(cost),
            "description": clean_desc
        })
    
    return {
        "id": guild_id,
        "name": guild_name.replace('"', '\\"'),
        "level": guild_level,
        "description": description,
        "progression": progression,
        "entries": entries
    }


def write_guild_data(f, data):
    f.write(f'    "{data["id"]}": {{\n')
    f.write(f'        "name": "{data["name"]}",\n')
    f.write(f'        "level": "{data["level"]}",\n')
    f.write(f'        "description": "{data["description"][:500]}",\n')
    
    f.write('        "progression": [\n')
    for p in data["progression"]:
        f.write(f'            {{"guild_level": {p["guild_level"]}, "kind": "{p["kind"]}", "name": "{p["name"]}"}},\n')
    f.write('        ],\n')
    
    f.write('        "entries": [\n')
    for e in data["entries"]:
        desc = e["description"][:300]  # Truncate to keep file manageable
        f.write(f'            {{\n')
        f.write(f'                "kind": "{e["kind"]}",\n')
        f.write(f'                "name": "{e["name"]}",\n')
        f.write(f'                "guild_level": "{e["guild_level"]}",\n')
        f.write(f'                "type": "{e["type"]}",\n')
        f.write(f'                "cost": {e["cost"]},\n')
        f.write(f'                "description": "{desc}",\n')
        f.write(f'            }},\n')
    f.write('        ],\n')
    f.write('    },\n')


def main():
    files = sorted(glob.glob(os.path.join(GUILDS_DIR, "*.md")))
    print(f"Found {len(files)} guild files")
    
    all_guilds = {}
    total_entries = 0
    
    for filepath in files:
        guild_id = os.path.basename(filepath).replace('.md', '')
        try:
            data = parse_guild_file(filepath)
            all_guilds[guild_id] = data
            total_entries += len(data["entries"])
            print(f"  Parsed {guild_id}: {len(data['progression'])} progression, {len(data['entries'])} entries")
        except Exception as e:
            print(f"  ERROR {guild_id}: {e}")
            import traceback
            traceback.print_exc()
    
    print(f"\nWriting {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write('#!/usr/bin/env python3\n')
        f.write('"""\n')
        f.write('Islands of Myth - Complete Guild Database\n')
        f.write(f'Auto-generated: 2026-05-24\n')
        f.write(f'Total guilds: {len(all_guilds)}\n')
        f.write(f'Total skill/spell entries: {total_entries}\n')
        f.write('"""\n\n')
        
        # GUILD_TREES
        f.write('GUILD_TREES = {\n')
        f.write('    "warrior": {"alpha": ["warrior"], "beta": ["knight", "defender_of_the_crown", "berserker", "traveler"], "gamma": ["blade_dancer", "barbarian", "shield_master", "flogger", "thruster", "champion_of_the_crown"]},\n')
        f.write('    "martial_artist": {"alpha": ["martial_artist"], "beta": ["dragonfist", "mystic", "traveler", "fighter", "warriors"], "gamma": ["toad_master", "tiger_master", "crane_master", "snake_master", "order_of_the_crescent_moon", "dragon_master"]},\n')
        f.write('    "acrobat": {"alpha": ["acrobat"], "beta": ["street_brawler", "juggler", "bard", "traveler"], "gamma": ["minstrel", "bartender", "bannerman", "gleeman", "troubadour"]},\n')
        f.write('    "abjurer": {"alpha": ["abjurer"], "beta": ["protector_of_the_earth", "masters_of_energy", "irrifletta", "navigator", "traveler"], "gamma": ["master_abjurer", "harbinger_of_anguish", "enchanter", "master_navigators", "master_of_disruption", "guardians"]},\n')
        f.write('    "psychics": {"alpha": ["psychics"], "beta": ["mystics", "witch", "telekinetics", "traveler", "navigator"], "gamma": ["cauldron_magic", "oneiromancers", "watchers_of_the_night", "psionists", "enchanter", "master_navigators"], "delta": ["talisman_magic"]},\n')
        f.write('    "elemental": {"alpha": ["elemental"], "beta": ["fire_mage", "earth_mage", "air_mage", "water_mage", "navigator", "traveler"], "gamma": ["lava_mage", "mist_mage", "enchanter", "master_navigators", "nether_mage"]},\n')
        f.write('    "necromancer": {"alpha": ["necromancer"], "beta": ["traveler", "necroscope", "voodooist", "bone_mage", "navigator"], "gamma": ["stygian_sorcerer", "embalmer", "dreadlord", "scourge", "enchanter", "master_navigators"], "delta": ["lords_of_undeath", "blood_brother"]},\n')
        f.write('    "evoker": {"alpha": ["evoker"], "beta": ["evoker_of_elements", "evoker_of_ether", "traveler", "navigator"], "gamma": ["evoker_of_magic", "evoker_of_vacuum", "evoker_of_flames", "evoker_of_force"], "delta": ["evoker_of_poison", "evoker_of_acid", "evoker_of_lightning", "evoker_of_ice"], "epsilon": ["enchanter", "master_navigators", "sorcerer"]},\n')
        f.write('    "weaver": {"alpha": ["weaver"], "beta": ["healer", "martyr", "confessor", "navigator", "traveler"], "gamma": ["avatar", "exorcist", "templar", "shields_of_faith", "enchanter", "master_navigators"], "delta": ["high_priest"]},\n')
        f.write('    "unraveller": {"alpha": ["unraveller"], "beta": ["harmer", "sacrificer", "magical_torturer", "traveler", "navigator"], "gamma": ["servant_of_mordulak", "servant_of_shirija", "servant_of_talakh", "servant_of_lloth"], "delta": ["enchanter", "master_navigator"], "epsilon": ["elder_of_mordulak", "patriarch_of_shirija", "sword_of_talakh", "primate_of_lloth", "master_enchanter"]},\n')
        f.write('    "druid": {"alpha": ["druid"], "beta": ["weather_watcher", "animal_tamer", "herbalist", "traveler"], "gamma": ["adept_of_the_stones", "enchanter", "shaman_of_soil"], "delta": ["chanter_of_deep_earth"]},\n')
        f.write('    "shapeshifter": {"alpha": ["shapeshifter"], "beta": ["bestial_seccedaneum", "savager", "animal_tamer", "traveler"], "gamma": ["animal_healer", "animal_trainer", "beast_lord", "dragon_lord"]},\n')
        f.write('    "woodsman": {"alpha": ["woodsman"], "beta": ["sylvan_guard", "sylvan_ward", "animal_tamer", "herbalist", "traveler"], "gamma": ["sylvan_scout", "sylvan_protector", "sylvan_woodlord"]},\n')
        f.write('    "lurker": {"alpha": ["lurker"], "beta": ["street_brawler", "poison_brewer", "trickster", "traveler"], "gamma": ["assassin", "bartender", "master_assassin", "disciple_of_shadow"], "delta": ["silent_hand"]},\n')
        f.write('}\n\n')
        
        # GUILD_DATA
        f.write('GUILD_DATA = {\n')
        for gid in sorted(all_guilds.keys()):
            write_guild_data(f, all_guilds[gid])
        f.write('}\n\n')
        
        # Helper functions
        f.write('''
def get_guild(guild_id):
    return GUILD_DATA.get(guild_id)

def get_tree(tree_name):
    tree = GUILD_TREES.get(tree_name, {})
    result = []
    for tier, guilds in tree.items():
        for gid in guilds:
            data = GUILD_DATA.get(gid)
            if data:
                result.append({"id": gid, "tier": tier, **data})
    return result

def search_skill(name):
    results = []
    for gid, data in GUILD_DATA.items():
        for entry in data.get("entries", []):
            if name.lower() in entry["name"].lower():
                results.append({"guild": gid, **entry})
    return results

if __name__ == "__main__":
    print(f"Loaded {len(GUILD_DATA)} guilds from {len(GUILD_TREES)} trees")
''')
    
    print(f"Done! Wrote {len(all_guilds)} guilds, {total_entries} entries to {OUTPUT_FILE}")
    print(f"File size: {os.path.getsize(OUTPUT_FILE)} bytes")

if __name__ == "__main__":
    main()
