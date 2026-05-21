#!/usr/bin/env python3
"""
Islands of Myth - Warrior Guild Visit (Adaptive Navigation)
Finds current location, navigates to guild, visits Warrior guild hall.
"""

import telnetlib
import time
import sys

HOST = "islandsofmyth.org"
PORT = 3000
TIMEOUT = 15

CHAR_NAME = b'explorer\n'
CHAR_PASS = b'testpass123\n'

OUTPUT_FILE = "/root/.openclaw/workspace/mud/iom_warrior_guild.txt"

with open(OUTPUT_FILE, 'w') as f:
    f.write("# Islands of Myth — Warrior Guild Hall\n# " + time.strftime("%Y-%m-%d %H:%M:%S") + "\n\n")

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

# Figure out where we are
time.sleep(1)
tn.read_very_eager()
tn.write(b'look\n')
text = read_all(tn, 1)
write_out("CURRENT LOCATION", text)

# Navigate to guild entrance
# If on Titan Street -> north -> west -> south (guild interior)
# If elsewhere, adapt
print("[*] Navigating to guild...", file=sys.stderr)

# Check if we're already at the guild or nearby
if "Titan street" in text or "Titan Street" in text:
    print("[*] On Titan Street, going north...", file=sys.stderr)
    tn.write(b'north\n')
    text = read_all(tn, 1)
    write_out("NORTH", text)
    
    tn.write(b'west\n')
    text = read_all(tn, 1)
    write_out("WEST", text)
    
    tn.write(b'south\n')
    text = read_all(tn, 1)
    write_out("SOUTH TO GUILD", text)

elif "Intersection of Cloud and Titan" in text:
    print("[*] At Cloud/Titan intersection, going west then south...", file=sys.stderr)
    tn.write(b'west\n')
    text = read_all(tn, 1)
    write_out("WEST", text)
    
    tn.write(b'south\n')
    text = read_all(tn, 1)
    write_out("SOUTH TO GUILD", text)

elif "On Cloud Road between Gossamer and Titan" in text:
    print("[*] At Cloud Road, going south to guild...", file=sys.stderr)
    tn.write(b'south\n')
    text = read_all(tn, 1)
    write_out("SOUTH TO GUILD", text)

else:
    print("[*] Unknown location, trying to find guild...", file=sys.stderr)
    # Try going to a known intersection and then to guild
    # First, try to find a street we recognize
    # Let's just try going to Titan Street area
    # From most central locations, we can reach the guild via:
    # Anywhere -> find Cloud Road or Titan Street -> navigate
    
    # Try south repeatedly until we hit something familiar
    for i in range(5):
        tn.write(b'look\n')
        text = read_all(tn, 1)
        write_out(f"LOOK {i}", text)
        if "Titan" in text or "Guild" in text or "Cloud Road" in text:
            break
        tn.write(b'south\n')
        text = read_all(tn, 1)
        write_out(f"SOUTH {i}", text)
    
    # Now try to reach guild
    if "Titan street" in text or "Titan Street" in text:
        tn.write(b'north\n')
        text = read_all(tn, 1)
        write_out("NORTH", text)
        tn.write(b'west\n')
        text = read_all(tn, 1)
        write_out("WEST", text)
        tn.write(b'south\n')
        text = read_all(tn, 1)
        write_out("SOUTH TO GUILD", text)

# Verify we're at the guild
tn.write(b'look\n')
text = read_all(tn, 1)
write_out("VERIFY GUILD", text)

# Visit Portal Room
tn.write(b'southwest\n')
text = read_all(tn, 1)
write_out("PORTAL ROOM", text)

# Look at portal room
tn.write(b'look\n')
text = read_all(tn, 1)
write_out("LOOK PORTAL", text)

tn.write(b'exits\n')
text = read_all(tn, 1)
write_out("EXITS PORTAL", text)

# Visit Warrior guild
tn.write(b'warrior\n')
text = read_all(tn, 1)
write_out("WARRIOR GUILD", text)

# Look around
tn.write(b'look\n')
text = read_all(tn, 1)
write_out("LOOK WARRIOR", text)

tn.write(b'exits\n')
text = read_all(tn, 1)
write_out("EXITS WARRIOR", text)

# Try guild commands
tn.write(b'list\n')
text = read_all(tn, 1)
write_out("LIST", text)

tn.write(b'info\n')
text = read_all(tn, 1)
write_out("INFO", text)

tn.write(b'help\n')
text = read_all(tn, 1)
write_out("HELP WARRIOR", text)

# Return to portal room
tn.write(b'northeast\n')
text = read_all(tn, 1)
write_out("BACK PORTAL", text)

# Return to guild
tn.write(b'northeast\n')
text = read_all(tn, 1)
write_out("BACK TO GUILD", text)

# Go back to street and quit from a known outdoor location for next time
# From guild interior, let's go north to the street
tn.write(b'look\n')
text = read_all(tn, 1)
write_out("FINAL LOOK", text)

# If at guild, go north to street
if "Adventurer" in text or "Guild" in text:
    tn.write(b'north\n')
    text = read_all(tn, 1)
    write_out("TO STREET", text)

# Quit
tn.write(b'quit\n')
text = read_all(tn, 2)
write_out("QUIT", text)

tn.close()
print(f"[*] Done. Saved to {OUTPUT_FILE}", file=sys.stderr)
