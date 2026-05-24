# Red Dragon MUD — Evennia Integration Roadmap

> _"Use the tested foundation. Customize the content."_

## Current State vs. Target State

| Feature | What We Have | What Evennia Provides | Integration Status |
|---|---|---|---|
| Combat | Custom `CmdKill` with basic damage | `turnbattle` with initiative, equipment, magic, conditions, range | **NOT INTEGRATED** |
| Stats | Manual `db.str`, `db.dex` etc | `traits` with gauges, counters, auto-regen, tiers | **NOT INTEGRATED** |
| Buffs/Conditions | Ad-hoc scripts | `buffs` with triggers, ticking, stacking, playtime | **NOT INTEGRATED** |
| Achievements | Custom AI DM system | `achievements` with categories, progress, prereqs | **NOT INTEGRATED** |
| AI NPCs | Custom AI DM engine | `llm` with async LLM integration, memory, prompts | **NOT INTEGRATED** |
| City Grid | Python-coded rooms/exits | `xyzgrid` with ASCII map parser, pathfinding, `goto` | **NOT INTEGRATED** |
| Mail | None | `mail` with account/character messaging | **NOT INTEGRATED** |
| RP Emotes | None | `rpsystem` with sdescs, poses, language obfuscation | **NOT INTEGRATED** |
| Wilderness | None | `wilderness` with infinite terrain, coordinate rooms | **NOT INTEGRATED** |
| In-game Scripting | None | `ingame_python` with events, callbacks, builder tools | **NOT INTEGRATED** |
| Chat | Custom `chat` command | Built-in comms | **PARTIALLY DONE** |
| Login Screen | Custom `unloggedin.py` | `menu_login` or `email_login` contribs | **CUSTOM (keep)** |
| Rooms/Exits | Custom typeclasses | Extended room, slow exit, simple door contribs | **CUSTOM (keep base)** |

---

## Phase 1: Foundation Systems (Low Risk, High Impact)

### 1.1 Traits System (`contrib.rpg.traits`)
**What it does:** Replaces manual stat attributes with a proper trait handler.
**IOM mapping:**
- Static traits: STR, DEX, CON, INT, WIS, CHA (racial base + mod)
- Gauge traits: HP, SP, EP (health, spell points, endurance)
- Counter traits: Guild skills (Warrior 0-100, Thief 0-100, etc.)
- Rate-based regen: HP regen in light (Vampire exception: only in dark)
**Implementation:**
- [ ] Inherit `TraitHandler` in Character typeclass
- [ ] Define all IOM stats as static traits with racial bases
- [ ] Define HP/SP/EP as gauge traits
- [ ] Define guild skills as counter traits with desc tiers
- [ ] Hook trait regen into combat tick cycle
- [ ] Update `score` command to display traits
- [ ] Update `judge` (leveling) to modify traits instead of db attributes

### 1.2 Buffs System (`contrib.rpg.buffs`)
**What it does:** Timed status effects, buffs, debuffs with modifiers.
**IOM mapping:**
- Poison: ticking damage buff
- Regeneration: ticking heal buff
- Bless: +STR modifier
- Shock: -DEX modifier
- Vampire sunlight: damage over time in light rooms
- Giant "Fee fie fo fum": self-buff that breaks shock
**Implementation:**
- [ ] Add `BuffHandler` to Character typeclass
- [ ] Create base IOM buff classes (Poison, Regen, Bless, Curse)
- [ ] Hook buff checking into combat damage (taken_damage trigger)
- [ ] Hook buff ticking into global game tick
- [ ] Update `score`/`affects` command to show active buffs

### 1.3 Mail System (`contrib.game_systems.mail`)
**What it does:** In-game mail between accounts or characters.
**IOM mapping:** IOM has a mail system. Players can send messages to offline players.
**Implementation:**
- [ ] Add `CmdMail` to AccountCmdSet
- [ ] Add `CmdMailCharacter` to CharacterCmdSet (optional)
- [ ] Test sending/receiving mail
- [ ] Add mail notification on login

---

## Phase 2: Combat & RPG Core (Medium Risk, High Impact)

