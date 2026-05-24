# Red Dragon MUD — Evennia Contrib Integration Roadmap

> "Learn the foundation first. Map out all systems. Then build."

## Phase 1: Core Character Systems (FOUNDATION)
**Goal:** The character is the center of everything. Get stats, buffs, and traits right first.

| System | Contrib Path | Status | IOM Integration |
|--------|-------------|--------|-----------------|
| Traits (Stats) | `evennia.contrib.rpg.traits` | ✅ DONE | HP, SP, EP, Strength, Dexterity, Constitution, Intelligence, Charisma, Agility, Wisdom |
| Buffs | `evennia.contrib.rpg.buffs` | ✅ DONE | Poison, Regen, Bless, Curse, Shock, VampSunlight, GiantRoar |
| Achievements | `evennia.contrib.game_systems.achievements` | ✅ DONE | Combat, Exploration, Progression, Death, Economy, Social, RP |
| Mail | `evennia.contrib.game_systems.mail` | ✅ DONE | In-game messaging between players |

---

## Phase 2: Roleplay & Expression
**Goal:** Make the world feel alive through character expression and language.

| System | Contrib Path | Status | IOM Integration |
|--------|-------------|--------|-----------------|
| RP System (sdescs, poses, emotes) | `evennia.contrib.rpg.rpsystem` | ✅ DONE | Character sdescs replace raw names, poses visible in room, emote system |
| Languages | `evennia.contrib.rpg.rpsystem.rplanguage` | ✅ DONE | Racial languages (Drowish, Draconic, etc), language obfuscation |
| Extended Room | `evennia.contrib.grid.extended_room` | ✅ DONE | Weather, time-of-day descriptions, seasonal changes |
| Simple Door | `evennia.contrib.grid.simpledoor` | ✅ DONE | Open/close/lock/unlock doors with keys |
| In-Game Python | `evennia.contrib.base_systems.ingame_python` | ✅ DONE | Event callbacks on rooms/objects without code changes |

---

## Phase 3: Gameplay Systems
**Goal:** Core gameplay loops — combat, equipment, economy, crafting.

| System | Contrib Path | Status | IOM Integration |
|--------|-------------|--------|-----------------|
| Clothing | `evennia.contrib.game_systems.clothing` | ✅ DONE | Wearable equipment with coverage system |
| Barter | `evennia.contrib.game_systems.barter` | ✅ DONE | Player-to-player trading system |
| Crafting | `evennia.contrib.game_systems.crafting` | ✅ DONE | Formula crafting, recipes, tools |
| Cooldowns | `evennia.contrib.game_systems.cooldowns` | ✅ DONE | Skill/spell cooldowns, global cooldowns |
| Dice | `evennia.contrib.rpg.dice` | ✅ DONE | RPG dice rolling (1d20 + 5, etc) |
| Health Bar | `evennia.contrib.rpg.health_bar` | ✅ DONE | Visual HP/SP/EP bars in score display |
| Gender Sub | `evennia.contrib.game_systems.gendersub` | ✅ DONE | Pronoun-aware messaging (male/female/neutral/ambiguous) |
| Turn-Based Combat | `evennia.contrib.game_systems.turnbattle` | ⏳ PENDING | Equipment, magic, conditions, range modules (for data model) |

---

## Phase 4: Grid & World Building
**Goal:** Build the world efficiently with procedural and grid-based tools.

| System | Contrib Path | Status | IOM Integration |
|--------|-------------|--------|-----------------|
| Wilderness | `evennia.contrib.grid.wilderness` | ✅ DONE | Ocean travel with OceanMapProvider, sail/return commands |
| Slow Exit | `evennia.contrib.grid.slow_exit` | ✅ DONE | setspeed, stop commands for movement delays |
| Map Builder | `evennia.contrib.grid.mapbuilder` | ✅ DONE | @mapbuilder command for ASCII-to-room generation |
| In-Game Map Display | `evennia.contrib.grid.ingame_map_display` | ✅ DONE | ASCII mini-map with `map` command |
| XYZGrid | `evennia.contrib.grid.xyzgrid` | ⏳ PENDING | Ilium City grid builder, multi-level dungeons |

---

## Phase 5: AI & Advanced Features
**Goal:** Cutting-edge features for player engagement.

