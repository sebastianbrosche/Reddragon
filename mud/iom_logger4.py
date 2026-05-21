#!/usr/bin/env python3
"""
Islands of Myth - Character Creation Archivist
Captures every screen during character creation.
"""

import telnetlib
import time
import sys

HOST = "islandsofmyth.org"
PORT = 3000
TIMEOUT = 15

def log_section(label, data):
    ts = time.strftime("%H:%M:%S")
    header = f"\n{'='*70}\n[{ts}] === {label} ===\n{'='*70}"
    text = data.decode('ascii', errors='replace')
    print(header, file=sys.stderr)
    print(text, file=sys.stderr)
    print("="*70, file=sys.stderr)
    return text

def read_wait(tn, wait=2):
    time.sleep(wait)
    try:
        return tn.read_very_eager()
    except:
        return b''

# --- MAIN ---
print(f"[*] Connecting to {HOST}:{PORT}...", file=sys.stderr)
tn = telnetlib.Telnet(HOST, PORT, timeout=TIMEOUT)

# Capture login banner
time.sleep(2)
login_data = tn.read_very_eager()
text = log_section("LOGIN MENU", login_data)

# Step 1: Press 'c' to create
tn.write(b'c\n')
time.sleep(0.5)
data = read_wait(tn, 2)
text = log_section("AFTER 'c' - NAME PROMPT", data)

# Step 2: Name - lowercase
tn.write(b'archivist\n')
time.sleep(0.5)
data = read_wait(tn, 2)
text = log_section("AFTER NAME 'archivist'", data)

# Check for Yes/No confirmation
if "yes or no" in text.lower() or "correct?" in text.lower():
    tn.write(b'yes\n')
    time.sleep(0.5)
    data = read_wait(tn, 2)
    text = log_section("AFTER YES CONFIRM", data)

# Keep reading and responding to prompts
for i in range(40):
    time.sleep(1.5)
    try:
        data = tn.read_very_eager()
    except EOFError:
        break
    
    if data:
        text = log_section(f"STEP {i}", data)
        low = text.lower()
        
        if "yes or no" in low:
            tn.write(b'yes\n')
            time.sleep(0.3)
        elif "password" in low or "passwd" in low:
            tn.write(b'testpass123\n')
            time.sleep(0.3)
        elif "confirm" in low or "retype" in low or "again" in low:
            tn.write(b'testpass123\n')
            time.sleep(0.3)
        elif "gender" in low and ("?" in text or ":" in text or "choose" in low):
            tn.write(b'm\n')
            time.sleep(0.3)
        elif "[y/n]" in low or "(y/n)" in low:
            tn.write(b'y\n')
            time.sleep(0.3)
        elif "press enter" in low or "press return" in low:
            tn.write(b'\n')
            time.sleep(0.3)
        elif "try again" in low or "too short" in low:
            tn.write(b'archivist\n')
            time.sleep(0.3)
    else:
        # No data - try sending blank to flush
        tn.write(b'\n')
        time.sleep(1)
        try:
            data = tn.read_very_eager()
        except:
            break
        if data:
            log_section(f"FLUSH {i}", data)

tn.close()
print("[*] Done.", file=sys.stderr)
