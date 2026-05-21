#!/usr/bin/env python3
"""
MUD Leveling Bot v3 - Emalz to Level 5
Aggressive outward exploration. Uses warp as anchor.
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

class V3Bot:
    def __init__(self):
        self.tn = None
        self.session_file = None
        self.cmd_count = 0
        self.visited = set()
        
    def connect(self):
        self.tn = telnetlib.Telnet(HOST, PORT, timeout=30)
        epoch = str(int(time.time()))
        self.session_file = os.path.join(ARCHIVE_DIR, f"SESSION_V3_{epoch}.txt")
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
                    extra = self.tn.read_very_eager().decode('ascii', errors='replace')
                    buf += extra
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
    
    def parse_room_name(self, text):
        lines = text.split("\n")
        for line in lines:
            line = line.strip()
            if line and '[' in line and 'exits' in line.lower():
                return line.split('[')[0].strip()
        return ""
    
    def login(self):
        time.sleep(3)
        self.read_chunk(timeout=5)
        r = self.send(USERNAME, wait_time=3)
        if "password" in r.lower():
            r = self.send(PASSWORD, wait_time=5)
        time.sleep(2)
        self.read_chunk(timeout=5)
        log_line("[LOGIN] Done", self.session_file)
    
    def find_judge(self):
        """Judge is east of guild in first session."""
        log_line("[JUDGE] Finding judge", self.session_file)
        self.send("warp", wait_time=2)
        
        # Try east first (from first session)
        for direction in ["e", "w", "s", "se", "sw", "n", "ne", "nw"]:
            r = self.send(direction, wait_time=2)
            if "achman" in r.lower() or "judge" in r.lower():
                log_line(f"[JUDGE] Found at direction: {direction}", self.session_file)
                return direction
            # Return
            opp = {"n":"s","s":"n","e":"w","w":"e","ne":"sw","sw":"ne","se":"nw","nw":"se"}
            self.send(opp[direction], wait_time=1)
        
        return None
    
    def advance_level(self, judge_dir):
        if not judge_dir:
            return
        log_line("[LEVEL] Advancing", self.session_file)
        self.send("warp", wait_time=2)
        r = self.send(judge_dir, wait_time=2)
        if "achman" in r.lower() or "judge" in r.lower():
            r = self.send("talk to judge", wait_time=3)
            write_file(f"judge_menu_{int(time.time())}.txt", r)
            if "[abcdeq]" in r:
                r = self.send("c", wait_time=3)
                write_file(f"judge_advance_{int(time.time())}.txt", r)
                time.sleep(0.5)
                self.send("q", wait_time=2)
        self.send("warp", wait_time=2)
    
    def find_warrior_guild(self):
        log_line("[WARRIOR] Finding warrior guild", self.session_file)
        self.send("warp", wait_time=2)
        
        # Try all directions from guild to find portal room
        for d1 in ["ne", "e", "se", "s", "sw", "w", "nw", "n"]:
            r = self.send(d1, wait_time=2)
            low = r.lower()
            
            if "portal" in low and "warrior" in low:
                log_line(f"[WARRIOR] Portal room at {d1}", self.session_file)
                r = self.send("warrior", wait_time=3)
                write_file(f"warrior_enter_{int(time.time())}.txt", r)
                self.send("join guild", wait_time=3)
                self.send("advance guild level", wait_time=3)
                self.send("train skills", wait_time=3)
                self.send("warp", wait_time=2)
                return True
            
            # Also check if this room IS the warrior guild
            if "warrior" in low and ("guild" in low or "master" in low or "trainer" in low):
                log_line(f"[WARRIOR] Direct at {d1}", self.session_file)
                self.send("join guild", wait_time=3)
                self.send("advance guild level", wait_time=3)
                self.send("train skills", wait_time=3)
                self.send("warp", wait_time=2)
                return True
            
            # Try second step
            opp = {"n":"s","s":"n","e":"w","w":"e","ne":"sw","sw":"ne","se":"nw","nw":"se"}
            for d2 in ["e", "n", "ne", "se", "s", "w", "sw", "nw"]:
                r2 = self.send(d2, wait_time=2)
                low2 = r2.lower()
                if "warrior" in low2 and ("guild" in low2 or "master" in low2 or "trainer" in low2 or "portal" in low2):
                    log_line(f"[WARRIOR] Found at path {d1},{d2}", self.session_file)
                    self.send("join guild", wait_time=3)
                    self.send("advance guild level", wait_time=3)
                    self.send("train skills", wait_time=3)
                    self.send("warp", wait_time=2)
                    return True
                self.send(opp[d2], wait_time=1)
            
            self.send(opp[d1], wait_time=1)
        
        self.send("warp", wait_time=2)
        return False
    
    def explore_and_kill(self):
        """Explore outward from guild, kill anything found."""
        log_line("[HUNT] Exploring for monsters", self.session_file)
        self.send("warp", wait_time=2)
        
        # Start at guild, go north to Cloud Road
        r = self.send("n", wait_time=2)
        room = self.parse_room_name(r)
        self.visited.add(room)
        
        # From Cloud Road, go east to Intersection
        r = self.send("e", wait_time=2)
        room = self.parse_room_name(r)
        self.visited.add(room)
        
        # From Intersection, go north to Titan street
        r = self.send("n", wait_time=2)
        room = self.parse_room_name(r)
        self.visited.add(room)
        
        # EXPLORE FURTHER - keep going north on Titan street
        # Then try east/west at each intersection
        path_stack = ["n", "e", "n"]  # How we got here
        
        # Keep going north as far as possible
        for step in range(15):
            r = self.send("n", wait_time=2)
            room = self.parse_room_name(r)
            
            if "exits" not in r.lower():
                log_line(f"[HUNT] Dead end at step {step}", self.session_file)
                break
            
            if room in self.visited:
                log_line(f"[HUNT] Loop detected at step {step}", self.session_file)
                break
            
            self.visited.add(room)
            path_stack.append("n")
            
            # Check for monsters in this room
            if self.try_kill_in_room(r):
                return True
            
            # If no north exit, try east or west
            if "north" not in r.lower():
                for d in ["e", "w", "ne", "nw", "se", "sw", "u", "d"]:
                    if d in r.lower():
                        r2 = self.send(d, wait_time=2)
                        room2 = self.parse_room_name(r2)
                        if room2 not in self.visited:
                            self.visited.add(room2)
                            path_stack.append(d)
                            if self.try_kill_in_room(r2):
                                return True
                            # Try going back and trying other direction
                            opp = {"n":"s","s":"n","e":"w","w":"e","ne":"sw","sw":"ne","se":"nw","nw":"se","u":"d","d":"u"}
                            self.send(opp[d], wait_time=1)
                            break
                break
        
        # Return via warp
        log_line(f"[HUNT] Returning via warp", self.session_file)
        self.send("warp", wait_time=2)
        return False
    
    def try_kill_in_room(self, room_text):
        """Try to kill any monster in the current room."""
        low = room_text.lower()
        
        # Common low-level monsters
        monsters = ["earwig", "rat", "bug", "worm", "insect", "spider", "snake", 
                    "lizard", "goblin", "orc", "slime", "bat", "bee", "ant",
                    "mouse", "rabbit", "fox", "wolf", "boar", "deer", "bird",
                    "fly", "mosquito", "gnat", "cockroach", "beetle", "moth"]
        
        # Also look for capitalized names that might be NPCs (not "A " or "An " items)
        for monster in monsters:
            if monster in low:
                log_line(f"[MONSTER] Found {monster}!", self.session_file)
                return self.kill_monster(monster)
        
        # If no obvious monster, try generic kill commands
        for target in ["monster", "creature", "animal", "npc"]:
            r = self.send(f"kill {target}", wait_time=5)
            if any(x in r.lower() for x in ["you have slain", "dead", "corpse", "killed", "died", "you are fighting", "you attack"]):
                log_line(f"[MONSTER] Killed {target}", self.session_file)
                return self.handle_post_kill()
        
        return False
    
    def kill_monster(self, target):
        log_line(f"[COMBAT] Killing {target}", self.session_file)
        self.send("combat silent on", wait_time=1)
        
        r = self.send(f"kill {target}", wait_time=10)
        write_file(f"combat_{target}_{int(time.time())}.txt", r)
        
        # Wait for combat to resolve
        if any(x in r.lower() for x in ["you have slain", "dead", "corpse", "killed", "died"]):
            return self.handle_post_kill()
        
        if "you are fighting" in r.lower() or "you attack" in r.lower() or "begin" in r.lower():
            log_line("[COMBAT] Waiting for combat end...", self.session_file)
            for _ in range(15):
                time.sleep(2)
                r2 = self.read_chunk(timeout=2)
                if any(x in r2.lower() for x in ["you have slain", "dead", "corpse", "killed", "died", "fled", "escaped"]):
                    return self.handle_post_kill()
        
        return False
    
    def handle_post_kill(self):
        self.send("get all corpse", wait_time=1)
        self.send("eat corpse", wait_time=1)
        self.send("rest", wait_time=3)
        
        # Check if leveled
        r = self.send("score", wait_time=2)
        lvl = self.parse_level(r)
        return lvl >= 5
    
    def run(self):
        os.makedirs(ARCHIVE_DIR, exist_ok=True)
        self.connect()
        self.login()
        
        # Save initial
        r = self.send("score", wait_time=2)
        write_file(f"score_v3_start_{int(time.time())}.txt", r)
        r = self.send("skills", wait_time=2)
        write_file(f"skills_v3_start_{int(time.time())}.txt", r)
        
        # Find judge direction
        judge_dir = self.find_judge()
        
        # Find warrior guild once
        self.find_warrior_guild()
        
        # Main loop
        for cycle in range(40):
            log_line(f"[CYCLE] {cycle+1}", self.session_file)
            
            # Check level
            r = self.send("score", wait_time=2)
            lvl = self.parse_level(r)
            log_line(f"[STATUS] Level {lvl}", self.session_file)
            
            if lvl >= 5:
                log_line("[GOAL] LEVEL 5 REACHED!", self.session_file)
                break
            
            # Try to advance
            self.advance_level(judge_dir)
            
            # Go hunt
            reached = self.explore_and_kill()
            if reached:
                break
            
            # Try advance again
            self.advance_level(judge_dir)
        
        # Final saves
        r = self.send("score", wait_time=2)
        write_file(f"score_v3_final_{int(time.time())}.txt", r)
        r = self.send("skills", wait_time=2)
        write_file(f"skills_v3_final_{int(time.time())}.txt", r)
        r = self.send("inventory", wait_time=2)
        write_file(f"inventory_v3_final_{int(time.time())}.txt", r)
        
        self.send("quit", wait_time=2)
        log_line(f"[END] {datetime.now().isoformat()}", self.session_file)

if __name__ == "__main__":
    bot = V3Bot()
    try:
        bot.run()
        print("Done.")
    except Exception as e:
        import traceback
        print(f"Error: {e}")
        if bot.session_file:
            log_line(f"[FATAL] {e}\n{traceback.format_exc()}", bot.session_file)
