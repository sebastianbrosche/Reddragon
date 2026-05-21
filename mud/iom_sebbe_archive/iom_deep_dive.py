#!/usr/bin/env python3
"""
Islands of Myth MUD - Deep Dive
Explore intersections and hunt for guild halls.
"""

import telnetlib
import re
import os
import time
import json

HOST = "islandsofmyth.org"
PORT = 3000
USER = "sebbe"
PASSWORD = "creative"
ARCHIVE_DIR = "/root/.openclaw/workspace/mud/iom_sebbe_archive"

ANSI_RE = re.compile(r'\x1b(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

def strip_ansi(data):
    if isinstance(data, bytes):
        data = data.decode('utf-8', errors='replace')
    return ANSI_RE.sub('', data)

def log_file(name, content):
    path = os.path.join(ARCHIVE_DIR, f"deep_{name}.txt")
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"[LOGGED] {path}")
    return path

def send_wait(tn, cmd, wait=2.0):
    tn.write((cmd + "\n").encode('utf-8'))
    time.sleep(wait)
    return strip_ansi(tn.read_very_eager())

def connect():
    print("[*] Connecting...")
    tn = telnetlib.Telnet(HOST, PORT, timeout=15)
    time.sleep(2)
    strip_ansi(tn.read_very_eager())
    time.sleep(1)
    tn.write((USER + "\n").encode('utf-8'))
    time.sleep(1.5)
    strip_ansi(tn.read_very_eager())
    tn.write((PASSWORD + "\n").encode('utf-8'))
    time.sleep(2.5)
    strip_ansi(tn.read_very_eager())
    return tn

def explore_path(tn, path):
    """Follow a path of directions and capture the final room."""
    for step in path:
        send_wait(tn, step, wait=1.5)
    room = send_wait(tn, "look", wait=1.5)
    exits = send_wait(tn, "exits", wait=1.0)
    return {"look": room, "exits": exits, "path": path}

def main():
    print("="*60)
    print("DEEP DIVE - INTERSECTIONS AND GUILDS")
    print("="*60)
    
    tn = connect()
    
    # Get to Central Square
    send_wait(tn, "out", wait=2.0)
    send_wait(tn, "look", wait=1.0)
    
    all_data = {}
    
    # Explore each street one room deeper
    paths = {
        "north_illium_ethereal": ["north", "north"],
        "south_illium_crystal": ["south", "south"],
        "east_myst_gossamer": ["east", "east"],
        "west_myst_arcane": ["west", "west"],
    }
    
    for name, path in paths.items():
        print(f"[EXPLORING] {name}")
        # Return to square first
        send_wait(tn, "recall", wait=2.0)
        send_wait(tn, "look", wait=1.0)
        
        data = explore_path(tn, path)
        all_data[name] = data
        log_file(f"intersection_{name}", json.dumps(data, indent=2))
        
        # Also try going further from intersection
        for direction in ["north", "south", "east", "west"]:
            send_wait(tn, direction, wait=1.5)
            deeper = send_wait(tn, "look", wait=1.5)
            deeper_exits = send_wait(tn, "exits", wait=1.0)
            all_data[f"{name}_{direction}"] = {"look": deeper, "exits": deeper_exits}
            # Return
            opp = {"north":"south","south":"north","east":"west","west":"east"}.get(direction, "")
            if opp:
                send_wait(tn, opp, wait=1.5)
    
    # Try to find guild halls - look for buildings/entrances
    print("\n[GUILD HUNT] Looking for guild halls...")
    
    guild_hunt = {}
    
    # From each intersection, try common guild entry patterns
    for name, path in paths.items():
        send_wait(tn, "recall", wait=2.0)
        send_wait(tn, "look", wait=1.0)
        
        for step in path:
            send_wait(tn, step, wait=1.5)
        
        # Try various entry commands
        for entry in ["enter building", "enter shop", "enter store", "enter house",
                      "enter tower", "enter castle", "enter inn", "enter pub",
                      "enter temple", "enter church", "enter shrine", "enter hall",
                      "enter guild", "enter training", "enter academy", "enter school",
                      "enter dojo", "enter barracks", "enter fortress", "enter citadel",
                      "knock", "ring bell", "open door", "enter door"]:
            r = send_wait(tn, entry, wait=1.5)
            guild_hunt[f"{name}_{entry}"] = r
            
            # If we entered something, capture and get out
            if "can't" not in r.lower() and "do that" not in r.lower() and "possible" not in r.lower():
                room = send_wait(tn, "look", wait=1.5)
                guild_hunt[f"{name}_{entry}_room"] = room
                send_wait(tn, "out", wait=1.5)
                send_wait(tn, "leave", wait=1.5)
    
    log_file("guild_hunt", json.dumps(guild_hunt, indent=2, ensure_ascii=False))
    
    # Also try specific known guild commands
    print("\n[GUILD COMMANDS] Trying guild-specific commands...")
    guild_cmds = {}
    
    send_wait(tn, "recall", wait=2.0)
    send_wait(tn, "look", wait=1.0)
    
    for cmd in ["guilds", "guild list", "guilds list", "show guilds",
                "classes", "class list", "show classes",
                "professions", "profession list",
                "races", "race list", "show races",
                "clans", "clan list", "show clans",
                "orders", "order list", "show orders",
                "factions", "faction list", "show factions",
                "deities", "deity list", "show deities",
                "religions", "religion list", "show religions"]:
        r = send_wait(tn, cmd, wait=1.5)
        guild_cmds[cmd] = r
    
    log_file("guild_commands", json.dumps(guild_cmds, indent=2, ensure_ascii=False))
    
    # Try to look at specific objects in Central Square
    print("\n[OBJECTS] Examining objects in Central Square...")
    send_wait(tn, "recall", wait=2.0)
    send_wait(tn, "look", wait=1.0)
    
    objects = {}
    for obj in ["fountain", "machine", "moonflower", "vine", "potions", "pyroclasts",
                "window", "trees", "lorlings", "pools", "water"]:
        r = send_wait(tn, f"look {obj}", wait=1.5)
        objects[obj] = r
        
        r2 = send_wait(tn, f"examine {obj}", wait=1.5)
        objects[f"examine_{obj}"] = r2
    
    log_file("objects", json.dumps(objects, indent=2, ensure_ascii=False))
    
    # Try interacting with the fountain
    print("\n[FOUNTAIN] Interacting with fountain...")
    fountain = {}
    for cmd in ["enter fountain", "drink fountain", "touch fountain", "feel fountain",
                "search fountain", "look in fountain", "enter water", "drink water",
                "touch water", "swim", "dive fountain", "jump fountain"]:
        r = send_wait(tn, cmd, wait=1.5)
        fountain[cmd] = r
    
    log_file("fountain_interactions", json.dumps(fountain, indent=2, ensure_ascii=False))
    
    print("\n[FINAL] Saving and quitting...")
    send_wait(tn, "save", wait=1.5)
    send_wait(tn, "quit", wait=2.0)
    tn.close()
    
    print("\n" + "="*60)
    print("DEEP DIVE COMPLETE")
    print("="*60)

if __name__ == "__main__":
    main()
