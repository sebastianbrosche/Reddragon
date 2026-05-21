#!/usr/bin/env python3
"""
Islands of Myth - Tutorial Walker v4
Added finger command and other tutorial commands.
"""

import telnetlib
import time
import sys

HOST = "islandsofmyth.org"
PORT = 3000
TIMEOUT = 15

CHAR_NAME = b'chronicler\n'
CHAR_PASS = b'mudarchivist2026\n'

OUTPUT_FILE = "/root/.openclaw/workspace/mud/iom_tutorial_walk4.txt"

with open(OUTPUT_FILE, 'w') as f:
    f.write("# Islands of Myth — Tutorial Walk-Through v4\n# " + time.strftime("%Y-%m-%d %H:%M:%S") + "\n\n")

def write_out(label, text):
    block = f"\n{'='*70}\n=== {label} ===\n{'='*70}\n{text}\n"
    print(block, file=sys.stderr)
    with open(OUTPUT_FILE, 'a') as f:
        f.write(block)

def read_chunk(tn, wait=1.0):
    time.sleep(wait)
    try:
        return tn.read_very_eager().decode('ascii', errors='replace')
    except:
        return ""

print(f"[*] Connecting...", file=sys.stderr)
tn = telnetlib.Telnet(HOST, PORT, timeout=TIMEOUT)
time.sleep(2)

tn.read_very_eager()
tn.write(CHAR_NAME)
time.sleep(1.5)
tn.read_very_eager()
tn.write(CHAR_PASS)
time.sleep(2)

# Collect login text
text = ""
for _ in range(5):
    text += read_chunk(tn, 0.5)
write_out("LOGIN", text)

step = 0
while step < 200:
    # Read current state
    text = ""
    for _ in range(5):
        text += read_chunk(tn, 0.4)
    
    if text.strip():
        write_out(f"STEP {step}", text)
    
    lower = text.lower()
    
    # Check for specific tutorial prompts and respond
    # ORDER MATTERS - more specific matches first
    if "type 'finger'" in lower or "finger a player" in lower or "finger <player" in lower:
        print(f"[*] Step {step}: finger wildchild", file=sys.stderr)
        tn.write(b'finger wildchild\n')
    elif "type 'look at sign'" in lower or "look at sign" in lower:
        print(f"[*] Step {step}: look at sign", file=sys.stderr)
        tn.write(b'look at sign\n')
    elif "type 'look at'" in lower:
        obj = "sign"
        if "look at poster" in lower:
            obj = "poster"
        elif "look at board" in lower:
            obj = "board"
        print(f"[*] Step {step}: look at {obj}", file=sys.stderr)
        tn.write(f'look at {obj}\n'.encode())
    elif "type 'look' now" in lower:
        print(f"[*] Step {step}: look", file=sys.stderr)
        tn.write(b'look\n')
    elif "type 'exits' now" in lower:
        print(f"[*] Step {step}: exits", file=sys.stderr)
        tn.write(b'exits\n')
    elif "type 'inventory' now" in lower or "type 'i' now" in lower:
        print(f"[*] Step {step}: inventory", file=sys.stderr)
        tn.write(b'inventory\n')
    elif "type 'equipment' now" in lower or "type 'eq' now" in lower:
        print(f"[*] Step {step}: equipment", file=sys.stderr)
        tn.write(b'equipment\n')
    elif "type 'score' now" in lower:
        print(f"[*] Step {step}: score", file=sys.stderr)
        tn.write(b'score\n')
    elif "type 'who' now" in lower:
        print(f"[*] Step {step}: who", file=sys.stderr)
        tn.write(b'who\n')
    elif "type 'ansi on'" in lower and "ansi on" in lower:
        print(f"[*] Step {step}: ansi on", file=sys.stderr)
        tn.write(b'ansi on\n')
    elif "type 'ansi off'" in lower:
        print(f"[*] Step {step}: ansi off", file=sys.stderr)
        tn.write(b'ansi off\n')
    elif "type 'north' now" in lower or "go north" in lower:
        print(f"[*] Step {step}: north", file=sys.stderr)
        tn.write(b'north\n')
    elif "type 'south' now" in lower:
        print(f"[*] Step {step}: south", file=sys.stderr)
        tn.write(b'south\n')
    elif "type 'east' now" in lower:
        print(f"[*] Step {step}: east", file=sys.stderr)
        tn.write(b'east\n')
    elif "type 'west' now" in lower:
        print(f"[*] Step {step}: west", file=sys.stderr)
        tn.write(b'west\n')
    elif "type 'back' now" in lower:
        print(f"[*] Step {step}: back", file=sys.stderr)
        tn.write(b'back\n')
    elif "type 'say'" in lower:
        print(f"[*] Step {step}: say hello", file=sys.stderr)
        tn.write(b'say hello\n')
    elif "type 'tell'" in lower:
        print(f"[*] Step {step}: tell", file=sys.stderr)
        tn.write(b'tell someone hello\n')
    elif "type 'continue' now" in lower:
        print(f"[*] Step {step}: continue", file=sys.stderr)
        tn.write(b'continue\n')
    elif "type 'out' now" in lower:
        print(f"[*] Step {step}: out", file=sys.stderr)
        tn.write(b'out\n')
    elif "type 'faq'" in lower:
        print(f"[*] Step {step}: faq", file=sys.stderr)
        tn.write(b'faq\n')
    elif "type 'help'" in lower:
        print(f"[*] Step {step}: help", file=sys.stderr)
        tn.write(b'help\n')
    elif "type 'random'" in lower:
        print(f"[*] Step {step}: random", file=sys.stderr)
        tn.write(b'random\n')
    elif "[123456789101112q]" in text:
        print(f"[*] Step {step}: FAQ menu, sending q", file=sys.stderr)
        tn.write(b'q\n')
    elif "please select either 'continue', 'out', or 'back'" in lower:
        print(f"[*] Step {step}: choice prompt, sending continue", file=sys.stderr)
        tn.write(b'continue\n')
    elif "hp(" in text and "sp(" in text and "ep(" in text and ">" in text:
        if "guide" not in lower and "tour" not in lower and "void of white" not in lower:
            print(f"[*] Step {step}: Real world detected!", file=sys.stderr)
            write_out("REAL WORLD", text)
            break
        else:
            print(f"[*] Step {step}: Tutorial prompt, sending enter", file=sys.stderr)
            tn.write(b'\n')
    else:
        if text.strip():
            print(f"[*] Step {step}: No specific prompt, sending enter", file=sys.stderr)
            tn.write(b'\n')
    
    step += 1
    time.sleep(0.5)

