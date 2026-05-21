#!/usr/bin/env python3
"""
MUD Leveling Bot v2 - Emalz to Level 5
Direct paths, no loops, aggressive exploration.
"""
import telnetlib
import time
import os
import re
from datetime import datetime

HOST = "islandsofmyth.org"
PORT = 3000
USERNAME = "emalz"
PASSWORD = "creative"
ARCHIVE_DIR = "/root/.openclaw/workspace/mud/emalz_archive/"

ANSI_RE = re.compile(r'\x1b\[[0-9;]*m')

def strip_ansi(text):
    return ANSI_RE.sub('', text)

def log_line(text, session_file):
    with open(session_file, "a", encoding="utf-8", errors="replace") as f:
        f.write(strip_ansi(text).rstrip() + "\n")
        f.flush()

def write_file(name, content):
    path = os.path.join(ARCHIVE_DIR, name)
    with open(path, "w", encoding="utf-8", errors="replace") as f:
        f.write(content)
    return path

class FastLevelBot:
    def __init__(self):
        self.tn = None
        self.session_file = None
        self.cmd_count = 0
        
    def connect(self):
        self.tn = telnetlib.Telnet(HOST, PORT, timeout=30)
        epoch = str(int(time.time()))
        self.session_file = os.path.join(ARCHIVE_DIR, f"SESSION_FAST_{epoch}.txt")
        log_line(f"[START] {datetime.now().isoformat()}", self.session_file)
        
    def read_chunk(self, timeout=3):
        end = time.time() + timeout
        buf = ""
        while time.time() < end:
            try:
                data = self.tn.read_very_eager()
                if data:
                    buf += data.decode('ascii', errors='replace')
            except:
                pass
            if buf:
                # Check if prompt arrived
                if 'hp(' in buf and '>' in buf:
                    time.sleep(0.2)
                    try:
                        extra = self.tn.read_very_eager().decode('ascii', errors='replace')
                        buf += extra
                    except:
                        pass
                    break
                if '[abcdeq]' in buf or 'Your choice' in buf:
                    break
            time.sleep(0.1)
        if buf:
            log_line(buf, self.session_file)
        return buf
    
    def send(self, cmd, wait_time=3):
        log_line(f">>> {cmd}", self.session_file)
        self.tn.write((cmd + "\r\n").encode('ascii'))
        self.cmd_count += 1
        time.sleep(0.3)
        return self.read_chunk(timeout=wait_time)
    
    def login(self):
        time.sleep(3)
        self.read_chunk(timeout=5)
        r = self.send(USERNAME, wait_time=3)
        if "password" in r.lower() or "pass" in r.lower():
            r = self.send(PASSWORD, wait_time=5)
        time.sleep(2)
        self.read_chunk(timeout=5)
        log_line("[LOGIN] Done", self.session_file)
        
    def save_score_skills(self, label):
        r1 = self.send("score", wait_time=2)
        write_file(f"score_{label}_{int(time.time())}.txt", r1)
        r2 = self.send("skills", wait_time=2)
        write_file(f"skills_{label}_{int(time.time())}.txt", r2)
        return r1, r2
    
    def parse_level(self, score_text):
        for line in score_text.split("\n"):
            if "Level" in line and ":" in line:
                try:
                    val = line.split(":")[1].strip().split()[0]
                    return int(val)
                except:
                    pass
        return 1
    
    def join_warrior_guild(self):
        log_line("[GUILD] Joining warrior guild", self.session_file)
        self.send("warp", wait_time=2)
        r = self.send("ne", wait_time=2)
        if "portal" in r.lower():
            r = self.send("warrior", wait_time=3)
            write_file(f"warrior_enter_{int(time.time())}.txt", r)
            # Try to join
            r2 = self.send("join guild", wait_time=3)
            write_file(f"warrior_join_{int(time.time())}.txt", r2)
            # Try advance/train
            r3 = self.send("advance guild level", wait_time=3)
            write_file(f"warrior_advance_{int(time.time())}.txt", r3)
            r4 = self.send("train skills", wait_time=3)
            write_file(f"warrior_train_{int(time.time())}.txt", r4)
        self.send("warp", wait_time=2)
    
    def advance_level(self):
        log_line("[LEVEL] Advancing at judge", self.session_file)
        self.send("warp", wait_time=2)
        r = self.send("w", wait_time=2)  # Judge is WEST of guild
        if "achman" in r.lower() or "judge" in r.lower():
            r = self.send("talk to judge", wait_time=3)
            write_file(f"judge_menu_{int(time.time())}.txt", r)
            if "[abcdeq]" in r:
                r = self.send("c", wait_time=3)  # Advance level
                write_file(f"judge_advance_{int(time.time())}.txt", r)
                time.sleep(1)
                # Quit menu
                self.send("q", wait_time=2)
        self.send("warp", wait_time=2)
    
    def find_and_kill_monsters(self):
        """Explore outward from guild and kill anything."""
        log_line("[HUNT] Looking for monsters", self.session_file)
        
        # Start at guild
        self.send("warp", wait_time=2)
        
        # Go north to Cloud Road
        r = self.send("n", wait_time=2)
        
        # From Cloud Road, go east and keep exploring
        # Cloud Road has exits: south, west, east
        # Let's try east multiple times
        current = r
        path_taken = ["n"]
        
        # Try east from Cloud Road
        for step in range(8):  # Explore up to 8 rooms out
            r = self.send("e", wait_time=2)
            path_taken.append("e")
            
            # Check for monsters
            low = r.lower()
            if any(m in low for m in ["earwig", "rat", "bug", "worm", "insect", "spider", "snake", 
                                        "lizard", "goblin", "orc", "slime", "bat", "bee", "ant",
                                        "mouse", "rabbit", "fox", "wolf", "boar", "deer"]):
                # Found something! Try to kill
                log_line(f"[FOUND] Monster at step {step}", self.session_file)
                self.combat_cycle()
                
                # Check level
                r_score = self.send("score", wait_time=2)
                lvl = self.parse_level(r_score)
                if lvl >= 5:
                    return True
            
            # If no exits to continue east, try other directions
            if "exits" not in r.lower():
                break
            if "east" not in r.lower():
                # Try other directions to keep moving outward
                for d in ["n", "ne", "e", "se", "s", "u"]:
                    if d in r.lower() and d != "west" and d != "south":
                        r = self.send(d, wait_time=2)
                        path_taken.append(d)
                        break
                else:
                    break
        
        # Return to guild
        log_line(f"[HUNT] Returning from {len(path_taken)} steps", self.session_file)
        for d in reversed(path_taken):
            opp = {"n":"s","s":"n","e":"w","w":"e","ne":"sw","sw":"ne","se":"nw","nw":"se","u":"d","d":"u"}
            self.send(opp.get(d, ""), wait_time=1)
        
        return False
    
    def combat_cycle(self):
        """Kill monster, loot, eat, rest."""
        log_line("[COMBAT] Starting combat", self.session_file)
        
        # Enable combat silence
        self.send("combat silent on", wait_time=1)
        
        # Try kill commands
        targets = ["earwig", "rat", "bug", "worm", "insect", "spider", "snake", 
                   "lizard", "goblin", "orc", "slime", "bat", "monster"]
        
        for target in targets:
            r = self.send(f"kill {target}", wait_time=8)
            write_file(f"combat_{target}_{int(time.time())}.txt", r)
            
            if any(x in r.lower() for x in ["you have slain", "dead", "corpse", "killed", "died"]):
                log_line(f"[COMBAT] Killed {target}", self.session_file)
                self.send("get all corpse", wait_time=1)
                self.send("eat corpse", wait_time=1)
                self.send("rest", wait_time=3)
                return True
            elif "you are fighting" in r.lower() or "you attack" in r.lower():
                # Combat started, wait for it
                log_line("[COMBAT] Combat in progress...", self.session_file)
                for _ in range(15):
                    time.sleep(2)
                    r2 = self.read_chunk(timeout=2)
                    if any(x in r2.lower() for x in ["you have slain", "dead", "corpse", "killed", "died", "fled"]):
                        log_line("[COMBAT] Combat ended", self.session_file)
                        self.send("get all corpse", wait_time=1)
                        self.send("eat corpse", wait_time=1)
                        self.send("rest", wait_time=3)
                        return True
        
        return False
    
    def run(self):
        os.makedirs(ARCHIVE_DIR, exist_ok=True)
        self.connect()
        self.login()
        
        # Initial state
        self.save_score_skills("start")
        
        # Join warrior guild once
        self.join_warrior_guild()
        
        # Main loop
        cycles = 0
        while True:
            cycles += 1
            log_line(f"[CYCLE] {cycles}", self.session_file)
            
            # Check current level
            r = self.send("score", wait_time=2)
            lvl = self.parse_level(r)
            log_line(f"[STATUS] Level {lvl}", self.session_file)
            
            if lvl >= 5:
                log_line("[GOAL] Level 5 achieved!", self.session_file)
                break
            
            # Try to advance level if possible
            self.advance_level()
            
            # Go hunt
            self.find_and_kill_monsters()
            
            # After hunt, advance again if possible
            self.advance_level()
            
            # Check if we're stuck (no progress after many cycles)
            if cycles > 30:
                log_line("[WARN] Too many cycles, breaking", self.session_file)
                break
        
        # Final state
        self.save_score_skills("level5_final")
        r = self.send("inventory", wait_time=2)
        write_file(f"inventory_final_{int(time.time())}.txt", r)
        
        self.send("quit", wait_time=2)
        log_line(f"[END] {datetime.now().isoformat()}", self.session_file)

if __name__ == "__main__":
    bot = FastLevelBot()
    try:
        bot.run()
        print("Done.")
    except Exception as e:
        import traceback
        print(f"Error: {e}")
        if bot.session_file:
            log_line(f"[FATAL] {e}\n{traceback.format_exc()}", bot.session_file)
