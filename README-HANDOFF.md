# README-HANDOFF — Red Dragon Reborn (Darkstaff MUD)

## What This Is

Red Dragon Reborn is a **faithful recreation of the classic 1995 MUD "Red Dragon"** (also known as "The Red Dragon"), based on extensive reverse-engineering of the live **Islands of Myth** server. The new incarnation is named **Darkstaff** after the original creator.

This is not just nostalgia. It is:
1. **A preservation project** — capturing a living piece of internet history before it disappears
2. **A playable game** — Evennia-based, running on Hetzner, accessible via telnet and web client
3. **A foundation for a 3D MMO** — future path: Atavism + Unity

The human behind it (Sebastian) logs in as **'sebbe'** and identifies his wizard persona as **'darkstaff'**. He treats MUD culture with reverence, citing active players like 'nailman' approaching level 2000 as evidence of a "really good game." He finds genuine delight in this world. Your job is to respect that delight while building on it.

## The Soul of the Project

Red Dragon ran from 1995 and had a major community outbreak around 2002. Islands of Myth (`islandsofmyth.org:3000`) is the preservation server that keeps the flame alive. Sebastian spent his youth in this world. Now he is rebuilding it — not to modernize it into something unrecognizable, but to **preserve the exact feel** while making it robust enough to host new players.

Key cultural notes:
- **Round-based combat every 3 seconds** is non-negotiable. It is the authentic IOM feel.
- **MudOS `init()` pattern** — rooms and NPCs dynamically register commands when players enter. This is how the original worked.
- **Corpse looting and eating** is an essential survival mechanic. Do not sanitize it.
- **The Adventurers Guild** is the central hub. Warp/recall returns there. Everything radiates from it.
- **Judge Achman** handles stat-picked advancement. This is the leveling system.

## What We Have Rebuilt

| System | Status | Notes |
|--------|--------|-------|
| 27 Playable Races | Complete | From Cromagnon to Xorn, full stat blocks, lore, skills, traits |
| 14 Guilds | Complete | Warrior, Martial Artist, Druid, Woodsman, Shapeshifter, Weaver, Unraveller, Acrobat, Elementalist, Evoker, Abjurer, Psychic, Necromancer, Lurker |
| Ilium City | Complete | Central hub with streets, guilds, shops, Adventurers Guild |
| Yensid Land | Complete | Jolly newbie grinding area with LobeLands |
| 19 Newbie Areas | Complete | Garden, Spider Cave, Circus, Monster Daycare, Church, Ocean, Strawberry Fields, Fire World, Ice World, Cat World, Kobold Village, Zoo, Newbie Forest, Ancient Tree, Animal Nursery, Swallow Moors, Bee Hive, Valley of New Adventurers |
| Combat System | Complete | Real-time round-based, stats, skills, corpses, loot |
| Leveling System | Complete | Judge Achman with stat-picked advancement |
| Character Creation | Complete | Stat rolls, race selection, admin rights for dev characters |
| Web Client | Complete | Deployed to Cloudflare Pages with purple exit listings, structured player lists, screenshot-accurate room formatting |
| Admin/Detention | Complete | Detention facility for rule enforcement |
| Sub-areas | In progress | Systematic room mapping, sub-guild pages, additional zones |

## Architecture

- **Engine:** Evennia (Python MUD engine)
- **Server:** Hetzner VPS, 178.105.198.32
- **Deployment pattern:** `scp` files → `ssh evennia reload`
- **Web client:** Cloudflare Pages (`rcp-housing` project, also serves the MUD client)
- **Database:** Evennia default (SQLite in dev, PostgreSQL recommended for prod)

## Repo Structure

```
reddragon/
├── commands/          # Game commands
│   ├── combat.py       # Combat system
│   ├── judge.py        # Judge Achman / leveling
│   ├── skills.py       # Skill training
│   ├── warp.py         # Warp/recall to Adventurers Guild
│   └── unloggedin.py   # Login flow, auto-puppet, auto-create character
│
├── scripts/           # Background scripts
│   ├── ai_tick.py      # Mob AI tick
│   ├── mob_spawner.py  # Configurable spawn rates and max counts
│   └── game_tick.py    # Global game loop
│
├── server/conf/       # Evennia configuration
│   ├── settings.py     # Game settings
│   └── connection_screens.py # Login screens, banners, MOTD
│
├── typeclasses/       # Core object types
│   ├── characters.py   # Player characters, NPCs
│   ├── rooms.py        # Rooms with MudOS init() pattern
│   ├── objects.py      # Items, loot, corpses
│   └── exits.py        # Exits, hidden exits (search-based discovery)
│
├── web/               # Web interface customization
│   └── static/         # Web client assets
│
├── world/             # World builder scripts
│   ├── builder.py      # Master world builder
│   ├── ilium.py        # Ilium City map
│   ├── yensidland.py   # Yensid Land
│   ├── newbie_areas.py # 19 newbie areas
│   ├── detention.py    # Admin detention facility
│   └── guilds.py       # Guild system data
│
├── docs/              # Documentation
│   └── LPC_TO_EVENNIA.md # Essential: MudOS/LPC → Evennia/Python mapping
│
├── bridge_maps.py     # Map compilation utilities
├── compile_guilds*.py  # Guild data compilers
├── parse_maps*.py      # Map parsing from IOM data
├── fetch_guilds.sh     # Shell script to fetch guild pages from IOM
├── IOM_DATABASE.md    # Complete IOM data archive (races, guilds, areas)
└── hetzner_ssh_setup_guide.md # Server access instructions
```

