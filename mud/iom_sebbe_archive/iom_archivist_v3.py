#!/usr/bin/env python3
"""
Islands of Myth MUD - Sebbe Archive Mission v3
Menu-aware, reconnection-capable, robust exploration.
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
    print(f"[LOGGED] {path}")
    return path

def append_to_master(content):
    path = os.path.join(ARCHIVE_DIR, "MASTER_TRANSCRIPT.txt")
    with open(path, 'a', encoding='utf-8') as f:
        f.write(content)
        f.write("\n")

def send_wait(tn, cmd, wait=2.0):
    """Send command, read response, detect and escape menus."""
    tn.write((cmd + "\n").encode('utf-8'))
    time.sleep(wait)
    data = tn.read_very_eager()
    text = strip_ansi(data)
    
    # Detect common menu traps and escape
    menu_indicators = [
        "Invalid selection", "Enter your choice", "Select an option",
        "Press enter", "[q]uit", "[Q]uit", "(Q)uit", "Type 'quit'",
        "Type 'help'", "Type 'done'", "Type 'exit'", "Type 'return'",
        "Information for which", "Which one", "Choose a number",
        "Enter a number", "Make a selection", "Select from the list",
    ]
    
    escape_attempts = 0
    while escape_attempts < 5:
        is_menu = any(ind.lower() in text.lower() for ind in menu_indicators)
        if not is_menu:
            break
        # Try to escape menu
        for escape in ["q", "quit", "exit", "done", "return", "", "0", "x"]:
            tn.write((escape + "\n").encode('utf-8'))
            time.sleep(1.0)
            more = strip_ansi(tn.read_very_eager())
            text += "\n[ESCAPE:" + escape + "]\n" + more
            if not any(ind.lower() in more.lower() for ind in menu_indicators):
                break
        escape_attempts += 1
    
    append_to_master(f"CMD: {cmd}\n{'-'*40}\n{text}\n{'='*60}\n")
    return text

def connect_and_login():
    print(f"[*] Connecting to {HOST}:{PORT}...")
    tn = telnetlib.Telnet(HOST, PORT, timeout=15)
    time.sleep(2)
    
    banner = strip_ansi(tn.read_very_eager())
    print(f"[BANNER]\n{banner[:800]}")
    append_to_master(f"=== BANNER ===\n{banner}\n")
    
    time.sleep(1)
    tn.write((USER + "\n").encode('utf-8'))
    time.sleep(1.5)
    u_resp = strip_ansi(tn.read_very_eager())
    append_to_master(f"CMD: {USER}\n{u_resp}\n")
    print(f"[USER] {u_resp[:400]}")
    
    tn.write((PASSWORD + "\n").encode('utf-8'))
    time.sleep(2.5)
    p_resp = strip_ansi(tn.read_very_eager())
    append_to_master(f"CMD: [password]\n{p_resp}\n")
    print(f"[PASS] {p_resp[:600]}")
    
    return tn

def safe_cmd(tn, cmd, wait=1.5):
    """Execute command with menu detection but no master logging."""
    r = send_wait(tn, cmd, wait)
    return r

def archive_core(tn):
    print("\n[CORE] Archiving character state...")
    core = {}
    
    # Safe commands that don't enter menus
    safe_commands = [
        ("look", "look"),
        ("inventory", "i"),
        ("equipment", "eq"),
        ("score", "score"),
        ("who", "who"),
        ("time", "time"),
        ("weather", "weather"),
        ("report", "report"),
    ]
    
    for name, cmd in safe_commands:
        r = safe_cmd(tn, cmd)
        core[name] = r
        log_file(f"core_{name}", r)
    
    # Try spells/skills - might be a menu
    r = safe_cmd(tn, "spells")
    core["spells"] = r
    log_file("core_spells", r)
    
    r = safe_cmd(tn, "skills")
    core["skills"] = r
    log_file("core_skills", r)
    
    r = safe_cmd(tn, "abilities")
    core["abilities"] = r
    log_file("core_abilities", r)
    
    # Guild info
    r = safe_cmd(tn, "guild")
    core["guild"] = r
    log_file("core_guild", r)
    
    r = safe_cmd(tn, "clan")
    core["clan"] = r
    log_file("core_clan", r)
    
    r = safe_cmd(tn, "order")
    core["order"] = r
    log_file("core_order", r)
    
    # Character details
    r = safe_cmd(tn, "title")
    core["title"] = r
    log_file("core_title", r)
    
    r = safe_cmd(tn, "level")
    core["level"] = r
    log_file("core_level", r)
    
    r = safe_cmd(tn, "experience")
    core["experience"] = r
    log_file("core_experience", r)
    
    r = safe_cmd(tn, "hp")
    core["hp"] = r
    log_file("core_hp", r)
    
    r = safe_cmd(tn, "mana")
    core["mana"] = r
    log_file("core_mana", r)
    
    r = safe_cmd(tn, "money")
    core["money"] = r
    log_file("core_money", r)
    
    r = safe_cmd(tn, "weight")
    core["weight"] = r
    log_file("core_weight", r)
    
    r = safe_cmd(tn, "followers")
    core["followers"] = r
    log_file("core_followers", r)
    
    # Affects/buffs
    r = safe_cmd(tn, "affects")
    core["affects"] = r
    log_file("core_affects", r)
    
    r = safe_cmd(tn, "affect")
    core["affect"] = r
    log_file("core_affect", r)
    
    # Social
    r = safe_cmd(tn, "channels")
    core["channels"] = r
    log_file("core_channels", r)
    
    r = safe_cmd(tn, "group")
    core["group"] = r
    log_file("core_group", r)
    
    r = safe_cmd(tn, "party")
    core["party"] = r
    log_file("core_party", r)
    
    r = safe_cmd(tn, "buddylist")
    core["buddylist"] = r
    log_file("core_buddylist", r)
    
    r = safe_cmd(tn, "alias")
    core["alias"] = r
    log_file("core_alias", r)
    
    # Alignment
    r = safe_cmd(tn, "alignment")
    core["alignment"] = r
    log_file("core_alignment", r)
    
    # Deity
    r = safe_cmd(tn, "deity")
    core["deity"] = r
    log_file("core_deity", r)
    
    r = safe_cmd(tn, "patron")
    core["patron"] = r
    log_file("core_patron", r)
    
    return core

def explore_room(tn):
    """Get full room details."""
    room = {}
    room["look"] = safe_cmd(tn, "look", wait=1.5)
    room["exits"] = safe_cmd(tn, "exits", wait=1.0)
    room["scan"] = safe_cmd(tn, "scan", wait=1.5)
    room["consider"] = safe_cmd(tn, "consider", wait=1.0)
    return room

def map_from_square(tn):
    print("\n[MAP] Mapping from current location...")
    
    directions = ["north","south","east","west","up","down",
                  "northeast","northwest","southeast","southwest"]
    opposites = {"north":"south","south":"north","east":"west","west":"east",
                 "up":"down","down":"up","northeast":"southwest","southwest":"northeast",
                 "northwest":"southeast","southeast":"northwest"}
    
    # Get starting room
    start_room = explore_room(tn)
    start_name = start_room["look"].split('\n')[0] if start_room["look"] else "Start"
    log_file(f"room_{start_name.replace(' ','_')}", json.dumps(start_room, indent=2))
    
    mapped = {start_name: start_room}
    
    # Try each direction from start
    for d in directions:
        # Make sure we're at start
        safe_cmd(tn, "recall", wait=2.0)
        safe_cmd(tn, "look", wait=1.0)
        
        move_result = safe_cmd(tn, d, wait=1.5)
        
        # Check if movement succeeded
        if "can't" in move_result.lower() or "do that" in move_result.lower():
            mapped[f"blocked_{d}"] = move_result
            continue
        
        # We moved! Explore this room
        room = explore_room(tn)
        room["enter_direction"] = d
        room["enter_result"] = move_result
        
        room_name = room["look"].split('\n')[0] if room["look"] else f"Room_{d}"
        mapped[room_name] = room
        log_file(f"room_{room_name.replace(' ','_')}", json.dumps(room, indent=2))
        
        # Go back
        opp = opposites.get(d)
        if opp:
            safe_cmd(tn, opp, wait=1.5)
    
    log_file("room_map", json.dumps(mapped, indent=2, ensure_ascii=False))
    return mapped

def explore_guilds_safe(tn):
    print("\n[GUILDS] Exploring guild access...")
    
    # Return to safe point
    safe_cmd(tn, "recall", wait=2.0)
    safe_cmd(tn, "look", wait=1.0)
    
    guilds = {}
    
    # Try guild commands directly
    guild_cmds = ["guild", "clan", "order", "temple", "church"]
    for cmd in guild_cmds:
        r = safe_cmd(tn, cmd)
        guilds[cmd] = r
        log_file(f"guild_cmd_{cmd}", r)
        safe_cmd(tn, "recall", wait=2.0)
    
    # Try common guild hall directions from known MUD layouts
    # These are multi-step movements
    paths = [
        ["north"], ["south"], ["east"], ["west"],
        ["north", "north"], ["south", "south"],
        ["east", "east"], ["west", "west"],
        ["north", "east"], ["north", "west"],
        ["south", "east"], ["south", "west"],
        ["up"], ["down"],
        ["up", "up"], ["down", "down"],
        ["north", "north", "north"],
        ["south", "south", "south"],
        ["enter guild"], ["enter hall"], ["enter temple"],
    ]
    
    for path in paths:
        safe_cmd(tn, "recall", wait=2.0)
        path_name = "_".join(path).replace(" ", "_")
        
        for step in path:
            r = safe_cmd(tn, step, wait=1.5)
        
        final_look = safe_cmd(tn, "look", wait=1.5)
        guilds[path_name] = final_look
        log_file(f"guild_path_{path_name}", final_look)
    
    log_file("guild_exploration", json.dumps(guilds, indent=2, ensure_ascii=False))
    return guilds

def try_commands_list(tn):
    print("\n[COMMANDS] Testing available commands...")
    
    # These are common MUD commands that shouldn't break things
    test_cmds = [
        "help", "news", "motd", "rules", "credits",
        "areas", "maps", "world", "prompt",
        "brief", "compact", "verbose",
        "color", "colour", "terminal",
        "save", "scan",
        "socials", "emotes",
        "rank", "fame", "reputation",
        "title", "pretitle",
        "description", "background",
        "plan", "email",
        "afk", "busy", "dnd",
        "password",
        "wimpy",
        "report",
        "who",
        "where",
        "hints",
        "tips",
        "tutorial",
    ]
    
    results = {}
    for cmd in test_cmds:
        r = safe_cmd(tn, cmd)
        results[cmd] = r
        log_file(f"cmd_{cmd}", r)
    
    log_file("command_tests", json.dumps(results, indent=2, ensure_ascii=False))
    return results

def try_interactions(tn):
    print("\n[INTERACTIONS] Testing interaction commands...")
    
    interactions = [
        "rest", "stand", "sit", "sleep", "wake",
        "emote waves", "say Hello",
        "shout Testing", "yell Testing",
        "tell self test",
        "open", "close",
        "search", "track",
        "consider self",
        "train", "practice",
        "learn",
        "buy", "sell", "list",
        "donate", "sacrifice",
        "pray", "meditate",
        "cast detect invis",
        "cast detect magic",
        "lore",
        "appraise self",
        "identify self",
        "wear all", "remove all",
        "wield", "unwield",
        "hold",
        "dual",
        "quaff",
        "recite",
        "brandish",
        "zap",
        "rub",
        "touch",
        "wave",
        "point",
        "bow", "curtsy", "nod",
        "smile", "frown", "grin",
        "laugh", "cry", "sigh",
        "shrug", "stretch",
        "yawn", "blink",
        "whistle", "hum", "sing",
        "dance", "play",
    ]
    
    results = {}
    for cmd in interactions:
        r = safe_cmd(tn, cmd)
        results[cmd] = r
        log_file(f"interact_{cmd.replace(' ','_')}", r)
    
    log_file("interaction_tests", json.dumps(results, indent=2, ensure_ascii=False))
    return results

def deep_room_explore(tn):
    print("\n[DEEP] Deep room exploration...")
    
    # Try to find hidden things in the current room
    deep = {}
    
    # Look at everything
    r = safe_cmd(tn, "look")
    deep["look"] = r
    
    # Try various search commands
    search_cmds = [
        "search", "search room", "search ground",
        "examine room", "examine ground",
        "look ground", "look floor", "look walls",
        "look ceiling", "look sky", "look around",
        "inspect", "inspect room",
        "peek", "peek around",
    ]
    
    for cmd in search_cmds:
        r = safe_cmd(tn, cmd)
        deep[cmd] = r
        log_file(f"deep_{cmd.replace(' ','_')}", r)
    
    # Try object interaction
    obj_cmds = [
        "get", "drop", "put", "give",
        "push", "pull", "turn", "twist",
        "press", "lift", "lower", "raise",
        "slide", "roll", "move", "shift",
        "touch", "feel", "tap", "knock",
    ]
    
    for cmd in obj_cmds:
        r = safe_cmd(tn, cmd)
        deep[cmd] = r
        log_file(f"obj_{cmd}", r)
    
    log_file("deep_exploration", json.dumps(deep, indent=2, ensure_ascii=False))
    return deep

def main():
    print("="*60)
    print("ISLANDS OF MYTH - SEBBE ARCHIVE MISSION v3")
    print("="*60)
    
    tn = connect_and_login()
    
    archive_core(tn)
    map_from_square(tn)
    explore_guilds_safe(tn)
    try_commands_list(tn)
    try_interactions(tn)
    deep_room_explore(tn)
    
    print("\n[FINAL] Closing session...")
    safe_cmd(tn, "save", wait=1.5)
    safe_cmd(tn, "quit", wait=2.0)
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
