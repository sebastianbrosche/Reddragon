#!/usr/bin/env python3
"""Scrape Wildchild's Islands of Myth archive at iommud.silvanthalas.com"""
import requests
from bs4 import BeautifulSoup
import json, time, re
from urllib.parse import urljoin

BASE = "http://iommud.silvanthalas.com"
OUTPUT = "/root/.openclaw/workspace/mud/wildchild_content.json"

session = requests.Session()

def fetch(path):
    url = urljoin(BASE, path)
    try:
        r = session.get(url, timeout=15)
        return r.text
    except Exception as e:
        return f"ERROR: {e}"

def extract_text(html):
    soup = BeautifulSoup(html, "html.parser")
    # Remove scripts/styles
    for tag in soup(["script","style"]):
        tag.decompose()
    return soup.get_text(separator="\n", strip=True)

# Main page links
def scrape_main():
    main = fetch("/iommud.html")
    soup = BeautifulSoup(main, "html.parser")
    links = {}
    for a in soup.find_all("a", href=True):
        href = a["href"]
        text = a.get_text(strip=True)
        links[text] = href
    return links

# Scrape each section
def scrape_all():
    links = scrape_main()
    data = {"source": BASE, "scraped_at": time.ctime(), "pages": {}}
    
    for name, href in links.items():
        print(f"Fetching {name}: {href}...")
        html = fetch(href)
        text = extract_text(html)
        data["pages"][name] = {
            "url": urljoin(BASE, href),
            "html": html,
            "text": text
        }
        time.sleep(0.5)
    
    # Also try to follow sub-links in maps and quests
    # Maps section
    if "Maps" in data["pages"]:
        soup = BeautifulSoup(data["pages"]["Maps"]["html"], "html.parser")
        for a in soup.find_all("a", href=True):
            sub_name = a.get_text(strip=True)
            sub_href = a["href"]
            sub_url = urljoin(data["pages"]["Maps"]["url"], sub_href)
            print(f"  Fetching map sub-page: {sub_name}...")
            sub_html = fetch(sub_href)  # relative to base
            data["pages"][f"Maps/{sub_name}"] = {
                "url": sub_url,
                "html": sub_html,
                "text": extract_text(sub_html)
            }
            time.sleep(0.3)
    
    with open(OUTPUT, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Done. Saved to {OUTPUT}")
    return data

if __name__ == "__main__":
    scrape_all()
