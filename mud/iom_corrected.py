#!/usr/bin/env python3
"""
Islands of Myth - Central Square + Warrior Guild (Corrected Pathing)
"""

import telnetlib
import time
import sys

HOST = "islandsofmyth.org"
PORT = 3000
TIMEOUT = 15

CHAR_NAME = b'explorer\n'
CHAR_PASS = b'testpass123\n'

OUTPUT_FILE = "/root/.openclaw/workspace/mud/iom_corrected.txt"

with open(OUTPUT_FILE, 'w') as f:
    f.write("# Islands of Myth — Corrected Central Square + Warrior Guild\n# " + time.strftime("%Y-%m-%d %H:%M:%S") + "\n\n")

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

# === PATH TO CENTRAL SQUARE ===
# From guild entrance: north to Cloud Road, then west 4 times to Intersection of Illium and Cloud, then south
print("[*] Pathing to Central Square...", file=sys.stderr)

tn.write(b'north\n')
text = read_all(tn, 1)
write_out("STEP 1: NORTH", text)

tn.write(b'west\n')
text = read_all(tn, 1)
write_out("STEP 2: WEST", text)

tn.write(b'west\n')
text = read_all(tn, 1)
write_out("STEP 3: WEST", text)

tn.write(b'west\n')
text = read_all(tn, 1)
write_out("STEP 4: WEST", text)

tn.write(b'west\n')
text = read_all(tn, 1)
write_out("STEP 5: WEST (ILLIUM/CLOUD)", text)

# Now south to Central Square
tn.write(b'south\n')
text = read_all(tn, 1)
write_out("SOUTH TO CENTRAL SQUARE", text)

tn.write(b'look\n')
text = read_all(tn, 1)
write_out("LOOK CENTRAL SQUARE", text)

tn.write(b'exits\n')
text = read_all(tn, 1)
write_out("EXITS CENTRAL SQUARE", text)

# Try all directions from Central Square
dirs = ["north", "south", "east", "west", "northeast", "northwest", "southeast", "southwest"]
for d in dirs:
    print(f"[*] Central Square: {d}", file=sys.stderr)
    tn.write(f"{d}\n".encode())
    text = read_all(tn, 1)
    write_out(f"CENTRAL: {d.upper()}", text)
    if "it doesn't seem possible" not in text.lower() and "you can't go" not in text.lower():
        tn.write(b'look\n')
        text = read_all(tn, 1)
        write_out(f"LOOK {d.upper()}", text)
        opposites = {"north": "south", "south": "north", "east": "west", "west": "east",
                     "northeast": "southwest", "northwest": "southeast",
                     "southeast": "northwest", "southwest": "northeast"}
        tn.write(f"{opposites[d]}\n".encode())
        text = read_all(tn, 1)
        write_out(f"BACK FROM {d.upper()}", text)
    time.sleep(0.3)

# === RETURN TO GUILD ===
print("[*] Returning to guild...", file=sys.stderr)
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

tn.write(b'east\n')
text = read_all(tn, 1)
write_out("BACK EAST 4", text)

tn.write(b'south\n')
text = read_all(tn, 1)
write_out("BACK TO GUILD", text)

# Verify we're at guild
tn.write(b'look\n')
text = read_all(tn, 1)
write_out("VERIFY GUILD", text)

# === VISIT WARRIOR GUILD ===
print("[*] Visiting Warrior Guild...", file=sys.stderr)
tn.write(b'southwest\n')
text = read_all(tn, 1)
write_out("PORTAL ROOM", text)

tn.write(b'warrior\n')
text = read_all(tn, 1)
write_out("WARRIOR GUILD", text)

tn.write(b'look\n')
text = read_all(tn, 1)
write_out("LOOK WARRIOR", text)

tn.write(b'exits\n')
text = read_all(tn, 1)
write_out("EXITS WARRIOR", text)

# Try warrior-specific commands
tn.write(b'list\n')
text = read_all(tn, 1)
write_out("LIST", text)

tn.write(b'costs\n')
text = read_all(tn, 1)
write_out("COSTS", text)

tn.write(b'info\n')
text = read_all(tn, 1)
write_out("INFO", text)

# Back to portal room
tn.write(b'northeast\n')
text = read_all(tn, 1)
write_out("BACK PORTAL", text)

# Back to guild
tn.write(b'northeast\n')
text = read_all(tn, 1)
write_out("BACK TO GUILD", text)

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
