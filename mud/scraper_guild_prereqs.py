#!/usr/bin/env python3
"""
Scrape guild prerequisites from Daran's guide.
"""
import requests, json, time
from bs4 import BeautifulSoup

BASE = "http://daranmadrox.batcave.net/games/iom/guide"
GUILDS = [
    "warrior", "martialartist", "weaver", "unraveller", "abjurer",
    "elemental", "evoker", "necromancer", "psychics", "acrobat",
    "lurker", "druid", "woodsman", "shapeshifter"
]

session = requests.Session()
data = {}

for guild in GUILDS:
    url = f"{BASE}/guilds/{guild}/prereqs.html"
    try:
        r = session.get(url, timeout=15)
        r.raise_for_status()
    except Exception as e:
        print(f"FAIL {guild}: {e}")
        continue
    
    soup = BeautifulSoup(r.text, "html.parser")
    text = soup.get_text(separator="\n", strip=True)
    
    # Extract prerequisite lines
    prereqs = []
    for line in text.split("\n"):
        line = line.strip()
        if ":" in line and not line.startswith(("Home", "General", "Character", "Guilds", "Maps", "Links", "Page", "Valid", "Daran", "Islands", "Please", "Sections", "Prerequisites", "Locations", "Notes", "Messages")):
            prereqs.append(line)
    
    data[guild] = prereqs
    print(f"✓ {guild}: {len(prereqs)} prereqs")
    time.sleep(0.3)

with open("/root/.openclaw/workspace/mud/guild_prereqs.json", "w") as f:
    json.dump(data, f, indent=2)

print(f"\nSaved {len(data)} guilds to guild_prereqs.json")
