#!/usr/bin/env python3
"""
Islands of Myth - Elemental Guild Visit
Captures guild interior and outdoor area.
"""

import telnetlib
import time
import sys

HOST = "islandsofmyth.org"
PORT = 3000
TIMEOUT = 15

CHAR_NAME = b'explorer\n'
CHAR_PASS = b'testpass123\n'

OUTPUT_FILE = "/root/.openclaw/workspace/mud/iom_elemental_guild.txt"

with open(OUTPUT_FILE, 'w') as f:
    f.write("# Islands of Myth — Elemental Guild\n# " + time.strftime("%Y-%m-%d %H:%M:%S") + "\n\n")

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

print("[*] Connecting...", file=sys.stderr)
tn = telnetlib.Telnet(HOST, PORT, timeout=TIMEOUT)
time.sleep(2)
tn.read_very_eager()

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

# Navigate to guild entrance
tn.write(b'look\n')
text = read_all(tn, 1)
write_out("LOCATION", text)

if "Titan" in text or "Titan Street" in text:
    tn.write(b'north\n')
    text = read_all(tn, 1)
    tn.write(b'west\n')
    text = read_all(tn, 1)
    tn.write(b'south\n')
    text = read_all(tn, 1)
    write_out("TO GUILD", text)

# Verify at guild
tn.write(b'look\n')
text = read_all(tn, 1)
write_out("AT GUILD", text)

# Portal Room
tn.write(b'southwest\n')
text = read_all(tn, 1)
write_out("PORTAL ROOM", text)

# Elemental guild
tn.write(b'elemental\n')
text = read_all(tn, 1)
write_out("ELEMENTAL GUILD", text)

# Look around
tn.write(b'look\n')
text = read_all(tn, 1)
write_out("LOOK ELEMENTAL", text)

tn.write(b'exits\n')
text = read_all(tn, 1)
write_out("EXITS ELEMENTAL", text)

# Get guild info
tn.write(b'info\n')
text = read_all(tn, 1)
write_out("INFO ELEMENTAL", text)

# Quit pager if active
if "(h):" in text or "--More--" in text:
    tn.write(b'q')
    time.sleep(0.5)
    tn.write(b'\n')
    text = read_all(tn, 1)
    write_out("PAGER QUIT", text)

# Do out to see outdoor area
tn.write(b'out\n')
text = read_all(tn, 1)
write_out("AFTER OUT", text)

tn.write(b'look\n')
text = read_all(tn, 1)
write_out("OUT LOOK", text)

tn.write(b'exits\n')
text = read_all(tn, 1)
write_out("OUT EXITS", text)

# Explore all directions from the outdoor area to map the surroundings
dirs = ["north", "south", "east", "west", "northeast", "northwest", "southeast", "southwest"]
for d in dirs:
    print(f"[*] Outdoor: {d}", file=sys.stderr)
    tn.write(f"{d}\n".encode())
    text = read_all(tn, 1)
    write_out(f"OUT: {d.upper()}", text)
    if "it doesn't seem possible" not in text.lower():
        tn.write(b'look\n')
        text = read_all(tn, 1)
        write_out(f"LOOK {d.upper()}", text)
        # Go back
        opposites = {"north": "south", "south": "north", "east": "west", "west": "east",
                     "northeast": "southwest", "northwest": "southeast",
                     "southeast": "northwest", "southwest": "northeast"}
        tn.write(f"{opposites[d]}\n".encode())
        text = read_all(tn, 1)
        write_out(f"BACK FROM {d.upper()}", text)
    time.sleep(0.3)

# Try to go back to guild
tn.write(b'elemental\n')
text = read_all(tn, 1)
write_out("BACK TO ELEMENTAL", text)

# Quit
tn.write(b'quit\n')
text = read_all(tn, 2)
write_out("QUIT", text)
tn.close()
print("[*] Done.", file=sys.stderr)
