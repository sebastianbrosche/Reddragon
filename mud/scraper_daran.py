#!/usr/bin/env python3
"""
Scraper for Daran Madrox's Islands of Myth MUD Guide
Scrapes: maps, guilds, character info, equipment data
"""

import requests
from bs4 import BeautifulSoup
import json
import time
from urllib.parse import urljoin

BASE_URL = "http://daranmadrox.batcave.net/games/iom/guide"

# Map areas to scrape
MAP_ISLANDS = [
    "gossamer", "oddworld", "misty", "hyboria", "blackavar",
    "emerald", "darkcaverns", "everrest", "sombre", "twin", "underwater", "other"
]

# Guilds to scrape
GUILDS = [
    "warrior", "martialartist", "weaver", "unraveller", "abjurer",
    "elemental", "evoker", "necromancer", "psychics", "acrobat",
    "lurker", "druid", "woodsman", "shapeshifter", "other"
]

# Character sections
CHAR_SECTIONS = ["equipment", "races", "levels", "stats", "wishes", "armorclass", "hunger", "reinctax"]

def fetch(url, retries=3):
    for i in range(retries):
        try:
            resp = requests.get(url, timeout=15)
            resp.raise_for_status()
            return resp.text
        except Exception as e:
            if i == retries - 1:
                print(f"  Failed: {url} - {e}")
                return None
            time.sleep(1)
    return None

def parse_map_page(html, island):
    soup = BeautifulSoup(html, 'html.parser')
    areas = []
    base_island_url = f"{BASE_URL}/maps/{island}/"
    for link in soup.find_all('a'):
        href = link.get('href', '')
        text = link.get_text(strip=True)
        if href.endswith('.html') and href != 'index.html' and not href.startswith('http'):
            # Handle relative URLs properly
            full_url = urljoin(base_island_url, href)
            areas.append({"name": text, "url": full_url})
    return areas

def scrape_all():
    results = {
        "maps": {},
        "guilds": {},
        "character": {},
        "general": {},
        "links": {},
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }

    # Scrape maps
    print("Scraping maps...")
    for island in MAP_ISLANDS:
        url = f"{BASE_URL}/maps/{island}/index.html"
        html = fetch(url)
        if html:
            areas = parse_map_page(html, island)
            results["maps"][island] = {"areas": areas, "html": html}
            print(f"  {island}: {len(areas)} areas")
            # Scrape individual area pages (limit to first 5 per island to avoid overload)
            for area in areas[:5]:
                area_html = fetch(area["url"])
                if area_html:
                    area["content"] = area_html
                time.sleep(0.2)
        time.sleep(0.3)

    # Scrape guilds
    print("Scraping guilds...")
    for guild in GUILDS:
        url = f"{BASE_URL}/guilds/{guild}/index.html"
        html = fetch(url)
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            text = soup.get_text(separator='\n', strip=True)
            results["guilds"][guild] = {"html": html, "text": text}
            print(f"  {guild}: done")
        time.sleep(0.3)

    # Scrape character sections
    print("Scraping character info...")
    for section in CHAR_SECTIONS:
        url = f"{BASE_URL}/character/{section}.html"
        html = fetch(url)
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            text = soup.get_text(separator='\n', strip=True)
            results["character"][section] = {"html": html, "text": text}
            print(f"  {section}: done")
        time.sleep(0.3)

    # Scrape general info
    print("Scraping general info...")
    general_url = f"{BASE_URL}/general/index.html"
    html = fetch(general_url)
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        for link in soup.find_all('a'):
            href = link.get('href', '')
            text = link.get_text(strip=True)
            if href.endswith('.html') and href != 'index.html' and not href.startswith('http'):
                sub_url = urljoin(f"{BASE_URL}/general/", href)
                sub_html = fetch(sub_url)
                if sub_html:
                    sub_soup = BeautifulSoup(sub_html, 'html.parser')
                    results["general"][text] = {"html": sub_html, "text": sub_soup.get_text(separator='\n', strip=True)}
                time.sleep(0.3)

    return results

if __name__ == "__main__":
    print("Starting scraper...")
    data = scrape_all()
    with open("daran_content.json", "w") as f:
        json.dump(data, f, indent=2)
    print(f"\nDone! Saved to daran_content.json")
    print(f"Maps: {len(data['maps'])} islands")
    print(f"Guilds: {len(data['guilds'])} guilds")
    print(f"Character sections: {len(data['character'])} sections")
    print(f"General sections: {len(data['general'])} sections")
