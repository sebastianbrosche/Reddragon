# Gossamer Map Exploration — COMPLETE ROOM DATA

**New format:** Chain commands with `;` — `n;l;w;l;n;l` instead of separate lines
**Map source:** Wildchild's gossamer map at iommud.silvanthalas.com/maps/gossamer.html

## Rooms Confirmed (5 room types, 42+ room visits logged)

### 1. Sandy Beach (SE corner) — 9 visits logged
- **Exits:** west, south, southeast, southwest
- **Desc:** "You are on a long sandy beach. Waves gently lap at the sand, covering the footprints that you are making."
- **Terrain:** Coastal, beach symbol `b` on map

### 2. Ghastly Swamp — 1 visit logged
- **Exits:** northeast, west, south, southeast, northwest, north, east, southwest
- **Desc:** "Your footsteps squish as you struggle through this ghastly swamp. The odor is hideous."
- **Terrain:** Swamp, dark, s symbols on map

### 3. Badlands — 4 visits logged
- **Exits:** northeast, west, south, southeast, northwest, north, east, southwest
- **Desc:** "These tortured lands never know any respite from the cruel winds."
- **Terrain:** Barren, rocky

### 4. Forest — 12 visits logged
- **Exits:** northeast, west, south, southeast, northwest, north, east, southwest
- **Desc:** "You are in a forest. Large trees form a canopy overhead. The ground is moist and fertile."
- **Terrain:** f symbols on map, dense tree cover

### 5. Plains — 16 visits logged
- **Exits:** northeast, west, south, southeast, northwest, north, east, southwest
- **Desc:** "You are on a long rolling plain. You can see for miles in every direction. The grass is green, the breeze is cool."
- **Terrain:** p symbols on map, open grassland

## Exploration Progress

**Moves executed:** 320 + 1225 + 3175 (new batch queued) = ~4720 total moves
**Room visits logged:** 42+ (many revisits of same rooms)
**Unique room types found:** 5 (likely all gossamer terrain types)
**Coverage:** Multiple snake sweeps across the wilderness grid

## Map Symbols Decoded

From `map` command output:
- `b` = beach/sand
- `~` = water
- `f` = forest
- `p` = plains
- `s` = swamp
- `x` = badlands/rocky
- `?` = unexplored/transition
- `*` = points of interest

## For gossamer.py

```python
ROOMS = {
    'sandy_beach': {
        'name': 'Sandy Beach',
        'desc': 'You are on a long sandy beach. Waves gently lap at the sand, covering the footprints that you are making.',
        'exits': ['w', 's', 'se', 'sw'],
        'terrain': 'beach'
    },
    'ghastly_swamp': {
        'name': 'Ghastly Swamp',
        'desc': 'Your footsteps squish as you struggle through this ghastly swamp. The odor is hideous.',
        'exits': ['n', 'e', 's', 'w', 'ne', 'nw', 'se', 'sw'],
        'terrain': 'swamp'
    },
    'badlands': {
        'name': 'Badlands',
        'desc': 'These tortured lands never know any respite from the cruel winds.',
        'exits': ['n', 'e', 's', 'w', 'ne', 'nw', 'se', 'sw'],
        'terrain': 'badlands'
    },
    'forest': {
        'name': 'Forest',
        'desc': 'You are in a forest. Large trees form a canopy overhead. The ground is moist and fertile.',
        'exits': ['n', 'e', 's', 'w', 'ne', 'nw', 'se', 'sw'],
        'terrain': 'forest'
    },
    'plains': {
        'name': 'Plains',
        'desc': 'You are on a long rolling plain. You can see for miles in every direction. The grass is green, the breeze is cool.',
        'exits': ['n', 'e', 's', 'w', 'ne', 'nw', 'se', 'sw'],
        'terrain': 'plains'
    }
}
```

## Notes

- All wilderness rooms have 8 exits (full compass)
- Shopkeepers/NPCs wander through (Gab the Pawn Broker, Rufrin)
- `map` command shows terrain in a grid
- The gossamer area is a seamless wilderness grid — no doors, no locks

## UPDATE — 8 Hours Later (2026-05-22 14:33 GMT+8)

The random walk broke out of the Plains/Beach loop and discovered **40 unique room types**!

**Full discovery list (sorted by visit count):**
1. Forest — 4,528 visits
2. Plains — 2,005 visits
3. Sandy Beach — 704 visits
4. Deep River — 243 visits
5. Dark passage — 90 visits
6. On Gryffin street — 89 visits
7. Cathedral of Bones — 73 visits
8. Ghastly Swamp — 64 visits
9. Crossroad — 48 visits
10. On South Market Street — 37 visits
11. Hall of Resurrection — 35 visits
12. Badlands — 31 visits
13. Hall of Reincarnation — 28 visits
14. Outside a Market — 23 visits
15. HELL — 21 visits
16. On South Temple — 20 visits
17. Greasy Spoon — 15 visits
18. Tidy farm — 14 visits
19. North Temple — 14 visits
20. Intersection of Illuminated and South Market — 13 visits
21. Scenic Location — 13 visits
22. Outside east gate — 12 visits
23. Next to a strange wood — 12 visits
24. Path to docks — 10 visits
25. Near a Wooded Area — 10 visits
26. North of the Garden — 10 visits
27. Near a Glowing Pool — 9 visits
28. On Illuminated outside a pub — 9 visits
29. Intersection of West Periwinkle and South Market — 9 visits
30. Dense forest — 8 visits
31. Outside the village — 7 visits
32. Docks of the River Acheron — 7 visits
33. Near mounds of dirt — 6 visits
34. On West Periwinkle — 6 visits
35. Crumbling Ruins — 6 visits
36. Lurker Guild Portal Room — 5 visits
37. Intersection of Indigo and South Market — 5 visits
38. Entrance of a small glade — 2 visits
39. Road — 1 visit
40. On Cobalt street — 1 visit

**Key insight:** The gossamer wilderness connects to Ilium City streets, guild halls, rivers, and even HELL. The world is far more interconnected than the map suggested.

