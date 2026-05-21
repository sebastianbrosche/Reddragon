#!/usr/bin/env python3
"""
Islands of Myth - Race Selection Archivist
Enters the game, goes to race-select, and captures every race room.
"""

import telnetlib
import time
import sys

HOST = "islandsofmyth.org"
PORT = 3000
TIMEOUT = 15

# Pre-fill login sequence to get past creation quickly
# Since "archivist" might already exist, we'll use a new name
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

def wait_for_data(tn, wait=2):
    time.sleep(wait)
    try:
        return tn.read_very_eager()
    except:
        return b''

# --- MAIN ---
print(f"[*] Connecting to {HOST}:{PORT}...", file=sys.stderr)
tn = telnetlib.Telnet(HOST, PORT, timeout=TIMEOUT)
time.sleep(2)

# Read login menu
data = tn.read_very_eager()
log_section("LOGIN", data)

# Send 'c' for create
data = send_and_read(tn, b'c\n', 2)
log_section("CREATE", data)

# Name
data = send_and_read(tn, CHAR_NAME, 2)
text = log_section("NAME", data)

# Confirm name
if "yes or no" in text.lower() or "correct?" in text.lower():
    data = send_and_read(tn, b'yes\n', 2)
    text = log_section("NAME CONFIRMED", data)

# Password
data = send_and_read(tn, CHAR_PASS, 2)
text = log_section("PASSWORD", data)

# Confirm password
if "confirm" in text.lower() or "again" in text.lower():
    data = send_and_read(tn, CHAR_PASS, 2)
    text = log_section("PASS CONFIRMED", data)

# Gender
data = send_and_read(tn, b'male\n', 2)
text = log_section("GENDER", data)

# Email - skip with blank
data = send_and_read(tn, b'\n', 2)
text = log_section("EMAIL", data)

# How did you hear - skip
data = send_and_read(tn, b'\n', 2)
text = log_section("HEAR ABOUT", data)

# Now we should be in the game. Let's wait for the prompt.
time.sleep(2)
data = wait_for_data(tn, 2)
text = log_section("IN GAME", data)

# Go to race-select
print("[*] Sending 'race-select'...", file=sys.stderr)
data = send_and_read(tn, b'race-select\n', 3)
text = log_section("RACE SELECT ROOM", data)

# Explore - try to look at everything and move through exits
# Common MUD commands: look, exits, help
for cmd in [b'look\n', b'exits\n', b'help\n']:
    data = send_and_read(tn, cmd, 2)
    log_section(f"CMD: {cmd.decode().strip()}", data)

# Now try to explore each direction. Let's first see what exits are available.
# The room likely has exits to different race areas.
# Let's try common direction commands and capture everything.

directions = [b'north\n', b'south\n', b'east\n', b'west\n', 
              b'northeast\n', b'northwest\n', b'southeast\n', b'southwest\n',
              b'up\n', b'down\n']

for direction in directions:
    data = send_and_read(tn, direction, 2)
    log_section(f"GO: {direction.decode().strip()}", data)
    # Go back
    back = direction.decode().strip()
    back_cmd = None
    if back == 'north': back_cmd = b'south\n'
    elif back == 'south': back_cmd = b'north\n'
    elif back == 'east': back_cmd = b'west\n'
    elif back == 'west': back_cmd = b'east\n'
    elif back == 'northeast': back_cmd = b'southwest\n'
    elif back == 'northwest': back_cmd = b'southeast\n'
    elif back == 'southeast': back_cmd = b'northwest\n'
    elif back == 'southwest': back_cmd = b'northeast\n'
    elif back == 'up': back_cmd = b'down\n'
    elif back == 'down': back_cmd = b'up\n'
    if back_cmd:
        send_and_read(tn, back_cmd, 1)

# Try race-specific commands
race_cmds = [b'races\n', b'list\n', b'info\n', b'stats\n', b'race\n']
for cmd in race_cmds:
    data = send_and_read(tn, cmd, 2)
    log_section(f"RACE CMD: {cmd.decode().strip()}", data)

tn.close()
print("[*] Exploration complete.", file=sys.stderr)
