#!/usr/bin/env python3
"""
Test recall/home/return commands from wilderness.
"""
import telnetlib, time, sys
HOST, PORT = "islandsofmyth.org", 3000
CHAR_NAME, CHAR_PASS = b'explorer\n', b'testpass123\n'

tn = telnetlib.Telnet(HOST, PORT, timeout=15)
time.sleep(2)
tn.read_very_eager()
tn.write(CHAR_NAME)
time.sleep(1)
tn.read_very_eager()
tn.write(CHAR_PASS)
time.sleep(1)
text = tn.read_very_eager().decode('ascii', errors='replace')
print("=== AFTER LOGIN ===\n" + text)

# Try various recall commands
for cmd in ["recall", "home", "return", "portal", "goto illium", "travel illium", "recall illium"]:
    print(f"\n[*] Trying: {cmd}")
    tn.write(f"{cmd}\n".encode())
    time.sleep(1.5)
    text = tn.read_very_eager().decode('ascii', errors='replace')
    print(f"=== {cmd.upper()} ===\n{text}")
    if "portal" in text.lower() or "illium" in text.lower() or "city" in text.lower() or "adventurer" in text.lower():
        print(f"[***] FOUND RECALL: {cmd}")
        break

# Also try help recall
tn.write(b'help recall\n')
time.sleep(1.5)
text = tn.read_very_eager().decode('ascii', errors='replace')
print(f"\n=== HELP RECALL ===\n{text}")

tn.write(b'quit\n')
time.sleep(2)
print(tn.read_very_eager().decode('ascii', errors='replace'))
tn.close()
