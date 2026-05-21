#!/usr/bin/env python3
"""
Islands of Myth - World Explorer v2
Skips tour, selects a race, enters the world, explores.
"""

import telnetlib
import time
import sys

HOST = "islandsofmyth.org"
PORT = 3000
TIMEOUT = 15

CHAR_NAME = b'chronicler\n'
CHAR_PASS = b'mudarchivist2026\n'

OUTPUT_FILE = "/root/.openclaw/workspace/mud/iom_world_explore2.txt"

with open(OUTPUT_FILE, 'w') as f:
    f.write("# Islands of Myth — World Exploration v2\n# " + time.strftime("%Y-%m-%d %H:%M:%S") + "\n\n")

def write_out(label, text):
    block = f"\n{'='*70}\n=== {label} ===\n{'='*70}\n{text}\n"
    print(block, file=sys.stderr)
    with open(OUTPUT_FILE, 'a') as f:
        f.write(block)

# Connect
print(f"[*] Connecting...", file=sys.stderr)
tn = telnetlib.Telnet(HOST, PORT, timeout=TIMEOUT)
time.sleep(2)

tn.read_very_eager()
tn.write(CHAR_NAME)
time.sleep(1.5)
tn.read_very_eager()
tn.write(CHAR_PASS)
time.sleep(2)

text = tn.read_very_eager().decode('ascii', errors='replace')
write_out("LOGIN", text)

# Go straight to race-select, skip tour
tn.write(b'race-select\n')
time.sleep(2)
text = tn.read_very_eager().decode('ascii', errors='replace')
write_out("RACE-SELECT", text)

# Select human
tn.write(b'touch human\n')
time.sleep(2)
text = tn.read_very_eager().decode('ascii', errors='replace')
write_out("SELECT HUMAN", text)

# Now we should be in the world
time.sleep(1)

def page_through(tn, wait=1.5):
    time.sleep(wait)
    all_text = ""
    for _ in range(20):
        try:
            chunk = tn.read_very_eager().decode('ascii', errors='replace')
        except:
            break
        all_text += chunk
        if "(h):" in chunk or "--More--" in chunk:
            tn.write(b' ')
            time.sleep(0.4)
        elif "hp(" in chunk and "sp(" in chunk and "ep(" in chunk and ">" in chunk:
            break
        else:
            time.sleep(0.5)
    return all_text

# Look at starting room
tn.write(b'look\n')
text = page_through(tn)
write_out("STARTING ROOM", text)

# Exits
tn.write(b'exits\n')
text = page_through(tn)
write_out("EXITS", text)

# Who
tn.write(b'who\n')
text = page_through(tn)
write_out("WHO", text)

# Score
tn.write(b'score\n')
text = page_through(tn)
write_out("SCORE", text)

# Inventory
tn.write(b'i\n')
text = page_through(tn)
write_out("INVENTORY", text)

# Equipment
tn.write(b'eq\n')
text = page_through(tn)
write_out("EQUIPMENT", text)

# Try various commands
cmds = [
    ("SKILLS", b'skills\n'),
    ("SPELLS", b'spells\n'),
    ("MAPPER", b'mapper\n'),
    ("MAP", b'map\n'),
    ("AREAS", b'areas\n'),
    ("WORLDS", b'worlds\n'),
    ("COMMANDS", b'commands\n'),
    ("TIME", b'time\n'),
    ("WEATHER", b'weather\n'),
    ("MONEY", b'money\n'),
    ("BANK", b'bank\n'),
    ("SHOPS", b'shops\n'),
    ("TRAINERS", b'trainers\n'),
    ("QUESTS", b'quests\n'),
    ("TOP", b'top\n'),
    ("TOP2", b'top 2\n'),
    ("TOP10", b'top 10\n'),
    ("TITLE", b'title\n'),
    ("DESCRIBE", b'describe\n'),
    ("HISTORY", b'history\n'),
    ("KILLS", b'kills\n'),
    ("DEATHS", b'deaths\n'),
    ("LEVELS", b'levels\n'),
    ("EXPERIENCE", b'experience\n'),
    ("COMBAT", b'combat\n'),
    ("CONDITION", b'condition\n'),
    ("ALIGNMENT", b'alignment\n'),
    ("HUNGER", b'hunger\n'),
    ("WIMPY", b'wimpy\n'),
    ("GHOST", b'ghost\n'),
    ("WHERE", b'where\n'),
    ("LOOK SELF", b'look self\n'),
    ("LOOK GROUND", b'look ground\n'),
]

for label, cmd in cmds:
    print(f"[*] Running: {label}", file=sys.stderr)
    tn.write(cmd)
    text = page_through(tn)
    write_out(label, text)
    time.sleep(0.3)

# Try moving around
tn.write(b'north\n')
text = page_through(tn)
write_out("GO NORTH", text)

tn.write(b'look\n')
text = page_through(tn)
write_out("LOOK NORTH ROOM", text)

tn.write(b'exits\n')
text = page_through(tn)
write_out("EXITS NORTH ROOM", text)

# Try to go south back
tn.write(b'south\n')
text = page_through(tn)
write_out("GO SOUTH", text)

# Try all directions from start
dirs = ["north", "south", "east", "west", "up", "down", "northeast", "northwest", "southeast", "southwest"]
for d in dirs:
    tn.write(f"{d}\n".encode())
    text = page_through(tn)
    write_out(f"GO {d.upper()}", text)
    time.sleep(0.3)

# Look at any interesting objects/people
tn.write(b'look\n')
text = page_through(tn)
write_out("FINAL LOOK", text)

# Quit
tn.write(b'quit\n')
text = page_through(tn)
write_out("QUIT", text)

tn.close()
print(f"[*] Done. Saved to {OUTPUT_FILE}", file=sys.stderr)
