#!/usr/bin/env python3
"""
Emalz MUD Leveling Bot - Focused combat script
Logs in as Emalz, grinds earwigs in Yensidland, levels to 5.
"""

import telnetlib
import time
import re
import os

HOST = "islandsofmyth.org"
PORT = 3000
USER = "emalz"
PASS = "creative"
ARCHIVE = "/root/.openclaw/workspace/mud/emalz_archive"

def log_file(name, content):
    os.makedirs(ARCHIVE, exist_ok=True)
    path = os.path.join(ARCHIVE, f"{name}_{int(time.time())}.txt")
    with open(path, "w") as f:
        f.write(content)
    return path

class MUDSession:
    def __init__(self):
        self.tn = None
        self.buffer = ""
        self.session_log = ""
        
    def connect(self):
        self.tn = telnetlib.Telnet(HOST, PORT, timeout=30)
        time.sleep(2)
        # Send name
        self.tn.write(f"{USER}\n".encode())
        time.sleep(1)
        self.tn.write(f"{PASS}\n".encode())
        time.sleep(3)
        # Read initial output
        data = self.read_all_pending()
        self.session_log += data
        print("[LOGIN] Done")
        return data
        
    def read_all_pending(self, timeout=3):
        data = ""
        start = time.time()
        while time.time() - start < timeout:
            try:
                chunk = self.tn.read_very_eager().decode('ascii', errors='ignore')
                if chunk:
                    data += chunk
                    start = time.time()
            except:
                break
        return data
        
    def send(self, cmd, wait=2):
        self.tn.write(f"{cmd}\n".encode())
        time.sleep(wait)
        data = self.read_all_pending()
        self.session_log += f"\n>>> {cmd}\n{data}"
        print(f"[{cmd}] {data[:200]}...")
        return data
        
    def send_and_wait(self, cmd, wait=3):
        return self.send(cmd, wait)
        
    def close(self):
        if self.tn:
            self.tn.close()
        # Save full session
        log_file("FULL_SESSION", self.session_log)

# ---- MAIN SCRIPT ----
session = MUDSession()
try:
    session.connect()
    
    # Check status
    score = session.send("score", 2)
    skills = session.send("skills", 2)
    
    # Join warrior guild if not already
    if "warrior" not in score.lower():
        session.send("warp", 2)
        session.send("sw", 2)
        session.send("warrior", 2)
        join = session.send("join guild", 2)
        log_file("JOIN_WARRIOR", join)
    
    # Get to Yensidland
    session.send("warp", 2)
    session.send("se", 2)
    session.send("e", 2)
    gnosis = session.send("talk to gnosis", 3)
    log_file("GNOSIS", gnosis)
    
    # Find and kill earwigs - keep trying until we find one
    kills = 0
    level = 1
    attempts = 0
    
    while level < 5 and attempts < 50:
        attempts += 1
        
        # Look for monsters in current room
        room = session.send("look", 2)
        
        # Try to kill anything that might be here
        for target in ["earwig", "insect", "bug", "monster", "creature"]:
            result = session.send(f"kill {target}", 3)
            if "You attack" in result or "You hit" in result or "fighting" in result.lower():
                log_file(f"COMBAT_{kills}", result)
                kills += 1
                # Wait for combat to finish
                time.sleep(10)
                after = session.read_all_pending(5)
                log_file(f"COMBAT_AFTER_{kills}", after)
                
                # Loot and eat
                session.send("get all", 2)
                session.send("eat corpse", 2)
                
                # Check score
                score = session.send("score", 2)
                log_file(f"SCORE_KILL_{kills}", score)
                
                # Check if leveled
                if "Level" in score:
                    lvl_match = re.search(r"Level\s+:\s+(\d+)", score)
                    if lvl_match:
                        new_level = int(lvl_match.group(1))
                        if new_level > level:
                            level = new_level
                            print(f"[LEVEL UP] Now level {level}")
                            
                            # Go level up at judge
                            session.send("warp", 2)
                            session.send("e", 2)
                            session.send("talk to judge", 2)
                            session.send("d", 2)  # advance picking stat
                            session.send("a", 2)  # pick strength
                            session.send("q", 2)
                            
                            # Advance guild
                            session.send("warp", 2)
                            session.send("sw", 2)
                            session.send("warrior", 2)
                            session.send("advance guild level", 2)
                            session.send("train skills", 2)
                            
                            # Get new skills list
                            skills = session.send("list skills", 2)
                            log_file(f"SKILLS_LEVEL_{level}", skills)
                            
                            # Back to Yensidland
                            session.send("warp", 2)
                            session.send("se", 2)
                            session.send("e", 2)
                break
        else:
            # No monster found, try moving around in Yensidland
            for direction in ["n", "s", "e", "w", "ne", "nw", "se", "sw"]:
                move = session.send(direction, 2)
                if "You can't go" not in move and "no exit" not in move.lower():
                    break
    
    # Final status
    final_score = session.send("score", 2)
    final_skills = session.send("skills", 2)
    log_file("FINAL_SCORE", final_score)
    log_file("FINAL_SKILLS", final_skills)
    
    print(f"[DONE] Kills: {kills}, Level: {level}")
    
finally:
    session.close()
