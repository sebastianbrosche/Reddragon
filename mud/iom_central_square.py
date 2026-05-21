#!/usr/bin/env python3
"""
Islands of Myth - Central Square + Handbook + Guild Hall
Explore south toward Central Square, read handbook, peek into a guild.
"""

import telnetlib
import time
import sys

HOST = "islandsofmyth.org"
PORT = 3000
TIMEOUT = 15

CHAR_NAME = b'explorer\n'
CHAR_PASS = b'testpass123\n'

OUTPUT_FILE = "/root/.openclaw/workspace/mud/iom_central_square.txt"

with open(OUTPUT_FILE, 'w') as f:
    f.write("# Islands of Myth — Central Square + Handbook + Guild Hall\n# " + time.strftime("%Y-%m-%d %H:%M:%S") + "\n\n")

def write_out(label, text):
    block = f"\n{'='*70}\n=== {label} ===\n{'='*70}\n{text}\n"
    print(block, file=sys.stderr)
    with open(OUTPUT_FILE, 'a') as f:
        f.write(block)

def read_all(tn, wait=1.5):
    time.sleep(wait)
    all_text = ""
    for _ in range(10):
        try:
            chunk = tn.read_very_eager().decode('ascii', errors='replace')
        except:
            break
        all_text += chunk
        if "(h):" in chunk or "--More--" in chunk:
            tn.write(b' ')
            time.sleep(0.4)
        elif chunk:
            time.sleep(0.3)
        else:
            break
    return all_text

def read_through_pager(tn, wait=1.5):
    time.sleep(wait)
    all_text = ""
    for _ in range(30):
        try:
            chunk = tn.read_very_eager().decode('ascii', errors='replace')
        except:
            break
        all_text += chunk
        if "--More--" in chunk or "(h):" in chunk:
            tn.write(b' ')
            time.sleep(0.3)
        elif chunk:
            time.sleep(0.2)
        else:
            break
    return all_text

print(f"[*] Connecting...", file=sys.stderr)
tn = telnetlib.Telnet(HOST, PORT, timeout=TIMEOUT)
time.sleep(2)

# Clear banner
tn.read_very_eager()

# Login
tn.write(CHAR_NAME)
time.sleep(1)
text = read_all(tn, 1)
write_out("LOGIN", text)

tn.write(CHAR_PASS)
time.sleep(1)
text = read_all(tn, 1)
write_out("PASSWORD", text)

# Enter portal
time.sleep(1)
tn.read_very_eager()
tn.write(b'enter portal\n')
text = read_all(tn, 2)
write_out("ENTER PORTAL", text)

print("[*] In the real world!", file=sys.stderr)

# First, read all handbook topics
handbook_topics = [
    "Introduction", "Newbie", "Movement", "Interaction", "Directions",
    "Advancement", "Events", "Guilds", "Party", "Quests", "Channels",
    "Sales", "Combat", "News", "Abbreviations", "Misc"
]
for topic in handbook_topics:
    print(f"[*] Handbook topic: {topic}", file=sys.stderr)
    tn.write(f"read about {topic}\n".encode())
    text = read_through_pager(tn, 1)
    write_out(f"HANDBOOK: {topic}", text)
    time.sleep(0.3)
    tn.read_very_eager()

# Now explore south from guild entrance toward Central Square
# From guild: north to Cloud Road, then go various directions
# Actually let's start from guild and try going south... but south is Myth Room
# Let's go: north, west, west, west, south (toward Central Square from Illium/Cloud intersection)
tn.write(b'north\n')
text = read_all(tn, 1)
write_out("NORTH TO CLOUD", text)

tn.write(b'west\n')
text = read_all(tn, 1)
write_out("WEST 1", text)

tn.write(b'west\n')
text = read_all(tn, 1)
write_out("WEST 2", text)

tn.write(b'west\n')
text = read_all(tn, 1)
write_out("WEST 3", text)

tn.write(b'south\n')
text = read_all(tn, 1)
write_out("SOUTH TO CENTRAL SQUARE", text)

tn.write(b'look\n')
text = read_all(tn, 1)
write_out("LOOK CENTRAL SQUARE", text)

tn.write(b'exits\n')
text = read_all(tn, 1)
write_out("EXITS CENTRAL SQUARE", text)

# Try a few directions from Central Square
dirs = ["north", "south", "east", "west"]
for d in dirs:
    print(f"[*] From Central Square: {d}", file=sys.stderr)
    tn.write(f"{d}\n".encode())
    text = read_all(tn, 1)
    write_out(f"CENTRAL SQUARE: {d.upper()}", text)
    if "it doesn't seem possible" not in text.lower():
        tn.write(b'look\n')
        text = read_all(tn, 1)
        write_out(f"LOOK {d.upper()} FROM CENTRAL", text)
        # Go back
        opposites = {"north": "south", "south": "north", "east": "west", "west": "east"}
        tn.write(f"{opposites[d]}\n".encode())
        text = read_all(tn, 1)
        write_out(f"BACK FROM {d.upper()}", text)
    time.sleep(0.3)

# Return to guild
tn.write(b'north\n')
text = read_all(tn, 1)
write_out("BACK NORTH", text)

tn.write(b'east\n')
text = read_all(tn, 1)
write_out("BACK EAST 1", text)

tn.write(b'east\n')
text = read_all(tn, 1)
write_out("BACK EAST 2", text)

tn.write(b'east\n')
text = read_all(tn, 1)
write_out("BACK EAST 3", text)

tn.write(b'south\n')
text = read_all(tn, 1)
write_out("BACK TO GUILD", text)

# Now visit one guild hall - let's try Warrior
tn.write(b'southwest\n')
text = read_all(tn, 1)
write_out("GO PORTAL ROOM", text)

tn.write(b'warrior\n')
text = read_all(tn, 1)
write_out("GO WARRIOR GUILD", text)

tn.write(b'look\n')
text = read_all(tn, 1)
write_out("LOOK WARRIOR GUILD", text)

tn.write(b'exits\n')
text = read_all(tn, 1)
write_out("EXITS WARRIOR GUILD", text)

# Try to get guild info
tn.write(b'help warrior\n')
text = read_all(tn, 1)
write_out("HELP WARRIOR", text)

# Go back to portal room
tn.write(b'northeast\n')
text = read_all(tn, 1)
write_out("BACK TO PORTAL ROOM", text)

# Visit one more guild - Elemental
tn.write(b'elemental\n')
text = read_all(tn, 1)
write_out("GO ELEMENTAL GUILD", text)

tn.write(b'look\n')
text = read_all(tn, 1)
write_out("LOOK ELEMENTAL GUILD", text)

tn.write(b'exits\n')
text = read_all(tn, 1)
write_out("EXITS ELEMENTAL GUILD", text)

# Back to portal room
tn.write(b'northeast\n')
text = read_all(tn, 1)
write_out("BACK TO PORTAL ROOM 2", text)

# Back to guild
tn.write(b'northeast\n')
text = read_all(tn, 1)
write_out("BACK TO GUILD FROM PORTAL", text)

# Final
tn.write(b'look\n')
text = read_all(tn, 1)
write_out("FINAL LOOK", text)

# Quit
tn.write(b'quit\n')
text = read_all(tn, 2)
write_out("QUIT", text)

tn.close()
print(f"[*] Done. Saved to {OUTPUT_FILE}", file=sys.stderr)
