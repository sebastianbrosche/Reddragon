#!/usr/bin/env python3
"""
Islands of Myth - World Explorer v1
Continues archival work: explore rooms, guilds, commands, world.
"""

import telnetlib
import time
import sys

HOST = "islandsofmyth.org"
PORT = 3000
TIMEOUT = 15

CHAR_NAME = b'chronicler\n'
CHAR_PASS = b'mudarchivist2026\n'

OUTPUT_FILE = "/root/.openclaw/workspace/mud/iom_world_explore.txt"

with open(OUTPUT_FILE, 'w') as f:
    f.write("# Islands of Myth — World Exploration\n# " + time.strftime("%Y-%m-%d %H:%M:%S") + "\n\n")

def write_out(label, text):
    block = f"\n{'='*70}\n=== {label} ===\n{'='*70}\n{text}\n"
    print(block, file=sys.stderr)
    with open(OUTPUT_FILE, 'a') as f:
        f.write(block)

# Connect
print(f"[*] Connecting...", file=sys.stderr)
tn = telnetlib.Telnet(HOST, PORT, timeout=TIMEOUT)
time.sleep(2)

tn.read_very_eager()
tn.write(CHAR_NAME)
time.sleep(1.5)
tn.read_very_eager()
tn.write(CHAR_PASS)
time.sleep(2)

text = tn.read_very_eager().decode('ascii', errors='replace')
write_out("LOGIN", text)

# Helper: page through any pager and collect all output
def page_through(tn, wait=1.5):
    time.sleep(wait)
    all_text = ""
    for _ in range(20):
        try:
            chunk = tn.read_very_eager().decode('ascii', errors='replace')
        except:
            break
        all_text += chunk
        if "(h):" in chunk or "--More--" in chunk:
            tn.write(b' ')
            time.sleep(0.4)
        elif "hp(" in chunk and "sp(" in chunk and "ep(" in chunk and ">" in chunk:
            break
        else:
            time.sleep(0.5)
    return all_text

# ---- EXPLORATION COMMANDS ----

commands_to_try = [
    ("WHO", b'who\n'),
    ("SCORE", b'score\n'),
    ("STATS", b'stats\n'),
    ("INVENTORY", b'inventory\n'),
    ("EQUIPMENT", b'equipment\n'),
    ("LOOK", b'look\n'),
    ("EXITS", b'exits\n'),
    ("TOUR", b'tour\n'),
    ("HELP", b'help\n'),
    ("FAQ", b'faq\n'),
]

for label, cmd in commands_to_try:
    print(f"[*] Running: {label}", file=sys.stderr)
    tn.write(cmd)
    text = page_through(tn)
    write_out(label, text)
    time.sleep(0.5)

# Look at all guilds (from poster)
# First go to where guilds can be looked at
# Try the 'guild' command or look for guild hall
print("[*] Trying guild commands...", file=sys.stderr)

guild_cmds = [
    ("GUILD CMD", b'guild\n'),
    ("GUILDS LIST", b'guilds\n'),
    ("GUILD INFO", b'guild info\n'),
]

for label, cmd in guild_cmds:
    tn.write(cmd)
    text = page_through(tn)
    write_out(label, text)
    time.sleep(0.5)

# Try to look at all exits and rooms
tn.write(b'look\n')
text = page_through(tn)
write_out("LOOK ROOM", text)

# Try north
tn.write(b'north\n')
text = page_through(tn)
write_out("GO NORTH", text)

# Look at new room
tn.write(b'look\n')
text = page_through(tn)
write_out("LOOK NORTH ROOM", text)

# Try south back
tn.write(b'south\n')
text = page_through(tn)
write_out("GO SOUTH", text)

# Try tour
tn.write(b'tour\n')
text = page_through(tn)
write_out("TOUR ROOM", text)

# Look at tour room
tn.write(b'look\n')
text = page_through(tn)
write_out("LOOK TOUR ROOM", text)

# Try commands from the room
tn.write(b'news\n')
text = page_through(tn)
write_out("NEWS", text)

tn.write(b'rules\n')
text = page_through(tn)
write_out("RULES", text)

tn.write(b'help\n')
text = page_through(tn)
write_out("HELP FULL", text)

# Channel list
tn.write(b'channels\n')
text = page_through(tn)
write_out("CHANNELS", text)

# Time
tn.write(b'time\n')
text = page_through(tn)
write_out("TIME", text)

# Weather
tn.write(b'weather\n')
text = page_through(tn)
write_out("WEATHER", text)

# Map
tn.write(b'map\n')
text = page_through(tn)
write_out("MAP", text)

# Areas
tn.write(b'areas\n')
text = page_through(tn)
write_out("AREAS", text)

# World
tn.write(b'world\n')
text = page_through(tn)
write_out("WORLD", text)

# Quests
tn.write(b'quests\n')
text = page_through(tn)
write_out("QUESTS", text)

# Top players
tn.write(b'top\n')
text = page_through(tn)
write_out("TOP", text)

# Title
tn.write(b'title\n')
text = page_through(tn)
write_out("TITLE", text)

# Describe
tn.write(b'describe\n')
text = page_through(tn)
write_out("DESCRIBE", text)

# History
tn.write(b'history\n')
text = page_through(tn)
write_out("HISTORY", text)

# Kill count
tn.write(b'kills\n')
text = page_through(tn)
write_out("KILLS", text)

# Deaths
tn.write(b'deaths\n')
text = page_through(tn)
write_out("DEATHS", text)

# Levels
tn.write(b'levels\n')
text = page_through(tn)
write_out("LEVELS", text)

# Experience
tn.write(b'experience\n')
text = page_through(tn)
write_out("EXPERIENCE", text)

# Quit
tn.write(b'quit\n')
text = page_through(tn)
write_out("QUIT", text)

tn.close()
print(f"[*] Done. Saved to {OUTPUT_FILE}", file=sys.stderr)
