#!/usr/bin/env python3
"""
MUD Telnet Client for Islands of MUD - emalz character exploration
Logs into islandsofmyth.org:3000, archives all output, performs game actions.
"""
import telnetlib
import time
import os
import sys
import re
from datetime import datetime
from threading import Thread, Event
from queue import Queue, Empty

# Configuration
HOST = "islandsofmyth.org"
PORT = 3000
USERNAME = "emalz"
PASSWORD = "creative"
RACE = "kobold"
ARCHIVE_DIR = "/root/.openclaw/workspace/mud/emalz_archive/"
TIMEOUT = 3600  # 60 minutes max

# State tracking
command_count = 0
last_save_command_count = 0
session_log = None
combat_active = False
current_room = ""

# ANSI color codes to strip
ANSI_RE = re.compile(r'\x1b\[[0-9;]*m')

def get_timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def get_epoch():
    return str(int(time.time()))

def strip_ansi(text):
    """Remove ANSI escape sequences"""
    return ANSI_RE.sub('', text)

def log_line(text, raw=False):
    """Append a line to the session log."""
    if session_log is None:
        return
    if not raw:
        text = strip_ansi(text)
    with open(session_log, "a", encoding="utf-8", errors="replace") as f:
        f.write(text + "\n")
        f.flush()

def save_snapshot(label="state"):
    """Save current game state: score, skills, spells, and a screen capture."""
    ts = get_timestamp()
    epoch = get_epoch()
    
    # Capture current screen
    screen_path = os.path.join(ARCHIVE_DIR, f"screen_{label}_{ts}_{epoch}.txt")
    
    # We queue commands and the main loop handles responses
    # This function just schedules saves via command queue
    return ts, epoch

def write_output(path, text):
    """Write text to a file in archive directory."""
    filepath = os.path.join(ARCHIVE_DIR, path)
    with open(filepath, "w", encoding="utf-8", errors="replace") as f:
        f.write(text)
        f.flush()
    log_line(f"[ARCHIVE] Saved: {filepath}")

