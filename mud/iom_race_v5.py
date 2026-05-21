#!/usr/bin/env python3
"""
Islands of Myth - Targeted Race Capture v5
Captures only the 7 missing races with strict pager handling.
Uses enter (not space) to page, and long waits between races.
"""

import telnetlib
import time
import sys

HOST = "islandsofmyth.org"
PORT = 3000
TIMEOUT = 15

CHAR_NAME = b'chronicler\n'
CHAR_PASS = b'mudarchivist2026\n'

OUTPUT_FILE = "/root/.openclaw/workspace/mud/iom_race_missing.txt"

with open(OUTPUT_FILE, 'w') as f:
    f.write("# Missing Races Capture\n# " + time.strftime("%Y-%m-%d %H:%M:%S") + "\n\n")

def write_out(label, text):
    block = f"\n{'='*70}\n=== {label} ===\n{'='*70}\n{text}\n"
    print(block, file=sys.stderr)
    with open(OUTPUT_FILE, 'a') as f:
        f.write(block)

# Connect
print(f"[*] Connecting...", file=sys.stderr)
tn = telnetlib.Telnet(HOST, PORT, timeout=TIMEOUT)
time.sleep(2)

# Login flow
tn.read_very_eager()
tn.write(CHAR_NAME)
time.sleep(1.5)
tn.read_very_eager()
tn.write(CHAR_PASS)
time.sleep(2)

text = tn.read_very_eager().decode('ascii', errors='replace')
write_out("LOGIN", text)

# Race-select
tn.write(b'race-select\n')
time.sleep(2)
text = tn.read_very_eager().decode('ascii', errors='replace')
write_out("RACE-SELECT", text)

# Helper: fully drain until prompt
def wait_for_prompt(tn, max_attempts=20):
    for i in range(max_attempts):
        time.sleep(0.5)
        try:
            chunk = tn.read_very_eager().decode('ascii', errors='replace')
        except:
            return ""
        if "hp(" in chunk and "sp(" in chunk and "ep(" in chunk and ">" in chunk:
            return chunk
    return ""

# Races we still need full data for
RACES = ["drow", "elf", "leprechaun", "lizardman", "ogier", "snakeman", "vinnipier"]

for race in RACES:
    print(f"[*] Capturing {race}...", file=sys.stderr)
    
    # Make sure we're at a clean prompt first
    wait_for_prompt(tn)
    
    # Send look at race
    tn.write(f"la {race}\n".encode())
    time.sleep(1.5)
    
    all_text = ""
    
    for page in range(15):
        try:
            chunk = tn.read_very_eager().decode('ascii', errors='replace')
        except:
            break
        all_text += chunk
        
        # If we see the game prompt, we're done
        if "hp(" in chunk and "sp(" in chunk and "ep(" in chunk and ">" in chunk:
            # But check if pager is still active too
            if "(h):" not in chunk and "--More--" not in chunk:
                break
        
        # If pager active, send enter
        if "(h):" in chunk or "--More--" in chunk:
            tn.write(b'\n')
            time.sleep(0.6)
        else:
            # No pager, no prompt - wait more
            time.sleep(1)
    
    write_out(f"RACE: {race.upper()}", all_text)
    
    # Extra safety: send q + look to reset any stuck pager state
    tn.write(b'q\n')
    time.sleep(0.5)
    tn.write(b'look\n')
    time.sleep(1)
    wait_for_prompt(tn)
    time.sleep(1)  # extra buffer

tn.close()
print(f"[*] Done. Saved to {OUTPUT_FILE}", file=sys.stderr)
