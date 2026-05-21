#!/usr/bin/env python3
"""
Islands of Myth - Street Exploration of Illium City
Walk Cloud Road, Titan Street, Gossamer Street, and adjacent areas.
"""

import telnetlib
import time
import sys

HOST = "islandsofmyth.org"
PORT = 3000
TIMEOUT = 15

CHAR_NAME = b'explorer\n'
CHAR_PASS = b'testpass123\n'

OUTPUT_FILE = "/root/.openclaw/workspace/mud/iom_streets.txt"

with open(OUTPUT_FILE, 'w') as f:
    f.write("# Islands of Myth — Illium City Street Exploration\n# " + time.strftime("%Y-%m-%d %H:%M:%S") + "\n\n")

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

# From guild entrance, go north to Cloud Road
tn.write(b'north\n')
text = read_all(tn, 1)
write_out("CLOUD ROAD", text)

# Walk east along Titan Street - try 5 rooms east
tn.write(b'east\n')
text = read_all(tn, 1)
write_out("TITAN STREET 1", text)

tn.write(b'east\n')
text = read_all(tn, 1)
write_out("TITAN STREET 2", text)

tn.write(b'east\n')
text = read_all(tn, 1)
write_out("TITAN STREET 3", text)

tn.write(b'east\n')
text = read_all(tn, 1)
write_out("TITAN STREET 4", text)

tn.write(b'east\n')
text = read_all(tn, 1)
write_out("TITAN STREET 5", text)

# Go back west all the way
tn.write(b'west\n')
text = read_all(tn, 1)
write_out("BACK WEST 1", text)

tn.write(b'west\n')
text = read_all(tn, 1)
write_out("BACK WEST 2", text)

tn.write(b'west\n')
text = read_all(tn, 1)
write_out("BACK WEST 3", text)

tn.write(b'west\n')
text = read_all(tn, 1)
write_out("BACK WEST 4", text)

tn.write(b'west\n')
text = read_all(tn, 1)
write_out("BACK WEST 5", text)

# Now go west along Gossamer Street
tn.write(b'west\n')
text = read_all(tn, 1)
write_out("GOSSAMER STREET 1", text)

tn.write(b'west\n')
text = read_all(tn, 1)
write_out("GOSSAMER STREET 2", text)

tn.write(b'west\n')
text = read_all(tn, 1)
write_out("GOSSAMER STREET 3", text)

tn.write(b'west\n')
text = read_all(tn, 1)
text = read_all(tn, 1)
write_out("GOSSAMER STREET 4", text)

tn.write(b'west\n')
text = read_all(tn, 1)
write_out("GOSSAMER STREET 5", text)

# Go back east
tn.write(b'east\n')
text = read_all(tn, 1)
write_out("BACK EAST 1", text)

tn.write(b'east\n')
text = read_all(tn, 1)
write_out("BACK EAST 2", text)

tn.write(b'east\n')
text = read_all(tn, 1)
write_out("BACK EAST 3", text)

tn.write(b'east\n')
text = read_all(tn, 1)
write_out("BACK EAST 4", text)

tn.write(b'east\n')
text = read_all(tn, 1)
write_out("BACK EAST 5", text)

# Return to guild
tn.write(b'south\n')
text = read_all(tn, 1)
write_out("BACK TO GUILD", text)

# Final look
tn.write(b'look\n')
text = read_all(tn, 1)
write_out("FINAL LOOK", text)

# Try looking at the lodestones in the Myth Room
tn.write(b'south\n')
text = read_all(tn, 1)
write_out("GO MYTH ROOM", text)

tn.write(b'look at lodestone\n')
text = read_all(tn, 1)
write_out("LOOK LODESTONE", text)

tn.write(b'look at pyroclast\n')
text = read_all(tn, 1)
write_out("LOOK PYROCLAST", text)

tn.write(b'look at statue\n')
text = read_all(tn, 1)
write_out("LOOK STATUE", text)

# Go back to guild
tn.write(b'north\n')
text = read_all(tn, 1)
write_out("BACK NORTH", text)

# Try the equipment machine (exit 7 from map)
tn.write(b'east\n')
text = read_all(tn, 1)
write_out("GO EAST", text)

tn.write(b'southeast\n')
text = read_all(tn, 1)
write_out("GO SE TO NEWBIE", text)

tn.write(b'east\n')
text = read_all(tn, 1)
write_out("GO EAST TO NEWBIE GUILD", text)

tn.write(b'look\n')
text = read_all(tn, 1)
write_out("LOOK NEWBIE GUILD", text)

tn.write(b'exits\n')
text = read_all(tn, 1)
write_out("EXITS NEWBIE GUILD", text)

# Go back
tn.write(b'west\n')
text = read_all(tn, 1)
write_out("BACK WEST", text)

tn.write(b'northwest\n')
text = read_all(tn, 1)
write_out("BACK NW", text)

tn.write(b'west\n')
text = read_all(tn, 1)
write_out("BACK W", text)

# Try going to Maxxis' shop (exit 6 from map)
# From guild entrance: east, then north? Let me check the map
# Map shows: 1-@-2 +-6  so 6 branches from 2 (Level Advance)
# So from guild entrance -> east (Level Room) -> north? Let's try
tn.write(b'east\n')
text = read_all(tn, 1)
write_out("GO EAST TO LEVEL", text)

tn.write(b'north\n')
text = read_all(tn, 1)
write_out("GO NORTH FROM LEVEL", text)

if "it doesn't seem possible" not in text.lower():
    tn.write(b'look\n')
    text = read_all(tn, 1)
    write_out("LOOK NORTH FROM LEVEL", text)
    tn.write(b'south\n')
    text = read_all(tn, 1)
    write_out("BACK SOUTH", text)

# Try other directions from level room
tn.write(b'south\n')
text = read_all(tn, 1)
write_out("GO SOUTH FROM LEVEL", text)

if "it doesn't seem possible" not in text.lower():
    tn.write(b'look\n')
    text = read_all(tn, 1)
    write_out("LOOK SOUTH FROM LEVEL", text)
    tn.write(b'north\n')
    text = read_all(tn, 1)
    write_out("BACK NORTH", text)

# Back to guild
tn.write(b'west\n')
text = read_all(tn, 1)
write_out("BACK TO GUILD FINAL", text)

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
