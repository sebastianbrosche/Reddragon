# Islands of Myth — Complete Data Archive

> Central repository for all IOM game data collected for Red Dragon MUD replication.
> **Sources:** iommud.silvanthalas.com, islandsofmyth.org, live MUD sessions

---

## Table of Contents

1. [Races](#races) — 27 playable races with stats, skills, lore
2. [Guilds](#guilds) — 14 guilds with equipment, ranks, skill trees
3. [Equipment](#equipment) — Guild equipment database
4. [Domains/Maps](#domains) — 11 island domains with ASCII maps
5. [Monsters](#monsters) — Known monsters and spawn locations
6. [Quests](#quests) — Quest data (incomplete, needs more sources)
7. [Skills & Spells](#skills-spells) — Guild skill trees
8. [Commands](#commands) — IOM command reference

---

## Races {#races}

**File:** `mud/iom_race_archive_complete.md` (52KB)

### All 27 Races

| Race | Stat Focus | Special Traits |
|------|-----------|----------------|
| Cromagnon | STR/CON | Primal rage, brute strength |
| Drow | DEX/INT | Darkvision, spider affinity |
| Dwarf | CON/STR | Mining, ale mastery, darkvision |
| Elf | INT/CHA | Forest affinity, immortality (slow aging) |
| Ent | CON/WIS | Tree-form, extremely slow, nature bond |
| Faerie | DEX/CHA | Wings (cannot fly), small size, pixie dust |
| Gargoyle | STR/CON | Stone skin, flight (statue form) |
| Giant | STR/CON | Huge size, "Fee fie fo fum!" shout breaks shock |
| Gnome | INT/WIS | Tinkering, illusion affinity, small size |
| Goblin | DEX/CON | Sneaky, scavenging, repulsive |
| Grorrark | STR/CON | Roar ability (roar/roar LIV), reptilian |
| Halfelf | CHA/DEX | Human resilience + elven grace |
| Hobbit | DEX/CON | Second breakfast, lucky, small size |
| Human | Balanced | Adaptable, no penalties, quick learners |
| Kobold | DEX/INT | Cowardly, flee combat without penalty, trap affinity |
| Leprechaun | LUCK/CHA | Rainbow gold, trickster, small size |
| Lizardman | CON/STR | Regeneration, swamp affinity, cold-blooded |
| Mindflayer | INT/WIS | Psionic powers, brain eating, terrifying |
| Minotaur | STR/CON | Maze sense, charging, bull-headed |
| Ogier | STR/CON | From the Stedding, fierce warriors, huge |
| Phoenix | WIS/CON | Rebirth, fire affinity, immortal (resurrect) |
| Snakeman | INT/DEX | Created by mage, killed creator, best mages |
| Thrikhren | INT/DEX | Insectoid, hive mind potential, acid spit |
| Troll | STR/REGEN | Extreme regeneration, fire vulnerability |
| Vampire | INT/CHA | Blood drinking, undead, heal only in darkness |
| Vinnipier | CHA/??? | "Genetic mistake in elf offbreed", stagger constantly |
| Xorn | CON/STR | Can dig through solid rock (dig to <loc>), earth elemental |

### Race Archive Files
- `mud/iom_race_archive_complete.md` — Full compiled archive
- `mud/iom_race_archive_raw.txt` — Raw capture logs
- `mud/iom_race_missing.txt` — Final 7 race captures

---

## Guilds {#guilds}

**File:** `world/guild_equipment.py`

### Guild Hierarchy

```
Beta Guilds:
  Animist: Druid, Shapeshifter, Woodsman
  Cleric: Inquisitor, Weaver
  Fighter: Martial Artist, Warrior
  Mage: Abjurer, Elemental, Evoker, Necromancer
  Rogue: Acrobat, Thief

Gamma Guilds:
  Mage: Witch
```

### Guild Equipment Summary

| Guild | Equipment | Type | Key Stats |
|-------|-----------|------|-----------|
| Abjurer | mystical shield | shield | int, wis, spr |
| Acrobat | bard feathered hat | head | dex, wis, cha, avoid_hits |
| Druid | druidic staff | blunt (56 WC) | wis 46, int 37, sp_regen 56 |
| Elemental | ring of the elements | finger | wis 14, sp_regen 43, int 38 |
| Evoker | prismatic amulet | amulet | int 35, wis 25, spr 40, all resists 5 |
| Inquisitor | ceremonial robe | torso | int, wis, spr, unholy resist |
| Martial Artist | black leather gloves | hands | str, dex, hpr, epr, damage |
| Necromancer | Wooden staff | staff | int 33, wis 28, sp_regen 39 |
| Shapeshifter | Shapeshifters' Collar | neck | int 25, str/con 15, all lores 6 |
| Warrior | ornamented warrior belt | belt | hpr, str, con, phys resist |
| Weaver | holy ankh | neck | wis 35, con 25, spr 40, holy 20 |
| Woodsman | magical woodsman cloak | cloak | dex 33, str 24, hp/ep_regen 14 |
| Witch | wooden broom | blunt (45 WC) | int 45, wis 40, spr 55 |
| Thief | *Cannot join beta currently |

### Guild Ranks (7 ranks each)

Each guild has 7 ranks. Examples:
- **Druid:** Novice → Initiate of Gaia → Affiliate of Gaia → Druid of Gaia → Priest of Gaia → Master Druid → Druid Lord
- **Warrior:** Warrior trainee → Warrior → Veteran warrior → [blank] → Warrior of the crown → [blank] → [blank]
- **Witch:** Servant to the Coven → Apprentice warlock → Learning Warlock → Hex brother → [blank] → Master of the Coven → Elder warlock

---

## Equipment {#equipment}

### Equipment Slots (IOM standard)

| Slot | Description |
|------|-------------|
| head | Helmets, hats |
| neck | Amulets, collars |
| torso | Robes, armor, shirts |
| cloak | Cloaks, capes |
| belt | Belts, girdles |
| finger | Rings |
| hands | Gloves, gauntlets |
| shield | Shields (off-hand) |
| weapon | Main hand weapon |
| both | Two-handed weapon |

### Stat Abbreviations

| Abbrev | Full Name |
|--------|-----------|
| str | Strength |
| int | Intelligence |
| wis | Wisdom |
| con | Constitution |
| dex | Dexterity |
| cha | Charisma |
| spr | Spell points |
| hpr | Hit point regeneration |
| spr/sp_regen | Spell point regeneration |
| epr/ep_regen | Endurance point regeneration |
| sta | Stamina |

### Resistance Types

- physical
- fire
- cold
- electric
- poison
- acid
- magic
- holy
- unholy
- asphyxiation
- psi

---

## Domains/Maps {#domains}

**Files:** `world/maps/*.py` (11 domain modules)

### Island Domains

| Domain | Size | Terrain Features | Key Locations |
|--------|------|-----------------|---------------|
| Blackavar | 83×83 | Forest, mountains, swamp, desert, dungeon | Valley of Magic, Mt Olympus, Ruo Gen City, Merlins Keep, Mt Nevermind, Spirit Temple, Desert Storm, Dryad Forest, Valley of Giants, Goodwin Castle, Insect Mound, Forlorn Forest, Tunnel, Underworld, Draculas Castle, Blackavar City, Southern Wastes, Draejars Tower, Newbie Valley, Stony Brook Forest, Lynne Mine, Mountain Dungeon, Tavern, Mountain Path, Mindflayer City, Curly Grubb Inn, Tower of Arabidopsis, Old Church, Ankh-Morpork City, Abandoned Tower, Tower Ruins, Highland Keep, City of Bakhgrul |
| Gossamer | 33×33 | Forest, city, roads, beach | Central city grid, surrounding forest, docks |
| Sombre | 60×60 | Mixed | Various |
| Darkcaverns | 6×6 | Dungeon | Compact dungeon |
| Hyboria | 21×21 | Mixed | Conan-themed |
| Southcape | 29×29 | Coastal | Southern cape |
| Emerald | 28×28 | Forest | Green realm |
| Mists | 33×33 | Swamp/fog | Misty domain |
| Twin Islands | 40×40 | Islands | Two-island chain |
| Everrest | 46×46 | Mountains | High peaks |
| Oddworld | 32×32 | Strange | Weird terrain |

### Ferry Routes

All islands connected via ferry system:
- Gossamer ↔ Blackavar (15g, 20s)
- Gossamer ↔ Sombre (20g, 25s)
- Gossamer ↔ Twin Islands (10g, 15s)
- Blackavar ↔ Hyboria (25g, 30s)
- Blackavar ↔ Everrest (30g, 35s)
- Sombre ↔ Mists (15g, 20s)
- Sombre ↔ Southcape (20g, 25s)
- Twin Islands ↔ Emerald (15g, 20s)
- Twin Islands ↔ Oddworld (25g, 30s)
- Hyboria ↔ Darkcaverns (20g, 25s)

**Implementation:** `typeclasses/ferry.py`, `world/ferries.py`

---

## Monsters {#monsters}

### Known Monsters (from MUD sessions)

| Monster | Location | Level | Notes |
|---------|----------|-------|-------|
| earwig | Yensid Land, LobeLands | 1-3 | Grinding mob for low levels |
| bumble bee | LobeLands | ? | Flying insect |
| Sisong | Yensid Land | NPC | Quest giver, teleport to 19 newbie areas |
| Achman | Adventurer Guild | NPC | Level judge, stat trainer |

### Monster Categories (to be documented)

- Forest creatures (wolves, bears, spiders)
- Swamp creatures (slimes, lizardmen)
- Dungeon monsters (skeletons, zombies, demons)
- City guards and humanoids
- Boss monsters ( dragons, liches, etc.)

**Need more sources for complete monster database.**

---

## Quests {#quests}

### Known Quests

| Quest | Giver | Location | Description |
|-------|-------|----------|-------------|
| Sisong's Tour | Sisong | Yensid Land | Teleport to 19 newbie areas |

### Quest System Notes

- IOM uses a guild-based quest system
- Some quests require specific guild ranks
- Quest items are typically guild equipment
- Quests may involve killing specific monsters, finding items, or visiting locations

**Need more sources for complete quest database.**

---

## Skills & Spells {#skills-spells}

**File:** `mud/iom_skills_spells_archive.md`

### Skills (All Guilds)

| Skill | Guild | Cost | Effect |
|-------|-------|------|--------|
| quick chant | Multiple | SP | Faster casting |
| weaponmaster | Warrior | EP | Better weapon damage |
| dodge | Warrior | EP | Avoid attacks |
| fists of fury | Martial Artist | EP | Unarmed combat |
| dragonfist | Martial Artist | EP | Powerful strike |
| storytelling | Acrobat | SP | Buff/entertain |
| please audience | Acrobat | SP | Crowd control |
| enhance abjuration | Abjurer | SP | Stronger shields |
| lengthen abjuration | Abjurer | SP | Longer duration |
| strengthen abjuration | Abjurer | SP | More HP |
| mastery of elements | Elemental | SP | Elemental damage |
| mastery of evocation | Evoker | SP | Evocation damage |
| anatomy | Necromancer | SP | Undead creation |
| dead speak | Necromancer | SP | Communicate with dead |
| hematology | Necromancer | SP | Blood magic |
| minion control | Necromancer | SP | Control undead |
| avian lore | Shapeshifter | SP | Bird forms |
| canine lore | Shapeshifter | SP | Wolf forms |
| draconian lore | Shapeshifter | SP | Dragon forms |
| feline lore | Shapeshifter | SP | Cat forms |
| ursine lore | Shapeshifter | SP | Bear forms |
| harmony with nature | Woodsman | SP | Nature buffs |
| natural weapon lore | Woodsman | SP | Weapon crafting |
| brewing lore | Witch | SP | Potion making |
| lore of the elders | Witch | SP | Ancient magic |
| talisman ceremonies | Witch | SP | Enchantment |
| mental tide | Witch | SP | Mental attacks |
| dreamweaving lore | Witch | SP | Sleep/mind magic |
| lore of the watchers | Witch | SP | Scrying |
| mastery fo healing | Weaver | SP | Stronger heals |
| enhance healing | Weaver | SP | Healing buffs |
| crystal efficiency | Druid | SP | Crystal magic |
| lore of the soil sha | Druid | SP | Earth/nature |

### Spells (Evoker Example)

| Spell | Level | SP Cost | Damage Type |
|-------|-------|---------|-------------|
| magic missile | 1 | 5 | Magic |
| fireball | 5 | 15 | Fire |
| lightning bolt | 8 | 20 | Electric |
| cone of cold | 10 | 25 | Cold |
| prismatic spray | 15 | 35 | All |

**Complete spell list needs more documentation.**

---

## Commands {#commands}

### Core Commands

| Command | Description |
|---------|-------------|
| score | Show character stats |
| skills | Show learned skills |
| spells | Show learned spells |
| inventory / i | Show carried items |
| equipment / eq | Show worn equipment |
| look / l | Look at room or object |
| get / take | Pick up item |
| drop | Drop item |
| kill | Attack target |
| eat | Consume food |
| drink | Consume liquid |
| wear | Wear equipment |
| wield | Wield weapon |
| remove | Remove equipment |
| talk | Talk to NPC |
| warp | Recall to guild |
| ferry | Travel between islands |

### Guild Commands

| Command | Guild | Description |
|---------|-------|-------------|
| judge | Adventurer Guild | Level up, train stats |
| advance | Judge | Choose stat to increase |

---

## Character Creation System

**File:** `commands/chargen_roll.py`

### Stat Rolling

| Stat | Range | Average |
|------|-------|---------|
| Strength | 3-18 | 10 |
| Intelligence | 3-18 | 10 |
| Wisdom | 3-18 | 10 |
| Constitution | 3-18 | 10 |
| Dexterity | 3-18 | 10 |
| Charisma | 3-18 | 10 |

### Experience Rate

- **Base:** 100%
- **High stats (>60 total):** Slower (50-99%)
- **Low stats (<60 total):** Faster (101-150%)
- **Formula:** 100 - ((total - 60) × 2)
- **Clamp:** 50% minimum, 150% maximum

### Rerolls

- **Maximum:** 3 rerolls
- **Command:** `roll` or `reroll`
- **Accept:** `accept` to finalize

---

## Build System Reference

### Map Builder Usage

```
@mapbuilder world.maps.gossamer.GOSSAMER_MAP world.maps.gossamer.GOSSAMER_LEGEND
```

### Domain Builder

```
@py from world.maps import DomainBuilder; DomainBuilder.build_all(caller)
```

### Ferry Setup

```
@py from world.ferries import setup_island_ferries; setup_island_ferries()
```

---

## Data Sources

| Source | URL | Status |
|--------|-----|--------|
| Guild Equipment | iommud.silvanthalas.com/misc/guildeq.txt | ✅ Fetched |
| Links Page | iommud.silvanthalas.com/misc/links.html | ✅ Fetched |
| Main Site | iommud.silvanthalas.com | ✅ Fetched |
| Guilds Page | www.islandsofmyth.org/guilds.html | ❌ Failed |
| Races Page | www.islandsofmyth.org/races.html | ❌ Failed |
| Live MUD | islandsofmyth.org:3000 | ✅ Sessions |

---

## Missing Data (Need Sources)

1. **Complete Monster Database** — Need mob files or database dump
2. **Complete Quest Database** — Need quest files or walkthroughs
3. **Complete Equipment List** — Need non-guild equipment (random drops, shop items)
4. **Shop Inventories** — Need shop item lists
5. **Spell Database** — Need complete spell list with all guilds
6. **Skill Database** — Need complete skill list with effects/costs
7. **Area Descriptions** — Need room descriptions for all domains
8. **NPC Database** — Need all NPCs, their dialogues, and functions

---

## Evennia Integration Status

| System | Status | File |
|--------|--------|------|
| Character Rolling | ✅ | commands/chargen_roll.py |
| Guild Equipment DB | ✅ | world/guild_equipment.py |
| Ferry System | ✅ | typeclasses/ferry.py |
| Domain Maps | ✅ | world/maps/*.py |
| Terrain Builder | ✅ | world/maps/terrain.py |
| Combat System | ✅ | commands/combat.py |
| Traits/Stats | ✅ | Uses Evennia contrib |
| Buffs | ✅ | world/buffs.py |
| Clothing | ✅ | Evennia contrib |
| Crafting | ✅ | Evennia contrib |
| Mail | ✅ | Evennia contrib |
| Achievements | ✅ | Evennia contrib |

---

*Last updated: 2026-05-24*
*Next priority: Monster database, Quest system, Complete spell/skill lists*
