#!/usr/bin/env python3
"""
Islands of Myth - Character Creation Archivist
Sequential, step-by-step capture of the entire creation flow.
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
    """Send command, wait, read response."""
    if cmd_bytes:
        tn.write(cmd_bytes)
        time.sleep(0.3)
    time.sleep(wait)
    try:
        return tn.read_very_eager()
    except:
        return b''

def wait_for_prompt(tn, wait=3):
    """Wait and read whatever comes."""
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

# 2. Send 'c' for create
data = send_and_read(tn, b'c\n', 2)
text = log_section("02 - NAME PROMPT", data)

# 3. Send name (lowercase)
data = send_and_read(tn, b'archivist\n', 2)
text = log_section("03 - NAME CONFIRM", data)

# 4. Confirm name with 'yes'
if "yes or no" in text.lower() or "correct?" in text.lower():
    data = send_and_read(tn, b'yes\n', 2)
    text = log_section("04 - AFTER YES", data)

# 5. Password
data = send_and_read(tn, b'mudarchivist2026\n', 2)
text = log_section("05 - AFTER PASSWORD", data)

# 6. Confirm password (if asked)
if "confirm" in text.lower() or "retype" in text.lower() or "again" in text.lower():
    data = send_and_read(tn, b'mudarchivist2026\n', 2)
    text = log_section("06 - AFTER CONFIRM PASS", data)

# 7. Keep capturing until we see race selection or get stuck
for i in range(50):
    time.sleep(1.5)
    try:
        data = tn.read_very_eager()
    except EOFError:
        break
    
    if data:
        text = log_section(f"STEP {i}", data)
        low = text.lower()
        
        # Check for specific prompts
        if "yes or no" in low:
            data = send_and_read(tn, b'yes\n', 2)
            log_section(f"STEP {i}a - YES", data)
        elif "password" in low and ("?" in text or ":" in text):
            data = send_and_read(tn, b'mudarchivist2026\n', 2)
            log_section(f"STEP {i}b - PASS", data)
        elif "confirm" in low or "retype" in low:
            data = send_and_read(tn, b'mudarchivist2026\n', 2)
            log_section(f"STEP {i}c - CONFIRM", data)
        elif "gender" in low and ("?" in text or ":" in text):
            data = send_and_read(tn, b'm\n', 2)
            log_section(f"STEP {i}d - GENDER", data)
        elif "race" in low and ("select" in low or "choose" in low or "list" in low):
            print("[*] RACE SELECTION DETECTED!", file=sys.stderr)
            break
        elif "[y/n]" in low:
            data = send_and_read(tn, b'y\n', 2)
            log_section(f"STEP {i}e - Y/N", data)
        elif "press enter" in low or "press return" in low:
            data = send_and_read(tn, b'\n', 2)
            log_section(f"STEP {i}f - ENTER", data)
        elif "try again" in low:
            # Something went wrong, send name again
            data = send_and_read(tn, b'archivist\n', 2)
            log_section(f"STEP {i}g - RETRY", data)

# Extra capture
for _ in range(10):
    time.sleep(1)
    try:
        data = tn.read_very_eager()
        if data:
            log_section("EXTRA", data)
    except:
        break

tn.close()
print("[*] Session complete.", file=sys.stderr)