### 2.1 Turn-Based Combat (`contrib.game_systems.turnbattle`)
**What it does:** Full D&D-style turn combat with initiative, turn order, timed decisions.
**IOM mapping:** IOM is NOT turn-based — it's real-time tick combat. However, `turnbattle` provides the framework we can adapt.
**Decision:** Use `turnbattle.tb_basic` as reference, but keep real-time tick-based combat (IOM style). Still integrate:
- Equipment modifiers (from `tb_equip`)
- Conditions/status effects (from `tb_items`)
- Magic/spell system (from `tb_magic`)
- Abstract positioning (from `tb_range`) — optional
**Implementation:**
- [ ] Study `tb_basic.py` combat flow
- [ ] Integrate equipment system: weapons, armor, wield/don commands
- [ ] Integrate conditions: poison, stun, blind, etc.
- [ ] Integrate magic system: spell casting with MP cost
- [ ] Adapt to real-time tick instead of turn order
- [ ] Update `kill` command to use new combat framework

### 2.2 Achievements System (`contrib.game_systems.achievements`)
**What it does:** Track player achievements with categories, progress counts, prerequisites.
**IOM mapping:**
- First login: "Welcome to Myth of Islands"
- Kill 10 rats: "The Usual"
- Kill 10 dire rats: "Once More, But Bigger" (prereq: 10 rats)
- Reach level 10: "Novice Adventurer"
- Reach level 50: "Seasoned Warrior"
- Explore 100 rooms: "Wanderer"
- Die 10 times: "Persistent"
**Implementation:**
- [ ] Create `world/achievements.py` with all IOM achievement definitions
- [ ] Add `ACHIEVEMENT_CONTRIB_MODULES` to settings
- [ ] Add `CmdAchieve` to CharacterCmdSet
- [ ] Track achievements on: login, kill, level up, explore, death, buy, sell
- [ ] Display achievement unlocks with fanfare

---

## Phase 3: World Building & Grid (Medium Risk, High Value)

### 3.1 XYZGrid (`contrib.grid.xyzgrid`)
**What it does:** Build world from ASCII maps with auto-spawn, pathfinding, auto-walk.
**IOM mapping:**
- Draw Ilium City as ASCII map
- Spawn entire city from map string
- Players can `goto <location>` with auto-walk
- In-game `map` command shows local area
**Implementation:**
- [ ] Install xyzgrid (add commands, settings, launcher)
- [ ] Draw Ilium City ASCII map from our existing grid
- [ ] Define map legend with room prototypes
- [ ] Add transitions to non-grid areas (Guild, Yensid Land)
- [ ] Test `goto`, `path`, `map` commands
- [ ] Rebuild Gossamer, Yensid Land, other areas as xyzgrid maps

### 3.2 Wilderness System (`contrib.grid.wilderness`)
**What it does:** Infinite terrain without infinite rooms — recycled room with dynamic descriptions.
**IOM mapping:**
- Ocean sailing between islands
- Forests between cities
- Deserts, plains, swamps
**Implementation:**
- [ ] Create wilderness map provider for ocean areas
- [ ] Add `enter_wilderness` command or exit
- [ ] Customize coordinate-based descriptions
- [ ] Add random encounters in wilderness

### 3.3 Extended Room Features
**What it does:** Weather, seasons, time-of-day room descriptions.
**IOM mapping:** IOM rooms have static descriptions, but extended room could enhance immersion.
**Implementation:**
- [ ] Add `extended_room` typeclass for outdoor rooms
- [ ] Configure weather cycles for Ilium City
- [ ] Time-of-day description variations

---

## Phase 4: Social & RP Systems (Low Risk, Medium Impact)

### 4.1 RP System (`contrib.rpg.rpsystem`)
**What it does:** Advanced emotes with sdescs, recognition, poses, masks, language support.
**IOM mapping:**
- sdescs: "a tall man", "a kobold warrior" instead of player names
- poses: "standing by the bar", "leaning against the wall"
- language: racial languages (Orcish, Elvish, Draconic)
- masks: hide identity
**Implementation:**
- [ ] Inherit `ContribRPCharacter`, `ContribRPRoom`, `ContribRPObject`
- [ ] Add `RPSystemCmdSet` to CharacterCmdSet
- [ ] Set default sdescs on character creation (based on race)
- [ ] Configure language obfuscation for racial languages
- [ ] Add `pose` command

