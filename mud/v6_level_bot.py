#!/usr/bin/env python3
"""
MUD Leveling Bot v6 - Emalz to Level 5
Robust reconnection, focused on judge level-up + monster grinding.
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
            "gnoll", "thug", "bandit", "rogue", "scout", "guard", "soldier",
            "drone", "minion", "hound", "pup", "cub", "feral", "beast", "critter"]

EXPLORATION_DIRS = ["n", "e", "s", "w", "ne", "nw", "se", "sw", "u", "d"]

def strip_ansi(text):
    return ANSI_RE.sub('', text)

def log(text, sf):
    with open(sf, "a", encoding="utf-8", errors="replace") as f:
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
        self.sf = None
        self.cmd = 0
        self.connected = False

    def connect(self):
        for attempt in range(3):
            try:
                self.tn = telnetlib.Telnet(HOST, PORT, timeout=30)
                self.connected = True
                break
            except Exception as e:
                print(f"Connect attempt {attempt+1} failed: {e}")
                time.sleep(5)
        if not self.connected:
            raise Exception("Failed to connect after 3 attempts")
        epoch = str(int(time.time()))
        self.sf = os.path.join(ARCHIVE_DIR, f"SESSION_V6_{epoch}.txt")
        log(f"[START] {datetime.now().isoformat()}", self.sf)

    def read(self, timeout=3):
        end = time.time() + timeout
        buf = ""
        while time.time() < end:
            try:
                d = self.tn.read_very_eager()
                if d:
                    buf += d.decode('ascii', errors='replace')
            except Exception as e:
                log(f"[READ_ERR] {e}", self.sf)
                break
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
        self.cmd += 1
        for attempt in range(2):
            try:
                self.tn.write((cmd + "\r\n").encode('ascii'))
                break
            except Exception as e:
                log(f"[SEND_ERR] {e}, reconnecting...", self.sf)
                self.connect()
                self.login()
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
        # Wait extra for "taken over" messages to settle
        time.sleep(8)
        self.read(timeout=3)
        log("[LOGIN] Done", self.sf)

    def judge_level_up(self):
        """Go to judge and advance a level. Returns new level."""
        log("[JUDGE] Leveling up", self.sf)
        self.send("warp", wait=2)
        r = self.send("e", wait=2)
        if "achman" not in r.lower() and "judge" not in r.lower():
            log("[JUDGE] Judge not found!", self.sf)
            self.send("warp", wait=2)
            return 1

        r = self.send("talk to judge", wait=3)
        save(f"judge_menu_{int(time.time())}.txt", r)

        if "[abcdeq]" not in r:
            log("[JUDGE] No menu!", self.sf)
            self.send("warp", wait=2)
            return 1

        # Use 'd' to advance with stat pick
        r = self.send("d", wait=3)
        save(f"judge_pick_{int(time.time())}.txt", r)

        if "[abcdefghijmq]" not in r:
            log("[JUDGE] No stat menu!", self.sf)
            self.send("q", wait=2)
            self.send("warp", wait=2)
            return 1

        # Pick strength
        r = self.send("a", wait=4)
        save(f"judge_stat_{int(time.time())}.txt", r)

        # Quit menu
        r = self.send("q", wait=2)
        save(f"judge_quit_{int(time.time())}.txt", r)

        self.send("warp", wait=2)

        # Check level
        r = self.send("score", wait=2)
        save(f"score_after_level_{int(time.time())}.txt", r)
        return self.parse_level(r)

    def warrior_guild(self):
        """Visit warrior guild and try commands."""
        log("[WARRIOR] Visiting guild", self.sf)
        self.send("warp", wait=2)
        self.send("sw", wait=2)
        r = self.send("warrior", wait=3)
        save(f"warrior_enter_{int(time.time())}.txt", r)

        for cmd in ["advance", "level", "train", "train skills", "list skills", "skills"]:
            r = self.send(cmd, wait=3)
            save(f"warrior_{cmd.replace(' ','_')}_{int(time.time())}.txt", r)
            if "learn" in r.lower() or "improve" in r.lower() or "trained" in r.lower():
                log(f"[WARRIOR] Success with: {cmd}", self.sf)

        self.send("warp", wait=2)

    def find_monsters(self, room_text):
        """Look for monsters in room text."""
        low = room_text.lower()
        for monster in MONSTERS:
            if monster in low:
                return monster
        return None

    def do_kill(self, target):
        log(f"[KILL] Attacking {target}", self.sf)
        self.send("combat silent on", wait=1)
        r = self.send(f"kill {target}", wait=15)
        save(f"combat_{target}_{int(time.time())}.txt", r)

        # Wait for combat to finish
        if any(x in r.lower() for x in ["slain", "dead", "corpse", "killed", "died"]):
            return True

        if any(x in r.lower() for x in ["fighting", "attack", "begin", "engaged", "combat", "hit", "damage"]):
            log("[KILL] Combat in progress...", self.sf)
            for _ in range(30):
                time.sleep(2)
                r2 = self.read(timeout=2)
                if any(x in r2.lower() for x in ["slain", "dead", "corpse", "killed", "died", "fled", "escaped", "defeated"]):
                    return True

        return False

    def post_kill(self):
        log("[KILL] Post-kill", self.sf)
        self.send("get all corpse", wait=1)
        self.send("eat corpse", wait=1)
        self.send("rest", wait=5)
        r = self.send("score", wait=2)
        return self.parse_level(r)

    def explore(self):
        """Explore outward from guild, return True if level 5 reached."""
        log("[EXPLORE] Starting", self.sf)
        self.send("warp", wait=2)

        # Try each primary direction from guild
        primary_dirs = ["n", "e", "w", "ne", "nw", "se", "sw", "s"]
        opp = {"n":"s","s":"n","e":"w","w":"e","ne":"sw","sw":"ne","se":"nw","nw":"se","u":"d","d":"u"}

        for primary in primary_dirs:
            log(f"[EXPLORE] Primary direction: {primary}", self.sf)
            self.send("warp", wait=2)
            r = self.send(primary, wait=2)
            room = self.parse_room(r)
            if not room or "adventurer" in room.lower():
                continue

            visited = {room}
            path = [primary]

            for step in range(25):
                monster = self.find_monsters(r)
                if monster:
                    log(f"[EXPLORE] Found {monster} at step {step}", self.sf)
                    if self.do_kill(monster):
                        lvl = self.post_kill()
                        if lvl >= 5:
                            return True
                    r = self.read(timeout=2)
                    continue

                # Try generic kill
                for target in ["monster", "creature", "animal"]:
                    r2 = self.send(f"kill {target}", wait=8)
                    if any(x in r2.lower() for x in ["slain", "dead", "corpse", "killed", "died", "fighting", "attack", "begin", "engaged"]):
                        lvl = self.post_kill()
                        if lvl >= 5:
                            return True
                        r = self.read(timeout=2)
                        break
                else:
                    # No kill happened, try to move forward
                    exits = self.get_exits(r)
                    room = self.parse_room(r)
                    if room in visited:
                        log(f"[EXPLORE] Loop at {room}", self.sf)
                        break
                    if room:
                        visited.add(room)

                    # Prefer continuing in same general direction
                    moved = False
                    for d in [primary] + [x for x in EXPLORATION_DIRS if x != opp.get(path[-1], "")]:
                        if d in exits:
                            r = self.send(d, wait=2)
                            path.append(d)
                            moved = True
                            break
                    if not moved:
                        log("[EXPLORE] No forward exit", self.sf)
                        break

            self.send("warp", wait=2)

        return False

    def run(self):
        os.makedirs(ARCHIVE_DIR, exist_ok=True)
        self.connect()
        self.login()

        # Initial state
        r = self.send("score", wait=2)
        save(f"score_v6_start_{int(time.time())}.txt", r)
        r = self.send("skills", wait=2)
        save(f"skills_v6_start_{int(time.time())}.txt", r)

        lvl = self.parse_level(r)
        log(f"[START] Level {lvl}", self.sf)

        # Main loop
        for cycle in range(80):
            log(f"[CYCLE] {cycle+1}", self.sf)

            # Check level
            r = self.send("score", wait=2)
            lvl = self.parse_level(r)
            log(f"[STATUS] Level {lvl}", self.sf)

            if lvl >= 5:
                log("[GOAL] LEVEL 5!", self.sf)
                break

            # Try to level up at judge
            new_lvl = self.judge_level_up()
            if new_lvl > lvl:
                log(f"[LEVEL] Leveled to {new_lvl}!", self.sf)
                lvl = new_lvl
                self.warrior_guild()

            if lvl >= 5:
                break

            # Explore and kill
            if self.explore():
                break

        # Final
        r = self.send("score", wait=2)
        save(f"score_v6_final_{int(time.time())}.txt", r)
        r = self.send("skills", wait=2)
        save(f"skills_v6_final_{int(time.time())}.txt", r)
        r = self.send("inventory", wait=2)
        save(f"inventory_v6_final_{int(time.time())}.txt", r)

        self.send("quit", wait=2)
        log(f"[END] {datetime.now().isoformat()}", self.sf)
        print(f"Finished at level {lvl}")

if __name__ == "__main__":
    bot = Bot()
    try:
        bot.run()
    except Exception as e:
        import traceback
        print(f"Error: {e}")
        if bot.sf:
            log(f"[FATAL] {e}\n{traceback.format_exc()}", bot.sf)
