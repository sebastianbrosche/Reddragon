#!/usr/bin/env python3
"""
Comprehensive scraper for Islands of Myth website.
Pulls races, guilds, guild trees, help files, and maps.
"""
import requests, json, re, time, os
from bs4 import BeautifulSoup
from urllib.parse import urljoin

requests.packages.urllib3.disable_warnings()

BASE = "https://www.islandsofmyth.org"
OUTDIR = "/root/.openclaw/workspace/mud"

RACES = [
    "cromagnon", "drow", "dwarf", "elf", "ent", "faerie", "gargoyle",
    "giant", "gnome", "goblin", "grorrark", "halfelf", "hobbit", "human",
    "kobold", "leprechaun", "lizardman", "mindflayer", "minotaur", "ogier",
    "phoenix", "snakeman", "thrikhren", "troll", "vampire", "vinnipier", "xorn"
]

GUILDS = [
    "warrior", "martialartist", "acrobat", "abjurer", "elemental",
    "psychics", "evoker", "necromancer", "weaver", "unraveller",
    "druid", "shapeshifter", "woodsman", "lurker"
]

HELP_PAGES = [
    "/faq/index.html", "/newbiefaq.html", "/scorehelp.html",
    "/help/", "/connect/", "/links/", "/gameinfo/"
]

OTHER = [
    "/3k/cgi/castle_map.c",
    "/themud/",
]


def fetch(path):
    url = urljoin(BASE, path)
    try:
        r = requests.get(url, timeout=15, verify=False)
        r.raise_for_status()
        return r.text
    except Exception as e:
        return f"ERROR: {e}"


def clean_text(soup):
    """Extract meaningful text, drop nav."""
    # Remove common nav elements
    for tag in soup.find_all(['nav', 'header', 'footer', 'script', 'style']):
        tag.decompose()
    text = soup.get_text(separator='\n')
    # Clean up excessive whitespace
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    return '\n'.join(lines)


def parse_race(name, html):
    soup = BeautifulSoup(html, 'html.parser')
    full = clean_text(soup)
    
    # Extract stat block
    stats = {}
    stat_patterns = [
        (r'Strength:\s*(\w+(?:\s+\w+)?)', 'strength'),
        (r'Constitution:\s*(\w+(?:\s+\w+)?)', 'constitution'),
        (r'Hp Max:\s*(\w+(?:\s+\w+)?)', 'hp_max'),
        (r'Hp Regen:\s*(\w+(?:\s+\w+)?)', 'hp_regen'),
        (r'Dexterity:\s*(\w+(?:\s+\w+)?)', 'dexterity'),
        (r'Stamina:\s*(\w+(?:\s+\w+)?)', 'stamina'),
        (r'Ep Max:\s*(\w+(?:\s+\w+)?)', 'ep_max'),
        (r'Ep Regen:\s*(\w+(?:\s+\w+)?)', 'ep_regen'),
        (r'Intelligence:\s*(\w+(?:\s+\w+)?)', 'intelligence'),
        (r'Wisdom:\s*(\w+(?:\s+\w+)?)', 'wisdom'),
        (r'Sp Max:\s*(\w+(?:\s+\w+)?)', 'sp_max'),
        (r'Sp Regen:\s*(\w+(?:\s+\w+)?)', 'sp_regen'),
    ]
    for pattern, key in stat_patterns:
        m = re.search(pattern, full, re.IGNORECASE)
        if m:
            stats[key] = m.group(1)
    
    # Extract notes/bullet points
    notes = []
    for line in full.split('\n'):
        if line.startswith('They ') or line.startswith('They can') or line.startswith('Their'):
            notes.append(line)
    
    # Extract description (paragraph after race name)
    desc = ""
    name_spaced = ' '.join(name.upper())  # e.g., "H U M A N" or "D R O W"
    idx = full.find(name_spaced)
    if idx == -1:
        idx = full.upper().find(name.upper())
    if idx != -1:
        after = full[idx + len(name):]
        lines_after = [l for l in after.split('\n') if l.strip() and not l.startswith('Strength')]
        desc = ' '.join(lines_after[:8])
    
    return {
        "name": name.capitalize(),
        "description": desc[:500],
        "stats": stats,
        "notes": notes,
        "raw": full
    }


def parse_guild(name, html):
    soup = BeautifulSoup(html, 'html.parser')
    full = clean_text(soup)
    
    # Extract ASCII tree as raw
    tree_lines = []
    in_tree = False
    for line in full.split('\n'):
        if '_' in line or '|' in line or any(g in line.lower() for g in ['knight', 'mage', 'master', 'traveler']):
            in_tree = True
        if in_tree:
            tree_lines.append(line)
    
    # Extract guild name mentions as tree nodes
    tree_nodes = []
    # Look for links in the page that are guild tree links
    for a in soup.find_all('a', href=re.compile(r'guildtree\.c')):
        text = a.get_text(strip=True)
        if text and text not in tree_nodes:
            tree_nodes.append(text)
    
    return {
        "name": name.capitalize(),
        "tree_ascii": '\n'.join(tree_lines[:40]),
        "tree_nodes": tree_nodes,
        "raw": full
    }


def scrape_all():
    results = {"races": {}, "guilds": {}, "help": {}, "other": {}}
    
    print("=== RACES ===")
    for race in RACES:
        print(f"  {race}...")
        html = fetch(f"/races/{race}.html")
        if not html.startswith("ERROR"):
            results["races"][race] = parse_race(race, html)
        else:
            results["races"][race] = {"name": race, "error": html}
        time.sleep(0.2)
    
    print("=== GUILDS ===")
    for guild in GUILDS:
        print(f"  {guild}...")
        html = fetch(f"/guild/{guild}.html")
        if not html.startswith("ERROR"):
            results["guilds"][guild] = parse_guild(guild, html)
        else:
            results["guilds"][guild] = {"name": guild, "error": html}
        time.sleep(0.2)
    
    print("=== HELP & OTHER ===")
    for page in HELP_PAGES + OTHER:
        print(f"  {page}...")
        html = fetch(page)
        results["other"][page] = {
            "url": urljoin(BASE, page),
            "raw": html if not html.startswith("ERROR") else html
        }
        time.sleep(0.2)
    
    # Save
    os.makedirs(OUTDIR, exist_ok=True)
    with open(f"{OUTDIR}/all_content.json", 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nDone. Saved to {OUTDIR}/all_content.json")
    print(f"Races: {len(results['races'])}, Guilds: {len(results['guilds'])}, Other: {len(results['other'])}")


if __name__ == "__main__":
    scrape_all()
