#!/usr/bin/env python3
"""
MUD Leveling Bot - Emalz to Level 5
Optimized for earwig grinding in Yensidland.
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

class MUDBot:
    def __init__(self):
        self.tn = None
        self.session_file = None
        self.cmd_count = 0
        self.in_menu = False
        
    def connect(self):
        self.tn = telnetlib.Telnet(HOST, PORT, timeout=30)
        epoch = str(int(time.time()))
        self.session_file = os.path.join(ARCHIVE_DIR, f"SESSION_LEVEL5_{epoch}.txt")
        log_line(f"[START] {datetime.now().isoformat()}", self.session_file)
        
    def read_chunk(self, timeout=3):
        """Read available data with timeout."""
        end = time.time() + timeout
        buf = ""
        while time.time() < end:
            try:
                data = self.tn.read_very_eager()
                if data:
                    buf += data.decode('ascii', errors='replace')
            except:
                pass
            if buf and not self._has_prompt(buf):
                time.sleep(0.3)
                continue
            if buf:
                break
            time.sleep(0.2)
        if buf:
            log_line(buf, self.session_file)
            # Check if we're in a menu
            if '[abcdeq]' in buf or 'Your choice' in buf.lower() or 'select' in buf.lower() and '[' in buf:
                self.in_menu = True
            elif 'hp(' in buf and '>' in buf:
                self.in_menu = False
        return buf
    
    def _has_prompt(self, text):
        return 'hp(' in text or '>' in text or ']' in text or 'Your choice' in text or '[abcdeq]' in text
    
    def send(self, cmd, wait_time=3, log_cmd=True):
        if log_cmd:
            log_line(f">>> {cmd}", self.session_file)
        self.tn.write((cmd + "\r\n").encode('ascii'))
        self.cmd_count += 1
        time.sleep(0.3)
        return self.read_chunk(timeout=wait_time)
    
    def menu_cmd(self, choice):
        """Send a menu selection."""
        log_line(f">>> [MENU] {choice}", self.session_file)
        self.tn.write((choice + "\r\n").encode('ascii'))
        self.cmd_count += 1
        time.sleep(0.5)
        return self.read_chunk(timeout=3)
    
    def save_snapshot(self, label):
        """Save score and skills."""
        r1 = self.send("score", wait_time=2)
        write_file(f"score_{label}_{int(time.time())}.txt", r1)
        r2 = self.send("skills", wait_time=2)
        write_file(f"skills_{label}_{int(time.time())}.txt", r2)
        return r1, r2
    
    def login(self):
        log_line("[PHASE] Login", self.session_file)
        time.sleep(3)
        self.read_chunk(timeout=5)
        
        # Send name
        r = self.send(USERNAME, wait_time=3)
        if "password" in r.lower() or "pass" in r.lower():
            r = self.send(PASSWORD, wait_time=5)
        
        # Wait for welcome
        time.sleep(2)
        self.read_chunk(timeout=5)
        log_line("[PHASE] Logged in", self.session_file)
        
    def explore_to_earwigs(self):
        """Navigate from Adventurer Guild to Yensidland to find earwigs."""
        log_line("[PHASE] Exploring to find earwigs", self.session_file)
        
        # Start at adventurer guild, go north to Cloud Road
        self.send("warp", wait_time=2)
        self.send("n", wait_time=2)
        
        # From Cloud Road, explore multiple directions
        # Try various paths to find earwigs
        dirs = ["n", "ne", "e", "se", "s", "sw", "w", "nw", "u", "d"]
        
        for d in dirs:
            r = self.send(d, wait_time=2)
            if "earwig" in r.lower():
                log_line(f"[FOUND] Earwigs at direction: {d}", self.session_file)
                return True, d
            # Check if we can go further
            if "exits" in r.lower():
                # Try a second move
                for d2 in dirs:
                    r2 = self.send(d2, wait_time=2)
                    if "earwig" in r2.lower():
                        log_line(f"[FOUND] Earwigs at path: {d},{d2}", self.session_file)
                        return True, f"{d},{d2}"
                    # Go back
                    self.send(self._opposite(d2), wait_time=1)
            # Go back to start
            self.send(self._opposite(d), wait_time=1)
            self.send("warp", wait_time=2)
            self.send("n", wait_time=2)
        
        return False, ""
    
    def _opposite(self, d):
        opp = {"n":"s","s":"n","e":"w","w":"e","ne":"sw","sw":"ne","se":"nw","nw":"se","u":"d","d":"u"}
        return opp.get(d, "")
    
    def find_gnosis(self):
        """Try to find gnosis and get assignment."""
        log_line("[PHASE] Finding Gnosis", self.session_file)
        self.send("warp", wait_time=2)
        
        # Try different paths from adventurer guild
        # Previous: warp->se->e = newbie guild, not gnosis
        # Try other directions
        paths = [
            ["se", "e"],  # newbie guild - has sisong
            ["se", "s"], ["se", "n"], ["se", "w"],
            ["e"], ["ne"], ["s"], ["sw"], ["w"], ["nw"], ["n", "e"], ["n", "w"]
        ]
        
        for path in paths:
            self.send("warp", wait_time=1)
            current = ""
            for d in path:
                current = self.send(d, wait_time=2)
                if "gnosis" in current.lower():
                    log_line(f"[FOUND] Gnosis at path: {','.join(path)}", self.session_file)
                    # Talk and get assignment
                    r = self.send("talk to gnosis", wait_time=3)
                    write_file(f"gnosis_talk_{int(time.time())}.txt", r)
                    r = self.send("get assignment", wait_time=3)
                    write_file(f"gnosis_assignment_{int(time.time())}.txt", r)
                    return True
            # Go back
            for d in reversed(path):
                self.send(self._opposite(d), wait_time=1)
        
        log_line("[WARN] Could not find Gnosis", self.session_file)
        return False
    
    def find_warrior_guild(self):
        """Find and enter warrior guild."""
        log_line("[PHASE] Finding Warrior Guild", self.session_file)
        self.send("warp", wait_time=2)
        
        # Try paths from adventurer guild
        paths = [["s"], ["se"], ["e"], ["ne"], ["n"], ["nw"], ["w"], ["sw"],
                 ["s","s"],["s","e"],["s","w"],["se","s"],["se","e"]]
        
        for path in paths:
            self.send("warp", wait_time=1)
            for d in path:
                r = self.send(d, wait_time=2)
                low = r.lower()
                if "warrior" in low or "fighter" in low or "combat" in low:
                    log_line(f"[FOUND] Warrior area at: {','.join(path)}", self.session_file)
                    # Try to join
                    r = self.send("join guild", wait_time=3)
                    write_file(f"join_warrior_{int(time.time())}.txt", r)
                    if "joined" in r.lower() or "welcome" in r.lower():
                        return True
                # Check for guild master
                if "guild" in low and "master" in low or "leader" in low or "trainer" in low:
                    log_line(f"[FOUND] Guild master at: {','.join(path)}", self.session_file)
                    r = self.send("list skills", wait_time=3)
                    write_file(f"warrior_skills_list_{int(time.time())}.txt", r)
                    r = self.send("advance guild level", wait_time=3)
                    write_file(f"warrior_advance_{int(time.time())}.txt", r)
                    r = self.send("train skills", wait_time=3)
                    write_file(f"warrior_train_{int(time.time())}.txt", r)
                    return True
            # Go back
            for d in reversed(path):
                self.send(self._opposite(d), wait_time=1)
        
        return False
    
    def advance_at_judge(self):
        """Use judge menu to advance level."""
        log_line("[PHASE] Advancing at Judge", self.session_file)
        self.send("warp", wait_time=2)
        r = self.send("e", wait_time=2)
        
        if "achman" in r.lower() or "judge" in r.lower():
            r = self.send("talk to judge", wait_time=3)
            write_file(f"judge_menu_{int(time.time())}.txt", r)
            
            if "[abcdeq]" in r:
                # c = advance level, d = advance picking stat, q = quit
                r = self.menu_cmd("c")
                write_file(f"judge_advance_{int(time.time())}.txt", r)
                time.sleep(1)
                # Check if still in menu
                if "[abcdeq]" in r:
                    self.menu_cmd("q")
                return True
        
        return False
    
    def run(self):
        os.makedirs(ARCHIVE_DIR, exist_ok=True)
        self.connect()
        self.login()
        
        # Initial snapshot
        self.save_snapshot("initial")
        
        # Try to find gnosis (optional, don't spend too long)
        self.find_gnosis()
        
        # Find earwigs
        found, path = self.explore_to_earwigs()
        
        if not found:
            log_line("[ERROR] Could not find earwigs anywhere", self.session_file)
            # Last resort: explore randomly and kill anything
            self.kill_anything()
        else:
            # Set combat silence
            self.send("combat silent on", wait_time=2)
            
            # Kill earwigs in a loop until level 5
            kills = 0
            while True:
                # Check level
                r = self.send("score", wait_time=2)
                write_file(f"score_combat_{kills}_{int(time.time())}.txt", r)
                
                level = self._parse_level(r)
                log_line(f"[STATUS] Current level: {level}, kills: {kills}", self.session_file)
                
                if level >= 5:
                    log_line("[GOAL] Level 5 reached!", self.session_file)
                    break
                
                # Try to kill earwig
                r = self.send("kill earwig", wait_time=10)
                write_file(f"combat_{kills}_{int(time.time())}.txt", r)
                kills += 1
                
                # Loot and eat
                self.send("get all corpse", wait_time=1)
                self.send("eat corpse", wait_time=1)
                
                # Rest
                self.send("rest", wait_time=3)
                
                # Every 5 kills, try to level up
                if kills % 5 == 0:
                    self.advance_at_judge()
                    self.find_warrior_guild()
                    # Return to earwigs
                    if "," in path:
                        p1, p2 = path.split(",")
                        self.send("warp", wait_time=1)
                        self.send(p1, wait_time=1)
                        self.send(p2, wait_time=1)
                    else:
                        self.send("warp", wait_time=1)
                        self.send(path, wait_time=1)
        
        # Final level up attempts
        self.advance_at_judge()
        self.find_warrior_guild()
        
        # Final snapshots
        self.save_snapshot("level5_final")
        
        # Get inventory
        r = self.send("inventory", wait_time=2)
        write_file(f"inventory_level5_{int(time.time())}.txt", r)
        
        # Quit
        self.send("quit", wait_time=2)
        log_line(f"[END] {datetime.now().isoformat()}, cmds={self.cmd_count}", self.session_file)
        
    def _parse_level(self, score_text):
        """Parse level from score output."""
        for line in score_text.split("\n"):
            if "Level" in line and ":" in line:
                parts = line.split(":")
                if len(parts) >= 2:
                    try:
                        return int(parts[1].strip().split()[0])
                    except:
                        pass
        return 1
    
    def kill_anything(self):
        """Last resort: wander and kill any monster."""
        log_line("[PHASE] Kill anything mode", self.session_file)
        dirs = ["n","e","s","w","ne","se","sw","nw"]
        kills = 0
        while kills < 20:
            for d in dirs:
                r = self.send(d, wait_time=2)
                # Look for monsters
                if any(m in r.lower() for m in ["rat","bug","worm","insect","spider","snake","lizard","goblin","orc"]):
                    r = self.send("kill monster", wait_time=10)
                    write_file(f"combat_any_{kills}_{int(time.time())}.txt", r)
                    kills += 1
                    self.send("get all corpse", wait_time=1)
                    self.send("eat corpse", wait_time=1)
                    self.send("rest", wait_time=3)
                    
                    # Check level
                    r = self.send("score", wait_time=2)
                    if self._parse_level(r) >= 5:
                        return
                
                self.send(self._opposite(d), wait_time=1)

if __name__ == "__main__":
    bot = MUDBot()
    try:
        bot.run()
        print("Done. Check archive directory.")
    except Exception as e:
        import traceback
        print(f"Error: {e}")
        if bot.session_file:
            log_line(f"[FATAL] {e}\n{traceback.format_exc()}", bot.session_file)
        raise
