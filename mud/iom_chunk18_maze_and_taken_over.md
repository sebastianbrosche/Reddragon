# Islands of Myth — Forest Maze Around Buildings + "Taken Over" Event
# Explored by Sebbe (Snakeman Lv157) — 2026-05-17

---

## CHUNK 18: FOREST MAZE SURROUNDS `#####` BUILDINGS

---

### **The Forest Maze**
The `#####` buildings (likely **Illium City**) are surrounded by a **multi-room forest maze**. All forest rooms have identical descriptions:
> "You are in a forest. Large trees form a canopy overhead. The ground is moist and fertile."

But the **map positions differ**, confirming they are distinct rooms forming a maze perimeter around the city.

**Attempted path:**
1. Forest → `south` → Forest (maze)
2. Forest → `south` → Forest (maze)
3. Forest → `south` → Forest (maze)
4. Forest → `east` → Forest (maze)
5. Forest → `enter` → Forest (no effect)
6. Forest → `south` → Forest (maze)
7. Eventually ended up on **East-West Road**

**Key insight:** The buildings cannot be reached by simple cardinal direction walking from the forest. There must be a **specific entrance path** (likely via `p` path/portal network or `=` connector rooms).

---

### Map Position Analysis — Near Buildings
```
fffff?fffffffffffffff#####fpppppp
fffff+--------------=#####=--+-----
fff/ffffffffffffffff#####fpp|ppppp
ff/ffffffff?ffffffffff=fffpp|ppppp
f/ffffffffffffffffffff|ffffp+-ccc
```

- `*` was at `ffff?fff` position — one cell northwest of `#####`
- `p` = path/portal network surrounding buildings
- `=` = bridge/connector between crossroad and buildings
- `+` = crossroad
- `ccc` = **NEW SYMBOL** (appears at bottom right, connected via `p+-`)

---

### **NEW SYMBOL: `ccc`**
First appearance in map:
```
f/ffffffffffffffffffff|ffffp+-ccc
```
- Located at end of path network, southeast of buildings
- Connected via `p` (path) → `+` (crossroad?) → `-` (connector) → `ccc`
- Possible meanings: cave cluster, city center, crystal cluster, church complex

---

### **"You are taken over by yourself, or something."**
Event captured after multiple failed navigation attempts in the maze:
```
You are taken over by yourself, or something.
```

**Possible explanations:**
1. **Auto-movement script** — the character's movement macros or aliases triggered
2. **Possession spell/ability** — another player or NPC cast a mind-control effect
3. **Maze disorientation mechanic** — the game automatically moves the player when lost
4. **Lag/connection glitch** — command buffer overflow caused erratic movement
5. **Death/reincarnation echo** — possibly related to Sebbe's 83 lifetime deaths

After this message, the character spontaneously moved to **East-West Road**.

---

### Path Network Around Buildings
The `p` symbol forms a **perimeter path** around `#####`:
```
#####fppppppp       <- north side
#####fpp|pppp       <- east side
=fffpp|ppppp        <- southeast
ffffp+-ccc          <- south side path to ccc
```

**Hypothesis:** Entering the city requires:
- Following the `p` path network to a **gate/entrance room**
- Using a **specific command** (`enter city`, `enter gate`, `enter illium`)
- Reaching an `=` connector room and using `enter`

---

*Captured during live exploration — chunk 18, 2026-05-17*