class MUDClient:
    def __init__(self):
        self.tn = None
        self.output_buffer = ""
        self.command_queue = Queue()
        self.running = False
        self.login_state = "connecting"
        self.character_created = False
        self.logged_in = False
        self.in_combat = False
        self.pending_save = False
        self.pending_commands = []
        self.current_command_idx = 0
        self.waiting_for_prompt = True
        self.last_output_time = time.time()
        self.collecting_output = False
        self.collected_output = ""
        self.collect_target = ""
        
    def connect(self):
        log_line(f"[SYSTEM] Connecting to {HOST}:{PORT}...")
        try:
            self.tn = telnetlib.Telnet(HOST, PORT, timeout=30)
            log_line(f"[SYSTEM] Connected to {HOST}:{PORT}")
            return True
        except Exception as e:
            log_line(f"[ERROR] Connection failed: {e}")
            return False
    
    def read_until_prompt(self, timeout=10):
        """Read until we see a prompt pattern."""
        end_time = time.time() + timeout
        buffer = ""
        while time.time() < end_time:
            try:
                data = self.tn.read_very_eager()
                if data:
                    text = data.decode('ascii', errors='replace')
                    buffer += text
                    log_line(text.rstrip(), raw=True)
                    self.last_output_time = time.time()
                    # Check for common MUD prompts
                    if any(p in buffer for p in ['>', ']', ')', ':', 'Password', 'name', 'choice', 'press']):
                        if len(buffer.strip()) > 0:
                            time.sleep(0.3)  # Let more data arrive
                            extra = self.tn.read_very_eager().decode('ascii', errors='replace')
                            if extra:
                                buffer += extra
                                log_line(extra.rstrip(), raw=True)
                            return buffer
            except Exception:
                pass
            time.sleep(0.1)
        return buffer
    
    def send_command(self, cmd, wait=True, wait_time=3):
        """Send a command and optionally wait for response."""
        global command_count
        cmd_clean = cmd.strip()
        log_line(f"[COMMAND] >>> {cmd_clean}")
        self.tn.write((cmd + "\r\n").encode('ascii'))
        command_count += 1
        
        if wait:
            time.sleep(0.5)
            response = self.read_until_prompt(timeout=wait_time)
            return response
        return ""
    
    def collect_command_output(self, cmd, label, wait_time=3):
        """Send command, collect output, save to file."""
        log_line(f"[COLLECT] Executing: {cmd} -> {label}")
        self.send_command(cmd, wait=False)
        time.sleep(0.5)
        response = self.read_until_prompt(timeout=wait_time)
        
        # Save the output
        ts = get_timestamp()
        epoch = get_epoch()
        filename = f"{label}_{ts}_{epoch}.txt"
        write_output(filename, response)
        return response
    
    def run_login_sequence(self):
        """Handle login or character creation."""
        log_line("[SYSTEM] Starting login sequence...")
        
        # Wait for initial banner
        time.sleep(3)
        banner = self.read_until_prompt(timeout=10)
        log_line("[SYSTEM] Initial banner received")
        
        # Check if we need to press enter or make a choice
        if "press" in banner.lower() or "enter" in banner.lower():
            self.send_command("", wait=False)
            time.sleep(1)
            banner += self.read_until_prompt(timeout=5)
        
        # Check for login prompt - try to login with emalz
        # Most MUDs ask for name at a prompt
        log_line("[SYSTEM] Attempting to login as emalz...")
        response = self.send_command(USERNAME, wait=True, wait_time=5)
        
        # Check if character exists
        if any(k in response.lower() for k in ['new player', 'new character', 'create', 'does not exist', 'not found', 'new user']):
            log_line("[SYSTEM] Character does not exist. Creating new character...")
            self.character_created = True
            self._create_character()
        elif "password" in response.lower() or "pass" in response.lower():
            log_line("[SYSTEM] Password prompt detected. Sending password...")
            response = self.send_command(PASSWORD, wait=True, wait_time=5)
            log_line("[SYSTEM] Login response received")
            self.logged_in = True
        else:
            # Try sending password anyway
            log_line("[SYSTEM] Sending password...")
            response = self.send_command(PASSWORD, wait=True, wait_time=5)
            self.logged_in = True
        
        # Wait for character to fully load
        time.sleep(3)
        welcome = self.read_until_prompt(timeout=10)
        log_line("[SYSTEM] Login sequence complete")
        return True
    
    def _create_character(self):
        """Create a new character as Kobold."""
        log_line("[SYSTEM] Character creation flow...")
        
        # Usually MUDs will ask for password for new character
        response = self.send_command(PASSWORD, wait=True, wait_time=5)
        
        # Confirm password
        if "again" in response.lower() or "confirm" in response.lower() or "re-enter" in response.lower():
            response = self.send_command(PASSWORD, wait=True, wait_time=5)
        
        # Wait for race/class selection
        time.sleep(3)
        response = self.read_until_prompt(timeout=10)
        
        # Look for race prompt
        log_line("[SYSTEM] Looking for race selection...")
        # Try selecting Kobold
        if "race" in response.lower() or "select" in response.lower() or "choice" in response.lower():
            # Try kobold as a number or name
            self.send_command(RACE, wait=False)
            time.sleep(2)
            response = self.read_until_prompt(timeout=5)
        
        # Handle any additional prompts (class, alignment, etc.)
        for _ in range(10):  # Max 10 prompts
            time.sleep(2)
            response = self.read_until_prompt(timeout=5)
            if not response.strip():
                break
            
            low = response.lower()
            if "class" in low or "guild" in low:
                self.send_command("warrior", wait=False)
            elif "alignment" in low or "align" in low:
                self.send_command("good", wait=False)  
            elif "sex" in low or "gender" in low:
                self.send_command("male", wait=False)
            elif "roll" in low and "stats" in low:
                self.send_command("accept", wait=False)
            elif "accept" in low:
                self.send_command("accept", wait=False)
            elif "continue" in low:
                self.send_command("", wait=False)
            elif ">" in response or "]" in response:
                break  # At prompt, done
        
        self.logged_in = True
        log_line("[SYSTEM] Character creation complete")
    
    def initial_snapshot(self):
        """Save initial character state after login."""
        log_line("[SYSTEM] Taking initial snapshots...")
        
        self.collect_command_output("score", "score", wait_time=3)
        time.sleep(1)
        self.collect_command_output("skills", "skills", wait_time=3)
        time.sleep(1)
        self.collect_command_output("spells", "spells", wait_time=3)
        time.sleep(1)
    
    def join_warrior_guild(self):
        """Join warrior guild: warp, s, warrior, join guild"""
        log_line("[SYSTEM] Joining Warrior guild...")
        
        self.collect_command_output("warp", "warp_to_warrior", wait_time=3)
        time.sleep(1)
        self.collect_command_output("s", "go_south", wait_time=3)
        time.sleep(1)
        self.collect_command_output("warrior", "enter_warrior_guild", wait_time=3)
        time.sleep(1)
        self.collect_command_output("join guild", "join_warrior", wait_time=3)
        time.sleep(1)
    
    def get_assignment(self):
        """Get assignment from gnosis: warp, se, e, talk to gnosis, get assignment"""
        log_line("[SYSTEM] Getting assignment from Gnosis...")
        
        self.collect_command_output("warp", "warp_to_gnosis", wait_time=3)
        time.sleep(1)
        self.collect_command_output("se", "go_southeast", wait_time=3)
        time.sleep(1)
        self.collect_command_output("e", "go_east", wait_time=3)
        time.sleep(1)
        self.collect_command_output("talk to gnosis", "talk_gnosis", wait_time=5)
        time.sleep(1)
        
        # Try getting assignment
        response = self.collect_command_output("get assignment", "get_assignment", wait_time=5)
        time.sleep(1)
        return response
    
    def kill_earwigs(self):
        """Kill earwigs in Yensidland with combat data collection."""
        log_line("[SYSTEM] Starting earwig combat in Yensidland...")
        
        # Go to Yensidland
        self.collect_command_output("warp", "warp_to_yensid", wait_time=3)
        time.sleep(1)
        # Try various directions to find earwigs
        directions = ["n", "ne", "e", "se", "s", "sw", "w", "nw", "u", "d"]
        found_earwigs = False
        
        for direction in directions[:3]:  # Try first few directions
            response = self.collect_command_output(direction, f"yensid_{direction}", wait_time=3)
            if "earwig" in response.lower():
                found_earwigs = True
                log_line("[SYSTEM] Found earwigs!")
                break
            time.sleep(1)
        
        if not found_earwigs:
            # Try looking around
            self.collect_command_output("look", "look_yensid", wait_time=3)
            time.sleep(1)
        
        # Set combat silence for detailed stats
        self.send_command("combat silence", wait=False)
        time.sleep(1)
        
        # Try killing earwigs (up to 5 attempts)
        for i in range(5):
            log_line(f"[COMBAT] Kill attempt {i+1}...")
            
            # Save pre-combat state
            self.collect_command_output("score", f"score_pre_kill_{i}", wait_time=3)
            time.sleep(0.5)
            
            # Try to kill
            response = self.send_command("kill earwig", wait=True, wait_time=10)
            time.sleep(2)
            
            # Read extended combat output
            combat_output = ""
            for _ in range(20):  # Read for up to 10 seconds
                chunk = self.read_until_prompt(timeout=0.5)
                if chunk:
                    combat_output += chunk
                    # Check if combat ended
                    if any(x in chunk.lower() for x in ['you have slain', 'dead', 'corpse', 'killed', 'died', 'fled']):
                        break
                time.sleep(0.5)
            
            # Save combat log
            write_output(f"combat_kill_{i}_{get_timestamp()}.txt", combat_output)
            
            # Loot and eat
            self.send_command("get all corpse", wait=False)
            time.sleep(1)
            self.send_command("eat corpse", wait=False)
            time.sleep(1)
            
            # Save post-combat state
            self.collect_command_output("score", f"score_post_kill_{i}", wait_time=3)
            time.sleep(1)
            self.collect_command_output("skills", f"skills_post_kill_{i}", wait_time=3)
            time.sleep(1)
            
            # Check if we need to heal or rest
            if i < 4:  # Don't rest on last iteration
                self.send_command("rest", wait=False)
                time.sleep(3)
    
    def ocean_route(self):
        """Ocean route: shack, ask ahab for story, wear ring, out, ocean, kill guppys"""
        log_line("[SYSTEM] Starting ocean route...")
        
        self.collect_command_output("warp", "warp_ocean", wait_time=3)
        time.sleep(1)
        self.collect_command_output("shack", "enter_shack", wait_time=3)
        time.sleep(1)
        self.collect_command_output("ask ahab for story", "ahab_story", wait_time=5)
        time.sleep(1)
        self.collect_command_output("wear ring", "wear_ring", wait_time=3)
        time.sleep(1)
        self.collect_command_output("out", "leave_shack", wait_time=3)
        time.sleep(1)
        self.collect_command_output("ocean", "enter_ocean", wait_time=3)
        time.sleep(1)
        
        # Set combat silence
        self.send_command("combat silence", wait=False)
        time.sleep(1)
        
        # Kill guppys
        for i in range(3):
            log_line(f"[COMBAT] Ocean kill attempt {i+1}...")
            
            self.collect_command_output("score", f"score_pre_ocean_{i}", wait_time=3)
            time.sleep(0.5)
            
            response = self.send_command("kill guppy", wait=True, wait_time=10)
            time.sleep(2)
            
            combat_output = ""
            for _ in range(20):
                chunk = self.read_until_prompt(timeout=0.5)
                if chunk:
                    combat_output += chunk
                    if any(x in chunk.lower() for x in ['you have slain', 'dead', 'corpse', 'killed', 'died']):
                        break
                time.sleep(0.5)
            
            write_output(f"combat_ocean_{i}_{get_timestamp()}.txt", combat_output)
            
            self.send_command("get all corpse", wait=False)
            time.sleep(1)
            self.send_command("eat corpse", wait=False)
            time.sleep(1)
            
            self.collect_command_output("score", f"score_post_ocean_{i}", wait_time=3)
            time.sleep(1)
            self.send_command("rest", wait=False)
            time.sleep(3)
    
    def level_up(self):
        """Level up routine: warp, e, talk to judge, advance level, advance guild level, train skills"""
        log_line("[SYSTEM] Attempting level up...")
        
        self.collect_command_output("warp", "warp_judge", wait_time=3)
        time.sleep(1)
        self.collect_command_output("e", "go_east_judge", wait_time=3)
        time.sleep(1)
        self.collect_command_output("talk to judge", "talk_judge", wait_time=5)
        time.sleep(1)
        self.collect_command_output("advance level", "advance_level", wait_time=5)
        time.sleep(1)
        self.collect_command_output("advance guild level", "advance_guild", wait_time=5)
        time.sleep(1)
        self.collect_command_output("train skills", "train_skills", wait_time=5)
        time.sleep(1)
        
        # Save post-level state
        self.collect_command_output("score", "score_post_level", wait_time=3)
        time.sleep(1)
        self.collect_command_output("skills", "skills_post_level", wait_time=3)
        time.sleep(1)
    
    def check_for_level_up(self, score_output):
        """Check if character leveled up based on score output."""
        # Look for level indicators or XP thresholds
        low = score_output.lower()
        if any(x in low for x in ['level up', 'advance', 'experience', 'xp']):
            return True
        return False
    
    def run(self):
        """Main execution flow."""
        global session_log
        
        # Create session log file
        epoch = get_epoch()
        session_log = os.path.join(ARCHIVE_DIR, f"SESSION_{epoch}.txt")
        
        log_line(f"[SYSTEM] MUD Session Started: {datetime.now().isoformat()}")
        log_line(f"[SYSTEM] Target: {HOST}:{PORT}")
        log_line(f"[SYSTEM] Character: {USERNAME}")
        log_line(f"[SYSTEM] Archive directory: {ARCHIVE_DIR}")
        
        # Connect
        if not self.connect():
            log_line("[SYSTEM] FAILED: Could not connect to MUD")
            return False
        
        # Login
        if not self.run_login_sequence():
            log_line("[SYSTEM] FAILED: Login sequence failed")
            return False
        
        # Take initial snapshots
        self.initial_snapshot()
        
        # Join Warrior guild
        self.join_warrior_guild()
        
        # Get assignment from Gnosis
        self.get_assignment()
        
        # Combat: Kill earwigs
        self.kill_earwigs()
        
        # Ocean route
        self.ocean_route()
        
        # Try leveling up
        self.level_up()
        
        # Final snapshots
        log_line("[SYSTEM] Taking final snapshots...")
        self.collect_command_output("score", "score_final", wait_time=3)
        time.sleep(1)
        self.collect_command_output("skills", "skills_final", wait_time=3)
        time.sleep(1)
        self.collect_command_output("spells", "spells_final", wait_time=3)
        time.sleep(1)
        self.collect_command_output("inventory", "inventory_final", wait_time=3)
        time.sleep(1)
        
        # Disconnect
        self.send_command("quit", wait=False)
        time.sleep(2)
        
        try:
            self.tn.close()
        except:
            pass
        
        log_line(f"[SYSTEM] MUD Session Complete: {datetime.now().isoformat()}")
        log_line(f"[SYSTEM] Total commands sent: {command_count}")
        log_line(f"[SYSTEM] Session log: {session_log}")
        
        return True

if __name__ == "__main__":
    # Ensure archive directory exists
    os.makedirs(ARCHIVE_DIR, exist_ok=True)
    
    client = MUDClient()
    try:
        success = client.run()
        if success:
            print(f"Session complete. Archive: {ARCHIVE_DIR}")
            sys.exit(0)
        else:
            print("Session failed.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("Interrupted by user.")
        sys.exit(130)
    except Exception as e:
        log_line(f"[ERROR] Fatal error: {e}")
        import traceback
        log_line(traceback.format_exc())
        print(f"Fatal error: {e}")
        sys.exit(1)
