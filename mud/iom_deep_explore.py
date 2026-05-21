#!/usr/bin/env python3
"""
Islands of Myth - Deep Exploration
Explore remaining exits from Adventurer Guild and pull more info.
"""

import telnetlib
import time
import sys

HOST = "islandsofmyth.org"
PORT = 3000
TIMEOUT = 15

CHAR_NAME = b'explorer\n'
CHAR_PASS = b'testpass123\n'

OUTPUT_FILE = "/root/.openclaw/workspace/mud/iom_deep_explore.txt"

with open(OUTPUT_FILE, 'w') as f:
    f.write("# Islands of Myth — Deep Exploration of Illium Starting Area\n# " + time.strftime("%Y-%m-%d %H:%M:%S") + "\n\n")

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

# Enter portal to get to real world
time.sleep(1)
tn.read_very_eager()
tn.write(b'enter portal\n')
text = read_all(tn, 2)
write_out("ENTER PORTAL", text)

print("[*] In the real world!", file=sys.stderr)

# Look at the handbook in inventory
tn.write(b'look at handbook\n')
text = read_all(tn, 1)
write_out("HANDBOOK", text)

# Try remaining directions from guild entrance: southeast, northeast, southwest
remaining = ["southeast", "northeast", "southwest"]
for d in remaining:
    print(f"[*] Moving: {d}", file=sys.stderr)
    tn.write(f"{d}\n".encode())
    text = read_all(tn, 1)
    write_out(f"GO {d.upper()}", text)
    
    if "it doesn't seem possible" not in text.lower() and "you can't go" not in text.lower():
        tn.write(b'look\n')
        text = read_all(tn, 1)
        write_out(f"LOOK {d.upper()}", text)
        
        tn.write(b'exits\n')
        text = read_all(tn, 1)
        write_out(f"EXITS {d.upper()}", text)
        
        # Go back
        opposites = {"southeast": "northwest", "northeast": "southwest", "southwest": "northeast"}
        if d in opposites:
            tn.write(f"{opposites[d]}\n".encode())
            text = read_all(tn, 1)
            write_out(f"BACK FROM {d.upper()}", text)
    time.sleep(0.3)

# Back at guild entrance, try some info commands
cmds = [
    ("MAP", b'map\n'),
    ("HELP GUILDS", b'help guilds\n'),
    ("HELP FAQ", b'help faq\n'),
    ("HELP TOPICS", b'help topics\n'),
    ("HELP ALL_RACES", b'help all_races\n'),
    ("HELP ALL_SKILLS", b'help all_skills\n'),
    ("HELP ALL_SPELLS", b'help all_spells\n'),
    ("HELP GUILD_TREE", b'help guild_tree\n'),
    ("HELP RACE HUMAN", b'help race human\n'),
    ("LOOK ACHMAN", b'look achman\n'),
    ("LOOK MEMORIAL", b'look memorial\n'),
    ("LOOK MOONFLOWER", b'look moonflower\n'),
    ("LOOK FORMULA", b'look formula\n'),
    ("LOOK LODESTONE", b'look lodestone\n'),
    ("LOOK PYROCLAST", b'look pyroclast\n'),
    ("LOOK STATUE", b'look statue\n'),
]

for label, cmd in cmds:
    print(f"[*] Running: {label}", file=sys.stderr)
    tn.write(cmd)
    text = read_all(tn, 1)
    write_out(label, text)
    time.sleep(0.3)

# Try walking out to the streets and see what's out there
# From guild entrance, go north to Cloud Road, then east
tn.write(b'north\n')
text = read_all(tn, 1)
write_out("GO NORTH TO CLOUD ROAD", text)

tn.write(b'east\n')
text = read_all(tn, 1)
write_out("GO EAST ON CLOUD ROAD", text)

tn.write(b'look\n')
text = read_all(tn, 1)
write_out("LOOK EAST ON CLOUD ROAD", text)

tn.write(b'exits\n')
text = read_all(tn, 1)
write_out("EXITS EAST ON CLOUD ROAD", text)

# Go further east if possible
tn.write(b'east\n')
text = read_all(tn, 1)
write_out("GO FURTHER EAST", text)

if "it doesn't seem possible" not in text.lower():
    tn.write(b'look\n')
    text = read_all(tn, 1)
    write_out("LOOK FURTHER EAST", text)
    tn.write(b'exits\n')
    text = read_all(tn, 1)
    write_out("EXITS FURTHER EAST", text)

# Go back to guild
tn.write(b'west\n')
text = read_all(tn, 1)
write_out("BACK WEST", text)
tn.write(b'west\n')
text = read_all(tn, 1)
write_out("BACK TO GUILD", text)
tn.write(b'south\n')
text = read_all(tn, 1)
write_out("BACK SOUTH TO GUILD", text)

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
