#!/usr/bin/env python3
"""
Islands of Myth - Guided Tour Follower
Actually follows the tutorial prompts properly.
Captures the full new player experience.
"""

import telnetlib
import time
import sys

HOST = "islandsofmyth.org"
PORT = 3000
TIMEOUT = 15

CHAR_NAME = b'chronicler\n'
CHAR_PASS = b'mudarchivist2026\n'

OUTPUT_FILE = "/root/.openclaw/workspace/mud/iom_tour_complete.txt"

with open(OUTPUT_FILE, 'w') as f:
    f.write("# Islands of Myth — Complete Guided Tour + World Entry\n# " + time.strftime("%Y-%m-%d %H:%M:%S") + "\n\n")

def write_out(label, text):
    block = f"\n{'='*70}\n=== {label} ===\n{'='*70}\n{text}\n"
    print(block, file=sys.stderr)
    with open(OUTPUT_FILE, 'a') as f:
        f.write(block)

def read_all(tn, wait=1.5):
    time.sleep(wait)
    all_text = ""
    for _ in range(15):
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
            time.sleep(0.3)
    return all_text

print(f"[*] Connecting...", file=sys.stderr)
tn = telnetlib.Telnet(HOST, PORT, timeout=TIMEOUT)
time.sleep(2)

tn.read_very_eager()
tn.write(CHAR_NAME)
time.sleep(1.5)
tn.read_very_eager()
tn.write(CHAR_PASS)
time.sleep(2)

text = read_all(tn)
write_out("LOGIN", text)

# Wait for the "continue/out" prompt, then type 'continue'
for _ in range(20):
    text = read_all(tn, 1)
    if text.strip():
        write_out("PRE-TOUR", text)
    if "type 'continue' now" in text.lower() or "type 'out' now" in text.lower():
        print("[*] Found continue/out prompt, sending 'continue'", file=sys.stderr)
        tn.write(b'continue\n')
        break
    time.sleep(0.5)

# Now follow the tour - it asks for specific commands
# The tour teaches: look, exits, inventory, equipment, score, who, etc.

# Collect all tour screens
tour_step = 0
while tour_step < 100:
    text = read_all(tn, 1.5)
    if text.strip():
        write_out(f"TOUR STEP {tour_step}", text)
    
    # Check what the tour is asking for
    lower_text = text.lower()
    
    if "please type 'look'" in lower_text:
        print(f"[*] Step {tour_step}: Sending 'look'", file=sys.stderr)
        tn.write(b'look\n')
    elif "please type 'exits'" in lower_text:
        print(f"[*] Step {tour_step}: Sending 'exits'", file=sys.stderr)
        tn.write(b'exits\n')
    elif "type 'inventory'" in lower_text or "type 'i'" in lower_text:
        print(f"[*] Step {tour_step}: Sending 'inventory'", file=sys.stderr)
        tn.write(b'inventory\n')
    elif "type 'equipment'" in lower_text or "type 'eq'" in lower_text:
        print(f"[*] Step {tour_step}: Sending 'equipment'", file=sys.stderr)
        tn.write(b'equipment\n')
    elif "type 'score'" in lower_text:
        print(f"[*] Step {tour_step}: Sending 'score'", file=sys.stderr)
        tn.write(b'score\n')
    elif "type 'who'" in lower_text:
        print(f"[*] Step {tour_step}: Sending 'who'", file=sys.stderr)
        tn.write(b'who\n')
    elif "type 'ansi on'" in lower_text or "turn color on" in lower_text:
        print(f"[*] Step {tour_step}: Sending 'ansi on'", file=sys.stderr)
        tn.write(b'ansi on\n')
    elif "type 'ansi off'" in lower_text:
        print(f"[*] Step {tour_step}: Sending 'ansi off'", file=sys.stderr)
        tn.write(b'ansi off\n')
    elif "type 'north'" in lower_text or "go north" in lower_text:
        print(f"[*] Step {tour_step}: Sending 'north'", file=sys.stderr)
        tn.write(b'north\n')
    elif "type 'south'" in lower_text or "go south" in lower_text:
        print(f"[*] Step {tour_step}: Sending 'south'", file=sys.stderr)
        tn.write(b'south\n')
    elif "type 'back'" in lower_text:
        print(f"[*] Step {tour_step}: Sending 'back'", file=sys.stderr)
        tn.write(b'back\n')
    elif "type 'say'" in lower_text:
        print(f"[*] Step {tour_step}: Sending 'say hello'", file=sys.stderr)
        tn.write(b'say hello\n')
    elif "type 'tell'" in lower_text:
        print(f"[*] Step {tour_step}: Sending 'tell'", file=sys.stderr)
        tn.write(b'tell someone hello\n')
    elif "type 'continue'" in lower_text or "type 'out'" in lower_text:
        print(f"[*] Step {tour_step}: At continue/out, sending 'continue'", file=sys.stderr)
        tn.write(b'continue\n')
    elif "type 'faq'" in lower_text:
        print(f"[*] Step {tour_step}: Sending 'faq'", file=sys.stderr)
        tn.write(b'faq\n')
    elif "type 'help'" in lower_text:
        print(f"[*] Step {tour_step}: Sending 'help'", file=sys.stderr)
        tn.write(b'help\n')
    elif "type 'random'" in lower_text:
        print(f"[*] Step {tour_step}: Sending 'random'", file=sys.stderr)
        tn.write(b'random\n')
    elif "hp(" in text and "sp(" in text and "ep(" in text and ">" in text and "guide" not in lower_text and "tour" not in lower_text:
        # We might be in the real world now
        print(f"[*] Step {tour_step}: Possible real world prompt detected", file=sys.stderr)
        write_out("POSSIBLE REAL WORLD", text)
        break
    else:
        # Default: just hit enter or send 'continue'
        if text.strip():
            print(f"[*] Step {tour_step}: Unknown prompt, sending enter", file=sys.stderr)
            tn.write(b'\n')
    
    tour_step += 1
    time.sleep(0.5)

