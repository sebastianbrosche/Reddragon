#!/usr/bin/env python3
"""
Islands of Myth - World Explorer v3
Handles the guided tour properly: types 'out' to skip to real gameplay.
Then explores the actual world.
"""

import telnetlib
import time
import sys

HOST = "islandsofmyth.org"
PORT = 3000
TIMEOUT = 15

CHAR_NAME = b'chronicler\n'
CHAR_PASS = b'mudarchivist2026\n'

OUTPUT_FILE = "/root/.openclaw/workspace/mud/iom_world_explore3.txt"

with open(OUTPUT_FILE, 'w') as f:
    f.write("# Islands of Myth — World Exploration v3\n# " + time.strftime("%Y-%m-%d %H:%M:%S") + "\n\n")

def write_out(label, text):
    block = f"\n{'='*70}\n=== {label} ===\n{'='*70}\n{text}\n"
    print(block, file=sys.stderr)
    with open(OUTPUT_FILE, 'a') as f:
        f.write(block)

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

# The MUD puts us in guided tour. Type 'out' to skip to character creation.
print("[*] Sending 'out' to exit guided tour...", file=sys.stderr)
tn.write(b'out\n')
time.sleep(2)
text = tn.read_very_eager().decode('ascii', errors='replace')
write_out("EXIT TOUR", text)

# Now we should be at the starting room (Welcome to Islands of Myth)
# From there, race-select to pick a race and enter world
print("[*] Going to race-select...", file=sys.stderr)
tn.write(b'race-select\n')
time.sleep(2)
text = tn.read_very_eager().decode('ascii', errors='replace')
write_out("RACE-SELECT ROOM", text)

# Pick human
tn.write(b'touch human\n')
time.sleep(2)
text = tn.read_very_eager().decode('ascii', errors='replace')
write_out("TOUCH HUMAN", text)

# Check if we got "There is no human here" - maybe the name is different
if "no human" in text.lower():
    # Try looking at all races to find the right name
    tn.write(b'all races\n')
    time.sleep(1)
    text = tn.read_very_eager().decode('ascii', errors='replace')
    write_out("ALL RACES LIST", text)

# Page helper
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

# If we're in the world now, look around
print("[*] Looking around...", file=sys.stderr)
tn.write(b'look\n')
text = page_through(tn)
write_out("LOOK START", text)

tn.write(b'exits\n')
text = page_through(tn)
write_out("EXITS START", text)

# Try to explore
tn.write(b'who\n')
text = page_through(tn)
write_out("WHO", text)

tn.write(b'score\n')
text = page_through(tn)
write_out("SCORE", text)

tn.write(b'stats\n')
text = page_through(tn)
write_out("STATS", text)

# Inventory and equipment
tn.write(b'i\n')
text = page_through(tn)
write_out("INVENTORY", text)

tn.write(b'eq\n')
text = page_through(tn)
write_out("EQUIPMENT", text)

# Try movement - go north first (to Hall of Races? or to world?)
tn.write(b'north\n')
text = page_through(tn)
write_out("GO NORTH", text)

tn.write(b'look\n')
text = page_through(tn)
write_out("LOOK NORTH", text)

tn.write(b'exits\n')
text = page_through(tn)
write_out("EXITS NORTH", text)

# Try all directions
dirs = ["south", "east", "west", "up", "down"]
for d in dirs:
    tn.write(f"{d}\n".encode())
    text = page_through(tn)
    write_out(f"GO {d.upper()}", text)
    # Look after each move
    tn.write(b'look\n')
    text = page_through(tn)
    write_out(f"LOOK {d.upper()}", text)
    time.sleep(0.3)

# Try various game commands
cmds = [
    ("SKILLS", b'skills\n'),
    ("SPELLS", b'spells\n'),
    ("HELP", b'help\n'),
    ("TIME", b'time\n'),
    ("WEATHER", b'weather\n'),
    ("MONEY", b'money\n'),
    ("CONDITION", b'condition\n'),
    ("ALIGNMENT", b'alignment\n'),
    ("HUNGER", b'hunger\n'),
    ("WIMPY", b'wimpy\n'),
    ("GHOST", b'ghost\n'),
    ("WHERE", b'where\n'),
    ("LEVELS", b'levels\n'),
    ("EXPERIENCE", b'experience\n'),
    ("COMBAT", b'combat\n'),
    ("TITLE", b'title\n'),
    ("DESCRIBE", b'describe\n'),
    ("HISTORY", b'history\n'),
    ("KILLS", b'kills\n'),
    ("DEATHS", b'deaths\n'),
    ("TOP", b'top\n'),
    ("CHANNELS", b'channels\n'),
    ("NEWS", b'news\n'),
    ("RULES", b'rules\n'),
]

for label, cmd in cmds:
    print(f"[*] Running: {label}", file=sys.stderr)
    tn.write(cmd)
    text = page_through(tn)
    write_out(label, text)
    time.sleep(0.3)

# Try to look at self and any objects
tn.write(b'look self\n')
text = page_through(tn)
write_out("LOOK SELF", text)

tn.write(b'look ground\n')
text = page_through(tn)
write_out("LOOK GROUND", text)

# Try guild-related commands
tn.write(b'guild\n')
text = page_through(tn)
write_out("GUILD", text)

tn.write(b'guilds\n')
text = page_through(tn)
write_out("GUILDS", text)

tn.write(b'guild info\n')
text = page_through(tn)
write_out("GUILD INFO", text)

# Try to find trainers, shops
tn.write(b'shops\n')
text = page_through(tn)
write_out("SHOPS", text)

tn.write(b'trainers\n')
text = page_through(tn)
write_out("TRAINERS", text)

# Try map/area commands
tn.write(b'map\n')
text = page_through(tn)
write_out("MAP", text)

tn.write(b'areas\n')
text = page_through(tn)
write_out("AREAS", text)

tn.write(b'world\n')
text = page_through(tn)
write_out("WORLD", text)

tn.write(b'mapper\n')
text = page_through(tn)
write_out("MAPPER", text)

# Try to see if there are any NPCs/mobs to look at
# (might need to be in a room with mobs)

# Final look
tn.write(b'look\n')
text = page_through(tn)
write_out("FINAL LOOK", text)

# Quit
tn.write(b'quit\n')
text = page_through(tn)
write_out("QUIT", text)

tn.close()
print(f"[*] Done. Saved to {OUTPUT_FILE}", file=sys.stderr)
