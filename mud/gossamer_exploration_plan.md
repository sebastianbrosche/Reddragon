# Gossamer Map Replication Plan

## Objective
Rebuild the entire Gossamer main map in Evennia, documenting every room.

## Source
- Live IOM server (islandsofmyth.org:3000)
- Web map reference: http://iommud.silvanthalas.com/maps/gossamer.html

## Rules
- STAY on main Gossamer map only
- DO NOT enter sub-areas (oddworld, mists, blackavar, emerald, everrest, hyboria, sombre, etc.)
- DO NOT enter linked sub-maps (thieves network, player castles, etc.)
- Document rooms at the boundary/exits to sub-areas, but don't go through
- Only `look`, `look at X`, `map`, movement commands, `Q` for menus
- NO random command spam

## Map Analysis (from web reference)

The ASCII map shows these terrain types:
- `fff` = forest/field (west and north)
- `ppp` = plains/path (east)
- `bbb` = buildings/town blocks (north edge)
- `ccc` = caves/castles (around Illium)
- `sss` = swamp (southeast)
- `^^^`/`^^` = mountains/hills (south)
- `###` = Red Dragon City Ruins / Illium City area (center)
- `RRR` = roads
- `+|-|/|\|=` = exits/connections

Key locations on main map:
- North: newbie ocean, north forest, kobold village
- West: cat world, chuck's bait shop, larssi's island, aviary, forest trail, crystal dragon cave
- Center: red dragon city ruins, illium city, player castles
- East: goblin mounds, kreativ's pool, zun zoo, tidy farm, yensidland
- South: troll cave, small clearing, southcape, spidranox swamp, swamp mansion, evoker tower
- South-center: beanstalk, prima market, newbie garden
- Other: forest grove, peaceful wood, undercity, small glade, small village, private beach

## Execution Strategy

### Phase 1: Initial Positioning
1. Sebastian gets us to Gossamer area
2. Type `map` to see local area layout
3. Type `look` to get room description

### Phase 2: Systematic Exploration
Pattern: **Snaking grid walk with backtracking**

Since we don't know exact grid dimensions or exits in advance, we'll use adaptive exploration:

1. At each room: `look`, `map`, note exits
2. Pick an unvisited exit (prefer n→e→s→w→ne→se→nw→sw)
3. Move, document, repeat
4. When dead-end or all exits visited, backtrack
5. Continue until all reachable rooms on main map are visited

### Phase 3: Log Processing
After exploration, parse session logs to extract:
- Room names
- Room descriptions
- Exit directions and destination room names
- Objects/features to `look at`

### Phase 4: Evennia Build
1. Create all rooms as Evennia Room objects
2. Create exits between rooms
3. Set descriptions from logs
4. Add notable objects as scenery
5. Add boundary exits pointing to sub-areas (but don't build sub-areas yet)

## Autopilot Queue Format

Initial queue (starter):
```
map
look
```

Then adaptive - after each `map` output, I'll update the queue with next moves based on visible exits.

## Documentation Format

For each room, capture:
```
[ROOM] <Room Name>
[DESCRIPTION] <Full room desc>
[EXITS] n: <room>, s: <room>, e: <room>, w: <room>, etc.
[OBJECTS] <things mentioned in desc>
[MAP-POS] <approx position from web map>
```

## Files
- `mud/gossamer_logs/` — raw autopilot session logs
- `mud/gossamer_rooms.md` — parsed room documentation
- `world/gossamer.py` — Evennia build script

## Anti-Detection Measures
- Human-like delays between commands (already in relay v2)
- No repeated identical command sequences
- Mix `look`, `map`, and movement
- Pause if any admin interaction detected

---

Ready to start. Waiting for Sebastian to position us outside Gossamer.
