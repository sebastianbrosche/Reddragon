#!/usr/bin/env python3
"""
Islands of Myth - Character Creation Archivist
Logs every screen, every race, every detail.
"""

import telnetlib
import time
import re
import sys

HOST = "islandsofmyth.org"
PORT = 3000
TIMEOUT = 10

def log_raw(data, label=""):
    """Log raw bytes with clear markers."""
    timestamp = time.strftime("%H:%M:%S")
    print(f"\n{'='*60}", file=sys.stderr)
    print(f"[{timestamp}] {label}", file=sys.stderr)
    print(f"{'='*60}", file=sys.stderr)
    # Print as text, replacing unprintable chars
    text = data.decode('ascii', errors='replace')
    print(text, file=sys.stderr)
    print(f"{'='*60}\n", file=sys.stderr)
    return text

def send_and_wait(tn, cmd, wait_time=2, label=""):
    """Send command and read response."""
    if cmd:
        tn.write(cmd.encode('ascii') + b'\n')
        time.sleep(0.5)
    time.sleep(wait_time)
    try:
        data = tn.read_very_eager()
    except:
        data = b''
    return log_raw(data, label)

def main():
    print(f"[*] Connecting to {HOST}:{PORT}...", file=sys.stderr)
    
    tn = telnetlib.Telnet(HOST, PORT, timeout=TIMEOUT)
    
    # Wait for login screen
    time.sleep(2)
    data = tn.read_very_eager()
    log_raw(data, "LOGIN SCREEN")
    
    # Try 'c' for create
    print("\n[*] Sending 'c' to create character...", file=sys.stderr)
    text = send_and_wait(tn, "c", 3, "CHAR CREATE - START")
    
    # Capture all prompts and respond
    for step in range(50):  # Max 50 interactions
        time.sleep(1)
        try:
            data = tn.read_very_eager()
        except:
            break
        if data:
            text = log_raw(data, f"STEP {step}")
            
            # Look for common prompts and auto-respond
            if "name" in text.lower() and "?" in text:
                print("[*] Detected name prompt, sending 'Archivist'...", file=sys.stderr)
                tn.write(b'Archivist\n')
            elif "password" in text.lower() or "passwd" in text.lower():
                print("[*] Detected password prompt, sending 'testpass123'...", file=sys.stderr)
                tn.write(b'testpass123\n')
            elif "confirm" in text.lower() or "retype" in text.lower():
                print("[*] Detected confirm prompt, sending same...", file=sys.stderr)
                tn.write(b'testpass123\n')
            elif "gender" in text.lower():
                print("[*] Detected gender prompt, sending 'm'...", file=sys.stderr)
                tn.write(b'm\n')
            elif "race" in text.lower() and ("select" in text.lower() or "choose" in text.lower() or "list" in text.lower()):
                # We'll need to handle races specially
                print("[*] Detected race selection!", file=sys.stderr)
                break
            elif "y/n" in text.lower() or "[y/n]" in text.lower():
                print("[*] Detected yes/no, sending 'y'...", file=sys.stderr)
                tn.write(b'y\n')
            elif "enter" in text.lower() and "continue" in text.lower():
                print("[*] Detected continue prompt...", file=sys.stderr)
                tn.write(b'\n')
    
    # Keep reading until connection closes
    for _ in range(20):
        time.sleep(1)
        try:
            data = tn.read_very_eager()
            if data:
                log_raw(data, "CONTINUOUS")
        except:
            break
    
    tn.close()
    print("[*] Session closed.", file=sys.stderr)

if __name__ == "__main__":
    main()
