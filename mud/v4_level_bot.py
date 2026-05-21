#!/usr/bin/env python3
"""
MUD Leveling Bot v4 - Emalz to Level 5
DFS exploration, fixed judge menu, proper warrior guild path.
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
MONSTER_NAMES = ["earwig", "rat", "bug", "worm", "insect", "spider", "snake", "lizard", "goblin", 
                 "orc", "slime", "bat", "bee", "ant", "mouse", "rabbit", "fox", "wolf", "boar", 
                 "deer", "bird", "fly", "mosquito", "gnat", "cockroach", "beetle", "moth",
                 "skeleton", "zombie", "ghost", "spirit", "imp", "fairy", "pixie", "sprite"]

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

class V4Bot:
    def __init__(self):
        self.tn = None
        self.session_file = None
        self.cmd_count = 0
        
    def connect(self):
        self.tn = telnetlib.Telnet(HOST, PORT, timeout=30)
        epoch = str(int(time.time()))
        self.session_file = os.path.join(ARCHIVE_DIR, f"SESSION_V4_{epoch}.txt")
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
            if buf and ('hp(' in buf and '>' in buf or '[abcdeq]' in buf):
                time.sleep(0.3)
                try:
                    buf += self.tn.read_very_eager().decode('ascii', errors='replace')
                except:
                    pass
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
    
    def parse_exits(self, text):
        """Extract available exits from room description."""
        for line in text.split("\n"):
            line = line.strip().lower()
            if 'exits:' in line or '[exits' in line:
                exits = []
                for d in ["north","south","east","west","northeast","southwest","southeast","northwest","up","down"]:
                    if d in line:
                        exits.append(d)
                # Also check short forms if long forms not found
                if not exits:
                    for d in ["n ","s ","e ","w ","ne ","sw ","se ","nw ","u ","d "]:
                        if d in line or d.rstrip() in line:
                            exits.append(d.rstrip())
                return exits
        return []
    
    def login(self):
        time.sleep(3)
        self.read_chunk(timeout=5)
        r = self.send(USERNAME, wait_time=3)
        if "password" in r.lower():
            r = self.send(PASSWORD, wait_time=5)
        time.sleep(2)
        self.read_chunk(timeout=5)
        log_line("[LOGIN] Done", self.session_file)
    
    def advance_level(self):
        log_line("[LEVEL] Advancing at judge", self.session_file)
        self.send("warp", wait_time=2)
        r = self.send("e", wait_time=2)
        if "achman" in r.lower() or "judge" in r.lower():
            r = self.send("talk to judge", wait_time=3)
            write_file(f"judge_menu_{int(time.time())}.txt", r)
            if "[abcdeq]" in r:
                r = self.send("d", wait_time=3)  # 'd' = advance picking a stat (needed!)
                write_file(f"judge_advance_{int(time.time())}.txt", r)
                time.sleep(0.5)
                # Quit menu
                r2 = self.send("q", wait_time=2)
                write_file(f"judge_quit_{int(time.time())}.txt", r2)
        self.send("warp", wait_time=2)
    
    def join_warrior_guild(self):
        log_line("[GUILD] Warrior guild", self.session_file)
        self.send("warp", wait_time=2)
        r = self.send("sw", wait_time=2)  # sw from guild = Portal Room
        if "portal" in r.lower():
            r = self.send("warrior", wait_time=3)
            write_file(f"warrior_enter_{int(time.time())}.txt", r)
            # Try commands in warrior guild
            r2 = self.send("join guild", wait_time=3)
            write_file(f"warrior_join_{int(time.time())}.txt", r2)
            r3 = self.send("advance guild level", wait_time=3)
            write_file(f"warrior_advance_{int(time.time())}.txt", r3)
            r4 = self.send("train skills", wait_time=3)
            write_file(f"warrior_train_{int(time.time())}.txt", r4)
            r5 = self.send("list skills", wait_time=3)
            write_file(f"warrior_list_{int(time.time())}.txt", r5)
        self.send("warp", wait_time=2)
    
    def try_kill_anything(self, room_text):
        """Attempt to find and kill a monster in current room."""
        low = room_text.lower()
        
        # Check for known monsters in room description
        for monster in MONSTER_NAMES:
            if monster in low:
                log_line(f"[MONSTER] Detected: {monster}", self.session_file)
                return self.do_kill(monster)
        
        # Try generic kill commands for unseen monsters
        for target in ["monster", "creature", "animal"]:
            r = self.send(f"kill {target}", wait_time=6)
            if any(x in r.lower() for x in ["you have slain", "dead", "corpse", "killed", "died", 
                                              "you are fighting", "you attack", "begin", "engaged"]):
                return self.handle_post_kill(r)
        
        return False
    
    def do_kill(self, target):
        log_line(f"[COMBAT] Killing {target}", self.session_file)
        self.send("combat silent on", wait_time=1)
        
        r = self.send(f"kill {target}", wait_time=12)
        write_file(f"combat_{target}_{int(time.time())}.txt", r)
        
        if any(x in r.lower() for x in ["you have slain", "dead", "corpse", "killed", "died"]):
            return self.handle_post_kill(r)
        
        if any(x in r.lower() for x in ["you are fighting", "you attack", "begin", "engaged", "combat"]):
            log_line("[COMBAT] In progress, waiting...", self.session_file)
            for _ in range(20):
                time.sleep(2)
                r2 = self.read_chunk(timeout=2)
                if any(x in r2.lower() for x in ["you have slain", "dead", "corpse", "killed", "died", "fled"]):
                    return self.handle_post_kill(r + r2)
        
        return False
    
    def handle_post_kill(self, combat_text):
        log_line("[COMBAT] Post-kill cleanup", self.session_file)
        self.send("get all corpse", wait_time=1)
        self.send("eat corpse", wait_time=1)
        self.send("rest", wait_time=4)
        
        r = self.send("score", wait_time=2)
        lvl = self.parse_level(r)
        return lvl >= 5
    
    def dfs_explore(self, depth=0, max_depth=12, visited=None):
        """Depth-first search exploring all exits. Returns True if level 5 reached."""
        if visited is None:
            visited = set()
        
        if depth > max_depth:
            return False
        
        # Read current room
        r = self.read_chunk(timeout=2)
        room = self.parse_room(r)
        
        if room in visited:
            return False
        visited.add(room)
        
        log_line(f"[DFS] Depth {depth}, room: {room}", self.session_file)
        
        # Try to kill anything here
        if self.try_kill_anything(r):
            return True
        
        # Get exits
        exits = self.parse_exits(r)
        log_line(f"[DFS] Exits: {exits}", self.session_file)
        
        # Try each exit (skip backtracking direction if possible)
        opp = {"north":"south","south":"north","east":"west","west":"east",
               "northeast":"southwest","southwest":"northeast","southeast":"northwest","northwest":"southeast",
               "up":"down","down":"up","n":"s","s":"n","e":"w","w":"e",
               "ne":"sw","sw":"ne","se":"nw","nw":"se","u":"d","d":"u"}
        
        for ex in exits:
            # Skip if it's just going back
            if depth > 0 and ex == opp.get(self.last_dir, ""):
                continue
            
            self.last_dir = ex
            r2 = self.send(ex, wait_time=2)
            
            # Recurse
            if self.dfs_explore(depth + 1, max_depth, visited):
                return True
            
            # Go back
            back = opp.get(ex, "")
            if back:
                self.send(back, wait_time=2)
        
        return False
    
    def explore_from_guild(self):
        """Start exploration from guild going north."""
        log_line("[EXPLORE] Starting from guild", self.session_file)
        self.send("warp", wait_time=2)
        self.send("n", wait_time=2)  # Cloud Road
        self.last_dir = "north"
        
        visited = set()
        found = self.dfs_explore(0, max_depth=12, visited=visited)
        
        # Return via warp
        self.send("warp", wait_time=2)
        return found
    
    def run(self):
        os.makedirs(ARCHIVE_DIR, exist_ok=True)
        self.connect()
        self.login()
        
        # Initial state
        r = self.send("score", wait_time=2)
        write_file(f"score_v4_start_{int(time.time())}.txt", r)
        r = self.send("skills", wait_time=2)
        write_file(f"skills_v4_start_{int(time.time())}.txt", r)
        
        # Join warrior guild once
        self.join_warrior_guild()
        
        # Main loop
        for cycle in range(50):
            log_line(f"[CYCLE] {cycle+1}", self.session_file)
            
            r = self.send("score", wait_time=2)
            lvl = self.parse_level(r)
            log_line(f"[STATUS] Level {lvl}", self.session_file)
            
            if lvl >= 5:
                log_line("[GOAL] LEVEL 5!", self.session_file)
                break
            
            # Try to advance
            self.advance_level()
            
            # Explore and kill
            reached = self.explore_from_guild()
            if reached:
                break
            
            # Try advance again
            self.advance_level()
            
            # Also try warrior guild again
            self.join_warrior_guild()
        
        # Final
        r = self.send("score", wait_time=2)
        write_file(f"score_v4_final_{int(time.time())}.txt", r)
        r = self.send("skills", wait_time=2)
        write_file(f"skills_v4_final_{int(time.time())}.txt", r)
        r = self.send("inventory", wait_time=2)
        write_file(f"inventory_v4_final_{int(time.time())}.txt", r)
        
        self.send("quit", wait_time=2)
        log_line(f"[END] {datetime.now().isoformat()}", self.session_file)

if __name__ == "__main__":
    bot = V4Bot()
    try:
        bot.run()
        print("Done.")
    except Exception as e:
        import traceback
        print(f"Error: {e}")
        if bot.session_file:
            log_line(f"[FATAL] {e}\n{traceback.format_exc()}", bot.session_file)
