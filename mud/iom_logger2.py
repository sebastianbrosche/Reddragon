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

def expect_and_send(tn, send_bytes, wait=2):
    """Send data, wait, read response."""
    if send_bytes:
        tn.write(send_bytes)
        time.sleep(0.3)
    time.sleep(wait)
    return tn.read_very_eager()

# --- MAIN ---
print(f"[*] Connecting to {HOST}:{PORT}...", file=sys.stderr)
tn = telnetlib.Telnet(HOST, PORT, timeout=TIMEOUT)
time.sleep(2)

# Capture login banner
login_data = tn.read_very_eager()
text = log_section("LOGIN MENU", login_data)

# Step 1: Press 'c' to create
data = expect_and_send(tn, b'c\n', 2)
text = log_section("AFTER 'c' - NAME PROMPT", data)

# Step 2: Name
data = expect_and_send(tn, b'Archivist\n', 2)
text = log_section("AFTER NAME", data)

# Step 3: Password (if asked)
if "password" in text.lower() or "passwd" in text.lower():
    data = expect_and_send(tn, b'testpass123\n', 2)
    text = log_section("AFTER PASSWORD", data)

# Step 4: Confirm password (if asked)
if "confirm" in text.lower() or "retype" in text.lower() or "again" in text.lower():
    data = expect_and_send(tn, b'testpass123\n', 2)
    text = log_section("AFTER CONFIRM", data)

# Step 5: Gender (if asked)
if "gender" in text.lower() or "sex" in text.lower():
    data = expect_and_send(tn, b'm\n', 2)
    text = log_section("AFTER GENDER", data)

# Step 6+: Keep capturing until race selection or game entry
for i in range(30):
    time.sleep(1.5)
    try:
        data = tn.read_very_eager()
    except EOFError:
        break
    if data:
        text = log_section(f"STEP {i}", data)
        
        # Auto-respond to simple prompts
        if "[y/n]" in text.lower() or "(y/n)" in text.lower():
            tn.write(b'y\n')
            time.sleep(0.3)
        elif "press enter" in text.lower() or "press return" in text.lower():
            tn.write(b'\n')
            time.sleep(0.3)
        elif "gender" in text.lower() and ("?" in text or ":" in text):
            tn.write(b'm\n')
            time.sleep(0.3)
    else:
        # Send blank to see if there's a prompt waiting
        tn.write(b'\n')
        time.sleep(1)
        try:
            data = tn.read_very_eager()
        except:
            break
        if data:
            log_section(f"PROMPT CHECK {i}", data)

tn.close()
print("[*] Done.", file=sys.stderr)
