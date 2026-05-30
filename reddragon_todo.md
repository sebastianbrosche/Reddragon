# RedDragon MUD - TODO List

## ACTIVE TASKS

### 1. Character Creation / Login Flow
- [x] Auto-create character on new account (no more charcreate + ic)
- [x] Spawn new players in race selection room (Hall of Races exists)
- [x] Players get 1 billion EXP on creation
- [x] Admin rights granted automatically
- [x] Add `exits` command to show available exits
- [x] Implement IOM-style race selection: `all races`, `touch <race>`, `la <race>`, `read poster`, `read sign`
- [x] Log into IOM to observe live race selection and character roll mechanic
- [x] Implement IOM character roll/stat assignment mechanic (random stat variation at creation)
- [x] Add `accept` and `reroll` commands for stat rolling
- [x] Create Hall of Races room with IOM-style commands (all races, touch, la, read poster, read sign)
- [x] Build portal from Hall of Races to Adventurer Guild
- [x] Add south/north exits to Hall of Races (matching IOM layout: south→Welcome Room, north→Guild)
- [x] Race selection mandatory (accept command enforces rolled stats before world entry)

### 2. IOM Sub-Areas Integration
- [x] Hall of Races exists with 27 races available
- [x] IOM-style commands added (all races, touch, la, read poster, read sign)
- [x] Log into IOM and observe sub-areas for replication
- [ ] Map IOM areas room by room for replication (in progress)
- [x] Build portal from Hall of Races to Adventurer Guild
- [x] Add race/guild compatibility matrix poster
- [x] Add help sign for new players
- [x] Build Welcome Room (IOM starting room with tour/race-select exits)
- [x] Create Gates Room (At the Gates of Islands of Myth with portal/mirror)
- [x] Update unloggedin.py to spawn in Welcome Room instead of Hall of Races
- [ ] Add auto-channels on race selection (newbie, chat, death, myth, login)
- [ ] Change starting EXP from 1 billion to 2k (IOM accurate)
- [ ] Add handbook item on world entry
- [ ] Add 'start here' command for setting spawn location
- [x] Build detailed city: Market District, Weapon Smith, Armor Shop, General Store
- [x] Build Residential Quarter and City Park
- [x] Build Training Grounds and Sparring Arena
- [x] Build wilderness: Sandy Beach, Rocky Coastline, Shipwreck Cove
- [x] Build wilderness: Ghastly Swamp, Deeper Swamp
- [x] Build wilderness: Badlands, Canyon Depths
- [x] Build wilderness: Gossamer Forest, Open Plains
- [x] Connect all areas with proper exits and aliases

### 3. Ilium City Mobs
- [ ] Spawn random mobs in Ilium city with 1-100 HP
- [ ] Add variety: rats, thugs, stray dogs, guards, beggars
- [ ] Make some aggressive, some passive
- [ ] Add loot tables for city mobs

### 4. Economy & Shops
- [x] Shopkeepers spawned and stocked
- [ ] Test buy/sell transactions with real gold
- [ ] Verify bank commands work (deposit/withdraw/balance)
- [ ] Spawn banker NPCs in bank rooms
- [ ] Test auction system

### 5. Guilds & Leveling
- [x] Advance command works end-to-end
- [x] Guild XP from kills (10%)
- [x] Score display shows correct "To Guild Level"
- [ ] Add more guilds (Bravo guilds require level 20)
- [ ] Implement spell system for magic guilds
- [ ] Add guild prerequisites checking

### 6. Extended Grid Cleanup
- [ ] Fix duplicate exits in some rooms (Fiery Flagon shows north twice)
- [ ] Verify all shop rooms are accessible
- [ ] Add descriptions to all extended rooms
- [ ] Connect remaining sub-areas

### 7. Admin Tasks
- [x] All new characters get admin rights automatically
- [x] All new characters get 1 billion EXP
- [ ] Backfill admin rights and 1 billion EXP for EXISTING old characters
- [ ] Add @dig/@create builder commands for admins

## NOTES
- IOM Race Archive captured: 27 races with full stat blocks, traits, descriptions
- Hall of Races has: `all races`, `touch <race>`, `la <race>`, `read poster`, `read sign`
- Race selection room should be first spawn point for new characters
- Need to observe IOM live for exact prompt flow (automated telnet timing issues)
- IOM sub-areas need to be mapped and replicated
- Character roll mechanic: random stat variation at creation based on race
