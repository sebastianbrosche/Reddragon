# Emalz MUD Session Notes — Updated 2026-05-18 05:13 GMT+8

## Status: CHARACTER DETAINED
Emalz is currently in the MUD's **Detention Facility** (anti-bot jail). `warp` fails. No exits.
Cannot grind or map until released. User advised of situation in previous turn.

---

## CORRECTED YENSIDLAND EARWIG PATH (from user)
1. `warp` → `se` → `e` → `talk to sisong`
2. Pick **option 7** for Yensidland
   - *Note: earlier log showed option 9 — menu may have changed or user's info is authoritative*
3. Once in Yensidland: `nw` → `n` → `ne` → `e` → `se` → `s`
4. **Earwig density:** 2–3 earwigs per room along this circuit
5. This suggests a **6-room loop** rather than the 2-room LobeLands circuit we found earlier

### Earlier discovered LobeLands circuit (2 rooms)
- `Welcome to YENSIDLAND` → `nw` → Room 1 `[exits: southeast, north]` → `n` → Room 2 `[exits: northeast, south]`
- Each room had 3 earwigs (6 total per respawn cycle)
- User's path (`nw, n, ne, e, se, s`) may extend into additional earwig rooms beyond LobeLands

---

## NEWBIE VALLEY QUEST (from user)
- Access via Sisong's menu → pick **"newbie valley"**
- Quest: explore each room
- Targets:
  - Find **bird's nest**
  - **Dive down** in pond in **eastern corner** of the map
- This corresponds to menu option **2) "The Valley of New Adventurers"** in earlier log

---

## ILIUM CITY MAPPING PROGRESS (completed before detention)
### Central Hub
- **Adventurer Guild Entrance** — `[exits: west, south, southeast, northeast, north, southwest, east]`
- **Cloud Road** — between Gossamer Street (west) and Titan Street (east)
- **Level Room** (east of guild) — `[exits: west]` — **Achman the Judge** controls level advancement
- **Portal Room** (southwest of guild) — `[exits: shifter, abjurer, elemental, woodsman, northeast, martial_artist, lurker, druid, acrobat, weaver, evoker, unraveller, psychics, warrior]` — direct `warrior` portal
- **Myth Room** (south of guild) — `[exits: north]` — statues of original creators (Vor, Khosan, etc.)
- **Newbie Guild Entrance** — `[exits: northwest, east]`
- **Entrance to the Newbie Guild** — `[exits: west, south, east, north]` — Sisong the Newbie Navigator
- **Brightly Lit Hallway** — `[exits: south, east]` — Temuthril the Green Dragon
- **Plaque Rooms** — `[exits: east]`

### NPCs Catalogued
- **Sisong the Newbie Navigator** — Newbie Guild, provides teleport menus
- **Achman the Judge** — Level Room, handles level advancement (requires stat selection via `d` menu or `advance` command)
- **Dritthil the Ghyrdon** — Myth Room
- **Temuthril the Green Dragon** — Brightly Lit Hallway

### Key Discoveries
- Level advancement is **manual** via Achman — XP accumulates but does not auto-level
- `advance` direct command exists: "Pick a stat to advance!" → send stat name
- `warp` spell available for guild recall
- `combat silence` toggles verbose combat output (useful for data capture)

---

## CHARACTER SNAPSHOT (pre-detention)
| Field | Value |
|-------|-------|
| Level | 6 |
| XP | 1,276 |
| Next Level | 2,118 (needs 842) |
| Open Guild Levels | 2 |
| Guild Level | 645 |
| Kills | 8 |
| Gold | 1,000 |
| Str | 42 | Dex | 36 | Con | 43 | Stam | 33 | Int | 24 | Wis | 24 | Cha | 84 |
| HP | 880/880 | SP | 714/714 | EP | 634/634 |
| AC | VLow | Stealth | 15% | Size | 3'6" | Weight | 77 lb |
| Alignment | Neutral | Warrior (4) |

### Warrior Skills
- attack: 20%
- honor of the gods: 20%
- flesh of stone: 20%
- tanking: 20%
- weapon skill blunt: 20%

---

## FILES ARCHIVED
All raw transcripts saved in `/root/.openclaw/workspace/mud/iom_emalz_archive/`:
- `session_20260518.log` — initial login session
- `ilium_map.log` — Ilium city mapping attempt
- `ilium_map_data.txt` — parsed room data
- `yensid_explore.log` — Yensidland east/southeast exploration
- `yensid_nw_explore.log` — Yensidland northwest/LobeLands exploration
- `grind_final.log` — initial earwig grinding session
- Various `.expect` script files