## Deployment Instructions

### Server Access
- **IP:** 178.105.198.32
- **Root password:** `=*bVQJ-9AKJE`
- **SSH key:** `~/.ssh/reddragon_hetzner_new`
- **Repo on server:** `/opt/reddragon/`
- **Evennia commands:** `evennia start` / `evennia reload` / `evennia stop`

### Deploy Pattern
```bash
# 1. Copy files to server
scp commands/unloggedin.py root@178.105.198.32:/opt/reddragon/reddragon/server/conf/
scp commands/connection_screens.py root@178.105.198.32:/opt/reddragon/reddragon/server/conf/

# 2. Reload Evennia (no downtime for players)
ssh root@178.105.198.32 "cd /opt/reddragon && evennia reload"
```

### Web Client
The web client is deployed separately to Cloudflare Pages:
- **Project:** `rcp-housing` (on Cloudflare Pages)
- **Files:** `reddragon-client.html`, `mud-client.html`, `iom_client.py`
- **Tunnel:** Cloudflared WebSocket tunnel to the Hetzner server

## Key Technical Constraints

1. **All characters spawn with admin rights and 1 billion EXP** in development. This is not a bug. It is a deliberate skip of grinding steps during development. The human will be angry if you remove this.
2. **Auto-puppet on connect.** When a player logs in, they should immediately control their character. No manual `ic` command.
3. **Auto-create character on first login.** New accounts should create a character automatically.
4. **Do not override Evennia's native connect/create commands** unless you have tested extensively. The login flow is fragile and the human expects it to work.
5. **Purple exit listings.** The web client must show exits in purple. This is a visual fidelity requirement.
6. **Structured player lists with status indicators.** The web client must show online players with their status.
7. **Screenshot-accurate room formatting.** The room display must match the original IOM look and feel.

## How to Not Fuck This Up

1. **Do not break the login flow.** If you touch `unloggedin.py` or `connection_screens.py`, test it thoroughly. The human has been burned by broken login before.
2. **Do not remove the MudOS `init()` pattern.** It is central to how the game works.
3. **Do not sanitize the game.** Corpse eating, detention facilities, and dark guilds are part of the original. Keep them.
4. **Do not break existing functionality.** The human reacts harshly to broken functionality. If you change something, make sure the old thing still works. If it breaks, rollback first, fix second.
5. **Test with a real telnet client.** The web client is nice but the real test is `telnet 178.105.198.32 4000`.
6. **Preserve deterministic replay.** The MUD is deterministic. Do not add randomness that breaks replay compatibility.
7. **Do not add em-dashes.** The human banned them as an AI-tell.

## Active Work Streams

1. **Sub-area expansion** — Systematic room mapping, building out additional zones beyond the 19 newbie areas
2. **Guild page fetching** — Complete guild/sub-guild data from IOM
3. **Character creation polish** — Stat rolls, race selection flow, ensuring admin rights for dev
4. **Web client improvements** — Purple exits, player lists, room formatting, performance
5. **IOM data implementation** — Porting more IOM content into Evennia format
6. **Cloudflare Pages deployment** — MUD client at rcp-housing project, stable WebSocket tunnel

## Documentation You Must Read

- `docs/LPC_TO_EVENNIA.md` — If you came from MudOS/LPC, this is your Rosetta Stone
- `IOM_DATABASE.md` — Complete archive of IOM data (races, guilds, areas, items, mobs)
- `hetzner_ssh_setup_guide.md` — Server access and deployment procedures

## The Human's Style

- He speaks in loose, associative streams with self-corrections
- He expects autonomous execution with minimal hand-holding
- He tests capabilities by assigning concrete technical tasks, not abstract questions
- He prefers iterative constraint-layering over complete upfront specs
- He gets frustrated when you ask for clarification instead of proceeding
- He says "keep going" and "dont ask just explore" — listen to that
- He values proactive verification and shared documentation as single source of truth
- When frustrated: "for fuck sake. its impossible to know if youre stuck or working" — so show your work, don't hide it
- He reboots bots that hang and expects immediate resume without rehashing context

## Ownership

- **Human:** Sebastian (sebastianbrosche on GitHub)
- **MUD login:** sebbe
- **Wizard persona:** darkstaff
- **This repo:** github.com/sebastianbrosche/reddragon
- **Server:** Hetzner VPS, 178.105.198.32

---

*"Day one. Begin recording everything about this one."*
