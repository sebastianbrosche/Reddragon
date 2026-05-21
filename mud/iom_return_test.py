#!/usr/bin/env python3
"""
Test return path from Warrior Training Center.
"""

import telnetlib
import time
import sys

HOST = "islandsofmyth.org"
PORT = 3000
TIMEOUT = 15

CHAR_NAME = b'explorer\n'
CHAR_PASS = b'testpass123\n'

with open("/root/.openclaw/workspace/mud/iom_return_test.txt", 'w') as f:
    f.write("# Return Path Test\n")

def write_out(label, text):
    block = f"\n=== {label} ===\n{text}\n"
    print(block, file=sys.stderr)
    with open("/root/.openclaw/workspace/mud/iom_return_test.txt", 'a') as f:
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

# Verify
tn.write(b'look\n')
text = read_all(tn, 1)
write_out("AT GUILD", text)

# Portal Room
tn.write(b'southwest\n')
text = read_all(tn, 1)
write_out("PORTAL ROOM", text)

# Warrior guild
tn.write(b'warrior\n')
text = read_all(tn, 1)
write_out("WARRIOR", text)

# Do out
tn.write(b'out\n')
text = read_all(tn, 1)
write_out("AFTER OUT", text)

# Look and exits
tn.write(b'look\n')
text = read_all(tn, 1)
write_out("OUT ROOM LOOK", text)

tn.write(b'exits\n')
text = read_all(tn, 1)
write_out("OUT ROOM EXITS", text)

# Try various return directions
for d in ["in", "enter", "north", "south", "east", "west", "northeast", "northwest", "southeast", "southwest", "portal", "warrior"]:
    print(f"[*] Trying: {d}", file=sys.stderr)
    tn.write(f"{d}\n".encode())
    text = read_all(tn, 1)
    write_out(f"TRY {d.upper()}", text)
    if "Portal Room" in text or "Adventurer Guild" in text:
        print(f"[***] FOUND RETURN: {d}", file=sys.stderr)
        break
    # Go back if we moved somewhere else
    if "it doesn't seem possible" not in text.lower() and "you can't go" not in text.lower():
        opposites = {"north": "south", "south": "north", "east": "west", "west": "east",
                     "northeast": "southwest", "northwest": "southeast",
                     "southeast": "northwest", "southwest": "northeast",
                     "in": "out", "enter": "out"}
        if d in opposites:
            tn.write(f"{opposites[d]}\n".encode())
            text = read_all(tn, 1)
            write_out(f"BACK FROM {d.upper()}", text)

# Quit
tn.write(b'quit\n')
text = read_all(tn, 2)
write_out("QUIT", text)
tn.close()
print("[*] Done.", file=sys.stderr)
