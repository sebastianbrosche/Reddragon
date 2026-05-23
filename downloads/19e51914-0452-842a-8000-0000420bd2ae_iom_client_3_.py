#!/usr/bin/env python3
"""
IOM Hybrid MUD Client - Phase 3: Audio Layer

Layout:
- Default: Top = tile map viewport, Bottom = MUD console
- Split mode: Left = map, Right = console (toggle with F2)
- Room-by-room view when walking normally
- Zooms out during speedwalk to show larger area
- Audio: Ambient music per terrain, SFX folders

Audio folders (create these next to the .exe):
  audio/music/           - Ambient loops (.ogg/.wav)
  audio/sfx/combat/      - Combat sounds
  audio/sfx/shops/       - Shop sounds
  audio/sfx/footsteps/   - Walking sounds
  audio/sfx/transformations/ - Level up, buffs
  audio/sfx/npcs/        - NPC chatter
"""

import pygame
import threading
import queue
import re
import telnetlib
import time
import random
import os
from datetime import datetime
from pathlib import Path
from collections import defaultdict

# Config
HOST = "islandsofmyth.org"
PORT = 3000
LOG_FILE = Path("iom_client_session.log")

# Audio paths (relative to script location)
SCRIPT_DIR = Path(__file__).parent.resolve()
AUDIO_DIR = SCRIPT_DIR / "audio"
MUSIC_DIR = AUDIO_DIR / "music"
SFX_DIR = AUDIO_DIR / "sfx"

# Display
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
MAP_TILE_SIZE = 48
ZOOMED_TILE_SIZE = 16
FONT_SIZE = 13
LINE_HEIGHT = 15
INPUT_HISTORY = 50

# Terrain colors
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
    'plains': ['plains', 'field', 'meadow', 'grassland'],
    'forest': ['forest', 'woods', 'grove', 'jungle'],
    'sandy beach': ['beach', 'sand', 'shore', 'coast'],
    'water': ['water', 'ocean', 'sea', 'lake', 'pond'],
    'swamp': ['swamp', 'marsh', 'bog'],
    'badlands': ['badlands', 'wasteland', 'desert'],
    'city': ['city', 'town', 'village', 'street', 'road', 'square'],
    'dungeon': ['dungeon', 'cave', 'cavern', 'lair'],
    'tunnel': ['tunnel', 'passage', 'corridor'],
    'hell': ['hell', 'underworld', 'abyss', 'inferno'],
    'mountain': ['mountain', 'hill', 'peak', 'cliff'],
    'dock': ['dock', 'pier', 'wharf', 'port'],
    'river': ['river', 'stream', 'brook'],
    'guild': ['guild', 'hall', 'adventurer'],
    'temple': ['temple', 'shrine', 'church', 'cathedral'],
    'market': ['market', 'bazaar', 'shop', 'store'],
}

# ANSI Colors
ANSI_COLORS = {
    0: (0, 0, 0), 1: (170, 0, 0), 2: (0, 170, 0), 3: (170, 170, 0),
    4: (0, 0, 170), 5: (170, 0, 170), 6: (0, 170, 170), 7: (170, 170, 170),
}
BRIGHT_COLORS = {
    0: (85, 85, 85), 1: (255, 85, 85), 2: (85, 255, 85), 3: (255, 255, 85),
    4: (85, 85, 255), 5: (255, 85, 255), 6: (85, 255, 255), 7: (255, 255, 255),
}

DIR_VECTORS = {
    'n': (0, -1), 's': (0, 1), 'e': (1, 0), 'w': (-1, 0),
    'ne': (1, -1), 'nw': (-1, -1), 'se': (1, 1), 'sw': (-1, 1),
}


