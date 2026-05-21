#!/usr/bin/env python3
"""
Islands of Myth - Complete Race Archivist v3
Handles pager properly, captures ALL pages, saves to file.
"""

import telnetlib
import time
import sys

HOST = "islandsofmyth.org"
PORT = 3000
TIMEOUT = 15

CHAR_NAME = b'chronicler\n'
CHAR_PASS = b'mudarchivist2026\n'

def log_section(label, data):
    ts = time.strftime("%H:%M:%S")
    header = f"\n{'='*70}\n[{ts}] === {label} ===\n{'='*70}"
    text = data.decode('ascii', errors='replace')
    print(header, file=sys.stderr)
    print(text, file=sys.stderr)
    print("="*70, file=sys.stderr)
    return text

def send_and_read(tn, cmd_bytes, wait=2):
    if cmd_bytes:
        tn.write(cmd_bytes)
        time.sleep(0.3)
    time.sleep(wait)
    try:
        return tn.read_very_eager()
    except:
        return b''

def get_full_description(tn, race_name):
    """Get complete race description handling pager."""
    cmd = f"la {race_name}\n".encode()
    tn.write(cmd)
    time.sleep(0.5)
    
    all_data = b''
    for _ in range(15):  # Max 15 pages
        time.sleep(1.5)
        try:
            data = tn.read_very_eager()
        except:
            break
        all_data += data
        text = data.decode('ascii', errors='replace')
        
        # If we see the prompt, we're done
        if "hp(" in text and "sp(" in text and "ep(" in text and ">" in text:
            break
        
        # If pager is active, send space
        if "--More--" in text or "(h):" in text:
            tn.write(b' ')
            time.sleep(0.3)
    
    return all_data

# --- CONNECT AND LOGIN ---
print(f"[*] Connecting to {HOST}:{PORT}...", file=sys.stderr)
tn = telnetlib.Telnet(HOST, PORT, timeout=TIMEOUT)
time.sleep(2)

# Login menu
data = tn.read_very_eager()
log_section("LOGIN MENU", data)

# Login
data = send_and_read(tn, CHAR_NAME, 2)
log_section("NAME ENTRY", data)

data = send_and_read(tn, CHAR_PASS, 2)
log_section("PASSWORD ENTRY", data)

# Go to race-select
data = send_and_read(tn, b'race-select\n', 3)
log_section("RACE-SELECT ROOM", data)

# --- ARCHIVE ALL RACES ---
RACES = [
    "cromagnon", "drow", "dwarf", "elf", "ent", "faerie", "gargoyle",
    "giant", "gnome", "goblin", "grorrark", "halfelf", "hobbit", "human",
    "kobold", "leprechaun", "lizardman", "mindflayer", "minotaur", "ogier",
    "phoenix", "snakeman", "thrikhren", "troll", "vampire", "vinnipier", "xorn"
]

# Also get poster and sign
print("[*] Reading sign...", file=sys.stderr)
data = send_and_read(tn, b'read sign\n', 4)
text = log_section("READ SIGN", data)
# Handle pager for sign
if "(h):" in text or "--More--" in text:
    for _ in range(10):
        data = send_and_read(tn, b' ', 2)
        log_section("SIGN CONT", data)
        if "hp(" in data.decode('ascii', errors='replace'):
            break

print("[*] Reading poster...", file=sys.stderr)
data = send_and_read(tn, b'read poster\n', 4)
text = log_section("READ POSTER", data)
# Handle pager for poster
if "(h):" in text or "--More--" in text:
    for _ in range(15):
        data = send_and_read(tn, b' ', 2)
        log_section("POSTER CONT", data)
        if "hp(" in data.decode('ascii', errors='replace'):
            break

# Get each race
for race in RACES:
    print(f"[*] Examining {race}...", file=sys.stderr)
    data = get_full_description(tn, race)
    log_section(f"RACE: {race.upper()}", data)
    time.sleep(0.5)

tn.close()
print("[*] Archiving complete.", file=sys.stderr)
