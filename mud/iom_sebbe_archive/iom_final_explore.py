#!/usr/bin/env python3
"""
Islands of Myth MUD - Final Exploration
Focus: Get to Central Square, map properly, visit guilds, capture everything.
"""

import telnetlib
import re
import os
import time
import json
from datetime import datetime

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
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(ARCHIVE_DIR, f"final_{name}_{ts}.txt")
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"[LOGGED] {path}")
    return path

def send_wait(tn, cmd, wait=2.0):
    tn.write((cmd + "\n").encode('utf-8'))
    time.sleep(wait)
    data = tn.read_very_eager()
    text = strip_ansi(data)
    return text

def connect():
    print("[*] Connecting...")
    tn = telnetlib.Telnet(HOST, PORT, timeout=15)
    time.sleep(2)
    banner = strip_ansi(tn.read_very_eager())
    print(f"[BANNER] {banner[:200]}...")
    
    time.sleep(1)
    tn.write((USER + "\n").encode('utf-8'))
    time.sleep(1.5)
    u = strip_ansi(tn.read_very_eager())
    print(f"[USER] {u[:100]}")
    
    tn.write((PASSWORD + "\n").encode('utf-8'))
    time.sleep(2.5)
    p = strip_ansi(tn.read_very_eager())
    print(f"[PASS] {p[:200]}...")
    
    return tn

def get_room_data(tn):
    look = send_wait(tn, "look", wait=1.5)
    exits = send_wait(tn, "exits", wait=1.0)
    scan = send_wait(tn, "scan", wait=1.5)
    return {"look": look, "exits": exits, "scan": scan}

def explore_from_current(tn):
    print("\n[EXPLORE] Mapping from current room...")
    directions = ["north","south","east","west","up","down",
                  "northeast","northwest","southeast","southwest",
                  "n","s","e","w","u","d","ne","nw","se","sw"]
    opposites = {"north":"south","south":"north","east":"west","west":"east",
                 "up":"down","down":"up","northeast":"southwest","southwest":"northeast",
                 "northwest":"southeast","southeast":"northwest",
                 "n":"s","s":"n","e":"w","w":"e","u":"d","d":"u",
                 "ne":"sw","sw":"ne","nw":"se","se":"nw"}
    
    rooms = {}
    start = get_room_data(tn)
    start_name = start["look"].split('\n')[0].strip() if start["look"] else "Start"
    rooms[start_name] = start
    log_file(f"room_{start_name.replace(' ','_')}", json.dumps(start, indent=2))
    
    for d in directions:
        # Get current room name
        cur = send_wait(tn, "look", wait=1.0)
        cur_name = cur.split('\n')[0].strip() if cur else "Unknown"
        
        move = send_wait(tn, d, wait=1.5)
        
        if "can't" in move.lower() or "do that" in move.lower() or "possible" in move.lower():
            rooms[f"{cur_name}_blocked_{d}"] = move
            continue
        
        # New room
        new_room = get_room_data(tn)
        new_name = new_room["look"].split('\n')[0].strip() if new_room["look"] else f"Room_{d}"
        new_room["from"] = cur_name
        new_room["via"] = d
        new_room["enter_msg"] = move
        
        if new_name not in rooms:
            rooms[new_name] = new_room
            log_file(f"room_{new_name.replace(' ','_')}", json.dumps(new_room, indent=2))
        
        # Go back
        opp = opposites.get(d)
        if opp:
            back = send_wait(tn, opp, wait=1.5)
    
    log_file("room_map", json.dumps(rooms, indent=2, ensure_ascii=False))
    return rooms

def explore_guilds(tn):
    print("\n[GUILDS] Looking for guild halls...")
    guilds = {}
    
    # Try guild-specific commands
    for cmd in ["guild", "clan", "order", "church", "temple", "shrine", "hall"]:
        r = send_wait(tn, cmd, wait=1.5)
        guilds[cmd] = r
        log_file(f"guild_cmd_{cmd}", r)
    
    # Try enter commands from current location
    for target in ["guild", "hall", "temple", "church", "shrine", "sanctuary", "portal", "gate"]:
        r = send_wait(tn, f"enter {target}", wait=1.5)
        guilds[f"enter_{target}"] = r
        if "can't" not in r.lower() and "do that" not in r.lower():
            room = get_room_data(tn)
            guilds[f"enter_{target}_room"] = room
            log_file(f"guild_enter_{target}", json.dumps(room, indent=2))
            # Try to return
            send_wait(tn, "out", wait=1.5)
            send_wait(tn, "leave", wait=1.5)
            send_wait(tn, "exit", wait=1.5)
    
    log_file("guild_exploration", json.dumps(guilds, indent=2, ensure_ascii=False))
    return guilds

