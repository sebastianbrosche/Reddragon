#!/usr/bin/env python3
"""
Compile IOM guild pages - uses line-based parsing, no regex on large blocks
Fixes quote escaping for valid Python output
"""
import os

GUILDS_DIR = "/root/.openclaw/workspace/reddragon/docs/guilds"
OUTPUT_FILE = "/root/.openclaw/workspace/reddragon/world/guild_database.py"

def escape_for_python(s):
    """Escape a string for use in triple-quoted Python string"""
    return s.replace('\\', '\\\\').replace('"""', '\\"\\"\\"')

def parse_guild_file(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
    
    guild_id = os.path.basename(filepath).replace('.md', '')
    guild_name = guild_id.replace('_', ' ')
    guild_level = "unknown"
    description = ""
    
    import re
    
    # Parse header
    in_desc = False
    desc_lines = []
    
    for i, line in enumerate(lines):
        if "Guild info on" in line and "level" in line:
            parts = line.split("Guild info on ")
            if len(parts) > 1:
                gp = parts[1].split(".")
                if len(gp) > 0:
                    guild_name = gp[0].strip()
                lp = line.lower().split("level")
                if len(lp) > 0:
                    w = lp[0].split()
                    for word in reversed(w):
                        if word in ("alpha", "beta", "gamma", "delta", "epsilon"):
                            guild_level = word
                            break
        
        if "</pre>" in line.lower() or ("<p>" in line and not "</p>" in line):
            in_desc = True
        if in_desc:
            desc_lines.append(line)
            if "</p>" in line.lower():
                in_desc = False
                break
    
    if desc_lines:
        raw_desc = ' '.join(desc_lines)
        raw_desc = re.sub(r'<[^>]+>', '', raw_desc)
        raw_desc = re.sub(r'\s+', ' ', raw_desc).strip()
        description = raw_desc[:500]
    
    # Parse progression
    progression = []
    for i, line in enumerate(lines):
        if "[Level" in line and "]" in line:
            try:
                lvl_str = line.split("[Level")[1].split("]")[0].strip()
                lvl = int(lvl_str)
            except:
                continue
            if i + 1 < len(lines):
                next_line = lines[i + 1]
                if "New Skills:" in next_line or "New Spells:" in next_line:
                    kind = "skill" if "New Skills:" in next_line else "spell"
                    items_part = next_line.split(":", 1)[1] if ":" in next_line else next_line
                    names = re.findall(r'<a[^>]*>([^<]+)</a>', items_part)
                    if not names:
                        names = [items_part.strip()]
                    for name in names:
                        clean = name.strip()
                        if clean and clean.lower() != "and":
                            progression.append({"guild_level": lvl, "kind": kind, "name": clean})
    
    # Parse entries - line by line
    entries = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if "Help on" in line and ("skill" in line.lower() or "spell" in line.lower()):
            try:
                kind = "skill" if "skill" in line.lower() else "spell"
                name = line.split(":")[1].strip() if ":" in line else "unknown"
                
                entry_level = "unknown"
                j = i + 1
                while j < len(lines) and j < i + 10:
                    if "Guild Level" in lines[j]:
                        val = lines[j].split(":")[1].strip() if ":" in lines[j] else ""
                        entry_level = val.lower()
                        break
                    j += 1
                
                entry_type = "unknown"
                j = i + 1
                while j < len(lines) and j < i + 15:
                    if "Skill type" in lines[j] or "Spell type" in lines[j]:
                        val = lines[j].split(":")[1].strip() if ":" in lines[j] else ""
                        entry_type = val
                        break
                    j += 1
                
                cost = 0
                j = i + 1
                while j < len(lines) and j < i + 20:
                    if "Base Experience Cost" in lines[j]:
                        val = lines[j].split(":")[1].strip() if ":" in lines[j] else "0"
                        try:
                            cost = int(val)
                        except:
                            cost = 0
                        break
                    j += 1
                
                # Find description - between ====== after cost and next ======
                desc_start = j + 1
                while desc_start < len(lines) and "=" * 30 not in lines[desc_start]:
                    desc_start += 1
                desc_start += 1
                
                desc_lines = []
                j = desc_start
                while j < len(lines) and "=" * 30 not in lines[j]:
                    desc_lines.append(lines[j])
                    j += 1
                
                desc = ' '.join(desc_lines)
                desc = re.sub(r'<[^>]+>', '', desc)
                desc = re.sub(r'\s+', ' ', desc).strip()
                desc = desc[:300]
                
                entries.append({
                    "kind": kind,
                    "name": name,
                    "guild_level": entry_level,
                    "type": entry_type,
                    "cost": cost,
                    "description": desc
                })
                i = j - 1
            except:
                pass
        i += 1
    
    return {
        "id": guild_id,
        "name": guild_name,
        "level": guild_level,
        "description": description,
        "progression": progression,
        "entries": entries
    }


def main():
    import glob
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
            print(f"  OK {guild_id}: {len(data['progression'])} prog, {len(data['entries'])} entries")
        except Exception as e:
            print(f"  ERR {guild_id}: {e}")
    
    print(f"\nWriting {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write('#!/usr/bin/env python3\n')
        f.write('"""\n')
        f.write('Islands of Myth - Complete Guild Database\n')
        f.write('Auto-generated from islandsofmyth.org guild pages\n')
        f.write(f'Total guilds: {len(all_guilds)}\n')
        f.write(f'Total entries: {total_entries}\n')
        f.write('"""\n\n')
        
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
        
        f.write('GUILD_DATA = {\n')
        for gid in sorted(all_guilds.keys()):
            d = all_guilds[gid]
            f.write(f'    "{gid}": {{\n')
            f.write(f'        "name": "{escape_for_python(d["name"])}",\n')
            f.write(f'        "level": "{d["level"]}",\n')
            f.write(f'        "description": """{escape_for_python(d["description"])}""",\n')
            f.write('        "progression": [\n')
            for p in d["progression"]:
                f.write(f'            {{"guild_level": {p["guild_level"]}, "kind": "{p["kind"]}", "name": "{escape_for_python(p["name"])}"}},\n')
            f.write('        ],\n')
            f.write('        "entries": [\n')
            for e in d["entries"]:
                f.write(f'            {{"kind": "{e["kind"]}", "name": "{escape_for_python(e["name"])}", "guild_level": "{e["guild_level"]}", "type": "{escape_for_python(e["type"])}", "cost": {e["cost"]}, "description": """{escape_for_python(e["description"])}"""}},\n')
            f.write('        ],\n')
            f.write('    },\n')
        f.write('}\n\n')
        
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
    
    size = os.path.getsize(OUTPUT_FILE)
    print(f"Done! {len(all_guilds)} guilds, {total_entries} entries")
    print(f"File size: {size:,} bytes")

if __name__ == "__main__":
    main()
