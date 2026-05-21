#!/usr/bin/env python3
"""
Islands of Myth - Complete Race Archivist
Uses correct race names from the poster. Handles --More-- pager.
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

def send_and_read(tn, cmd_bytes, wait=3):
    if cmd_bytes:
        tn.write(cmd_bytes)
        time.sleep(0.5)
    time.sleep(wait)
    try:
        return tn.read_very_eager()
    except:
        return b''

def read_all_pages(tn, initial_data):
    """Handle --More-- pager by sending spaces until done."""
    all_data = initial_data
    text = initial_data.decode('ascii', errors='replace')
    
    # Check for pager
    for _ in range(20):  # Max 20 pages
        if "--More--" in text or "(h):" in text:
            # Send space to continue
            data = send_and_read(tn, b' ', 2)
            all_data += data
            text = data.decode('ascii', errors='replace')
        else:
            break
    
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
# Races from the poster (alphabetical)
RACES = [
    "cromagnon", "drow", "dwarf", "elf", "ent", "faerie", "gargoyle",
    "giant", "gnome", "goblin", "grorrark", "halfelf", "hobbit", "human",
    "kobold", "leprechaun", "lizardman", "mindflayer", "minotaur", "ogier",
    "phoenix", "snakeman", "thrikhren", "troll", "vampire", "vinnipier", "xorn"
]

for race in RACES:
    cmd = f"la {race}\n".encode()
    print(f"[*] Examining {race}...", file=sys.stderr)
    
    # Send command
    data = send_and_read(tn, cmd, 3)
    
    # Handle pager if present
    data = read_all_pages(tn, data)
    
    text = log_section(f"RACE: {race.upper()}", data)
    
    # Small delay between races
    time.sleep(0.5)

# Final look
data = send_and_read(tn, b'look\n', 2)
log_section("FINAL LOOK", data)

tn.close()
print("[*] Archiving complete.", file=sys.stderr)