| System | Contrib Path | Status | IOM Integration |
|--------|-------------|--------|-----------------|
| LLM NPCs | `evennia.contrib.rpg.llm` | ✅ DONE | LLMNPC and SmartMob typeclasses, `talk` command |
| Character Creator | `evennia.contrib.rpg.character_creator` | ✅ DONE | Interactive chargen with race/guild selection via EvMenu |
| Containers | `evennia.contrib.game_systems.containers` | ✅ DONE | Real container system (put in bag, get from bag) |
| Storage | `evennia.contrib.game_systems.storage` | ✅ DONE | Locker/bank storage rooms with store/retrieve/list |
| In-Game Reports | `evennia.contrib.base_systems.ingame_reports` | ✅ DONE | Bug/idea/player reporting system |
| Multi-Describer | `evennia.contrib.game_systems.multidescer` | ✅ DONE | Multiple character descriptions with `+desc` command |
| Gender Sub | `evennia.contrib.game_systems.gendersub` | ✅ DONE | Pronoun-aware messaging (male/female/neutral/ambiguous) |

---

## Phase 6: Time, Calendar & Utilities
**Goal:** Developer tools, debugging, and quality of life.

| System | Contrib Path | Status | IOM Integration |
|--------|-------------|--------|-----------------|
| Custom Gametime | `evennia.contrib.base_systems.custom_gametime` | ✅ DONE | IOM calendar with 30-day months, TIME_FACTOR=2 |
| In-Game Reports | `evennia.contrib.base_systems.ingame_reports` | ✅ DONE | Bug/typo/idea reporting system |
| Auditing | `evennia.contrib.utils.auditing` | ✅ DONE | Input/output logging settings (ready to enable) |
| Menu Login | `evennia.contrib.base_systems.menu_login` | 🔄 OPTIONAL | Menu-based login available (keeping IOM-style login) |

---

## IOM-Specific Systems (Not in Contribs)
These must remain custom-built because they're unique to Islands of Myth:

| System | Status | Notes |
|--------|--------|-------|
| AI Dungeon Master | ✅ DONE | Divine intervention system with 6 personalities |
| Combat System | ✅ DONE | Tick-based real-time combat (IOM style, not turn-based) |
| Race System | ✅ DONE | 27 races with stat blocks, traits, abilities |
| Judge/Achman Leveling | ✅ DONE | Stat selection menu on level up |
| Warp Command | ✅ DONE | Recall to Adventurer's Guild |
| Chat System | ✅ DONE | `chat` command with on/off toggle |
| Who Command | ✅ DONE | IOM-style player list with flags |
| Score Display | ✅ DONE | IOM-style score output |
| Skills System | ⏳ PARTIAL | IOM skills need integration with Evennia skills |
| Spell System | ⏳ PENDING | Full spell casting system |
| Guild System | ⏳ PENDING | Warrior guild, guild levels, guild skills |
| Shop System | ⏳ PENDING | ShopKeeper NPCs with buy/sell/list |
| Bank System | ⏳ PENDING | Deposit/withdraw/balance |
| Equipment System | ⏳ PENDING | Wear/wield/remove, armor values |
| Mob AI | ⏳ PARTIAL | Wander, aggro, combat — needs expansion |
| Item System | ⏳ PENDING | Consumables, containers, quest items |
| Corpse System | ⏳ PENDING | Lootable corpses with decay |
| Death System | ⏳ PENDING | Death penalties, resurrection |
| Quest System | ⏳ PENDING | Quest tracking and rewards |
| Clan System | ⏳ PENDING | Player clans with channels |
| Auction System | ⏳ PENDING | Global auction house |
| Mail System | ✅ DONE | In-game mail (Evennia contrib) |
| Time/Weather | ✅ DONE | Extended Room contrib |

---

## Implementation Notes

### Contrib Integration Philosophy
1. **Inherit from RP base classes**: Character → `ContribRPCharacter`, Room → `ContribRPRoom`, Object → `ContribRPObject`
2. **ExtendedRoom is separate**: `ContribExtendedRoom` does not inherit from `ContribRPRoom`, so it lives as its own class for outdoor areas
3. **In-game Python via EventHandler**: The `EventHandler` script patches `DefaultObject.callbacks` at server start — no mixin changes needed
4. **Traits as canonical stats**: Use `evennia.contrib.rpg.traits` as the stat foundation; keep legacy `self.db.*` attributes in sync

### Custom Combat Decision
IOM is real-time tick-based, not turn-based. We will:
- Use `turnbattle` equipment/conditions/magic modules for the data model
- Keep our real-time tick combat core
- Adapt equipment slots and condition effects to work with our combat ticks

---

## Git Commit Strategy
- **Phase 1 commit**: `feat(contribs): Phase 1 - Traits, Buffs, Achievements, Mail`
- **Phase 2 commit**: `feat(contribs): Phase 2 - RP System, Extended Room, Simple Door, In-Game Python`
- **Phase 3 commit**: `feat(contribs): Phase 3 - Cooldowns, Dice, Equipment/Combat prep`
- **Phase 4 commit**: `feat(contribs): Phase 4 - Clothing, Barter, Crafting`
- **Phase 5+ commits**: One per major system

---

*Generated after auditing all Evennia contrib modules. Never build blind again.*
