#!/usr/bin/env python3
"""
Scraper for Islands of Myth content.
Fetches all guild and race detail pages, extracts structured data.
"""
import requests
from bs4 import BeautifulSoup
import json, re, time

BASE = "https://www.islandsofmyth.org"

RACES = [
    "cromagnon","drow","dwarf","elf","ent","faerie","gargoyle","giant",
    "gnome","goblin","grorrark","halfelf","hobbit","human","kobold",
    "leprechaun","lizardman","mindflayer","minotaur","ogier","phoenix",
    "snakeman","thrikhren","troll","vampire","vinnipier","xorn"
]

GUILDS = [
    "warrior","martialartist","acrobat","abjurer","elemental","psychics",
    "evoker","necromancer","weaver","unraveller","druid","shapeshifter",
    "woodsman","lurker"
]

def fetch_text(path):
    try:
        url = f"{BASE}{path}"
        r = requests.get(url, timeout=15, verify=False)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, 'html.parser')
        # Strip nav/menu, keep main content
        for nav in soup.find_all(['nav','header','footer']):
            nav.decompose()
        text = soup.get_text(separator='\n', strip=True)
        # Clean up excessive newlines
        text = re.sub(r'\n{3,}', '\n\n', text)
        return text
    except Exception as e:
        return f"ERROR: {e}"

def parse_race(text, name):
    """Extract stat block and description from race page text."""
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    stats = {}
    desc = []
    in_stats = False
    for line in lines:
        if re.search(r'(Strength|Constitution|Dexterity|Intelligence|Wisdom|Stamina|Hp Max|Hp Regen|Ep Max|Ep Regen|Sp Max|Sp Regen|charisma|height|mass|experience|skill|spell)', line, re.I):
            in_stats = True
            # Try to extract key:value
            m = re.match(r'^([A-Za-z\s]+):\s*(.+)$', line)
            if m:
                k = m.group(1).strip().lower().replace(' ','_')
                v = m.group(2).strip()
                stats[k] = v
        elif in_stats and line.startswith('They') or line.startswith('Special'):
            stats.setdefault('notes', []).append(line)
        else:
            desc.append(line)
    return {"name": name, "description": '\n'.join(desc[:50]), "stats": stats, "raw": text}

def parse_guild(text, name):
    """Extract guild tree and description from guild page text."""
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    tree = []
    desc = []
    for line in lines:
        if re.search(r'(knight|berserker|dancer|master|tamer|watcher|shaman|enchanter|traveler|adept|chanter)', line, re.I) and len(line) < 60:
            tree.append(line)
        else:
            desc.append(line)
    return {"name": name, "tree": tree, "description": '\n'.join(desc[:30]), "raw": text}

# Fetch all races
race_data = {}
for r in RACES:
    print(f"Fetching race: {r}...")
    text = fetch_text(f"/races/{r}.html")
    race_data[r] = parse_race(text, r.title())
    time.sleep(0.3)

# Fetch all guilds
guild_data = {}
for g in GUILDS:
    print(f"Fetching guild: {g}...")
    text = fetch_text(f"/guild/{g}.html")
    guild_data[g] = parse_guild(text, g.title())
    time.sleep(0.3)

# Save everything
with open('/root/.openclaw/workspace/mud/scraped_races.json', 'w') as f:
    json.dump(race_data, f, indent=2)
with open('/root/.openclaw/workspace/mud/scraped_guilds.json', 'w') as f:
    json.dump(guild_data, f, indent=2)

print(f"Done. {len(race_data)} races, {len(guild_data)} guilds scraped.")
