#!/usr/bin/env python3
"""
Islands of Myth - Handbook + Help Guilds Capture
Carefully walks through pagers and quits menus.
"""

import telnetlib
import time
import sys

HOST = "islandsofmyth.org"
PORT = 3000
TIMEOUT = 15

CHAR_NAME = b'explorer\n'
CHAR_PASS = b'testpass123\n'

OUTPUT_FILE = "/root/.openclaw/workspace/mud/iom_handbook_help.txt"

with open(OUTPUT_FILE, 'w') as f:
    f.write("# Islands of Myth — Handbook + Help Guilds Capture\n# " + time.strftime("%Y-%m-%d %H:%M:%S") + "\n\n")

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

def read_through_pager(tn, wait=1.5):
    """Read all text through a pager, sending space to continue."""
    time.sleep(wait)
    all_text = ""
    for _ in range(30):
        try:
            chunk = tn.read_very_eager().decode('ascii', errors='replace')
        except:
            break
        all_text += chunk
        if "--More--" in chunk or "(h):" in chunk:
            tn.write(b' ')
            time.sleep(0.3)
        elif chunk:
            time.sleep(0.2)
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

# Read handbook topics list
tn.write(b'read handbook\n')
text = read_through_pager(tn, 1)
write_out("HANDBOOK TOPICS", text)

# Try reading a few handbook topics
handbook_topics = ["getting started", "commands", "combat", "guilds", "equipment", "levels", "races", "movement"]
for topic in handbook_topics:
    print(f"[*] Reading handbook topic: {topic}", file=sys.stderr)
    tn.write(f"read about {topic}\n".encode())
    text = read_through_pager(tn, 1)
    write_out(f"HANDBOOK: {topic.upper()}", text)
    time.sleep(0.3)
    # Make sure we're back at prompt
    tn.read_very_eager()

# Now get help guilds with full pager walkthrough
print("[*] Getting help guilds...", file=sys.stderr)
tn.write(b'help guilds\n')
text = read_through_pager(tn, 1)
write_out("HELP GUILDS", text)

# Quit from any menu
tn.write(b'q\n')
time.sleep(0.5)
tn.read_very_eager()

# Try some other help topics individually with q after each
helps = ["faq", "commands", "combat", "levels", "alignment", "races"]
for h in helps:
    print(f"[*] Help: {h}", file=sys.stderr)
    tn.write(f"help {h}\n".encode())
    text = read_through_pager(tn, 1)
    write_out(f"HELP: {h.upper()}", text)
    tn.write(b'q\n')
    time.sleep(0.5)
    tn.read_very_eager()
    time.sleep(0.3)

# Look at some things in the guild entrance
tn.write(b'look at formula\n')
text = read_all(tn, 1)
write_out("LOOK FORMULA", text)

tn.write(b'look at newbie handbook\n')
text = read_all(tn, 1)
write_out("LOOK NEWBIE HANDBOOK", text)

# Try to read about portals in the Portal Room
# Go southwest to portal room
tn.write(b'southwest\n')
text = read_all(tn, 1)
write_out("GO PORTAL ROOM", text)

tn.write(b'look\n')
text = read_all(tn, 1)
write_out("LOOK PORTAL ROOM", text)

# Look at a specific portal
tn.write(b'look at warrior\n')
text = read_all(tn, 1)
write_out("LOOK WARRIOR PORTAL", text)

tn.write(b'look at elemental\n')
text = read_all(tn, 1)
write_out("LOOK ELEMENTAL PORTAL", text)

# Go back
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
