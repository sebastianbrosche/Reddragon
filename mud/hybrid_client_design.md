# MUD Client Architecture — Hybrid Text + Graphics

## Vision
A standalone Windows .exe client that:
- Connects to Islands of Myth / Red Dragon via telnet
- Renders a Dwarf Fortress-style top-down tile map (16x16 tiles, 3FPS)
- Plays ambient music and SFX based on room/terrain type
- Runs on a 56.6k modem (minimal bandwidth)
- Hybrid: Full text MUD output + simple graphics overlay

## Why This Works
The MUD server stays pure text. The client:
1. Parses text output to extract room name, exits, terrain
2. Renders a local tile map from that data
3. Triggers audio based on room type
4. Sends player commands back as text

## Architecture

### Client ↔ Server Protocol
- **Primary:** Raw telnet (existing)
- **Optional enhancement:** JSON metadata over telnet escape sequences or secondary channel
- **Bandwidth target:** <1 KB/sec for text + map updates

### Rendering Engine
- **Display:** 80x25 text area + 20x20 tile map viewport
- **Tiles:** 16x16 pixel PNG sprites (grass, water, wall, tree, etc.)
- **Map:** Top-down 2D grid, revealed as player explores (fog of war)
- **FPS:** 3 frames/sec (static display, only updates on MUD output)
- **Resolution:** 800x600 window (fits on anything)

### Audio System
- **Ambient music:** Looped OGG per terrain type (forest, city, dungeon, battle)
- **SFX:** One-shot WAV for events (enter room, combat, level up, death)
- **Size:** ~10MB total compressed audio

### Tech Stack Options

#### Option A: Python + Pygame (Recommended)
- **Pros:** Fastest to prototype, easy to iterate, good docs
- **Build:** PyInstaller → single .exe
- **Size:** ~30MB with embedded Python
- **Audio:** pygame.mixer
- **Network:** telnetlib

#### Option B: Godot Engine
- **Pros:** Built-in export to .exe, better graphics pipeline, node system
- **Cons:** Learning curve, overkill for 3FPS tile map
- **Size:** ~20MB export

#### Option C: C++ + SDL2
- **Pros:** Smallest .exe (~5MB), fastest runtime
- **Cons:** Much longer dev time, manual memory management

## Map Rendering Logic

```
Client receives: "[Forest] [exits: n,e,w]"
↓
Parse: Room type = "Forest", exits = [n,e,w]
↓
Update local grid: current tile = forest
                   mark n,e,w as connected
↓
Render: Draw 20x20 viewport centered on player
        Forest tile = green tree sprite
        Unexplored = black fog
        Known but not current = dimmed tile
↓
Audio: Play "forest_ambient.ogg"
```

## Tile Set (Minimal)
- 16 terrain tiles: grass, forest, water, sand, mountain, city, dungeon, etc.
- 8 object tiles: player, NPC, door, stairs, chest, corpse
- Total: ~24 PNG files @ 16x16 = negligible size

## Bandwidth Budget (56.6k Modem)
- Text MUD output: ~500 bytes/sec average
- Map updates: 0 bytes (parsed from text)
- Audio: Local files, 0 bandwidth
- **Total:** <1 KB/sec — easily fits in 56.6k (7 KB/sec theoretical max)

## Development Phases

**Phase 1: Text Client**
- Basic telnet connection
- ANSI color rendering
- Command history
- Log file output

**Phase 2: + Tile Map**
- Parse room names to terrain types
- 2D grid map with fog of war
- 16x16 tile rendering
- Player movement tracking

**Phase 3: + Audio**
- Ambient music per terrain
- SFX triggers
- Volume controls

**Phase 4: Polish**
- Settings window
- Key remapping
- Macro buttons (n,s,e,w,look,inventory)
- Status bar (HP/MP/EXP)

## Next Step
Choose tech stack, then build Phase 1.
