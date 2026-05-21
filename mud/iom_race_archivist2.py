#!/usr/bin/env python3
"""
Islands of Myth - Race Archivist
Comprehensive capture of all race information from the Hall of Races.
Uses 'all races', 'la <race>' for every race, 'read poster', 'read sign'.
"""

import telnetlib
import time
import sys

HOST = "islandsofmyth.org"
PORT = 3000
TIMEOUT = 15

# Use existing character
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

def send_and_read(tn, cmd_bytes, wait=3):
    if cmd_bytes:
        tn.write(cmd_bytes)
        time.sleep(0.5)
    time.sleep(wait)
    try:
        return tn.read_very_eager()
    except:
        return b''

# --- CONNECT AND LOGIN ---
print(f"[*] Connecting to {HOST}:{PORT}...", file=sys.stderr)
tn = telnetlib.Telnet(HOST, PORT, timeout=TIMEOUT)
time.sleep(2)

# Login menu
data = tn.read_very_eager()
log_section("LOGIN MENU", data)

# Login as existing character
data = send_and_read(tn, CHAR_NAME, 2)
text = log_section("NAME ENTRY", data)

# Enter password
data = send_and_read(tn, CHAR_PASS, 2)
text = log_section("PASSWORD ENTRY", data)

# Go to race-select
print("[*] Going to race-select...", file=sys.stderr)
data = send_and_read(tn, b'race-select\n', 3)
text = log_section("RACE-SELECT ROOM", data)

# --- ARCHIVE EVERYTHING ---

# 1. Read the sign
print("[*] Reading sign...", file=sys.stderr)
data = send_and_read(tn, b'read sign\n', 3)
log_section("READ SIGN", data)

# 2. Read the poster
print("[*] Reading poster...", file=sys.stderr)
data = send_and_read(tn, b'read poster\n', 3)
log_section("READ POSTER", data)

# 3. Get all races list
print("[*] Getting all races...", file=sys.stderr)
data = send_and_read(tn, b'all races\n', 3)
text = log_section("ALL RACES LIST", data)

# 4. For each race, do 'la <race>'
RACES = [
    "human", "elf", "dwarf", "halfling", "gnome", "half-elf", "half-orc",
    "goblin", "orc", "troll", "ogre", "minotaur", "drow", "githyanki",
    "kobold", "gnoll", "celestial", "undead", "illithid", "gargoyle",
    "fae", "pixie", "naga", "rakshasa", "seraph", "draconian", "ghyrdon"
]

for race in RACES:
    cmd = f"la {race}\n".encode()
    print(f"[*] Examining {race}...", file=sys.stderr)
    data = send_and_read(tn, cmd, 3)
    text = log_section(f"RACE: {race.upper()}", data)
    
    low = text.lower()
    if "don't see" in low or "nothing" in low or "can't find" in low or "no such" in low:
        print(f"[!] Race '{race}' not found, skipping...", file=sys.stderr)
        continue

# 5. Help on races
print("[*] Getting help on races...", file=sys.stderr)
data = send_and_read(tn, b'help races\n', 3)
log_section("HELP RACES", data)

data = send_and_read(tn, b'help race\n', 3)
log_section("HELP RACE", data)

# 6. Final look
data = send_and_read(tn, b'look\n', 2)
log_section("FINAL LOOK", data)

tn.close()
print("[*] Archiving complete.", file=sys.stderr)
