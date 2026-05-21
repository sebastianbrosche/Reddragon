#!/usr/bin/env python3
"""
Islands of Myth - Multi-Guild Visit (Elemental, Psychics, Weaver)
Properly handles pager with 'q' after info. Returns via 'out'.
"""

import telnetlib
import time
import sys

HOST = "islandsofmyth.org"
PORT = 3000
TIMEOUT = 15

CHAR_NAME = b'explorer\n'
CHAR_PASS = b'testpass123\n'

OUTPUT_FILE = "/root/.openclaw/workspace/mud/iom_multi_guild.txt"

with open(OUTPUT_FILE, 'w') as f:
    f.write("# Islands of Myth — Elemental, Psychics, Weaver Guilds\n# " + time.strftime("%Y-%m-%d %H:%M:%S") + "\n\n")

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

def navigate_to_guild(tn):
    """Navigate from wherever we are to Adventurer Guild Entrance."""
    # First, figure out where we are
    tn.write(b'look\n')
    text = read_all(tn, 1)
    write_out("LOCATION CHECK", text)
    
    if "Adventurer Guild Entrance" in text:
        return text
    
    # Try to find a known path
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
    elif "Intersection of Cloud and Titan" in text:
        tn.write(b'west\n')
        text = read_all(tn, 1)
        write_out("WEST", text)
        tn.write(b'south\n')
        text = read_all(tn, 1)
        write_out("SOUTH TO GUILD", text)
    elif "On Cloud Road between Gossamer and Titan" in text:
        tn.write(b'south\n')
        text = read_all(tn, 1)
        write_out("SOUTH TO GUILD", text)
    else:
        # Unknown location, try to find something familiar
        for i in range(5):
            tn.write(b'look\n')
            text = read_all(tn, 1)
            write_out(f"LOOK {i}", text)
            if "Titan" in text or "Guild" in text or "Cloud Road" in text:
                break
            tn.write(b'south\n')
            text = read_all(tn, 1)
            write_out(f"SOUTH {i}", text)
        
        if "Titan" in text:
            tn.write(b'north\n')
            text = read_all(tn, 1)
            tn.write(b'west\n')
            text = read_all(tn, 1)
            tn.write(b'south\n')
            text = read_all(tn, 1)
            write_out("SOUTH TO GUILD", text)
    
    tn.write(b'look\n')
    text = read_all(tn, 1)
    write_out("VERIFY GUILD", text)
    return text

def visit_guild(tn, guild_name):
    """Visit a guild hall, capture data, and return."""
    print(f"[*] Visiting {guild_name} guild...", file=sys.stderr)
    
    # Go to Portal Room
    tn.write(b'southwest\n')
    text = read_all(tn, 1)
    write_out(f"PORTAL ROOM ({guild_name})", text)
    
    # Enter guild
    tn.write(f"{guild_name}\n".encode())
    text = read_all(tn, 1)
    write_out(f"{guild_name.upper()} GUILD", text)
    
    # Look around
    tn.write(b'look\n')
    text = read_all(tn, 1)
    write_out(f"LOOK {guild_name.upper()}", text)
    
    tn.write(b'exits\n')
    text = read_all(tn, 1)
    write_out(f"EXITS {guild_name.upper()}", text)
    
    # Get guild info
    tn.write(b'info\n')
    text = read_all(tn, 1)
    write_out(f"INFO {guild_name.upper()}", text)
    
    # Exit pager if active
    if "(h):" in text or "--More--" in text:
        tn.write(b'q')
        time.sleep(0.5)
        tn.write(b'\n')
        text = read_all(tn, 1)
        write_out(f"PAGER QUIT {guild_name.upper()}", text)
    
    # Leave guild
    tn.write(b'out\n')
    text = read_all(tn, 1)
    write_out(f"OUT {guild_name.upper()}", text)
    
    # If not at Portal Room, try to get back
    if "Portal Room" not in text:
        # Try northeast to get back to guild entrance
        tn.write(b'northeast\n')
        text = read_all(tn, 1)
        write_out(f"NE RETURN {guild_name.upper()}", text)
        
        if "Adventurer Guild Entrance" not in text and "Portal Room" not in text:
            # We're lost, navigate back from scratch
            navigate_to_guild(tn)
    else:
        # At Portal Room, go back to guild entrance
        tn.write(b'northeast\n')
        text = read_all(tn, 1)
        write_out(f"BACK TO GUILD ({guild_name})", text)

# Main
print(f"[*] Connecting...", file=sys.stderr)
tn = telnetlib.Telnet(HOST, PORT, timeout=TIMEOUT)
time.sleep(2)

tn.read_very_eager()

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

# Navigate to guild
navigate_to_guild(tn)

# Visit guilds
guilds = ["elemental", "psychics", "weaver"]
for guild in guilds:
    visit_guild(tn, guild)
    time.sleep(1)

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
