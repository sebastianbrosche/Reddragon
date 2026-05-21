#!/usr/bin/env python3
"""
Scraper for Daran Madrox's Islands of Myth Guide — Map Section
Corrected URL resolution for area pages.
"""
import requests, json, os, re, time
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "http://daranmadrox.batcave.net/games/iom/guide"
OUTPUT_FILE = "/root/.openclaw/workspace/mud/maps_daran.json"

ISLANDS = [
    "gossamer", "oddworld", "misty", "hyboria", "blackavar",
    "emerald", "darkcaverns", "everrest", "sombre", "twin",
    "underwater", "other"
]

session = requests.Session()

# Fetch main maps index
print("Fetching maps index...")
resp = session.get(f"{BASE_URL}/maps/index.html", timeout=15)
resp.raise_for_status()
soup = BeautifulSoup(resp.text, "html.parser")

maps_data = {"islands": {}}

for island in ISLANDS:
    print(f"\n=== {island.upper()} ===")
    island_url = f"{BASE_URL}/maps/{island}/index.html"
    try:
        r = session.get(island_url, timeout=15)
        r.raise_for_status()
    except Exception as e:
        print(f"  Failed to fetch island index: {e}")
        continue
    
    island_soup = BeautifulSoup(r.text, "html.parser")
    
    # Extract area links - fix URL resolution
    areas = []
    for li in island_soup.find_all("li"):
        link = li.find("a")
        if link and link.get("href") and ".html" in link.get("href"):
            area_name = link.get_text(strip=True)
            href = link.get("href")
            
            # The hrefs seem to be relative but include extra path prefix
            # e.g., "maps/gossamer/aviary.html" when we're at maps/gossamer/index.html
            # urljoin would double-prefix. Strip leading "maps/{island}/" if present.
            prefix = f"maps/{island}/"
            if href.startswith(prefix):
                href = href[len(prefix):]
            
            # Now resolve properly relative to island_url
            area_url = urljoin(island_url, href)
            
            # Skip navigation links (general, character, guilds, maps, links, page)
            if href in ["general/index.html", "character/index.html", "guilds/index.html", 
                        "maps/index.html", "links/index.html", "page/index.html",
                        f"maps/{island}/vmap.html"]:
                continue
            
            areas.append({"name": area_name, "url": area_url})
    
    print(f"  Found {len(areas)} areas")
    
    island_data = {"areas": []}
    
    for area in areas:
        area_name = area["name"]
        area_url = area["url"]
        print(f"  Fetching {area_name}...", end=" ")
        try:
            ar = session.get(area_url, timeout=15)
            ar.raise_for_status()
        except Exception as e:
            print(f"FAILED: {e}")
            continue
        
        area_soup = BeautifulSoup(ar.text, "html.parser")
        
        # Extract all text content
        full_text = area_soup.get_text(separator="\n", strip=True)
        
        # Try to find ASCII map - look for preformatted text
        ascii_map = None
        for pre in area_soup.find_all("pre"):
            text = pre.get_text()
            if len(text) > 200 and ("#" in text or "-" in text or "|" in text):
                ascii_map = text
                break
        
        # Also check paragraphs for map-like content
        if not ascii_map:
            for p in area_soup.find_all("p"):
                text = p.get_text()
                if len(text) > 300 and text.count("#") > 10:
                    ascii_map = text
                    break
        
        # Extract room labels if present (A:, B:, etc.)
        room_labels = {}
        label_pattern = re.findall(r'([A-Za-z0-9]):\s*([^\n]+)', full_text)
        for label, desc in label_pattern:
            room_labels[label] = desc.strip()
        
        # Extract key/info paragraphs
        info_paragraphs = []
        for p in area_soup.find_all("p"):
            text = p.get_text(strip=True)
            if len(text) > 20 and len(text) < 500 and not text.startswith("Valid"):
                info_paragraphs.append(text)
        
        area_data = {
            "name": area_name,
            "url": area_url,
            "has_ascii_map": ascii_map is not None,
            "ascii_map": ascii_map,
            "room_labels": room_labels,
            "info": info_paragraphs[:5],
            "full_text_preview": full_text[:500]
        }
        
        island_data["areas"].append(area_data)
        print(f"OK (map={ascii_map is not None}, labels={len(room_labels)})")
        time.sleep(0.3)
    
    maps_data["islands"][island] = island_data

# Save
with open(OUTPUT_FILE, "w") as f:
    json.dump(maps_data, f, indent=2)

print(f"\n✅ Saved to {OUTPUT_FILE}")
print(f"   Islands: {len(maps_data['islands'])}")
total_areas = sum(len(v["areas"]) for v in maps_data["islands"].values())
print(f"   Total areas: {total_areas}")
