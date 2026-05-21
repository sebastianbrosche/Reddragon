#!/usr/bin/env python3
"""
IOM Autopilot Engine v1 — Non-Combat Explorer
Reads session log, makes decisions, queues commands to relay.

Rules (from Sebastian):
- NO combat. Never kill anything.
- Wimpy 90-95 set at start
- If stuck: gp → ep (guild portal → enter portal)
- Can take ferries between islands
- Start with Gossamer island
- Avoid aggro mobs: Speedron ox (SE), swamp in Gossamer, crystal dragons (SW)
- Document everything: room descriptions, exits, items, NPCs
- If in combat and wimpy doesn't flee, run to nearest exit
"""

import re
import time
import random
from pathlib import Path
from datetime import datetime
import json

SESSION_LOG = Path("/tmp/iom-session.log")
QUEUE_FILE = Path("/tmp/iom-autopilot-queue.txt")
STATE_FILE = Path("/tmp/iom-autopilot-state.json")
ROOMS_FILE = Path("/tmp/iom-rooms-discovered.jsonl")

class IOMAutopilot:
    def __init__(self):
        self.known_rooms = {}  # name -> {exits, description, items, npcs}
        self.current_room = None
        self.last_position = 0
        self.buffer = ""
        self.state = {
            "initialized": False,
            "on_ferry": False,
            "in_combat": False,
            "wimpy_set": False,
            "last_cmd": None,
            "pending_look": False,
            "exploration_queue": [],  # list of directions to try
            "visited_stack": [],  # breadcrumb trail for backtracking
            "current_area": "ilium",  # ilium, gossamer, etc.
            "ferry_targets": ["gossamer"],
            "rooms_found": 0,
            "stuck_counter": 0,
        }
        self.load_state()
        
    def load_state(self):
        if STATE_FILE.exists():
            try:
                with open(STATE_FILE) as f:
                    saved = json.load(f)
                    self.state.update(saved)
            except:
                pass
    
    def save_state(self):
        with open(STATE_FILE, 'w') as f:
            json.dump(self.state, f, indent=2)
    
    def queue_cmd(self, cmd, delay=0):
        """Add command to relay queue"""
        # Read existing queue
        existing = []
        if QUEUE_FILE.exists():
            with open(QUEUE_FILE) as f:
                existing = [l.strip() for l in f if l.strip()]
        
        existing.append(cmd)
        with open(QUEUE_FILE, 'w') as f:
            for c in existing:
                f.write(c + '\n')
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] QUEUED: {cmd}")
    
    def read_new_log_output(self):
        """Read new lines from session log"""
        if not SESSION_LOG.exists():
            return ""
        
        with open(SESSION_LOG, 'r', encoding='utf-8', errors='replace') as f:
            f.seek(self.last_position)
            new_data = f.read()
            self.last_position = f.tell()
        
        return new_data
    
    def parse_room(self, text):
        """Extract room information from MUD output"""
        room_info = {
            "name": None,
            "description": [],
            "exits": [],
            "items": [],
            "npcs": [],
            "players": [],
        }
        
        lines = text.split('\n')
        in_description = False
        
        for i, line in enumerate(lines):
            line_stripped = line.strip()
            
            # Room name detection — often in brackets or at top
            # Patterns like "[Room Name]" or just a short bold line
            if not room_info["name"] and len(line_stripped) > 0 and len(line_stripped) < 60:
                if not line_stripped.startswith('|') and not line_stripped.startswith('-'):
                    # Check if next lines have exits or description
                    room_info["name"] = line_stripped
                    in_description = True
                    continue
            
            # Exit detection
            if 'obvious exits:' in line_stripped.lower() or 'exits:' in line_stripped.lower():
                in_description = False
                # Next line should have exits
                if i + 1 < len(lines):
                    exits_line = lines[i + 1].strip().lower()
                    # Parse exits like "north, east, south"
                    exits = [e.strip() for e in re.split(r'[,\s]+', exits_line) if e.strip()]
                    # Filter valid directions
                    valid = {'n', 's', 'e', 'w', 'ne', 'nw', 'se', 'sw', 'u', 'd',
                             'north', 'south', 'east', 'west', 'northeast', 'northwest',
                             'southeast', 'southwest', 'up', 'down', 'in', 'out'}
                    room_info["exits"] = [e for e in exits if e in valid]
                continue
            
            # Item detection
            if line_stripped.startswith('A ') or line_stripped.startswith('The ') or line_stripped.startswith('An '):
                if 'is here' in line_stripped.lower() or 'lies here' in line_stripped.lower():
                    room_info["items"].append(line_stripped)
                    continue
            
            # NPC detection
            if line_stripped and not line_stripped.startswith('A ') and not line_stripped.startswith('The '):
                if any(x in line_stripped.lower() for x in ['stands here', 'is standing', 'sits here', 'rests here']):
                    room_info["npcs"].append(line_stripped)
                    continue
            
            # Player detection
            if line_stripped.startswith('(') and ')' in line_stripped:
                room_info["players"].append(line_stripped)
                continue
            
            # Description lines
            if in_description and line_stripped and len(line_stripped) > 20:
                room_info["description"].append(line_stripped)
        
        return room_info
    
    def detect_danger(self, text):
        """Detect combat or danger situations"""
        danger_signals = [
            'attacks you', 'hit you', 'wounds you', 'misses you',
            'are fighting', 'in combat', 'hp:', 'health:',
            'speedron', 'crystal dragon', 'swamp'
        ]
        text_lower = text.lower()
        for signal in danger_signals:
            if signal in text_lower:
                return True, signal
        return False, None
    
    def detect_stuck(self, text):
        """Detect if we're stuck (can't move that way, etc.)"""
        stuck_signals = [
            'you can\'t go', 'no exit', 'you cannot', 'is closed',
            'you bump', 'you are stunned', 'you are blinded'
        ]
        text_lower = text.lower()
        for signal in stuck_signals:
            if signal in text_lower:
                return True
        return False
    
    def detect_ferry(self, text):
        """Detect ferry or boat opportunities"""
        ferry_signals = [
            'ferry', 'boat', 'dock', 'harbor', 'pier', 'captain',
            'sail', 'voyage', 'ship', 'board'
        ]
        text_lower = text.lower()
        for signal in ferry_signals:
            if signal in text_lower:
                return True
        return False
    
    def choose_direction(self, exits):
        """Choose which direction to explore next"""
        if not exits:
            return None
        
        # Prefer unvisited directions
        unvisited = [e for e in exits if e not in self.state["visited_stack"]]
        if unvisited:
            return random.choice(unvisited)
        
        # Backtrack using breadcrumb
        if self.state["visited_stack"]:
            return self.state["visited_stack"].pop()
        
        return random.choice(exits)
    
    def run_tick(self):
        """Main decision loop — called repeatedly"""
        new_output = self.read_new_log_output()
        if not new_output:
            return
        
        self.buffer += new_output
        
        # Check for danger
        danger, danger_type = self.detect_danger(self.buffer)
        if danger:
            print(f"DANGER DETECTED: {danger_type}")
            self.state["in_combat"] = True
            
            # If wimpy doesn't auto-flee, try to run
            if self.state["stuck_counter"] > 2:
                print("Wimpy not working — running!")
                # Try all exits
                room = self.parse_room(self.buffer)
                if room["exits"]:
                    self.queue_cmd(random.choice(room["exits"]))
            
            self.state["stuck_counter"] += 1
            self.save_state()
            self.buffer = ""
            return
        
        # Check if stuck
        if self.detect_stuck(self.buffer):
            self.state["stuck_counter"] += 1
            print(f"STUCK ({self.state['stuck_counter']} times)")
            
            if self.state["stuck_counter"] >= 3:
                # Emergency escape
                print("Emergency escape: gp → ep")
                self.queue_cmd("gp")
                time.sleep(2)
                self.queue_cmd("ep")
                self.state["stuck_counter"] = 0
                self.state["visited_stack"] = []
                self.save_state()
                self.buffer = ""
                return
        
        # Parse current room
        room = self.parse_room(self.buffer)
        
        if room["name"] and room["name"] != self.current_room:
            # New room discovered!
            self.current_room = room["name"]
            self.state["rooms_found"] += 1
            self.state["stuck_counter"] = 0
            self.state["in_combat"] = False
            
            print(f"ROOM #{self.state['rooms_found']}: {room['name']}")
            print(f"  Exits: {room['exits']}")
            print(f"  Items: {len(room['items'])}, NPCs: {len(room['npcs'])}")
            
            # Save room to file
            room_record = {
                "timestamp": datetime.now().isoformat(),
                "name": room["name"],
                "description": '\n'.join(room["description"]),
                "exits": room["exits"],
                "items": room["items"],
                "npcs": room["npcs"],
                "area": self.state["current_area"],
            }
            with open(ROOMS_FILE, 'a') as f:
                f.write(json.dumps(room_record) + '\n')
            
            self.known_rooms[room["name"]] = room
            
            # Add to visited stack for backtracking
            # Map reverse directions
            reverse = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e',
                       'ne': 'sw', 'nw': 'se', 'se': 'nw', 'sw': 'ne',
                       'u': 'd', 'd': 'u', 'in': 'out', 'out': 'in'}
            # We don't know which direction we came from yet
        
        # Check for ferry
        if self.detect_ferry(self.buffer) and self.state["ferry_targets"]:
            target = self.state["ferry_targets"][0]
            print(f"FERRY DETECTED — targeting {target}")
            # Common ferry commands
            ferry_cmds = ['list', 'board', 'buy ticket', f'go {target}', 'enter ferry']
            for cmd in ferry_cmds:
                self.queue_cmd(cmd)
                time.sleep(1)
            self.state["on_ferry"] = True
        
        # Make a decision
        if not self.state["initialized"]:
            print("INITIALIZING — setting wimpy 90")
            self.queue_cmd("wimpy 90")
            self.state["initialized"] = True
            self.state["wimpy_set"] = True
            self.save_state()
            self.buffer = ""
            return
        
        # If we have a room with exits, explore
        if room["name"] and room["exits"]:
            direction = self.choose_direction(room["exits"])
            if direction:
                # Add reverse to breadcrumb
                reverse_map = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e',
                              'ne': 'sw', 'nw': 'se', 'se': 'nw', 'sw': 'ne',
                              'u': 'd', 'd': 'u', 'in': 'out', 'out': 'in',
                              'north': 'south', 'south': 'north', 'east': 'west', 'west': 'east'}
                rev = reverse_map.get(direction, 'look')
                self.state["visited_stack"].append(rev)
                
                self.queue_cmd(direction)
                time.sleep(random.uniform(2, 4))
                self.queue_cmd("look")
        else:
            # No room parsed yet, just look
            if not self.state["pending_look"]:
                self.queue_cmd("look")
                self.state["pending_look"] = True
        
        self.save_state()
        self.buffer = ""
    
    def run(self):
        """Main loop"""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] IOM Autopilot started")
        print(f"State: initialized={self.state['initialized']}, rooms={self.state['rooms_found']}")
        
        while True:
            try:
                self.run_tick()
                time.sleep(1)
            except KeyboardInterrupt:
                print("\nAutopilot stopped by user")
                self.save_state()
                break
            except Exception as e:
                print(f"ERROR: {e}")
                time.sleep(2)

if __name__ == '__main__':
    pilot = IOMAutopilot()
    pilot.run()
