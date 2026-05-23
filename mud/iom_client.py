#!/usr/bin/env python3
"""
IOM Hybrid MUD Client - Phase 4.2: Responsive Fullscreen + Font Size + IOM Login

New in Phase 4.2:
- Responsive fullscreen: layout expands to fill display
- Font size buttons (T-, T+) in toolbar
- Prominent FULLSCREEN button
- IOM-style login: connect <name>, create <name>, no password

New in Phase 4:
- Custom title bar with minimize, maximize, fullscreen (F11), close buttons
- Theme system: Classic zMUD green/white, Modern bright
- Autopilot: reads command queue file, human-like delays, safety toggle
- Mudlet-style triggers, aliases, timers (configured in client_config.py)
- Action buttons panel (heal, recall, combat, etc.)
- Health/MP/EP gauges (auto-parsed from MUD output)
- All Phase 3 features preserved: audio, map, split layout, ANSI, SFX

Configure triggers/aliases/timers in client_config.py (auto-created if missing)
"""

import pygame
import threading
import queue
import re
import telnetlib
import time
import random
import os
import sys
import json
from datetime import datetime
from pathlib import Path
from collections import defaultdict, namedtuple

# Try to import websocket-client for WebSocket mode
try:
    import websocket
    WEBSOCKET_AVAILABLE = True
except ImportError:
    WEBSOCKET_AVAILABLE = False

# ── VERSION & AUTO-UPDATE ──
CLIENT_VERSION = "4.3"
UPDATE_URL = "https://b073071f.rcp-housing.pages.dev/iom_client.py"
VERSION_URL = "https://b073071f.rcp-housing.pages.dev/iom_client.version"

# ── CONFIG ──
# Default: Myth of Islands (your Evennia MUD via SSH tunnel)
# Start tunnel first: ssh -L 3001:localhost:3001 root@47.237.80.25
# Or open port 3001 in Alibaba Cloud and use HOST=47.237.80.25
HOST = os.environ.get("MUD_HOST", "localhost")
PORT = int(os.environ.get("MUD_PORT", "3001"))

# Override for Islands of Myth:
# set MUD_HOST=islandsofmyth.org && set MUD_PORT=3000

# ── WEBSOCKET MODE (no SSH tunnel needed) ──
USE_WEBSOCKET = os.environ.get("MUD_WEBSOCKET", "1").lower() in ("1", "true", "yes", "on")
WEBSOCKET_URL = os.environ.get("MUD_WS_URL", "wss://unwrap-sagem-seafood-meeting.trycloudflare.com")
# To switch back to raw telnet: set MUD_WEBSOCKET=0

LOG_FILE = Path("iom_client_session.log")
QUEUE_FILE = Path("/tmp/iom-autopilot-queue.txt")
SCRIPT_DIR = Path(__file__).parent.resolve()
AUDIO_DIR = SCRIPT_DIR / "audio"
MUSIC_DIR = AUDIO_DIR / "music"
SFX_DIR = AUDIO_DIR / "sfx"
CONFIG_FILE = SCRIPT_DIR / "client_config.py"

# Display
SCREEN_WIDTH, SCREEN_HEIGHT = 1024, 768
TITLE_BAR_H = 30
TOOLBAR_H = 28
MAP_TILE_SIZE = 48
FONT_SIZE = 13
LINE_HEIGHT = 15
INPUT_HISTORY = 50