def capture_everything(tn):
    print("\n[CAPTURE] Getting everything...")
    
    everything = {}
    
    cmds = [
        "look", "look at me", "look self",
        "inventory", "i", "equipment", "eq",
        "score", "stats", "status",
        "spells", "skills", "abilities",
        "who", "where",
        "title", "level", "experience", "xp",
        "hp", "mana", "ep", "sp",
        "money", "gold", "bank",
        "weight", "encumbrance",
        "guild", "clan", "order", "faction",
        "alignment", "deity", "patron", "worship",
        "religion", "faith",
        "affects", "affect", "buffs",
        "followers", "pets", "mounts", "minions",
        "report", "channels", "chan",
        "group", "party",
        "buddylist", "friends", "ignore",
        "alias", "aliases",
        "prompt", "brief", "compact", "verbose",
        "wimpy", "autosave",
        "time", "weather", "date",
        "rank", "fame", "infamy", "reputation",
        "achievements", "badges", "titles",
        "quests", "tasks", "jobs", "bounties",
        "map", "maps", "world", "areas",
        "help", "news", "motd", "rules", "credits",
        "socials", "emotes", "emote list",
        "commands", "command list",
        "color", "colour", "ansi",
        "terminal", "mode",
        "password", "plan", "email", "description",
        "background", "history", "story",
        "afk", "busy", "dnd", "idle",
        "save", "quit",
        "consider self", "consider",
        "train", "practice", "learn",
        "buy", "sell", "list", "value",
        "repair", "appraise", "identify",
        "donate", "sacrifice", "offer",
        "pray", "meditate", "rest", "sleep",
        "stand", "sit", "wake",
        "cast detect magic", "cast identify",
        "lore", "appraise self", "identify self",
        "wear all", "remove all",
        "wield", "unwield", "hold", "dual",
        "quaff", "recite", "brandish", "zap",
        "rub", "touch", "wave", "point",
        "emote bows", "say Hello",
        "shout test", "yell test",
        "tell self test",
        "scan", "search", "track",
        "sneak", "hide", "camouflage",
        "peek", "listen", "smell", "taste",
        "climb", "jump", "swim", "dive", "fly",
        "push", "pull", "turn", "twist",
        "press", "lift", "lower", "raise",
        "slide", "roll", "move", "shift",
        "open", "close", "lock", "unlock",
        "knock", "ring", "bang",
    ]
    
    for cmd in cmds:
        r = send_wait(tn, cmd, wait=1.0)
        everything[cmd] = r
        log_file(f"cmd_{cmd.replace(' ','_')}", r)
    
    log_file("everything", json.dumps(everything, indent=2, ensure_ascii=False))
    return everything

def main():
    print("="*60)
    print("ISLANDS OF MYTH - FINAL EXPLORATION")
    print("="*60)
    
    tn = connect()
    
    # First: get out of Heart of Illium to Central Square
    print("\n[MOVE] Getting to Central Square...")
    r = send_wait(tn, "out", wait=2.0)
    print(f"[OUT] {r[:300]}")
    
    # Check where we are
    look = send_wait(tn, "look", wait=1.5)
    print(f"[LOCATION] {look[:300]}")
    
    explore_from_current(tn)
    explore_guilds(tn)
    capture_everything(tn)
    
    print("\n[FINAL] Saving and quitting...")
    send_wait(tn, "save", wait=1.5)
    send_wait(tn, "quit", wait=2.0)
    tn.close()
    
    print("\n" + "="*60)
    print("FINAL ARCHIVE COMPLETE")
    files = sorted(os.listdir(ARCHIVE_DIR))
    print(f"Total files: {len(files)}")
    print("="*60)

if __name__ == "__main__":
    main()
