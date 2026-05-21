#!/usr/bin/env python3
"""
MUD Leveling Bot v5 - Emalz to Level 5
Focused on finding and killing monsters. Fixed judge menu, fixed exploration.
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
MONSTERS = ["earwig", "rat", "bug", "worm", "insect", "spider", "snake", "lizard", "goblin", 
            "orc", "slime", "bat", "bee", "ant", "mouse", "rabbit", "fox", "wolf", "boar", 
            "deer", "bird", "fly", "mosquito", "gnat", "cockroach", "beetle", "moth",
            "skeleton", "zombie", "ghost", "spirit", "imp", "fairy", "pixie", "sprite",
            "gnoll", "kobold", "thug", "bandit", "rogue", "scout", "guard", "soldier",
            "scout", "patrol", "drone", "minion", "hound", "hound", "wolf", "pup", "cub"]

def strip_ansi(text):
    return ANSI_RE.sub('', text)

def log(text, session_file):
    with open(session_file, "a", encoding="utf-8", errors="replace") as f:
        f.write(strip_ansi(text).rstrip() + "\n")
        f.flush()

def save(name, content):
    path = os.path.join(ARCHIVE_DIR, name)
    with open(path, "w", encoding="utf-8", errors="replace") as f:
        f.write(content)
    return path

class Bot:
    def __init__(self):
        self.tn = None
        self.sf = None  # session file
        self.cmd = 0
        
    def connect(self):
        self.tn = telnetlib.Telnet(HOST, PORT, timeout=30)
        epoch = str(int(time.time()))
        self.sf = os.path.join(ARCHIVE_DIR, f"SESSION_V5_{epoch}.txt")
        log(f"[START] {datetime.now().isoformat()}", self.sf)
        
    def read(self, timeout=3):
        end = time.time() + timeout
        buf = ""
        while time.time() < end:
            try:
                d = self.tn.read_very_eager()
                if d:
                    buf += d.decode('ascii', errors='replace')
            except:
                pass
            if buf and (('hp(' in buf and '>' in buf) or '[abcdeq]' in buf or '[abcdefghijmq]' in buf):
                time.sleep(0.3)
                try:
                    buf += self.tn.read_very_eager().decode('ascii', errors='replace')
                except:
                    pass
                break
            time.sleep(0.1)
        if buf:
            log(buf, self.sf)
        return buf
    
    def send(self, cmd, wait=3):
        log(f">>> {cmd}", self.sf)
        self.tn.write((cmd + "\r\n").encode('ascii'))
        self.cmd += 1
        time.sleep(0.3)
        return self.read(timeout=wait)
    
    def parse_level(self, score_text):
        for line in score_text.split("\n"):
            if "Level" in line and ":" in line:
                try:
                    return int(line.split(":")[1].strip().split()[0])
                except:
                    pass
        return 1
    
    def parse_room(self, text):
        for line in text.split("\n"):
            line = line.strip()
            if line and '[' in line and 'exits' in line.lower():
                return line.split('[')[0].strip()
        return ""
    
    def get_exits(self, text):
        """Extract exits from room description line."""
        for line in text.split("\n"):
            line = line.strip().lower()
            if 'exits' in line:
                exits = []
                for d in ["north","south","east","west","northeast","southwest","southeast","northwest","up","down"]:
                    if d in line:
                        exits.append(d)
                return exits
        return []
    
    def login(self):
        time.sleep(3)
        self.read(timeout=5)
        r = self.send(USERNAME, wait=3)
        if "password" in r.lower():
            self.send(PASSWORD, wait=5)
        time.sleep(2)
        self.read(timeout=5)
        log("[LOGIN] Done", self.sf)
    
    def advance_level(self):
        """Go to judge and advance level."""
        log("[JUDGE] Advancing level", self.sf)
        self.send("warp", wait=2)
        r = self.send("e", wait=2)
        if "achman" in r.lower() or "judge" in r.lower():
            r = self.send("talk to judge", wait=3)
            save(f"judge_menu_{int(time.time())}.txt", r)
            if "[abcdeq]" in r:
                r = self.send("d", wait=3)  # advance picking a stat
                save(f"judge_pick_{int(time.time())}.txt", r)
                if "[abcdefghijmq]" in r:
                    # Pick strength (a)
                    r = self.send("a", wait=3)
                    save(f"judge_stat_{int(time.time())}.txt", r)
                    time.sleep(1)
                    # Quit judge menu
                    r = self.send("q", wait=2)
                    save(f"judge_quit_{int(time.time())}.txt", r)
        self.send("warp", wait=2)
    
    def warrior_stuff(self):
        """Go to warrior guild and try to advance/train."""
        log("[WARRIOR] Guild stuff", self.sf)
        self.send("warp", wait=2)
        self.send("sw", wait=2)   # Portal Room
        r = self.send("warrior", wait=3)
        save(f"warrior_enter_{int(time.time())}.txt", r)
        
        # Try various commands
        for cmd in ["advance", "level", "advance level", "advance guild level", 
                    "train", "train skills", "list skills", "skills"]:
            r = self.send(cmd, wait=3)
            save(f"warrior_{cmd.replace(' ','_')}_{int(time.time())}.txt", r)
        
        self.send("warp", wait=2)
    
    def try_kill(self, room_text):
        """Try to find and kill a monster in current room."""
        low = room_text.lower()
        
        # Look for monster names in room text
        for monster in MONSTERS:
            if monster in low:
                log(f"[KILL] Found {monster}", self.sf)
                return self.do_kill(monster)
        
        # Try generic targets
        for target in ["monster", "creature", "animal"]:
            r = self.send(f"kill {target}", wait=8)
            if any(x in r.lower() for x in ["slain", "dead", "corpse", "killed", "died", 
                                              "fighting", "attack", "begin", "engaged"]):
                return self.post_kill(r)
        
        return False
    
    def do_kill(self, target):
        log(f"[COMBAT] Killing {target}", self.sf)
        self.send("combat silent on", wait=1)
        
        r = self.send(f"kill {target}", wait=15)
        save(f"combat_{target}_{int(time.time())}.txt", r)
        
        if any(x in r.lower() for x in ["slain", "dead", "corpse", "killed", "died"]):
            return self.post_kill(r)
        
        if any(x in r.lower() for x in ["fighting", "attack", "begin", "engaged", "combat"]):
            log("[COMBAT] Waiting for end...", self.sf)
            for _ in range(25):
                time.sleep(2)
                r2 = self.read(timeout=2)
                if any(x in r2.lower() for x in ["slain", "dead", "corpse", "killed", "died", "fled"]):
                    return self.post_kill(r + r2)
        
        return False
    
    def post_kill(self, combat_text):
        log("[COMBAT] Post-kill", self.sf)
        self.send("get all corpse", wait=1)
        self.send("eat corpse", wait=1)
        self.send("rest", wait=5)
        
        r = self.send("score", wait=2)
        lvl = self.parse_level(r)
        return lvl >= 5
    
    def dfs_kill(self, depth, max_depth, visited, room_text, last_dir):
        """DFS exploring from current room. Returns True if level 5 reached."""
        if depth > max_depth:
            return False
        
        room = self.parse_room(room_text)
        if room in visited:
            return False
        visited.add(room)
        
        log(f"[DFS] d={depth} room='{room}'", self.sf)
        
        # Try to kill
        if self.try_kill(room_text):
            return True
        
        exits = self.get_exits(room_text)
        log(f"[DFS] exits={exits}", self.sf)
        
        opp = {"north":"south","south":"north","east":"west","west":"east",
               "northeast":"southwest","southwest":"northeast","southeast":"northwest","northwest":"southeast",
               "up":"down","down":"up"}
        
        for ex in exits:
            # Don't immediately backtrack
            if depth > 0 and ex == opp.get(last_dir, ""):
                continue
            
            r = self.send(ex, wait=2)
            if self.dfs_kill(depth + 1, max_depth, visited, r, ex):
                return True
            
            # Go back
            back = opp.get(ex, "")
            if back:
                self.send(back, wait=2)
        
        return False
    
    def explore_and_kill(self):
        """Explore from guild and try to kill monsters."""
        log("[EXPLORE] Starting hunt", self.sf)
        self.send("warp", wait=2)
        
        # Start at guild, go north
        r = self.send("n", wait=2)
        visited = set()
        found = self.dfs_kill(0, 15, visited, r, "north")
        
        self.send("warp", wait=2)
        return found
    
    def run(self):
        os.makedirs(ARCHIVE_DIR, exist_ok=True)
        self.connect()
        self.login()
        
        # Initial state
        r = self.send("score", wait=2)
        save(f"score_v5_start_{int(time.time())}.txt", r)
        r = self.send("skills", wait=2)
        save(f"skills_v5_start_{int(time.time())}.txt", r)
        
        # Do warrior guild once at start
        self.warrior_stuff()
        
        # Main loop
        for cycle in range(60):
            log(f"[CYCLE] {cycle+1}", self.sf)
            
            r = self.send("score", wait=2)
            lvl = self.parse_level(r)
            log(f"[STATUS] Level {lvl}", self.sf)
            
            if lvl >= 5:
                log("[GOAL] LEVEL 5 REACHED!", self.sf)
                break
            
            # Try to advance level
            self.advance_level()
            
            # Check level again
            r = self.send("score", wait=2)
            lvl = self.parse_level(r)
            if lvl >= 5:
                break
            
            # Explore and kill
            if self.explore_and_kill():
                break
            
            # Try advance again
            self.advance_level()
            
            # Warrior stuff again
            self.warrior_stuff()
        
        # Final
        r = self.send("score", wait=2)
        save(f"score_v5_final_{int(time.time())}.txt", r)
        r = self.send("skills", wait=2)
        save(f"skills_v5_final_{int(time.time())}.txt", r)
        r = self.send("inventory", wait=2)
        save(f"inventory_v5_final_{int(time.time())}.txt", r)
        
        self.send("quit", wait=2)
        log(f"[END] {datetime.now().isoformat()}", self.sf)

if __name__ == "__main__":
    bot = Bot()
    try:
        bot.run()
        print("Done.")
    except Exception as e:
        import traceback
        print(f"Error: {e}")
        if bot.sf:
            log(f"[FATAL] {e}\n{traceback.format_exc()}", bot.sf)