# ── AUTO-UPDATE ──
def check_for_updates():
    """Check remote version and auto-update if newer. Returns True if restart needed."""
    try:
        import urllib.request
        # Read remote version
        req = urllib.request.Request(VERSION_URL, headers={"User-Agent": "MUD-Client"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            remote_version = resp.read().decode("utf-8").strip()

        if not remote_version:
            return False

        def version_tuple(v):
            return tuple(int(x) if x.isdigit() else 0 for x in v.split("."))

        if version_tuple(remote_version) <= version_tuple(VERSION):
            return False

        print(f"[UPDATE] New version {remote_version} available (you have {VERSION})")
        print(f"[UPDATE] Downloading...")

        # Download new script
        new_file = SCRIPT_DIR / "iom_client.py.new"
        req = urllib.request.Request(UPDATE_URL, headers={"User-Agent": "MUD-Client"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = resp.read()

        with open(new_file, "wb") as f:
            f.write(data)

        print(f"[UPDATE] Downloaded {len(data)} bytes")

        # Write updater batch script
        updater_bat = SCRIPT_DIR / "update_client.bat"
        current_file = Path(__file__).resolve()
        with open(updater_bat, "w") as f:
            f.write('@echo off\n')
            f.write('timeout /t 1 /nobreak > nul\n')
            f.write(f'copy /Y "{new_file}" "{current_file}" > nul\n')
            f.write(f'del "{new_file}"\n')
            f.write(f'python "{current_file}"\n')
            f.write(f'del "{updater_bat}"\n')

        print("[UPDATE] Restarting to apply update...")
        import subprocess
        subprocess.Popen([str(updater_bat)], shell=True)
        return True

    except Exception as e:
        print(f"[UPDATE] Check failed: {e}")
        return False

# Run update check before pygame init (console output visible)
if __name__ == "__main__" and check_for_updates():
    sys.exit(0)

# ── THEME SYSTEM ──
THEMES = {
    "classic": {
        "name": "Classic zMUD",
        "bg": (0, 0, 0),
        "fg": (0, 170, 0),          # green text
        "fg_bright": (85, 255, 85),
        "console_bg": (10, 10, 10),
        "input_bg": (12, 12, 12),
        "input_border": (0, 100, 0),
        "title_bar": (20, 20, 20),
        "title_text": (0, 170, 0),
        "toolbar": (25, 25, 25),
        "toolbar_btn": (40, 40, 40),
        "toolbar_btn_hover": (60, 80, 60),
        "toolbar_btn_active": (0, 120, 0),
        "toolbar_text": (0, 200, 0),
        "map_bg": (15, 15, 15),
        "map_unvisited": (10, 10, 10),
        "map_player": (255, 255, 0),
        "map_player_dot": (255, 0, 0),
        "map_exit": (200, 200, 200),
        "gauge_bg": (40, 40, 40),
        "gauge_hp": (200, 50, 50),
        "gauge_mp": (50, 50, 200),
        "gauge_ep": (200, 180, 50),
        "button_bg": (30, 50, 30),
        "button_hover": (50, 90, 50),
        "button_text": (0, 255, 0),
        "status_disconnected": (170, 0, 0),
        "status_connected": (0, 170, 0),
        "divider": (60, 60, 60),
        "prompt": (0, 200, 200),
        "cursor": (0, 255, 0),
        "room_label_bg": (0, 0, 0),
        "room_label_text": (255, 255, 255),
        "scroll_ind": (100, 100, 100),
        "autopilot_on": (0, 200, 0),
        "autopilot_off": (100, 100, 100),
    },
    "modern": {
        "name": "Modern",
        "bg": (20, 20, 25),
        "fg": (200, 200, 200),
        "fg_bright": (255, 255, 255),
        "console_bg": (25, 25, 30),
        "input_bg": (30, 30, 35),
        "input_border": (100, 100, 120),
        "title_bar": (35, 35, 40),
        "title_text": (200, 200, 200),
        "toolbar": (40, 40, 45),
        "toolbar_btn": (60, 60, 70),
        "toolbar_btn_hover": (80, 80, 100),
        "toolbar_btn_active": (100, 150, 200),
        "toolbar_text": (220, 220, 220),
        "map_bg": (30, 30, 35),
        "map_unvisited": (20, 20, 25),
        "map_player": (255, 255, 0),
        "map_player_dot": (255, 80, 80),
        "map_exit": (180, 180, 180),
        "gauge_bg": (50, 50, 55),
        "gauge_hp": (220, 60, 60),
        "gauge_mp": (60, 60, 220),
        "gauge_ep": (220, 200, 60),
        "button_bg": (50, 50, 60),
        "button_hover": (70, 70, 90),
        "button_text": (200, 200, 255),
        "status_disconnected": (220, 60, 60),
        "status_connected": (60, 220, 60),
        "divider": (80, 80, 90),
        "prompt": (100, 200, 255),
        "cursor": (255, 255, 255),
        "room_label_bg": (30, 30, 35),
        "room_label_text": (255, 255, 255),
        "scroll_ind": (120, 120, 120),
        "autopilot_on": (0, 200, 100),
        "autopilot_off": (120, 120, 120),
    },
}

TERRAIN_COLORS = {
    'unknown': (40, 40, 40),
    'plains': (120, 180, 80),
    'forest': (34, 100, 34),
    'sandy beach': (210, 190, 140),
    'water': (50, 100, 180),
    'swamp': (80, 100, 60),
    'badlands': (180, 120, 80),
    'city': (150, 150, 160),
    'dungeon': (80, 60, 80),
    'tunnel': (100, 80, 60),
    'hell': (180, 30, 30),
    'mountain': (120, 120, 120),
    'dock': (100, 80, 60),
    'river': (60, 90, 160),
    'guild': (180, 160, 100),
    'temple': (200, 180, 120),
    'market': (160, 140, 100),
}

TERRAIN_ALIASES = {
    'plains': ['plains','field','meadow','grassland'],
    'forest': ['forest','woods','grove','jungle'],
    'sandy beach': ['beach','sand','shore','coast'],
    'water': ['water','ocean','sea','lake','pond'],
    'swamp': ['swamp','marsh','bog'],
    'badlands': ['badlands','wasteland','desert'],
    'city': ['city','town','village','street','road','square'],
    'dungeon': ['dungeon','cave','cavern','lair'],
    'tunnel': ['tunnel','passage','corridor'],
    'hell': ['hell','underworld','abyss','inferno'],
    'mountain': ['mountain','hill','peak','cliff'],
    'dock': ['dock','pier','wharf','port'],
    'river': ['river','stream','brook'],
    'guild': ['guild','hall','adventurer'],
    'temple': ['temple','shrine','church','cathedral'],
    'market': ['market','bazaar','shop','store'],
}

ANSI_COLORS = {
    0:(0,0,0),1:(170,0,0),2:(0,170,0),3:(170,170,0),
    4:(0,0,170),5:(170,0,170),6:(0,170,170),7:(170,170,170),
}
BRIGHT_COLORS = {
    0:(85,85,85),1:(255,85,85),2:(85,255,85),3:(255,255,85),
    4:(85,85,255),5:(255,85,255),6:(85,255,255),7:(255,255,255),
}

DIR_VECTORS = {
    'n':(0,-1),'s':(0,1),'e':(1,0),'w':(-1,0),
    'ne':(1,-1),'nw':(-1,-1),'se':(1,1),'sw':(-1,1),
}

# ── DEFAULT CONFIG (auto-written to client_config.py) ──
DEFAULT_CONFIG_PY = '''# MUD Client Configuration
# This file is auto-generated. Edit to customize triggers, aliases, timers, and buttons.

# ── TRIGGERS ──
# Format: [("regex_pattern", "command_to_send"), ...]
# When MUD output matches the regex, the command is sent automatically.
TRIGGERS = [
    # (r"You are hungry\\.", "eat bread"),
    # (r"You are thirsty\\.", "drink water"),
    # (r"You feel tired\\.", "sleep"),
    (r"\\[Exits:", ""),  # No-op trigger just to detect room
]

# ── ALIASES ──
# Format: {"shortcut": "expanded_command", ...}
# Typing the shortcut sends the expanded command instead.
ALIASES = {
    # "ga": "get all from corpse",
    # "gc": "get all corpse",
    # "hh": "cast heal",
    # "rr": "recall",
    # "ww": "wear all",
    "l": "look",
    "n": "north",
    "s": "south",
    "e": "east",
    "w": "west",
    "ne": "northeast",
    "nw": "northwest",
    "se": "southeast",
    "sw": "southwest",
    "u": "up",
    "d": "down",
}

# ── TIMERS ──
# Format: [(interval_seconds, "command"), ...]
# Command is sent every N seconds while connected.
TIMERS = [
    # (60, "look"),
    # (300, "save"),
]

# ── BUTTONS ──
# Format: [("Label", "command", "category"), ...]
# Categories: "combat", "heal", "move", "misc", "magic"
BUTTONS = [
    ("Look", "look", "misc"),
    ("Inventory", "inventory", "misc"),
    ("Score", "score", "misc"),
    ("Kill", "kill", "combat"),
    ("Flee", "flee", "combat"),
    # ("Heal", "cast heal", "magic"),
    # ("Recall", "recall", "misc"),
]

# ── GAUGE PARSING ──
# Regex patterns to extract HP/MP/EP from MUD output
# Each tuple: (regex, group_index_for_current, group_index_for_max, gauge_name)
GAUGE_PATTERNS = [
    # Islands of Myth style
    (r"Hp:\\s*(\\d+)\\s*/\\s*(\\d+)", 1, 2, "HP"),
    (r"Mp:\\s*(\\d+)\\s*/\\s*(\\d+)", 1, 2, "MP"),
    (r"Ep:\\s*(\\d+)\\s*/\\s*(\\d+)", 1, 2, "EP"),
    # Generic alternatives
    (r"HP\\s+(\\d+)\\s*/\\s*(\\d+)", 1, 2, "HP"),
    (r"MP\\s+(\\d+)\\s*/\\s*(\\d+)", 1, 2, "MP"),
    (r"EP\\s+(\\d+)\\s*/\\s*(\\d+)", 1, 2, "EP"),
    (r"Health:\\s*(\\d+)\\s*/\\s*(\\d+)", 1, 2, "HP"),
    (r"Mana:\\s*(\\d+)\\s*/\\s*(\\d+)", 1, 2, "MP"),
    (r"Energy:\\s*(\\d+)\\s*/\\s*(\\d+)", 1, 2, "EP"),
]
'''

# ── NAMED TUPLES ──
Trigger = namedtuple("Trigger", ["pattern", "command", "compiled"])
Timer = namedtuple("Timer", ["interval", "command", "last_fired"])
ButtonDef = namedtuple("ButtonDef", ["label", "command", "category"])

class AudioManager:
    def __init__(self):
        self.music_volume = 0.5
        self.sfx_volume = 0.7
        self.current_terrain = None
        self.current_music = None
        self.music_files = self._scan_folder(MUSIC_DIR)
        self.sfx_categories = {
            'combat': self._scan_folder(SFX_DIR / "combat"),
            'shops': self._scan_folder(SFX_DIR / "shops"),
            'footsteps': self._scan_folder(SFX_DIR / "footsteps"),
            'transformations': self._scan_folder(SFX_DIR / "transformations"),
            'npcs': self._scan_folder(SFX_DIR / "npcs"),
        }
        pygame.mixer.music.set_volume(self.music_volume)

    def _scan_folder(self, folder):
        if not folder.exists():
            return []
        exts = ('.ogg', '.wav', '.mp3')
        return [f for f in folder.iterdir() if f.suffix.lower() in exts]

    def play_random_music(self):
        if not self.music_files:
            return
        track = random.choice(self.music_files)
        if str(track) != self.current_music:
            pygame.mixer.music.load(str(track))
            pygame.mixer.music.play(-1)
            self.current_music = str(track)

    def play_terrain_music(self, terrain):
        self.play_random_music()

    def play_sfx(self, category):
        files = self.sfx_categories.get(category, [])
        if not files:
            return
        sound = pygame.mixer.Sound(str(random.choice(files)))
        sound.set_volume(self.sfx_volume)
        sound.play()

    def stop_music(self):
        pygame.mixer.music.stop()
        self.current_music = None

class MapCell:
    def __init__(self, name, terrain, exits, visited_time=None):
        self.name = name
        self.terrain = terrain
        self.exits = exits
        self.visited_time = visited_time or datetime.now()
        self.visit_count = 1

class IOMClient:
    def __init__(self):
        pygame.init()
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

        # Window
        self.fullscreen = False
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Myth of Islands Client v4.2")

        # Title bar drag state
        self.dragging = False
        self.drag_offset = (0, 0)

        # Fonts
        self.font = pygame.font.SysFont("consolas", FONT_SIZE)
        self.bold_font = pygame.font.SysFont("consolas", FONT_SIZE, bold=True)
        self.small_font = pygame.font.SysFont("consolas", 11)
        self.tile_font = pygame.font.SysFont("consolas", 10)
        self.title_font = pygame.font.SysFont("consolas", 14, bold=True)

        # Theme
        self.theme_name = "classic"
        self.t = THEMES[self.theme_name]

        # Audio
        self.audio = AudioManager()
        if self.audio.music_files:
            self.audio.play_random_music()
        self.muted = False

        # Layout
        self.layout_mode = 'horizontal'

        # Console
        self.lines = []
        self.scroll_offset = 0
        self._parse_buffer = ""

        # Input
        self.input_text = ""
        self.input_history = []
        self.history_idx = 0
        self.cursor_visible = True
        self.cursor_timer = 0

        # Telnet
        self.tn = None
        self.connected = False
        self.output_queue = queue.Queue()
        self.running = True

        # Map
        self.map_grid = {}
        self.player_pos = (0, 0)
        self.current_room = None
        self.current_exits = set()
        self.last_move_time = 0
        self.speedwalking = False
        self.zoom_level = 1.0
        self.target_zoom = 1.0

        # Combat
        self.in_combat = False

        # Gauges
        self.gauges = {}  # {"HP": {"current": 100, "max": 100}, ...}

        # Auto-reconnect
        self.auto_character = None
        self.auto_reconnect = True
        self.reconnect_timer = None
        self._pending_reconnect = False
        self.autopilot_queue = []
        self.autopilot_last_sent = 0
        self.autopilot_delay = 1.0

        # Config (triggers, aliases, timers, buttons)
        self.triggers = []
        self.aliases = {}
        self.timers = []
        self.buttons = []
        self.gauge_patterns = []
        self.load_config()

        # Log
        self.log_file = open(LOG_FILE, "a", encoding="utf-8", errors="replace")
        self.log_file.write(f"\n=== Session started {datetime.now()} ===\n")

    def load_config(self):
        """Load or create client_config.py"""
        if not CONFIG_FILE.exists():
            CONFIG_FILE.write_text(DEFAULT_CONFIG_PY, encoding="utf-8")
            self.add_line("[*] Created default client_config.py - edit to customize!", (0, 200, 200))

        # Exec the config file to get its variables
        config_globals = {}
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                exec(f.read(), config_globals)
        except Exception as e:
            self.add_line(f"[!] Config load error: {e}", (255, 0, 0))
            return

        # Triggers
        raw_triggers = config_globals.get("TRIGGERS", [])
        self.triggers = []
        for pattern, cmd in raw_triggers:
            if pattern and cmd:
                try:
                    self.triggers.append(Trigger(pattern, cmd, re.compile(pattern, re.IGNORECASE)))
                except re.error as e:
                    self.add_line(f"[!] Bad trigger regex '{pattern}': {e}", (255, 0, 0))

        # Aliases
        self.aliases = config_globals.get("ALIASES", {})

        # Timers
        raw_timers = config_globals.get("TIMERS", [])
        self.timers = []
        for interval, cmd in raw_timers:
            self.timers.append(Timer(interval, cmd, 0))

        # Buttons
        raw_buttons = config_globals.get("BUTTONS", [])
        self.buttons = []
        for label, cmd, cat in raw_buttons:
            self.buttons.append(ButtonDef(label, cmd, cat))

        # Gauge patterns
        self.gauge_patterns = config_globals.get("GAUGE_PATTERNS", [])

        self.add_line(f"[*] Config: {len(self.triggers)} triggers, {len(self.aliases)} aliases, {len(self.timers)} timers, {len(self.buttons)} buttons", (0, 200, 200))
        self.check_for_updates()

    def check_for_updates(self):
        """Check if a newer client version is available on the web server."""
        try:
            import urllib.request
            with urllib.request.urlopen(VERSION_URL, timeout=3) as resp:
                remote_version = resp.read().decode().strip()
            current = float(CLIENT_VERSION)
            remote = float(remote_version)
            if remote > current:
                self.add_line(f"", (0, 0, 0))  # blank line
                self.add_line(f"[UPDATE] Client v{remote_version} available! (You have v{CLIENT_VERSION})", (255, 200, 0))
                self.add_line(f"[UPDATE] Download: {UPDATE_URL}", (255, 200, 0))
                self.add_line(f"", (0, 0, 0))  # blank line
        except Exception:
            pass  # silently fail if no internet or server down

    def connect(self):
        def connect_thread():
            try:
                if USE_WEBSOCKET:
                    if not WEBSOCKET_AVAILABLE:
                        self.add_line("[!] websocket-client not installed. Run: python -m pip install websocket-client", self.t["status_disconnected"])
                        return
                    self.add_line(f"[*] Connecting via WebSocket to {WEBSOCKET_URL}...", self.t["fg"])
                    self.ws = websocket.WebSocketApp(
                        WEBSOCKET_URL,
                        on_open=lambda ws: self.on_ws_open(ws),
                        on_message=lambda ws, msg: self.on_ws_message(ws, msg),
                        on_error=lambda ws, err: self.on_ws_error(ws, err),
                        on_close=lambda ws, code, reason: self.on_ws_close(ws, code, reason),
                    )
                    self.connected = True
                    self.add_line("[*] WebSocket connected!", self.t["status_connected"])
                    self.ws.run_forever()
                else:
                    self.add_line(f"[*] Connecting via Telnet to {HOST}:{PORT}...", self.t["fg"])
                    self.tn = telnetlib.Telnet(HOST, PORT, timeout=30)
                    self.connected = True
                    self.add_line("[*] Telnet connected!", self.t["status_connected"])
                    while self.running and self.connected:
                        try:
                            data = self.tn.read_very_eager()
                            if data:
                                text = data.decode("utf-8", errors="replace")
                                self.output_queue.put(text)
                                self.log_file.write(text)
                                self.log_file.flush()
                            time.sleep(0.05)
                        except Exception as e:
                            self.add_line(f"[!] Read error: {e}", self.t["status_disconnected"])
                            break
            except Exception as e:
                self.add_line(f"[!] Connection failed: {e}", self.t["status_disconnected"])
                self.connected = False
        threading.Thread(target=connect_thread, daemon=True).start()

    def on_ws_open(self, ws):
        self.connected = True
        self.add_line("[*] WebSocket ready - waiting for MUD output...", self.t["status_connected"])

    def on_ws_message(self, ws, message):
        self.output_queue.put(message)
        self.log_file.write(message)
        self.log_file.flush()

    def on_ws_error(self, ws, error):
        self.add_line(f"[!] WebSocket error: {error}", self.t["status_disconnected"])
        self.connected = False
        self.schedule_reconnect()

    def on_ws_close(self, ws, code, reason):
        self.add_line(f"[*] WebSocket closed ({code})", self.t["status_disconnected"])
        self.connected = False
        self.schedule_reconnect()

    def schedule_reconnect(self):
        """Schedule auto-reconnect after disconnect"""
        if self._pending_reconnect or not self.auto_reconnect or not self.running:
            return
        self._pending_reconnect = True
        self.add_line("[*] Auto-reconnect in 3s...", (200, 200, 0))
        def do_reconnect():
            time.sleep(3)
            if self.running and not self.connected:
                self._pending_reconnect = False
                self.connect()
        threading.Thread(target=do_reconnect, daemon=True).start()

    def get_terrain(self, room_name):
        name_lower = room_name.lower()
        for terrain, aliases in TERRAIN_ALIASES.items():
            for alias in aliases:
                if alias in name_lower:
                    return terrain
        words = name_lower.split()
        for word in words:
            for terrain, aliases in TERRAIN_ALIASES.items():
                for alias in aliases:
                    if alias in word or word in alias:
                        return terrain
        return 'unknown'

    def update_map(self, room_name, exits):
        terrain = self.get_terrain(room_name)
        if self.player_pos in self.map_grid:
            cell = self.map_grid[self.player_pos]
            cell.visit_count += 1
            cell.exits = set(exits)
        else:
            self.map_grid[self.player_pos] = MapCell(room_name, terrain, set(exits))
        self.current_room = room_name
        self.current_exits = set(exits)
        self.audio.play_terrain_music(terrain)
        now = time.time()
        if now - self.last_move_time < 1.5:
            self.speedwalking = True
            self.target_zoom = 0.3
        else:
            self.speedwalking = False
            self.target_zoom = 1.0
        self.last_move_time = now

    def move_player(self, direction):
        if direction in DIR_VECTORS:
            dx, dy = DIR_VECTORS[direction]
            self.player_pos = (self.player_pos[0] + dx, self.player_pos[1] + dy)

    def send(self, text):
        # Apply aliases
        stripped = text.strip()
        if stripped.lower() in self.aliases:
            text = self.aliases[stripped.lower()]
            self.add_line(f"[alias] {stripped} → {text}", (100, 100, 200))

        sent = False
        if USE_WEBSOCKET and hasattr(self, 'ws') and self.ws and self.connected:
            try:
                self.ws.send(text)
                sent = True
            except Exception as e:
                self.add_line(f"[!] WebSocket send failed: {e}", self.t["status_disconnected"])
        elif self.tn and self.connected:
            self.tn.write(text.encode("utf-8") + b"\n")
            sent = True

        if sent:
            self.add_line(f">>> {text}", self.t["prompt"])
            cmd = text.strip().lower()
            # Store character name for auto-relogin after reboot
            for prefix in ("connect ", "login ", "l ", "create ", "c ", "new ", "n "):
                if cmd.startswith(prefix):
                    name = text.strip()[len(prefix):].strip()
                    if name:
                        self.auto_character = name
                        break
            if cmd in DIR_VECTORS:
                self.move_player(cmd)
                self.audio.play_sfx('footsteps')
            elif cmd in ('kill', 'attack', 'fight'):
                self.audio.play_sfx('combat')
            if text.strip() and (not self.input_history or self.input_history[-1] != text):
                self.input_history.append(text)
                if len(self.input_history) > INPUT_HISTORY:
                    self.input_history.pop(0)
            self.history_idx = len(self.input_history)

    def add_line(self, text, color=None, bold=False):
        if color is None:
            color = self.t["fg"]
        self.lines.append((text, color, bold))
        if len(self.lines) > 2000:
            self.lines.pop(0)
        self.scroll_offset = max(0, len(self.lines) - self.console_visible_lines())

    def console_visible_lines(self):
        avail = SCREEN_HEIGHT - TITLE_BAR_H - TOOLBAR_H
        if self.layout_mode == 'horizontal':
            avail = avail // 2
        return (avail - 50) // LINE_HEIGHT - 2

    def parse_ansi_and_add(self, text):
        i = 0
        buffer_text = ""
        fg = 7
        bg = 0
        bold = False
        while i < len(text):
            if text[i] == '\x1b' and i + 1 < len(text) and text[i+1] == '[':
                if buffer_text:
                    color = (BRIGHT_COLORS.get(fg, ANSI_COLORS.get(fg, self.t["fg"])) if bold
                           else ANSI_COLORS.get(fg, self.t["fg"]))
                    self.add_line(buffer_text, color, bold)
                    buffer_text = ""
                j = i + 2
                seq = ""
                while j < len(text):
                    c = text[j]
                    if c.isalpha():
                        seq = text[i+2:j]
                        break
                    j += 1
                if j >= len(text):
                    break
                params = [int(p) if p.isdigit() else 0 for p in seq.split(';')] if seq else [0]
                for p in params:
                    if p == 0:
                        fg, bg, bold = 7, 0, False
                    elif p == 1:
                        bold = True
                    elif p == 22:
                        bold = False
                    elif 30 <= p <= 37:
                        fg = p - 30
                    elif 40 <= p <= 47:
                        bg = p - 40
                    elif 90 <= p <= 97:
                        fg = p - 90
                        bold = True
                i = j + 1
                continue
            if text[i] == '\n':
                if buffer_text:
                    color = (BRIGHT_COLORS.get(fg, ANSI_COLORS.get(fg, self.t["fg"])) if bold
                           else ANSI_COLORS.get(fg, self.t["fg"]))
                    self.add_line(buffer_text, color, bold)
                    buffer_text = ""
                else:
                    self.add_line("")
                i += 1
                continue
            if ord(text[i]) < 32 and text[i] != '\t':
                i += 1
                continue
            buffer_text += text[i]
            i += 1
        if buffer_text:
            color = (BRIGHT_COLORS.get(fg, ANSI_COLORS.get(fg, self.t["fg"])) if bold
                   else ANSI_COLORS.get(fg, self.t["fg"]))
            self.add_line(buffer_text, color, bold)

    def _parse_room_from_buffer(self):
        clean = re.sub(r'\x1b\[[0-9;]*m', '', self._parse_buffer)
        flat = ' '.join(clean.split())
        room_match = re.search(r'([A-Za-z][a-zA-Z0-9 ]+?)\s*\[exits:\s*([a-z,\s]+)\]', flat)
        if room_match:
            room_name = room_match.group(1).strip()
            if room_name.lower() in ('level', 'hp', 'mp', 'exp', 'gold', 'str', 'dex', 'con', 'int', 'wis', 'cha'):
                return
            exits_str = room_match.group(2)
            exits = [e.strip() for e in re.split(r',\s*|\s+and\s+', exits_str)]
            valid_dirs = {'n','s','e','w','ne','nw','se','sw',
                         'north','south','east','west',
                         'northeast','northwest','southeast','southwest',
                         'up','down','in','out'}
            exits = [e for e in exits if e in valid_dirs]
            if exits:
                self.update_map(room_name, exits)
                self._parse_buffer = ""

    def check_combat(self, text):
        text_lower = text.lower()
        combat_triggers = ['you hit','you miss','hits you','misses you','you killed','died','death','corpse']
        for trigger in combat_triggers:
            if trigger in text_lower:
                if not self.in_combat:
                    self.audio.play_sfx('combat')
                    self.in_combat = True
                return True
        if 'not fighting' in text_lower or 'not in combat' in text_lower:
            self.in_combat = False
        return False

    def parse_gauges(self, text):
        """Extract HP/MP/EP from MUD output"""
        for pattern, cur_idx, max_idx, name in self.gauge_patterns:
            m = re.search(pattern, text, re.IGNORECASE)
            if m:
                try:
                    current = int(m.group(cur_idx))
                    max_val = int(m.group(max_idx))
                    self.gauges[name] = {"current": current, "max": max_val}
                except (IndexError, ValueError):
                    pass

    def check_triggers(self, text):
        """Check MUD output against trigger regexes"""
        for trigger in self.triggers:
            if trigger.compiled.search(text):
                if trigger.command.strip():
                    self.add_line(f"[trigger] Fired: {trigger.pattern}", (150, 150, 255))
                    self.send(trigger.command)

    def process_output(self):
        while not self.output_queue.empty():
            text = self.output_queue.get()
            text = text.replace('\r\n', '\n').replace('\r', '\n')
            self._parse_buffer += text
            self.parse_ansi_and_add(text)
            self._parse_room_from_buffer()
            self.check_combat(text)
            self.parse_gauges(text)
            self.check_triggers(text)
            # Auto-login after reboot: if we see login prompt and have stored character
            if self.auto_character and self.connected:
                lower = text.lower()
                if "connect" in lower and "character" in lower and "password" in lower:
                    time.sleep(0.3)
                    self.send(self.auto_character)
                    self.add_line(f"[*] Auto-login as {self.auto_character}", (0, 200, 200))
                    self.auto_character = None

    def update_timers(self):
        """Fire periodic timers"""
        now = time.time()
        for timer in self.timers:
            if now - timer.last_fired >= timer.interval:
                self.send(timer.command)
                timer.last_fired = now

    def update_autopilot(self):
        """Read queue file and send next command with delay"""
        if not self.autopilot_enabled:
            return

        # Try to load fresh commands from queue file
        try:
            if QUEUE_FILE.exists():
                with open(QUEUE_FILE, "r") as f:
                    lines = [l.strip() for l in f if l.strip()]
                if lines and not self.autopilot_queue:
                    self.autopilot_queue = lines
                    self.add_line(f"[autopilot] Loaded {len(lines)} commands", self.t["autopilot_on"])
                    # Clear file after reading
                    with open(QUEUE_FILE, "w") as f:
                        f.write("")
        except Exception:
            pass

        # Send next command
        now = time.time()
        if self.autopilot_queue and now - self.autopilot_last_sent >= self.autopilot_delay:
            cmd = self.autopilot_queue.pop(0)
            self.send(cmd)
            self.autopilot_last_sent = now
            self.autopilot_delay = random.uniform(0.8, 2.5)
            if not self.autopilot_queue:
                self.add_line("[autopilot] Queue empty - waiting for more", self.t["autopilot_off"])

    def stop_autopilot(self):
        self.autopilot_enabled = False
        self.autopilot_queue = []
        self.add_line("[autopilot] STOPPED - queue cleared", self.t["status_disconnected"])

    def toggle_theme(self):
        self.theme_name = "modern" if self.theme_name == "classic" else "classic"
        self.t = THEMES[self.theme_name]
        self.add_line(f"[*] Theme: {self.t['name']}", self.t["fg"])

    def toggle_fullscreen(self):
        """Toggle fullscreen mode and resize to fill the actual display."""
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            info = pygame.display.Info()
            w, h = info.current_w, info.current_h
        else:
            w, h = 1024, 768
        global SCREEN_WIDTH, SCREEN_HEIGHT
        SCREEN_WIDTH, SCREEN_HEIGHT = w, h
        flags = pygame.FULLSCREEN if self.fullscreen else pygame.RESIZABLE
        self.screen = pygame.display.set_mode((w, h), flags)
        self._resize_fonts()

    def adjust_font_size(self, delta):
        """Adjust font size by delta points."""
        global FONT_SIZE, LINE_HEIGHT
        FONT_SIZE = max(8, min(24, FONT_SIZE + delta))
        LINE_HEIGHT = FONT_SIZE + 2
        self._resize_fonts()
        self.add_line(f"[font] Size: {FONT_SIZE}px", (100, 200, 100))

    def _resize_fonts(self):
        """Recreate fonts after size change."""
        self.font = pygame.font.SysFont("consolas", FONT_SIZE)
        self.bold_font = pygame.font.SysFont("consolas", FONT_SIZE, bold=True)
        self.small_font = pygame.font.SysFont("consolas", max(9, FONT_SIZE - 2))
        self.tile_font = pygame.font.SysFont("consolas", max(8, FONT_SIZE - 3))
        self.title_font = pygame.font.SysFont("consolas", max(10, FONT_SIZE + 1), bold=True)

    # ── DRAWING ──
    def draw_title_bar(self):
        rect = pygame.Rect(0, 0, SCREEN_WIDTH, TITLE_BAR_H)
        pygame.draw.rect(self.screen, self.t["title_bar"], rect)

        # Title text
        title = f"Myth of Islands - {HOST}:{PORT}"
        if not self.connected:
            title += " [OFFLINE]"
        elif self.autopilot_enabled:
            title += " [BOT]"
        surf = self.title_font.render(title, True, self.t["title_text"])
        self.screen.blit(surf, (10, 6))

        # Window buttons (right side)
        btn_y = 4
        btn_h = TITLE_BAR_H - 8
        sw = self.screen.get_width()
        # Minimize
        min_rect = pygame.Rect(sw - 90, btn_y, 26, btn_h)
        pygame.draw.rect(self.screen, self.t["toolbar_btn"], min_rect, border_radius=2)
        pygame.draw.line(self.screen, self.t["toolbar_text"], (min_rect.centerx - 4, min_rect.centery), (min_rect.centerx + 4, min_rect.centery), 2)

        # Maximize/Restore
        max_rect = pygame.Rect(sw - 62, btn_y, 26, btn_h)
        pygame.draw.rect(self.screen, self.t["toolbar_btn"], max_rect, border_radius=2)
        if self.fullscreen:
            pygame.draw.rect(self.screen, self.t["toolbar_text"], max_rect.inflate(-8, -8), 1)
        else:
            pygame.draw.rect(self.screen, self.t["toolbar_text"], max_rect.inflate(-6, -6), 1)

        # Close
        close_rect = pygame.Rect(sw - 34, btn_y, 26, btn_h)
        pygame.draw.rect(self.screen, (180, 50, 50), close_rect, border_radius=2)
        pygame.draw.line(self.screen, (255, 255, 255), (close_rect.centerx - 4, close_rect.centery - 4), (close_rect.centerx + 4, close_rect.centery + 4), 2)
        pygame.draw.line(self.screen, (255, 255, 255), (close_rect.centerx + 4, close_rect.centery - 4), (close_rect.centerx - 4, close_rect.centery + 4), 2)

        return {"min": min_rect, "max": max_rect, "close": close_rect}

    def draw_toolbar(self):
        sw = self.screen.get_width()
        rect = pygame.Rect(0, TITLE_BAR_H, sw, TOOLBAR_H)
        pygame.draw.rect(self.screen, self.t["toolbar"], rect)

        x = 10
        btn_h = TOOLBAR_H - 6
        btn_y = TITLE_BAR_H + 3

        def draw_btn(label, active=False, color_key="toolbar_btn"):
            nonlocal x
            surf = self.small_font.render(label, True, self.t["toolbar_text"])
            w = max(surf.get_width() + 14, 50)
            r = pygame.Rect(x, btn_y, w, btn_h)
            bg = self.t["toolbar_btn_active"] if active else self.t[color_key]
            pygame.draw.rect(self.screen, bg, r, border_radius=3)
            self.screen.blit(surf, (r.centerx - surf.get_width()//2, r.centery - surf.get_height()//2))
            x += w + 6
            return r

        # Connection status
        status_color = "status_connected" if self.connected else "status_disconnected"
        conn_rect = draw_btn("● LIVE" if self.connected else "● OFF", active=self.connected, color_key=status_color)

        # Theme toggle
        theme_rect = draw_btn("🎨 " + self.theme_name.title(), color_key="toolbar_btn")

        # Autopilot toggle
        ap_rect = draw_btn("🤖 BOT" if self.autopilot_enabled else "🤖 Auto", active=self.autopilot_enabled)

        # Mute toggle
        mute_rect = draw_btn("🔊" if not self.muted else "🔇", active=self.muted)

        # Layout toggle
        layout_rect = draw_btn("⬌ Split" if self.layout_mode == 'horizontal' else "⬍ Stack", color_key="toolbar_btn")

        # Fullscreen - prominent button
        fs_rect = draw_btn("FULL", active=self.fullscreen, color_key="toolbar_btn")

        # Font size adjustment
        font_down = draw_btn("T-", color_key="toolbar_btn")
        font_up = draw_btn("T+", color_key="toolbar_btn")

        # Reload config
        reload_rect = draw_btn("↻ Cfg", color_key="toolbar_btn")

        return {
            "connect": conn_rect,
            "theme": theme_rect,
            "autopilot": ap_rect,
            "mute": mute_rect,
            "layout": layout_rect,
            "fullscreen": fs_rect,
            "font_down": font_down,
            "font_up": font_up,
            "reload": reload_rect,
        }

    def draw_gauges(self, rect):
        """Draw HP/MP/EP bars at top of console area"""
        if not self.gauges:
            return 0

        gauge_h = 20
        y = rect.y + 4
        total_w = rect.width - 20
        gauge_w = total_w // len(self.gauges)

        for i, (name, data) in enumerate(self.gauges.items()):
            x = rect.x + 10 + i * gauge_w
            g_rect = pygame.Rect(x, y, gauge_w - 8, gauge_h)
            pygame.draw.rect(self.screen, self.t["gauge_bg"], g_rect, border_radius=3)

            pct = min(1.0, data["current"] / max(1, data["max"]))
            fill_w = int((gauge_w - 8) * pct)
            fill_rect = pygame.Rect(x, y, fill_w, gauge_h)
            color = self.t.get(f"gauge_{name.lower()}", self.t["gauge_hp"])
            pygame.draw.rect(self.screen, color, fill_rect, border_radius=3)

            label = f"{name}: {data['current']}/{data['max']}"
            surf = self.small_font.render(label, True, (255, 255, 255))
            self.screen.blit(surf, (g_rect.centerx - surf.get_width()//2, g_rect.centery - surf.get_height()//2))

        return gauge_h + 8

    def draw_map(self, rect):
        pygame.draw.rect(self.screen, self.t["map_bg"], rect)
        self.zoom_level += (self.target_zoom - self.zoom_level) * 0.1
        tile_size = int(MAP_TILE_SIZE * self.zoom_level)
        if tile_size < 4:
            tile_size = 4

        cx, cy = self.player_pos
        view_w = rect.width // tile_size
        view_h = rect.height // tile_size
        start_x = cx - view_w // 2
        start_y = cy - view_h // 2

        for dy in range(view_h + 1):
            for dx in range(view_w + 1):
                gx, gy = start_x + dx, start_y + dy
                px, py = rect.x + dx * tile_size, rect.y + dy * tile_size

                if (gx, gy) == self.player_pos:
                    pygame.draw.rect(self.screen, self.t["map_player"], (px, py, tile_size-1, tile_size-1))
                    pygame.draw.circle(self.screen, self.t["map_player_dot"],
                                     (px + tile_size//2, py + tile_size//2), tile_size//3)
                elif (gx, gy) in self.map_grid:
                    cell = self.map_grid[(gx, gy)]
                    color = TERRAIN_COLORS.get(cell.terrain, (100, 100, 100))
                    pygame.draw.rect(self.screen, color, (px, py, tile_size-1, tile_size-1))
                    if tile_size > 12:
                        cxt, cyt = px + tile_size//2, py + tile_size//2
                        for ex in cell.exits:
                            if ex in DIR_VECTORS:
                                edx, edy = DIR_VECTORS[ex]
                                end_x = cxt + edx * tile_size//3
                                end_y = cyt + edy * tile_size//3
                                pygame.draw.line(self.screen, self.t["map_exit"], (cxt, cyt), (end_x, end_y), 1)
                else:
                    pygame.draw.rect(self.screen, self.t["map_unvisited"], (px, py, tile_size-1, tile_size-1))

        if self.current_room:
            name_surface = self.font.render(self.current_room, True, self.t["room_label_text"])
            bg_rect = name_surface.get_rect()
            bg_rect.topleft = (rect.x + 5, rect.y + 5)
            pygame.draw.rect(self.screen, self.t["room_label_bg"], bg_rect.inflate(10, 4))
            self.screen.blit(name_surface, (rect.x + 10, rect.y + 10))

        coord_text = f"({self.player_pos[0]}, {self.player_pos[1]}) | {len(self.map_grid)} rooms"
        coord_surface = self.font.render(coord_text, True, self.t["scroll_ind"])
        self.screen.blit(coord_surface, (rect.x + 5, rect.bottom - 20))

    def draw_console(self, rect):
        pygame.draw.rect(self.screen, self.t["console_bg"], rect)

        gauge_h = self.draw_gauges(rect)

        y = rect.y + 5 + gauge_h
        visible = (rect.height - 40 - gauge_h) // LINE_HEIGHT - 1
        start = max(0, len(self.lines) - visible - self.scroll_offset)
        end = min(len(self.lines), start + visible)

        for i in range(start, end):
            text, color, bold = self.lines[i]
            font = self.bold_font if bold else self.font
            max_width = rect.width - 20
            words = text.split(' ')
            line = ""
            for word in words:
                test = line + word + " "
                if font.size(test)[0] < max_width:
                    line = test
                else:
                    surface = font.render(line.rstrip(), True, color)
                    self.screen.blit(surface, (rect.x + 10, y))
                    y += LINE_HEIGHT
                    line = word + " "
            if line:
                surface = font.render(line.rstrip(), True, color)
                self.screen.blit(surface, (rect.x + 10, y))
                y += LINE_HEIGHT

        # Input bar
        input_y = rect.bottom - 28
        pygame.draw.rect(self.screen, self.t["input_bg"], (rect.x, input_y - 3, rect.width, 30))
        pygame.draw.rect(self.screen, self.t["input_border"], (rect.x, input_y - 3, rect.width, 30), 1)

        prompt = ">>> "
        prompt_surface = self.font.render(prompt, True, self.t["prompt"])
        self.screen.blit(prompt_surface, (rect.x + 10, input_y))

        input_surface = self.font.render(self.input_text, True, self.t["fg_bright"])
        self.screen.blit(input_surface, (rect.x + 40, input_y))

        if self.cursor_visible:
            cursor_x = rect.x + 40 + self.font.size(self.input_text)[0]
            pygame.draw.line(self.screen, self.t["cursor"], (cursor_x, input_y), (cursor_x, input_y + 14), 2)

    def draw_buttons(self, rect):
        """Draw action buttons panel on the right or bottom"""
        if not self.buttons:
            return

        pygame.draw.rect(self.screen, self.t["toolbar"], rect)

        # Group by category
        categories = defaultdict(list)
        for btn in self.buttons:
            categories[btn.category].append(btn)

        y = rect.y + 5
        x = rect.x + 5
        btn_w = rect.width - 10
        btn_h = 24

        for cat, btns in categories.items():
            cat_surf = self.small_font.render(cat.upper(), True, self.t["scroll_ind"])
            self.screen.blit(cat_surf, (x, y))
            y += 18

            for btn in btns:
                btn_rect = pygame.Rect(x, y, btn_w, btn_h)
                pygame.draw.rect(self.screen, self.t["button_bg"], btn_rect, border_radius=3)
                label = self.small_font.render(btn.label, True, self.t["button_text"])
                self.screen.blit(label, (btn_rect.centerx - label.get_width()//2, btn_rect.centery - label.get_height()//2))
                y += btn_h + 4

            y += 8

        return rect

    def draw(self):
        self.screen.fill(self.t["bg"])

        sw = self.screen.get_width()
        sh = self.screen.get_height()

        title_btns = self.draw_title_bar()
        toolbar_btns = self.draw_toolbar()

        content_top = TITLE_BAR_H + TOOLBAR_H
        content_h = sh - content_top

        # Layout calculation
        if self.layout_mode == 'horizontal':
            map_h = content_h // 2 - 2
            map_rect = pygame.Rect(0, content_top, sw, map_h)
            console_rect = pygame.Rect(0, content_top + map_h + 4, sw, content_h - map_h - 4)
            button_rect = None
        else:
            split = sw - 160
            map_rect = pygame.Rect(0, content_top, split // 2 - 2, content_h)
            console_rect = pygame.Rect(split // 2 + 2, content_top, split // 2 - 2, content_h)
            button_rect = pygame.Rect(split, content_top, sw - split, content_h)

        self.draw_map(map_rect)
        self.draw_console(console_rect)

        if button_rect:
            self.draw_buttons(button_rect)
            pygame.draw.line(self.screen, self.t["divider"], (button_rect.x, content_top), (button_rect.x, sh), 2)

        if self.layout_mode == 'horizontal':
            pygame.draw.line(self.screen, self.t["divider"], (0, content_top + content_h//2 - 2), (sw, content_top + content_h//2 - 2), 2)
        else:
            pygame.draw.line(self.screen, self.t["divider"], (sw//2, content_top), (sw//2, sh), 2)

        # Autopilot indicator
        if self.autopilot_enabled:
            ap_surf = self.small_font.render("AUTOPILOT ACTIVE", True, self.t["autopilot_on"])
            ap_bg = ap_surf.get_rect()
            ap_bg.topright = (sw - 10, TITLE_BAR_H + TOOLBAR_H + 5)
            pygame.draw.rect(self.screen, (20, 40, 20), ap_bg.inflate(8, 4))
            self.screen.blit(ap_surf, (ap_bg.x, ap_bg.y))

        # Help text
        help_text = "F2: Layout | F4: Theme | F11: Fullscreen | PgUp/PgDn: Scroll"
        help_surface = self.font.render(help_text, True, self.t["scroll_ind"])
        self.screen.blit(help_surface, (10, sh - 18))

        pygame.display.flip()
        return {**title_btns, **toolbar_btns}

    def run(self):
        self.connect()
        clock = pygame.time.Clock()
        last_buttons = {}

        while self.running:
            dt = clock.tick(30)

            self.process_output()
            self.update_autopilot()
            self.update_timers()

            self.cursor_timer += dt
            if self.cursor_timer >= 500:
                self.cursor_visible = not self.cursor_visible
                self.cursor_timer = 0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                elif event.type == pygame.VIDEORESIZE:
                    global SCREEN_WIDTH, SCREEN_HEIGHT
                    SCREEN_WIDTH, SCREEN_HEIGHT = event.size
                    flags = pygame.FULLSCREEN if self.fullscreen else pygame.RESIZABLE
                    self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags)
                    self._resize_fonts()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = event.pos

                    # Title bar buttons
                    if "min" in last_buttons and last_buttons["min"].collidepoint(mx, my):
                        pygame.display.iconify()
                    elif "max" in last_buttons and last_buttons["max"].collidepoint(mx, my):
                        self.toggle_fullscreen()
                    elif "close" in last_buttons and last_buttons["close"].collidepoint(mx, my):
                        self.running = False

                    # Toolbar buttons
                    elif "theme" in last_buttons and last_buttons["theme"].collidepoint(mx, my):
                        self.toggle_theme()
                    elif "autopilot" in last_buttons and last_buttons["autopilot"].collidepoint(mx, my):
                        self.autopilot_enabled = not self.autopilot_enabled
                        if not self.autopilot_enabled:
                            self.autopilot_queue = []
                            self.add_line("[autopilot] OFF", self.t["autopilot_off"])
                        else:
                            self.add_line("[autopilot] ON - reading queue file", self.t["autopilot_on"])
                    elif "mute" in last_buttons and last_buttons["mute"].collidepoint(mx, my):
                        self.muted = not self.muted
                        if self.muted:
                            pygame.mixer.music.set_volume(0)
                            self.audio.sfx_volume = 0
                        else:
                            pygame.mixer.music.set_volume(self.audio.music_volume)
                            self.audio.sfx_volume = 0.7
                    elif "layout" in last_buttons and last_buttons["layout"].collidepoint(mx, my):
                        self.layout_mode = 'split' if self.layout_mode == 'horizontal' else 'horizontal'
                    elif "fullscreen" in last_buttons and last_buttons["fullscreen"].collidepoint(mx, my):
                        self.toggle_fullscreen()
                    elif "font_down" in last_buttons and last_buttons["font_down"].collidepoint(mx, my):
                        self.adjust_font_size(-1)
                    elif "font_up" in last_buttons and last_buttons["font_up"].collidepoint(mx, my):
                        self.adjust_font_size(1)
                    elif "reload" in last_buttons and last_buttons["reload"].collidepoint(mx, my):
                        self.load_config()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if self.input_text.strip():
                            self.send(self.input_text)
                            self.input_text = ""
                            self.scroll_offset = 0

                    elif event.key == pygame.K_BACKSPACE:
                        self.input_text = self.input_text[:-1]

                    elif event.key == pygame.K_UP:
                        if self.input_history and self.history_idx > 0:
                            self.history_idx -= 1
                            self.input_text = self.input_history[self.history_idx]

                    elif event.key == pygame.K_DOWN:
                        if self.history_idx < len(self.input_history) - 1:
                            self.history_idx += 1
                            self.input_text = self.input_history[self.history_idx]
                        else:
                            self.history_idx = len(self.input_history)
                            self.input_text = ""

                    elif event.key == pygame.K_PAGEUP:
                        self.scroll_offset = min(self.scroll_offset + 5,
                                               max(0, len(self.lines) - self.console_visible_lines()))

                    elif event.key == pygame.K_PAGEDOWN:
                        self.scroll_offset = max(0, self.scroll_offset - 5)

                    elif event.key == pygame.K_ESCAPE:
                        if self.autopilot_enabled:
                            self.stop_autopilot()
                        else:
                            self.input_text = ""

                    elif event.key == pygame.K_F2:
                        self.layout_mode = 'split' if self.layout_mode == 'horizontal' else 'horizontal'

                    elif event.key == pygame.K_F3:
                        self.muted = not self.muted
                        if self.muted:
                            pygame.mixer.music.set_volume(0)
                            self.audio.sfx_volume = 0
                        else:
                            pygame.mixer.music.set_volume(self.audio.music_volume)
                            self.audio.sfx_volume = 0.7

                    elif event.key == pygame.K_F4:
                        self.toggle_theme()

                    elif event.key == pygame.K_F11:
                        self.toggle_fullscreen()

                    elif event.unicode.isprintable():
                        self.input_text += event.unicode

            last_buttons = self.draw()

        self.running = False
        self.connected = False
        if hasattr(self, 'ws') and self.ws:
            try:
                self.ws.close()
            except:
                pass
        if self.tn:
            try:
                self.tn.close()
            except:
                pass
        self.audio.stop_music()
        self.log_file.close()
        pygame.quit()


if __name__ == "__main__":
    client = IOMClient()
    client.run()
