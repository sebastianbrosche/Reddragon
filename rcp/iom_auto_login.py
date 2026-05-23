#!/usr/bin/env python3
"""
IOM Auto-Login Handler
Monitors relay connection and auto-logs in if disconnected.

Usage:
    python3 iom_auto_login.py

Credentials should be stored in ~/.iom_credentials.json:
    {"username": "sebbe", "password": "YOUR_PASSWORD"}
"""

import asyncio
import json
import time
from pathlib import Path
import subprocess

CREDENTIALS_FILE = Path.home() / ".iom_credentials.json"
RELAY_LOG = Path("/tmp/mud-relay-v2.log")
SESSION_LOG = Path("/tmp/iom-session.log")

def load_credentials():
    """Load IOM credentials from file"""
    if not CREDENTIALS_FILE.exists():
        print(f"No credentials file found at {CREDENTIALS_FILE}")
        print("Create it with: echo '{\"username\": \"sebbe\", \"password\": \"YOUR_PASSWORD\"}' > ~/.iom_credentials.json")
        return None
    
    try:
        with open(CREDENTIALS_FILE) as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading credentials: {e}")
        return None

def is_connected():
    """Check if relay is connected to IOM"""
    try:
        with open(RELAY_LOG) as f:
            lines = f.readlines()
            for line in reversed(lines[-50:]):
                if "Connected to IOM" in line:
                    return True
                if "Disconnected" in line or "connection open" in line:
                    return False
        return False
    except:
        return False

def send_login_commands(creds):
    """Write login sequence to autopilot queue"""
    login_sequence = [
        creds["username"],
        creds["password"],
        "",  # Press return after login
        "look",
        "map"
    ]
    
    with open("/tmp/iom-autopilot-queue.txt", "w") as f:
        f.write("\n".join(login_sequence) + "\n")
    
    print(f"Login sequence queued for {creds['username']}")

async def monitor():
    """Monitor connection and auto-login on disconnect"""
    creds = load_credentials()
    if not creds:
        print("Auto-login disabled - no credentials")
        return
    
    print(f"Monitoring IOM connection for {creds['username']}...")
    was_connected = True
    
    while True:
        connected = is_connected()
        
        if was_connected and not connected:
            print("Connection lost! Waiting for reconnect...")
            time.sleep(5)
            
            # Check if we're at login screen
            with open(SESSION_LOG) as f:
                content = f.read()
                if "Your Selection?" in content or "name or choice" in content:
                    print("At login screen - sending credentials...")
                    send_login_commands(creds)
        
        was_connected = connected
        await asyncio.sleep(10)

if __name__ == "__main__":
    asyncio.run(monitor())