# If we're in the real world, explore
text = read_all(tn)
if text.strip():
    write_out("REAL WORLD ENTRY", text)

# Do some basic exploration
tn.write(b'look\n')
text = read_all(tn)
write_out("LOOK", text)

tn.write(b'exits\n')
text = read_all(tn)
write_out("EXITS", text)

tn.write(b'who\n')
text = read_all(tn)
write_out("WHO", text)

tn.write(b'score\n')
text = read_all(tn)
write_out("SCORE", text)

tn.write(b'stats\n')
text = read_all(tn)
write_out("STATS", text)

tn.write(b'i\n')
text = read_all(tn)
write_out("INVENTORY", text)

tn.write(b'eq\n')
text = read_all(tn)
write_out("EQUIPMENT", text)

# Try movement
dirs = ["north", "south", "east", "west", "up", "down"]
for d in dirs:
    tn.write(f"{d}\n".encode())
    text = read_all(tn)
    write_out(f"GO {d.upper()}", text)
    tn.write(b'look\n')
    text = read_all(tn)
    write_out(f"LOOK {d.upper()}", text)
    time.sleep(0.3)

# Try various commands
cmds = [
    ("SKILLS", b'skills\n'),
    ("SPELLS", b'spells\n'),
    ("HELP", b'help\n'),
    ("TIME", b'time\n'),
    ("WEATHER", b'weather\n'),
    ("MONEY", b'money\n'),
    ("CONDITION", b'condition\n'),
    ("ALIGNMENT", b'alignment\n'),
    ("HUNGER", b'hunger\n'),
    ("WIMPY", b'wimpy\n'),
    ("GHOST", b'ghost\n'),
    ("WHERE", b'where\n'),
    ("LEVELS", b'levels\n'),
    ("EXPERIENCE", b'experience\n'),
    ("COMBAT", b'combat\n'),
    ("TITLE", b'title\n'),
    ("DESCRIBE", b'describe\n'),
    ("HISTORY", b'history\n'),
    ("KILLS", b'kills\n'),
    ("DEATHS", b'deaths\n'),
    ("TOP", b'top\n'),
    ("CHANNELS", b'channels\n'),
    ("NEWS", b'news\n'),
    ("RULES", b'rules\n'),
    ("GUILD", b'guild\n'),
    ("GUILDS", b'guilds\n'),
    ("SHOPS", b'shops\n'),
    ("TRAINERS", b'trainers\n'),
    ("MAP", b'map\n'),
    ("AREAS", b'areas\n'),
    ("WORLD", b'world\n'),
    ("MAPPER", b'mapper\n'),
    ("LOOK SELF", b'look self\n'),
    ("LOOK GROUND", b'look ground\n'),
]

for label, cmd in cmds:
    print(f"[*] Running: {label}", file=sys.stderr)
    tn.write(cmd)
    text = read_all(tn)
    write_out(label, text)
    time.sleep(0.3)

# Final
tn.write(b'quit\n')
text = read_all(tn)
write_out("QUIT", text)

tn.close()
print(f"[*] Done. Saved to {OUTPUT_FILE}", file=sys.stderr)
