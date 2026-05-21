#!/usr/bin/env python3
"""
Islands of Myth - Race Archivist v4
Properly handles pager: quits pager before each command, accumulates ALL pages.
Saves clean output to file.
"""

import telnetlib
import time
import sys

HOST = "islandsofmyth.org"
PORT = 3000
TIMEOUT = 15

CHAR_NAME = b'chronicler\n'
CHAR_PASS = b'mudarchivist2026\n'

OUTPUT_FILE = "/root/.openclaw/workspace/mud/iom_race_archive_raw.txt"

# Clear/create output file
with open(OUTPUT_FILE, 'w') as f:
    f.write("# Islands of Myth — Raw Race Capture\n# Session: " + time.strftime("%Y-%m-%d %H:%M:%S") + "\n\n")

def write_out(label, text):
    """Write to both stderr and file."""
    block = f"\n{'='*70}\n=== {label} ===\n{'='*70}\n{text}\n{'='*70}\n"
    print(block, file=sys.stderr)
    with open(OUTPUT_FILE, 'a') as f:
        f.write(block)

def send_and_read(tn, cmd_bytes, wait=2):
    if cmd_bytes:
        tn.write(cmd_bytes)
        time.sleep(0.3)
    time.sleep(wait)
    try:
        return tn.read_very_eager().decode('ascii', errors='replace')
    except:
        return ''

def drain_pager(tn):
    """Send 'q' repeatedly until we get a clean prompt."""
    for _ in range(5):
        tn.write(b'q')
        time.sleep(0.3)
        try:
            data = tn.read_very_eager().decode('ascii', errors='replace')
        except:
            return
        if "hp(" in data and ">" in data:
            return
        # Also try sending newline
        tn.write(b'\n')
        time.sleep(0.3)
        try:
            data = tn.read_very_eager().decode('ascii', errors='replace')
        except:
            return
        if "hp(" in data and ">" in data:
            return

def get_full_race(tn, race_name):
    """Get complete race description by paging through all output."""
    # First, make sure pager is clean
    drain_pager(tn)
    
    # Send the look command
    tn.write(f"la {race_name}\n".encode())
    time.sleep(1.5)
    
    all_text = ""
    
    for page in range(15):
        try:
            chunk = tn.read_very_eager().decode('ascii', errors='replace')
        except:
            break
        all_text += chunk
        
        # Check if we have the prompt (done)
        if "hp(" in chunk and "sp(" in chunk and ">" in chunk:
            break
        
        # Check if pager is still active
        if "(h):" in chunk or "--More--" in chunk:
            tn.write(b' ')
            time.sleep(0.5)
        else:
            # No pager prompt, but also no game prompt - wait a bit more
            time.sleep(1)
            try:
                chunk2 = tn.read_very_eager().decode('ascii', errors='replace')
                all_text += chunk2
                if "hp(" in chunk2 and ">" in chunk2:
                    break
                if "(h):" in chunk2 or "--More--" in chunk2:
                    tn.write(b' ')
                    time.sleep(0.5)
            except:
                break
    
    return all_text

# --- CONNECT AND LOGIN ---
print(f"[*] Connecting to {HOST}:{PORT}...", file=sys.stderr)
tn = telnetlib.Telnet(HOST, PORT, timeout=TIMEOUT)
time.sleep(2)

# Login menu
text = tn.read_very_eager().decode('ascii', errors='replace')
write_out("LOGIN MENU", text)

# Login
text = send_and_read(tn, CHAR_NAME, 2)
write_out("NAME ENTRY", text)

text = send_and_read(tn, CHAR_PASS, 2)
write_out("PASSWORD ENTRY", text)

# Go to race-select
text = send_and_read(tn, b'race-select\n', 3)
write_out("RACE-SELECT ROOM", text)

# --- READ SIGN ---
drain_pager(tn)
text = send_and_read(tn, b'read sign\n', 3)
write_out("READ SIGN", text)
# Page through sign if needed
for _ in range(5):
    if "(h):" in text or "--More--" in text:
        text = send_and_read(tn, b' ', 2)
        write_out("SIGN CONT", text)
    else:
        break

# --- READ POSTER ---
drain_pager(tn)
text = send_and_read(tn, b'read poster\n', 3)
write_out("READ POSTER PAGE 1", text)
poster_pages = 1
for _ in range(20):
    if "(h):" in text or "--More--" in text:
        text = send_and_read(tn, b' ', 2)
        poster_pages += 1
        write_out(f"READ POSTER PAGE {poster_pages}", text)
    else:
        break

# --- CAPTURE ALL RACES ---
RACES = [
    "cromagnon", "drow", "dwarf", "elf", "ent", "faerie", "gargoyle",
    "giant", "gnome", "goblin", "grorrark", "halfelf", "hobbit", "human",
    "kobold", "leprechaun", "lizardman", "mindflayer", "minotaur", "ogier",
    "phoenix", "snakeman", "thrikhren", "troll", "vampire", "vinnipier", "xorn"
]

for race in RACES:
    print(f"[*] Capturing {race}...", file=sys.stderr)
    text = get_full_race(tn, race)
    write_out(f"RACE: {race.upper()}", text)
    time.sleep(0.5)

# Final look
drain_pager(tn)
text = send_and_read(tn, b'look\n', 2)
write_out("FINAL LOOK", text)

tn.close()
print(f"[*] Complete. Raw data saved to: {OUTPUT_FILE}", file=sys.stderr)
