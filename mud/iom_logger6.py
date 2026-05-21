#!/usr/bin/env python3
"""
Islands of Myth - Character Creation Archivist
Full sequential walkthrough capturing every screen.
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

def send_and_read(tn, cmd_bytes, wait=2):
    if cmd_bytes:
        tn.write(cmd_bytes)
        time.sleep(0.3)
    time.sleep(wait)
    try:
        return tn.read_very_eager()
    except:
        return b''

# --- MAIN ---
print(f"[*] Connecting to {HOST}:{PORT}...", file=sys.stderr)
tn = telnetlib.Telnet(HOST, PORT, timeout=TIMEOUT)
time.sleep(2)

# 1. LOGIN SCREEN
data = tn.read_very_eager()
log_section("01 - LOGIN MENU", data)

# 2. 'c' for create
data = send_and_read(tn, b'c\n', 2)
log_section("02 - NAME PROMPT", data)

# 3. Name
data = send_and_read(tn, b'archivist\n', 2)
text = log_section("03 - NAME CONFIRM", data)

# 4. Yes confirm
if "yes or no" in text.lower() or "correct?" in text.lower():
    data = send_and_read(tn, b'yes\n', 2)
    text = log_section("04 - PASSWORD PROMPT", data)

# 5. Password
data = send_and_read(tn, b'mudarchivist2026\n', 2)
text = log_section("05 - CONFIRM PASSWORD", data)

# 6. Confirm password
if "confirm" in text.lower() or "again" in text.lower() or "retype" in text.lower():
    data = send_and_read(tn, b'mudarchivist2026\n', 2)
    text = log_section("06 - GENDER PROMPT", data)

# 7. Gender
data = send_and_read(tn, b'male\n', 2)
text = log_section("07 - AFTER GENDER", data)

# 8. Keep capturing - race selection, alignment, etc.
for i in range(50):
    time.sleep(2)
    try:
        data = tn.read_very_eager()
    except EOFError:
        break
    
    if not data:
        # Try sending blank to see if there's a prompt
        tn.write(b'\n')
        time.sleep(1)
        try:
            data = tn.read_very_eager()
        except:
            break
    
    if data:
        text = log_section(f"08 - STEP {i}", data)
        low = text.lower()
        
        # Respond to prompts
        if "yes or no" in low:
            data = send_and_read(tn, b'yes\n', 2)
            log_section(f"08 - STEP {i}a YES", data)
        elif "[y/n]" in low:
            data = send_and_read(tn, b'y\n', 2)
            log_section(f"08 - STEP {i}b Y/N", data)
        elif "press enter" in low or "press a enter" in low:
            data = send_and_read(tn, b'\n', 2)
            log_section(f"08 - STEP {i}c ENTER", data)
        elif "race" in low and "select" in low:
            print("[*] RACE SELECTION FOUND!", file=sys.stderr)
        elif "alignment" in low:
            print("[*] ALIGNMENT SELECTION FOUND!", file=sys.stderr)

tn.close()
print("[*] Done.", file=sys.stderr)