# If we broke into real world, do some exploration
text = ""
for _ in range(5):
    text += read_chunk(tn, 0.5)
if text.strip():
    write_out("POST-BREAK", text)

# Basic world commands
cmds = [
    b'look\n', b'exits\n', b'who\n', b'score\n', b'stats\n',
    b'i\n', b'eq\n', b'north\n', b'look\n', b'south\n', b'look\n',
    b'east\n', b'look\n', b'west\n', b'look\n',
    b'skills\n', b'spells\n', b'help\n', b'time\n', b'weather\n',
    b'money\n', b'condition\n', b'alignment\n', b'hunger\n',
    b'wimpy\n', b'ghost\n', b'where\n', b'levels\n',
    b'experience\n', b'combat\n', b'title\n', b'describe\n',
    b'history\n', b'kills\n', b'deaths\n', b'top\n',
    b'channels\n', b'news\n', b'rules\n',
    b'guild\n', b'guilds\n', b'guild info\n',
    b'shops\n', b'trainers\n', b'map\n', b'areas\n',
    b'world\n', b'mapper\n', b'look self\n', b'look ground\n',
]

for i, cmd in enumerate(cmds):
    label = cmd.decode().strip().upper()
    print(f"[*] Running: {label}", file=sys.stderr)
    tn.write(cmd)
    text = ""
    for _ in range(5):
        text += read_chunk(tn, 0.5)
    write_out(label, text)
    time.sleep(0.3)

# Quit
tn.write(b'quit\n')
text = ""
for _ in range(5):
    text += read_chunk(tn, 0.5)
write_out("QUIT", text)

tn.close()
print(f"[*] Done. Saved to {OUTPUT_FILE}", file=sys.stderr)