class AudioManager:
    """Manages ambient music and SFX"""
    def __init__(self):
        self.music_volume = 0.5
        self.sfx_volume = 0.7
        self.current_terrain = None
        self.current_music = None
        
        # Scan audio folders
        self.music_files = self._scan_folder(MUSIC_DIR)
        self.sfx_categories = {
            'combat': self._scan_folder(SFX_DIR / "combat"),
            'shops': self._scan_folder(SFX_DIR / "shops"),
            'footsteps': self._scan_folder(SFX_DIR / "footsteps"),
            'transformations': self._scan_folder(SFX_DIR / "transformations"),
            'npcs': self._scan_folder(SFX_DIR / "npcs"),
        }
        
        # Set volumes
        pygame.mixer.music.set_volume(self.music_volume)
    
    def _scan_folder(self, folder):
        """Get all audio files in a folder"""
        if not folder.exists():
            return []
        exts = ('.ogg', '.wav', '.mp3')
        return [f for f in folder.iterdir() if f.suffix.lower() in exts]
    
    def play_random_music(self):
        """Play random ambient track"""
        if not self.music_files:
            return
        track = random.choice(self.music_files)
        if str(track) != self.current_music:
            pygame.mixer.music.load(str(track))
            pygame.mixer.music.play(-1)  # Loop forever
            self.current_music = str(track)
    
    def play_terrain_music(self, terrain):
        """Play music based on terrain (placeholder for future mapping)"""
        # For now, just play random music from the pool
        # Future: terrain-specific subfolders like audio/music/forest/, audio/music/city/
        self.play_random_music()
    
    def play_sfx(self, category):
        """Play random SFX from a category"""
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
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("IOM Hybrid Client - Phase 3")
        
        self.font = pygame.font.SysFont("consolas", FONT_SIZE)
        self.bold_font = pygame.font.SysFont("consolas", FONT_SIZE, bold=True)
        self.tile_font = pygame.font.SysFont("consolas", 10)
        
        # Audio
        self.audio = AudioManager()
        if self.audio.music_files:
            self.audio.play_random_music()
        
        # Layout mode
        self.layout_mode = 'horizontal'
        
        # Console
        self.lines = []
        self.scroll_offset = 0
        self._parse_buffer = ""  # Accumulates text for room parsing
        
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
        
        # Map state
        self.map_grid = {}
        self.player_pos = (0, 0)
        self.current_room = None
        self.current_exits = set()
        self.last_move_time = 0
        self.speedwalking = False
        
        # Camera
        self.camera_offset = (0, 0)
        self.zoom_level = 1.0
        self.target_zoom = 1.0
        
        # Combat/event detection
        self.in_combat = False
        
        # Log
        self.log_file = open(LOG_FILE, "a", encoding="utf-8", errors="replace")
        self.log_file.write(f"\n=== Session started {datetime.now()} ===\n")
    
    def connect(self):
        def connect_thread():
            try:
                self.add_line(f"[*] Connecting to {HOST}:{PORT}...", (128, 128, 128))
                self.tn = telnetlib.Telnet(HOST, PORT, timeout=30)
                self.connected = True
                self.add_line("[*] Connected!", (0, 255, 0))
                
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
                        self.add_line(f"[!] Read error: {e}", (255, 0, 0))
                        break
            except Exception as e:
                self.add_line(f"[!] Connection failed: {e}", (255, 0, 0))
                self.connected = False
                
        thread = threading.Thread(target=connect_thread, daemon=True)
        thread.start()
    
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
        
        # Update music for new terrain
        self.audio.play_terrain_music(terrain)
        
        # Check speedwalking
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
        if self.tn and self.connected:
            self.tn.write(text.encode("utf-8") + b"\n")
            self.add_line(f">>> {text}", (0, 200, 200))
            
            cmd = text.strip().lower()
            if cmd in DIR_VECTORS:
                self.move_player(cmd)
                # Footstep SFX
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
            color = ANSI_COLORS[7]
        self.lines.append((text, color, bold))
        if len(self.lines) > 2000:
            self.lines.pop(0)
        self.scroll_offset = max(0, len(self.lines) - self.console_visible_lines())
    
    def console_visible_lines(self):
        if self.layout_mode == 'horizontal':
            return (SCREEN_HEIGHT // 2 - 50) // LINE_HEIGHT - 2
        else:
            return (SCREEN_HEIGHT - 50) // LINE_HEIGHT - 2
    
    def parse_ansi_and_add(self, text):
        i = 0
        buffer_text = ""
        fg = 7
        bg = 0
        bold = False
        
        while i < len(text):
            if text[i] == '\x1b' and i + 1 < len(text) and text[i + 1] == '[':
                if buffer_text:
                    color = BRIGHT_COLORS.get(fg, ANSI_COLORS.get(fg, (200, 200, 200))) if bold else ANSI_COLORS.get(fg, (200, 200, 200))
                    self.add_line(buffer_text, color, bold)
                    buffer_text = ""
                
                j = i + 2
                seq = ""
                while j < len(text):
                    c = text[j]
                    if c.isalpha():
                        seq = text[i + 2:j]
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
                    color = BRIGHT_COLORS.get(fg, ANSI_COLORS.get(fg, (200, 200, 200))) if bold else ANSI_COLORS.get(fg, (200, 200, 200))
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
            color = BRIGHT_COLORS.get(fg, ANSI_COLORS.get(fg, (200, 200, 200))) if bold else ANSI_COLORS.get(fg, (200, 200, 200))
            self.add_line(buffer_text, color, bold)
    
    def _parse_room_from_buffer(self):
        """Scan accumulated buffer for room data (may span multiple lines)"""
        # Strip ANSI codes
        clean = re.sub(r'\x1b\[[0-9;]*m', '', self._parse_buffer)
        # Collapse multiple newlines to single space for matching
        flat = ' '.join(clean.split())
        
        room_match = re.search(
            r'([A-Za-z][a-zA-Z0-9 ]+?)\s*\[exits:\s*([a-z,\s]+)\]',
            flat
        )
        if room_match:
            room_name = room_match.group(1).strip()
            # Skip non-room strings
            if room_name.lower() in ('level', 'hp', 'mp', 'exp', 'gold', 'str', 'dex', 'con', 'int', 'wis', 'cha'):
                return
            
            exits_str = room_match.group(2)
            exits = [e.strip() for e in re.split(r',\s*|\s+and\s+', exits_str)]
            valid_dirs = {'n', 's', 'e', 'w', 'ne', 'nw', 'se', 'sw',
                         'north', 'south', 'east', 'west',
                         'northeast', 'northwest', 'southeast', 'southwest',
                         'up', 'down', 'in', 'out'}
            exits = [e for e in exits if e in valid_dirs]
            if exits:
                self.update_map(room_name, exits)
                # Clear buffer after successful parse
                self._parse_buffer = ""
    
    def parse_room_data(self, text):
        """Legacy single-chunk parser (kept for compatibility)"""
        clean = re.sub(r'\x1b\[[0-9;]*m', '', text)
        
        room_match = re.search(
            r'([A-Za-z][a-zA-Z0-9 ]+?)\s*\[exits:\s*([^\]]+)\]',
            clean
        )
        if room_match:
            room_name = room_match.group(1).strip()
            if room_name.lower() in ('level', 'hp', 'mp', 'exp', 'gold'):
                return False
            
            exits_str = room_match.group(2)
            exits = [e.strip().lower() for e in re.split(r',\s*|\s+and\s+', exits_str)]
            valid_dirs = {'n', 's', 'e', 'w', 'ne', 'nw', 'se', 'sw',
                         'north', 'south', 'east', 'west',
                         'northeast', 'northwest', 'southeast', 'southwest',
                         'up', 'down', 'in', 'out'}
            exits = [e for e in exits if e in valid_dirs or e.rstrip('.') in valid_dirs]
            self.update_map(room_name, exits)
            return True
        return False
    
    def check_combat(self, text):
        """Detect combat events for SFX triggers"""
        text_lower = text.lower()
        combat_triggers = ['you hit', 'you miss', 'hits you', 'misses you', 
                          'you killed', 'died', 'death', 'corpse']
        for trigger in combat_triggers:
            if trigger in text_lower:
                if not self.in_combat:
                    self.audio.play_sfx('combat')
                    self.in_combat = True
                return True
        
        # End combat detection
        if 'not fighting' in text_lower or 'not in combat' in text_lower:
            self.in_combat = False
        return False
    
    def process_output(self):
        """Process queued MUD output"""
        while not self.output_queue.empty():
            text = self.output_queue.get()
            # Normalize line endings: \r\n → \n, lone \r → \n
            text = text.replace('\r\n', '\n').replace('\r', '\n')
            
            # Add to raw buffer for room parsing (we need multi-line context)
            self._parse_buffer += text
            
            # Process display text (ANSI parsing)
            self.parse_ansi_and_add(text)
            
            # Try to find room data in buffer (may span multiple lines)
            self._parse_room_from_buffer()
            
            self.check_combat(text)
    
    def draw_map(self, rect):
        pygame.draw.rect(self.screen, (20, 20, 20), rect)
        
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
                gx = start_x + dx
                gy = start_y + dy
                
                px = rect.x + dx * tile_size
                py = rect.y + dy * tile_size
                
                if (gx, gy) == self.player_pos:
                    color = (255, 255, 0)
                    pygame.draw.rect(self.screen, color, (px, py, tile_size - 1, tile_size - 1))
                    pygame.draw.circle(self.screen, (255, 0, 0),
                                     (px + tile_size // 2, py + tile_size // 2), tile_size // 3)
                elif (gx, gy) in self.map_grid:
                    cell = self.map_grid[(gx, gy)]
                    color = TERRAIN_COLORS.get(cell.terrain, (100, 100, 100))
                    pygame.draw.rect(self.screen, color, (px, py, tile_size - 1, tile_size - 1))
                    
                    if tile_size > 12:
                        cx_tile, cy_tile = px + tile_size // 2, py + tile_size // 2
                        for ex in cell.exits:
                            if ex in DIR_VECTORS:
                                edx, edy = DIR_VECTORS[ex]
                                end_x = cx_tile + edx * tile_size // 3
                                end_y = cy_tile + edy * tile_size // 3
                                pygame.draw.line(self.screen, (200, 200, 200), 
                                               (cx_tile, cy_tile), (end_x, end_y), 1)
                else:
                    pygame.draw.rect(self.screen, (10, 10, 10), (px, py, tile_size - 1, tile_size - 1))
        
        # Room name overlay
        if self.current_room:
            name_surface = self.font.render(self.current_room, True, (255, 255, 255))
            bg_rect = name_surface.get_rect()
            bg_rect.topleft = (rect.x + 5, rect.y + 5)
            pygame.draw.rect(self.screen, (0, 0, 0), bg_rect.inflate(10, 4))
            self.screen.blit(name_surface, (rect.x + 10, rect.y + 10))
        
        # Coords
        coord_text = f"({self.player_pos[0]}, {self.player_pos[1]}) | {len(self.map_grid)} rooms"
        coord_surface = self.font.render(coord_text, True, (128, 128, 128))
        self.screen.blit(coord_surface, (rect.x + 5, rect.bottom - 20))
    
    def draw_console(self, rect):
        pygame.draw.rect(self.screen, (15, 15, 15), rect)
        
        y = rect.y + 5
        visible = (rect.height - 40) // LINE_HEIGHT - 1
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
        pygame.draw.rect(self.screen, (35, 35, 35), (rect.x, input_y - 3, rect.width, 30))
        
        prompt = ">>> "
        prompt_surface = self.font.render(prompt, True, (0, 200, 200))
        self.screen.blit(prompt_surface, (rect.x + 10, input_y))
        
        input_surface = self.font.render(self.input_text, True, (255, 255, 255))
        self.screen.blit(input_surface, (rect.x + 40, input_y))
        
        if self.cursor_visible:
            cursor_x = rect.x + 40 + self.font.size(self.input_text)[0]
            pygame.draw.line(self.screen, (255, 255, 255),
                           (cursor_x, input_y), (cursor_x, input_y + 14), 2)
    
    def draw_audio_status(self):
        """Draw audio info in corner"""
        if self.audio.music_files:
            status = f"♫ Music: {len(self.audio.music_files)} tracks"
        else:
            status = "♫ No music folder"
        
        sfx_count = sum(len(v) for v in self.audio.sfx_categories.values())
        status += f" | SFX: {sfx_count} sounds"
        
        surface = self.font.render(status, True, (100, 100, 100))
        self.screen.blit(surface, (SCREEN_WIDTH - surface.get_width() - 10, SCREEN_HEIGHT - 18))
    
    def draw(self):
        self.screen.fill((10, 10, 10))
        
        if self.layout_mode == 'horizontal':
            map_rect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT // 2 - 2)
            console_rect = pygame.Rect(0, SCREEN_HEIGHT // 2 + 2, SCREEN_WIDTH, SCREEN_HEIGHT // 2 - 2)
        else:
            map_rect = pygame.Rect(0, 0, SCREEN_WIDTH // 2 - 2, SCREEN_HEIGHT)
            console_rect = pygame.Rect(SCREEN_WIDTH // 2 + 2, 0, SCREEN_WIDTH // 2 - 2, SCREEN_HEIGHT)
        
        self.draw_map(map_rect)
        self.draw_console(console_rect)
        
        if self.layout_mode == 'horizontal':
            pygame.draw.line(self.screen, (60, 60, 60), (0, SCREEN_HEIGHT // 2), (SCREEN_WIDTH, SCREEN_HEIGHT // 2), 2)
        else:
            pygame.draw.line(self.screen, (60, 60, 60), (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT), 2)
        
        help_text = "F2: Layout | F3: Mute | Arrows: History | PgUp/PgDn: Scroll"
        help_surface = self.font.render(help_text, True, (80, 80, 80))
        self.screen.blit(help_surface, (10, SCREEN_HEIGHT - 18))
        
        self.draw_audio_status()
        
        pygame.display.flip()
    
    def run(self):
        self.connect()
        clock = pygame.time.Clock()
        
        while self.running:
            dt = clock.tick(30)
            
            self.process_output()
            
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
                    self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
                    
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
                        self.input_text = ""
                        
                    elif event.key == pygame.K_F2:
                        self.layout_mode = 'split' if self.layout_mode == 'horizontal' else 'horizontal'
                        
                    elif event.key == pygame.K_F3:
                        # Mute/unmute
                        if pygame.mixer.music.get_volume() > 0:
                            pygame.mixer.music.set_volume(0)
                            self.audio.sfx_volume = 0
                        else:
                            pygame.mixer.music.set_volume(self.audio.music_volume)
                            self.audio.sfx_volume = 0.7
                            
                    elif event.unicode.isprintable():
                        self.input_text += event.unicode
            
            self.draw()
        
        self.running = False
        self.connected = False
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
