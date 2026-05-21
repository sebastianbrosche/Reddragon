#!/usr/bin/env python3
"""
Fresh character creator + single guild visitor (PURE LETTER NAMES).
Generates names with only lower-case letters, no numbers.
"""

import telnetlib
import time
import sys
import random
import string

HOST = "islandsofmyth.org"
PORT = 3000
TIMEOUT = 15

GUILD_NAME = sys.argv[1] if len(sys.argv) > 1 else "psychics"
# Generate name: 'scout' + 4 random lowercase letters (no numbers!)
CHAR_NAME = "scout" + ''.join(random.choices(string.ascii_lowercase, k=4))
CHAR_PASS = "testpass123"

OUTPUT_FILE = f"/root/.openclaw/workspace/mud/iom_guild_{GUILD_NAME}.txt"

with open(OUTPUT_FILE, 'w') as f:
    f.write(f"# Islands of Myth — {GUILD_NAME.title()} Guild\n# Character: {CHAR_NAME}\n# " + time.strftime("%Y-%m-%d %H:%M:%S") + "\n\n")

def write_out(label, text):
    block = f"\n{'='*70}\n=== {label} ===\n{'='*70}\n{text}\n"
    print(block, file=sys.stderr)
    with open(OUTPUT_FILE, 'a') as f:
        f.write(block)

def read_until_prompt(tn, wait=2):
    time.sleep(wait)
    all_text = ""
    for _ in range(15):
        try:
            chunk = tn.read_very_eager().decode('ascii', errors='replace')
        except:
            break
        all_text += chunk
        if "hp(" in chunk or "Your Selection?" in chunk or "New character name:" in chunk or "Please enter" in chunk or "Would you like" in chunk:
            break
        if chunk:
            time.sleep(0.3)
        else:
            break
    return all_text

def read_all(tn, wait=1.5, max_chunks=30):
    time.sleep(wait)
    all_text = ""
    for _ in range(max_chunks):
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

print(f"[*] Creating character '{CHAR_NAME}' to visit {GUILD_NAME} guild...", file=sys.stderr)
tn = telnetlib.Telnet(HOST, PORT, timeout=TIMEOUT)
time.sleep(2)

tn.read_very_eager()

# Step 1: Send name at "Your Selection?"
tn.write(f"{CHAR_NAME}\n".encode())
text = read_until_prompt(tn, 2)
write_out("NAME ENTRY 1", text)

# Step 2: Send 'c' at next "Your Selection?"
tn.write(b'c\n')
text = read_until_prompt(tn, 2)
write_out("CREATE", text)

# Step 3: Send name AGAIN at "New character name:"
tn.write(f"{CHAR_NAME}\n".encode())
text = read_until_prompt(tn, 2)
write_out("NAME ENTRY 2", text)

# Step 4: Password
tn.write(f"{CHAR_PASS}\n".encode())
text = read_until_prompt(tn, 2)
write_out("PASSWORD 1", text)

tn.write(f"{CHAR_PASS}\n".encode())
text = read_until_prompt(tn, 2)
write_out("PASSWORD 2", text)

# Step 5: Gender
tn.write(b'm\n')
text = read_until_prompt(tn, 2)
write_out("GENDER", text)

# Step 6: Email (blank)
tn.write(b'\n')
text = read_until_prompt(tn, 2)
write_out("EMAIL", text)

# Step 7: Referral (blank)
tn.write(b'\n')
text = read_until_prompt(tn, 2)
write_out("REFERRAL", text)

# Step 8: Skip tutorial
tn.write(b'yes\n')
text = read_until_prompt(tn, 3)
write_out("SKIP TUTORIAL", text)

# Step 9: Race select
tn.write(b'race-select\n')
text = read_all(tn, 2, max_chunks=30)
write_out("RACE SELECT", text)

tn.write(b'touch human\n')
text = read_all(tn, 2, max_chunks=30)
write_out("TOUCH HUMAN", text)

tn.write(b'enter portal\n')
text = read_all(tn, 2, max_chunks=30)
write_out("ENTER PORTAL", text)

print("[*] In the world!", file=sys.stderr)

# Navigate to guild entrance
tn.write(b'look\n')
text = read_all(tn, 1, max_chunks=30)
write_out("LOCATION", text)

if "Adventurer" in text or "Guild" in text:
    print("[*] At guild entrance.", file=sys.stderr)
else:
    print("[*] Not at guild, navigating...", file=sys.stderr)
    tn.write(b'north\n')
    text = read_all(tn, 1, max_chunks=30)
    if "Titan" in text:
        tn.write(b'west\n')
        text = read_all(tn, 1, max_chunks=30)
        tn.write(b'south\n')
        text = read_all(tn, 1, max_chunks=30)
        write_out("TO GUILD", text)

# Portal Room
tn.write(b'southwest\n')
text = read_all(tn, 1, max_chunks=30)
write_out("PORTAL ROOM", text)

# Enter target guild
tn.write(f"{GUILD_NAME}\n".encode())
text = read_all(tn, 1, max_chunks=30)
write_out(f"{GUILD_NAME.upper()} GUILD", text)

# Look around
tn.write(b'look\n')
text = read_all(tn, 1, max_chunks=30)
write_out(f"LOOK {GUILD_NAME.upper()}", text)

tn.write(b'exits\n')
text = read_all(tn, 1, max_chunks=30)
write_out(f"EXITS {GUILD_NAME.upper()}", text)

# Get guild info — 30 chunks and q flush
tn.write(b'info\n')
text = read_all(tn, 2, max_chunks=30)
write_out(f"INFO {GUILD_NAME.upper()}", text)

# Force quit pager
tn.write(b'q')
time.sleep(0.3)
tn.write(b'\n')
text = read_all(tn, 1, max_chunks=10)
write_out("PAGER QUIT", text)

# Do out to see outdoor area
tn.write(b'out\n')
text = read_all(tn, 1, max_chunks=30)
write_out("AFTER OUT", text)

tn.write(b'look\n')
text = read_all(tn, 1, max_chunks=30)
write_out("OUT LOOK", text)

tn.write(b'exits\n')
text = read_all(tn, 1, max_chunks=30)
write_out("OUT EXITS", text)

# Quit
tn.write(b'quit\n')
text = read_all(tn, 2, max_chunks=30)
write_out("QUIT", text)

tn.close()
print(f"[*] Done. Saved to {OUTPUT_FILE}", file=sys.stderr)
