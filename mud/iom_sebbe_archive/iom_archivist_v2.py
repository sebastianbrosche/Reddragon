#!/usr/bin/env python3
"""
Islands of Myth MUD - Sebbe Archive Mission v2
Focused, robust exploration and archival logging.
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
    path = os.path.join(ARCHIVE_DIR, f"{name}_{ts}.txt")
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"[LOGGED] {path} ({len(content)} chars)")
    return path

def append_to_master(content):
    path = os.path.join(ARCHIVE_DIR, "MASTER_TRANSCRIPT.txt")
    with open(path, 'a', encoding='utf-8') as f:
        f.write(content)
        f.write("\n")

def send_wait(tn, cmd, wait=2.0):
    tn.write((cmd + "\n").encode('utf-8'))
    time.sleep(wait)
    data = tn.read_very_eager()
    text = strip_ansi(data)
    append_to_master(f"CMD: {cmd}\n{'-'*40}\n{text}\n{'='*60}\n")
    return text

def connect_and_login():
    print(f"[*] Connecting to {HOST}:{PORT}...")
    tn = telnetlib.Telnet(HOST, PORT, timeout=15)
    time.sleep(2)
    
    banner = strip_ansi(tn.read_very_eager())
    print(f"[BANNER]\n{banner[:800]}")
    append_to_master(f"=== BANNER ===\n{banner}\n")
    
    print("[*] Sending username...")
    time.sleep(1)
    tn.write((USER + "\n").encode('utf-8'))
    time.sleep(1.5)
    u_resp = strip_ansi(tn.read_very_eager())
    append_to_master(f"CMD: {USER}\n{u_resp}\n")
    print(f"[USER RESP] {u_resp[:600]}")
    
    print("[*] Sending password...")
    tn.write((PASSWORD + "\n").encode('utf-8'))
    time.sleep(2.5)
    p_resp = strip_ansi(tn.read_very_eager())
    append_to_master(f"CMD: [password]\n{p_resp}\n")
    print(f"[PASS RESP] {p_resp[:800]}")
    
    return tn

def archive_character(tn):
    print("\n[PHASE 1] Character state...")
    cmds = {
        "inventory": ["inventory", "i"],
        "equipment": ["equipment", "eq"],
        "score": ["score", "stats", "status"],
        "spells": ["spells", "skills", "abilities"],
        "who": ["who"],
        "commands": ["commands", "help"],
        "look_self": ["look self", "look at me", "look me"],
        "title": ["title"],
        "level": ["level"],
        "experience": ["experience", "xp"],
        "hp": ["hp", "health"],
        "mana": ["mana"],
        "guild": ["guild", "clan", "order"],
        "money": ["money", "gold"],
        "weight": ["weight"],
        "affects": ["affects", "affect", "buffs"],
        "report": ["report"],
        "channels": ["channels", "chan"],
        "alias": ["alias", "aliases"],
        "group": ["group", "party"],
        "buddylist": ["buddylist"],
        "quests": ["quests", "quest"],
        "time": ["time"],
        "weather": ["weather"],
        "followers": ["followers", "pets", "mounts", "minions"],
    }
    
    results = {}
    for category, aliases in cmds.items():
        for cmd in aliases:
            r = send_wait(tn, cmd, wait=1.5)
            results[f"{category}_{cmd}"] = r
            if "Unknown" not in r and "can't" not in r.lower():
                break
    
    for name, content in results.items():
        log_file(name, content)
    return results

def explore_directions(tn):
    print("\n[PHASE 2] Directional exploration...")
    directions = ["north","south","east","west","up","down",
                  "northeast","northwest","southeast","southwest"]
    
    # First, capture starting room
    start = send_wait(tn, "look", wait=1.5)
    log_file("room_start", start)
    
    room_data = {"start": start}
    
    for d in directions:
        r = send_wait(tn, d, wait=1.5)
        room_data[f"move_{d}"] = r
        
        # If we moved, look around then return
        if "can't" not in r.lower() and "do that" not in r.lower():
            look_r = send_wait(tn, "look", wait=1.5)
            room_data[f"room_{d}"] = look_r
            # Try exits command
            exits_r = send_wait(tn, "exits", wait=1.0)
            room_data[f"exits_{d}"] = exits_r
            # Go back
            opposite = {"north":"south","south":"north","east":"west","west":"east",
                       "up":"down","down":"up","northeast":"southwest","southwest":"northeast",
                       "northwest":"southeast","southeast":"northwest"}.get(d, "")
            if opposite:
                send_wait(tn, opposite, wait=1.5)
                send_wait(tn, "look", wait=1.0)
    
    log_file("direction_exploration", json.dumps(room_data, indent=2, ensure_ascii=False))
    return room_data

def explore_guilds(tn):
    print("\n[PHASE 3] Guild hall exploration...")
    # Try common guild access patterns
    guild_cmds = [
        "recall", "home", "guild",
        "north", "north; north", "north; east", "north; west",
        "south", "south; south", "south; east", "south; west",
        "east", "east; east", "east; north", "east; south",
        "west", "west; west", "west; north", "west; south",
        "up", "up; up", "down", "down; down",
        "enter guild", "enter temple", "enter hall",
        "enter church", "enter shrine", "enter sanctuary",
    ]
    
    results = {}
    for cmd in guild_cmds:
        # Return to start first
        send_wait(tn, "recall", wait=2.0)
        send_wait(tn, "look", wait=1.0)
        
        # Execute the command (handle semicolons as separate)
        if ";" in cmd:
            for subcmd in cmd.split("; "):
                r = send_wait(tn, subcmd.strip(), wait=1.5)
        else:
            r = send_wait(tn, cmd, wait=1.5)
        
        results[cmd] = r
        look_r = send_wait(tn, "look", wait=1.5)
        results[f"{cmd}_look"] = look_r
    
    log_file("guild_exploration", json.dumps(results, indent=2, ensure_ascii=False))
    return results

def try_system_commands(tn):
    print("\n[PHASE 4] System commands...")
    sys_cmds = [
        "help", "news", "motd", "rules", "credits", "areas",
        "maps", "map", "world", "save", "scan",
        "consider self", "train", "practice", "learn",
        "prompt", "brief", "compact", "verbose",
        "color", "colour", "ansi", "terminal",
        "password", "email", "description", "plan",
        "afk", "busy", "dnd", "idle",
        "socials", "emote", "emotes",
        "say Hello from the archivist", "tell self test",
        "shout Hello", "yell Hello",
        "rank", "fame", "infamy", "reputation",
        "achievements", "badges", "titles",
        "clan", "faction", "alignment",
        "deity", "god", "patron", "worship",
        "religion", "faith", "belief", "church",
        "temple", "shrine", "altar", "sanctuary",
    ]
    
    results = {}
    for cmd in sys_cmds:
        r = send_wait(tn, cmd, wait=1.5)
        results[cmd] = r
    
    for name, content in results.items():
        log_file(f"sys_{name.replace(' ', '_')}", content)
    return results

def try_interactive_commands(tn):
    print("\n[PHASE 5] Interactive commands...")
    interact = [
        "rest", "sleep", "stand", "sit", "wake",
        "open", "close", "push", "pull", "turn",
        "climb", "jump", "swim", "dive", "fly",
        "search", "track", "scan", "peek",
        "sneak", "hide", "camouflage",
        "cast detect magic", "cast identify",
        "lore", "identify self", "appraise self",
        "eat", "drink", "feed",
        "wear all", "remove all", "wield", "unwield",
        "hold", "dual", "offhand",
        "quaff", "recite", "brandish", "zap",
        "rub", "touch", "wave", "point",
        "bow", "curtsy", "nod", "shake",
        "smile", "frown", "grin", "laugh",
        "cry", "sigh", "shrug", "stretch",
        "yawn", "blink", "sneeze", "cough",
        "hiccup", "snore", "dream", "whistle",
        "sing", "dance", "play", "hum",
    ]
    
    results = {}
    for cmd in interact:
        r = send_wait(tn, cmd, wait=1.0)
        results[cmd] = r
    
    for name, content in results.items():
        log_file(f"interact_{name.replace(' ', '_')}", content)
    return results

def main():
    print("="*60)
    print("ISLANDS OF MYTH - SEBBE ARCHIVE MISSION")
    print("="*60)
    
    tn = connect_and_login()
    
    archive_character(tn)
    explore_directions(tn)
    explore_guilds(tn)
    try_system_commands(tn)
    try_interactive_commands(tn)
    
    # Final
    print("\n[FINAL] Closing session...")
    send_wait(tn, "save", wait=1.5)
    send_wait(tn, "quit", wait=2.0)
    tn.close()
    
    print("\n" + "="*60)
    print("ARCHIVE COMPLETE")
    files = sorted(os.listdir(ARCHIVE_DIR))
    print(f"Files archived: {len(files)}")
    for f in files:
        fp = os.path.join(ARCHIVE_DIR, f)
        print(f"  {f} ({os.path.getsize(fp)} bytes)")
    print("="*60)

if __name__ == "__main__":
    main()
