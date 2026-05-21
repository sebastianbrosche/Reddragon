#!/usr/bin/env python3
"""
Islands of Myth - Enter the World
Log in as existing character, read the sign, enter portal, explore.
"""

import telnetlib
import time
import sys

HOST = "islandsofmyth.org"
PORT = 3000
TIMEOUT = 15

CHAR_NAME = b'explorer\n'
CHAR_PASS = b'testpass123\n'

OUTPUT_FILE = "/root/.openclaw/workspace/mud/iom_enter_world.txt"

with open(OUTPUT_FILE, 'w') as f:
    f.write("# Islands of Myth — Enter the World & Explore\n# " + time.strftime("%Y-%m-%d %H:%M:%S") + "\n\n")

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

# Login as existing character
tn.write(CHAR_NAME)
time.sleep(1)
text = read_all(tn, 1)
write_out("LOGIN", text)

# Should ask for password
tn.write(CHAR_PASS)
time.sleep(1)
text = read_all(tn, 1)
write_out("PASSWORD", text)

# In the Gates room now
print("[*] In Gates room", file=sys.stderr)

tn.write(b'look\n')
text = read_all(tn, 1)
write_out("GATES LOOK", text)

tn.write(b'look sign\n')
text = read_all(tn, 1)
write_out("GATES SIGN", text)

# Enter the portal!
print("[*] Entering portal...", file=sys.stderr)
tn.write(b'enter portal\n')
text = read_all(tn, 2)
write_out("ENTER PORTAL", text)

# Now we should be in the actual world
print("[*] In the real world!", file=sys.stderr)

tn.write(b'look\n')
text = read_all(tn, 1)
write_out("WORLD LOOK", text)

tn.write(b'exits\n')
text = read_all(tn, 1)
write_out("WORLD EXITS", text)

# Check what's here
tn.write(b'look sign\n')
text = read_all(tn, 1)
write_out("WORLD SIGN", text)

# Explore in each direction from the first real room
dirs = ["north", "south", "east", "west", "up", "down"]
for d in dirs:
    print(f"[*] Moving: {d}", file=sys.stderr)
    tn.write(f"{d}\n".encode())
    text = read_all(tn, 1)
    write_out(f"GO {d.upper()}", text)
    
    # If we moved successfully, look around
    if "it doesn't seem possible" not in text.lower():
        tn.write(b'look\n')
        text = read_all(tn, 1)
        write_out(f"LOOK {d.upper()}", text)
        
        tn.write(b'exits\n')
        text = read_all(tn, 1)
        write_out(f"EXITS {d.upper()}", text)
        
        # Go back
        opposite = {"north": "south", "south": "north", "east": "west", "west": "east", "up": "down", "down": "up"}
        tn.write(f"{opposite[d]}\n".encode())
        text = read_all(tn, 1)
        write_out(f"BACK FROM {d.upper()}", text)
    time.sleep(0.3)

# Final look at starting point
tn.write(b'look\n')
text = read_all(tn, 1)
write_out("FINAL LOOK", text)

# Try some exploration commands
cmds = [
    ("WHO", b'who\n'), ("SCORE", b'score\n'), ("STATS", b'stats\n'),
    ("MAP", b'map\n'), ("LOOK SELF", b'look self\n'), ("INVENTORY", b'i\n'),
]
for label, cmd in cmds:
    print(f"[*] Running: {label}", file=sys.stderr)
    tn.write(cmd)
    text = read_all(tn, 1)
    write_out(label, text)
    time.sleep(0.3)

# Quit
tn.write(b'quit\n')
text = read_all(tn, 2)
write_out("QUIT", text)

tn.close()
print(f"[*] Done. Saved to {OUTPUT_FILE}", file=sys.stderr)
