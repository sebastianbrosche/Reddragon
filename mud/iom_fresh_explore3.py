#!/usr/bin/env python3
"""
Islands of Myth - Fresh Character + World Explorer v3
Fixed: sends NAME after 'c' create prompt, not password.
"""

import telnetlib
import time
import sys

HOST = "islandsofmyth.org"
PORT = 3000
TIMEOUT = 15

CHAR_NAME = b'explorer\n'
CHAR_PASS = b'testpass123\n'
EMAIL = b'\n'
HEAR = b'\n'
GENDER = b'm\n'

OUTPUT_FILE = "/root/.openclaw/workspace/mud/iom_fresh_explore3.txt"

with open(OUTPUT_FILE, 'w') as f:
    f.write("# Islands of Myth — Fresh Character + World Exploration v3\n# " + time.strftime("%Y-%m-%d %H:%M:%S") + "\n\n")

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

# Step 1: Enter name at login menu
tn.write(CHAR_NAME)
time.sleep(1)
text = read_all(tn, 1)
write_out("LOGIN NAME", text)

# Step 2: If prompted to create, send 'c'
if "create" in text.lower() and "'c'" in text.lower():
    print("[*] Sending 'c' to create character...", file=sys.stderr)
    tn.write(b'c\n')
    time.sleep(1)
    text = read_all(tn, 1)
    write_out("CREATE PROMPT", text)

# Step 3: Send name again at "New character name:" prompt
if "new character name" in text.lower():
    print("[*] Sending name again...", file=sys.stderr)
    tn.write(CHAR_NAME)
    time.sleep(1)
    text = read_all(tn, 1)
    write_out("NAME ENTRY 2", text)

# Step 4: Confirm name if asked
if "correct" in text.lower():
    print("[*] Confirming name...", file=sys.stderr)
    tn.write(b'y\n')
    time.sleep(1)
    text = read_all(tn, 1)
    write_out("NAME CONFIRM", text)

# Step 5: Password
tn.write(CHAR_PASS)
time.sleep(1)
text = read_all(tn, 1)
write_out("PASSWORD", text)

# Step 6: Re-enter password if asked
if "re-enter" in text.lower() or "again" in text.lower() or "verify" in text.lower():
    print("[*] Re-entering password...", file=sys.stderr)
    tn.write(CHAR_PASS)
    time.sleep(1)
    text = read_all(tn, 1)
    write_out("PASSWORD VERIFY", text)

# Step 7: Email
tn.write(EMAIL)
time.sleep(1)
text = read_all(tn, 1)
write_out("EMAIL", text)

# Step 8: How did you hear
tn.write(HEAR)
time.sleep(1)
text = read_all(tn, 1)
write_out("HEAR ABOUT", text)

# Step 9: Gender
tn.write(GENDER)
time.sleep(1)
text = read_all(tn, 1)
write_out("GENDER", text)

# Now we should be in the starting room
print("[*] Should be in starting room now", file=sys.stderr)

tn.write(b'look\n')
text = read_all(tn, 1)
write_out("STARTING ROOM", text)

tn.write(b'exits\n')
text = read_all(tn, 1)
write_out("EXITS", text)

# Go to race-select and pick human
tn.write(b'race-select\n')
text = read_all(tn, 2)
write_out("RACE-SELECT", text)

tn.write(b'touch human\n')
text = read_all(tn, 2)
write_out("TOUCH HUMAN", text)

# Now in real world
print("[*] Should be in real world now", file=sys.stderr)

tn.write(b'look\n')
text = read_all(tn, 1)
write_out("REAL WORLD LOOK", text)

tn.write(b'exits\n')
text = read_all(tn, 1)
write_out("REAL WORLD EXITS", text)

# Basic commands
cmds = [
    ("WHO", b'who\n'), ("SCORE", b'score\n'), ("STATS", b'stats\n'),
    ("INVENTORY", b'i\n'), ("EQUIPMENT", b'eq\n'),
    ("SKILLS", b'skills\n'), ("SPELLS", b'spells\n'), ("HELP", b'help\n'),
    ("TIME", b'time\n'), ("WEATHER", b'weather\n'), ("MONEY", b'money\n'),
    ("CONDITION", b'condition\n'), ("ALIGNMENT", b'alignment\n'), ("HUNGER", b'hunger\n'),
    ("WIMPY", b'wimpy\n'), ("GHOST", b'ghost\n'), ("WHERE", b'where\n'),
    ("LEVELS", b'levels\n'), ("EXPERIENCE", b'experience\n'), ("COMBAT", b'combat\n'),
    ("TITLE", b'title\n'), ("DESCRIBE", b'describe\n'), ("HISTORY", b'history\n'),
    ("KILLS", b'kills\n'), ("DEATHS", b'deaths\n'), ("TOP", b'top\n'),
    ("CHANNELS", b'channels\n'), ("NEWS", b'news\n'), ("RULES", b'rules\n'),
    ("GUILD", b'guild\n'), ("GUILDS", b'guilds\n'), ("GUILD INFO", b'guild info\n'),
    ("SHOPS", b'shops\n'), ("TRAINERS", b'trainers\n'), ("MAP", b'map\n'),
    ("AREAS", b'areas\n'), ("WORLD", b'world\n'), ("MAPPER", b'mapper\n'),
    ("LOOK SELF", b'look self\n'), ("LOOK GROUND", b'look ground\n'),
]

for label, cmd in cmds:
    print(f"[*] Running: {label}", file=sys.stderr)
    tn.write(cmd)
    text = read_all(tn, 1)
    write_out(label, text)
    time.sleep(0.3)

# Movement from starting room
dirs = ["north", "south", "east", "west", "up", "down"]
for d in dirs:
    print(f"[*] Moving: {d}", file=sys.stderr)
    tn.write(f"{d}\n".encode())
    text = read_all(tn, 1)
    write_out(f"GO {d.upper()}", text)
    
    tn.write(b'look\n')
    text = read_all(tn, 1)
    write_out(f"LOOK {d.upper()}", text)
    
    opposite = {"north": "south", "south": "north", "east": "west", "west": "east", "up": "down", "down": "up"}
    tn.write(f"{opposite[d]}\n".encode())
    text = read_all(tn, 1)
    write_out(f"BACK FROM {d.upper()}", text)
    time.sleep(0.3)

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
