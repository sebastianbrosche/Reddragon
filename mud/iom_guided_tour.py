#!/usr/bin/env python3
"""
Islands of Myth - Guided Tour Archivist
Goes through the entire new player tutorial step by step.
Captures every screen of the guided tour + character creation flow.
"""

import telnetlib
import time
import sys

HOST = "islandsofmyth.org"
PORT = 3000
TIMEOUT = 15

CHAR_NAME = b'chronicler\n'
CHAR_PASS = b'mudarchivist2026\n'

OUTPUT_FILE = "/root/.openclaw/workspace/mud/iom_guided_tour.txt"

with open(OUTPUT_FILE, 'w') as f:
    f.write("# Islands of Myth — Complete Guided Tour Archive\n# " + time.strftime("%Y-%m-%d %H:%M:%S") + "\n\n")

def write_out(label, text):
    block = f"\n{'='*70}\n=== {label} ===\n{'='*70}\n{text}\n"
    print(block, file=sys.stderr)
    with open(OUTPUT_FILE, 'a') as f:
        f.write(block)

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
        else:
            time.sleep(0.5)
            try:
                chunk2 = tn.read_very_eager().decode('ascii', errors='replace')
                all_text += chunk2
            except:
                break
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

text = tn.read_very_eager().decode('ascii', errors='replace')
write_out("LOGIN", text)

# Step through the guided tour
step = 0
while step < 50:
    # Read current state
    time.sleep(1)
    text = tn.read_very_eager().decode('ascii', errors='replace')
    
    if text.strip():
        write_out(f"TOUR STEP {step}", text)
    
    # Check if we're at a choice prompt
    if "Please select either 'continue', 'out', or 'back'" in text:
        # For now, just capture the state and exit — we want to explore the world
        print(f"[*] Step {step}: At choice prompt", file=sys.stderr)
        # Send 'continue' to go through the tour
        tn.write(b'continue\n')
    elif "type 'continue' now" in text.lower() or "type 'out' now" in text.lower():
        print(f"[*] Step {step}: At continue/out prompt", file=sys.stderr)
        tn.write(b'continue\n')
    elif "hp(" in text and "sp(" in text and "ep(" in text and ">" in text:
        # We're in the real game world now
        print(f"[*] Step {step}: In real world!", file=sys.stderr)
        write_out(f"REAL WORLD STEP {step}", text)
        break
    elif "[123456789101112q]" in text:
        # FAQ menu
        print(f"[*] Step {step}: FAQ menu", file=sys.stderr)
        tn.write(b'q\n')  # quit FAQ
    else:
        # No recognizable prompt, send continue
        print(f"[*] Step {step}: Unknown state, sending continue", file=sys.stderr)
        tn.write(b'continue\n')
    
    step += 1
    time.sleep(1)

# If we broke out into the real world, explore
text = page_through(tn)
if text.strip():
    write_out("POST-TOUR", text)

# Look around
tn.write(b'look\n')
text = page_through(tn)
write_out("LOOK", text)

tn.write(b'exits\n')
text = page_through(tn)
write_out("EXITS", text)

tn.write(b'who\n')
text = page_through(tn)
write_out("WHO", text)

tn.write(b'score\n')
text = page_through(tn)
write_out("SCORE", text)

# Try to move
tn.write(b'north\n')
text = page_through(tn)
write_out("NORTH", text)

tn.write(b'look\n')
text = page_through(tn)
write_out("LOOK NORTH", text)

tn.write(b'south\n')
text = page_through(tn)
write_out("SOUTH", text)

tn.write(b'look\n')
text = page_through(tn)
write_out("LOOK SOUTH", text)

# Final
tn.write(b'quit\n')
text = page_through(tn)
write_out("QUIT", text)

tn.close()
print(f"[*] Done. Saved to {OUTPUT_FILE}", file=sys.stderr)