### 4.2 In-Game Python (`contrib.base_systems.ingame_python`)
**What it does:** Builders write Python scripts on objects in-game (like LPC softcode).
**IOM mapping:** This is essentially Evennia's answer to LPC. Perfect for IOM-style room scripts.
**Implementation:**
- [ ] Start EventHandler script
- [ ] Inherit `EventCharacter`, `EventRoom`, `EventObject`, `EventExit`
- [ ] Add `CmdCallback` (`call` command) for builders
- [ ] Set permissions: immortals edit without validation
- [ ] Document common events: `can_traverse`, `say`, `time`, `move`, `get`

---

## Phase 5: Advanced Systems (Higher Risk, Future Value)

### 5.1 LLM NPC Integration (`contrib.rpg.llm`)
**What it does:** AI-driven NPCs that respond to player `talk` using LLM APIs.
**IOM mapping:**
- NPCs with personality and memory
- Quest givers that adapt dialogue
- Shopkeepers with haggling
**Implementation:**
- [ ] Configure LLM settings (host, headers, prompt prefix)
- [ ] Add `CmdLLMTalk` to CharacterCmdSet
- [ ] Create LLMNPC typeclass for key NPCs (Judge Achman, Sisong)
- [ ] Test with local or remote LLM
- [ ] Customize prompt prefixes for IOM lore

### 5.2 Additional Game Systems
- [ ] `crafting` — Forgemaster, Alchemy, Enchanting
- [ ] `barter` — Player trading system
- [ ] `clothing` — Wearable armor layers
- [ ] `cooldowns` — Ability cooldown tracking
- [ ] `dice` — Dice rolling for RP

---

## Phase 6: Polish & Integration

### 6.1 Command Consolidation
- [ ] Audit all custom commands against Evennia defaults
- [ ] Remove redundant custom commands
- [ ] Ensure contrib commands are properly added to cmdsets
- [ ] Document all player-facing commands

### 6.2 Settings Cleanup
- [ ] Consolidate all contrib settings in `settings.py`
- [ ] Ensure no conflicting settings
- [ ] Document each setting with purpose

### 6.3 Testing Matrix
- [ ] Create test character for each race
- [ ] Test combat with equipment, magic, conditions
- [ ] Test trait progression through levels
- [ ] Test buff application/removal
- [ ] Test achievement tracking
- [ ] Test xyzgrid pathfinding
- [ ] Test mail system
- [ ] Test RP emotes and sdescs

### 6.4 Documentation
- [ ] Update `README.md` with all integrated systems
- [ ] Create player guide for new features
- [ ] Create builder guide for in-game scripting
- [ ] Document IOM-specific customizations

---

## Files to Create/Modify

### New Files
- `world/achievements.py` — IOM achievement definitions
- `world/buffs.py` — IOM-specific buff classes
- `world/traits_config.py` — Trait setup for races/guilds
- `world/xyzgrid_illium.py` — ASCII map of Ilium City
- `world/xyzgrid_gossamer.py` — ASCII map of Gossamer
- `world/wilderness_ocean.py` — Ocean wilderness provider

### Modified Files
- `server/conf/settings.py` — Add all contrib settings
- `typeclasses/characters.py` — Add TraitHandler, BuffHandler
- `commands/default_cmdsets.py` — Add all contrib commands
- `typeclasses/rooms.py` — Add extended room features
- `typeclasses/objects.py` — Add RP object features
- `commands/combat.py` — Integrate turnbattle framework
- `typeclasses/scripts/combat.py` — Replace with turnbattle-based system

---

## Integration Philosophy

1. **Start with the foundation** — Traits and Buffs first (they underpin everything)
2. **Build upward** — Combat on top of traits/buffs, achievements on top of combat
3. **Add social layer** — Mail, RP, chat enhancements
4. **World building last** — XYZGrid and wilderness once systems are solid
5. **Customize, don't replace** — Use Evennia's hooks and overrides, not forked code
6. **Test after every integration** — One system at a time, verify, commit, move on

---

## Success Criteria

> A new player logging into Red Dragon should experience:
> - Turn-based combat with equipment, magic, and conditions
> - Character stats that auto-regenerate and have skill tiers
> - Buffs/debuffs that tick, stack, and modify combat
> - Achievements that track progress across all activities
> - A world they can `goto` through with auto-walk and in-game maps
> - Mail to other players, RP emotes with sdescs, and in-game scripting for builders
> - All of it feeling like Islands of Myth, not a generic Evennia install

---

*Roadmap created 2026-05-24. Implementation begins Phase 1 immediately.*
