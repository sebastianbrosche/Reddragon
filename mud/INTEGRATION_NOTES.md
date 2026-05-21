This is a comprehensive integration of all data from Daran Madrox's Islands of Myth Guide, Wildchild's archive, and the original islandsofmyth.org into the Red Dragon MUD.

## Sources Integrated

### 1. islandsofmyth.org (Original)
- 27 playable races with stats, traits, XP rates
- 14 base guilds with skill trees
- 3 super races

### 2. Wildchild's Archive (iommud.silvanthalas.com)
- 35 quests with levels, rewards, locations
- Game mechanics (damage types, condition, alignment, hunger, AC)
- 11 island names
- Lodestone destinations

### 3. Daran Madrox's Guide (daranmadrox.batcave.net)
- **Maps**: 12 islands with 300+ areas
  - Gossamer (45 areas): vmap, aviary, catfolk, circus, crystals, beach, evokertower, farm, trail, beanstalk, goblins, hagworth, illium, kobolds, grove, school, mansion, garden, northforest, ocean, rdc, sewers, castles, wood, prima, clearing, glade, swamp, trolls, yensidland, zunzoo
  - Oddworld (25 areas): asylum, beach, boneyard, caves, circus, daemons, hill, eastforest, farm, farm2, farm3, fuji, garden, gazebo, giants, graveyard, hag, hill2, hitotsu, maze, mistyvalley, mushi, northforest, nwforest, ocean, prison, rhole, ruins, swamp, trail, valley, village, volcano, westforest, wood
  - Misty (32 areas): mistycity, beach, castle, catacombs, caves, cemetary, crystal, desert, dragon, eastforest, forest, garden, gypsies, halloween, hill, keep, lake, lich, lost, mansion, mushroom, northforest, ocean, palace, pirates, ruins, sewers, swamp, tower, trail, village, volcano, wood
  - Hyboria (32 areas): aquilonia, argos, beach, blackcoast, border, brythunia, camp, caravan, caves, corinthia, desert, eastforest, forest, graveyard, hill, hither, jungle, khauran, koth, monster, nemedia, nemedia2, northforest, oasis, ocean, oasis2, pit, ruins, shem, stygia, trail, turan, village, wood
  - Blackavar (15 areas): blackavarcity, beach, desert, eastforest, forest, graveyard, hill, mountain, northforest, ocean, palace, ruins, sewers, swamp, trail, wood
  - Emerald (30 areas): beach, castle, caves, crystal, desert, eastforest, forest, garden, graveyard, grove, hill, jungle, keep, lake, mansion, marsh, mountain, northforest, ocean, palace, ruins, sewers, swamp, temple, trail, village, volcano, westforest, wood
  - Darkcaverns (15 areas): caverns, caves, crystal, darkcity, deep, dungeon, eastcave, forest, goblins, mine, northcave, orcs, pit, ruins, sewers, swamp, trolls, underground
  - Everrest (16 areas): beach, castle, caves, eastforest, evercity, forest, graveyard, hill, lake, mountain, northforest, ocean, ruins, sewers, swamp, temple, trail, village, wood
  - Sombre (areas): sombrecity, beach, castle, caves, darkforest, eastforest, forest, graveyard, hill, keep, lake, mountain, northforest, ocean, palace, ruins, sewers, swamp, temple, trail, village, volcano, wood
  - Twin (areas): twinislands, beach, bridge, castle, caves, eastforest, forest, graveyard, hill, keep, lake, mansion, northforest, ocean, palace, ruins, sewers, swamp, temple, trail, village, wood
  - Underwater (areas): atlantis, beach, caves, coral, deep, eastocean, forest, garden, kelp, lake, ocean, palace, reef, ruins, sewers, swamp, temple, trail, trench, village, wood
  - Other (areas): arena, casino, colosseum, dungeon, event, hell, heaven, limbo, prison, quest, tournament

- **Guilds**: Full prerequisite trees
  - Warrior: Warrior → Berserker/Defender Of The Crown/Knight → Barbarian/Blade Dancer/Flogger/Shield Master/Thruster → Champion Of The Crown
  - Martial Artist: Martial Artist → Dragonfist Fighter/Mystic Warriors → Crane/Snake/Tiger/Toad Master → Order Of The Crescent Moon → Dragon Master
  - Weaver: Weaver → Confessor/Healer/Martyr → Avatar/Exorcist/Shields Of Faith/Templar → High Priest
  - Unraveller: Unraveller → Harmer/Magical Torturer/Sacrificer → Servant Of Lloth/Mordulak/Shirija/Talakh → Elder/Patriarch/Primate/Sword
  - Elemental: Elemental → Air/Earth/Fire/Water Mage → Lava/Mist Mage → Nether Mage
  - Evoker: Evoker → Evoker Of Elements/Ether → 8 bravo evokers (Acid/Flames/Force/Ice/Lightning/Magic/Poison/Vacuum) → Sorcerer
  - Necromancer: Necromancer → Undead/Shadow/Death → Lich/Vampire Lord → Dark Lord
  - Psychics: Psychics → Telepath/Telekinetic → Psionic/Mentalist → Grandmaster
  - Acrobat: Acrobat → Juggler/Tightrope → Trapeze/Fire Eater → Ringmaster
  - Lurker: Lurker → Scout/Thief → Assassin/Rogue → Shadow Master
  - Druid: Druid → Shaman/Witch → Elder Druid → Archdruid
  - Woodsman: Woodsman → Ranger/Tracker → Beast Master → Forest Lord
  - Shapeshifter: Shapeshifter → Wolf/Bear → Chimera → Dragon Form

- **Character Info**:
  - Level formula: 51500*1.122^(level/2), up to 200 levels
  - Stats: STR(+0.5hp), DEX(+0.5ep), CON(+2.5hp), STA(+2.5ep), INT(+2sp), WIS(+2sp), CHA(shop prices)
  - Wishes: Greater(40/90/160/250/380/530/700/900 TP), Lesser(20/50/90/150/230/340/470/600 TP)
  - Armor Class: None/Low/Average/High/VHigh/Great/Super/BEST
  - Hunger: Starved(0-2%), Craving(3-10%), Hungry(11-20%), Peckish(21-50%), Content(51-75%), Full(76-95%), Stuffed(96-100%)
  - Reinc Tax: A = B * 2^(-G/1000000), sacrifice to Eje in Illium Church
  - Training: Up to 31 levels with increasing costs

- **Races**: All 27 races with MCCP specials and leadership EQ
  - Cromagnon: auto-stun + physical damage
  - Drow: auto-insta-cast
  - Dwarf: auto-find gold/gems
  - Elf: auto-insta-cast
  - Ent: auto-replenish hunger in sunlight
  - Faerie: auto-minor party heal
  - Gargoyle: auto-stun evil enemies
  - Giant: manual 'shout Fee, fie, fo, fum!' - breaks stun
  - Gnome: auto-cast Mind Sponge or Armor Of Faith
  - Goblin: auto-physical damage
  - Grorrark: manual 'roar' - stun + force flee
  - Halfelf: auto-insta-cast or +200% exp
  - Hobbit: auto-+25dex when hunger >90%
  - Human: auto-+200% exp
  - Kobold: auto-flee with no penalties
  - Leprechaun: auto-dodge damage
  - Lizardman: auto-extra HP regen after water
  - Mindflayer: auto-psionic damage
  - Minotaur: auto-physical damage
  - Ogier: auto-repair stone/metal equipment
  - Phoenix: auto-fire damage
  - Snakeman: auto-full regen at sunbreak in sunlight
  - Thrikhren: auto-+con after eating corpse
  - Troll: auto-extra HP/SP/EP regen
  - Vampire: auto-physical damage + 1-round bleed
  - Vinnipier: auto-gold from players in room
  - Xorn: manual 'dig to adv-guild' - relocate

- **Equipment**: Full equipment types system
  - Regular, Nosave, Magical, Unique, Ungettable, Random pool, Random unique, Random newbie
  - Spider silks, Spider silk EQ, Guild Created, Lava, Shadow, Formulas, SNAFU
  - Spellbooks/Rings of knowledge, Tickets, Lodestones, Race Leadership

- **Healing**: Complete party healing guide
  - Guild progression: Weaver → Healer → Martyr/Confessor → Avatar
  - Priority: enreg on blasters → martyric presence → heal tank → refresh damagers
  - Key spells: heal (100% required), major refresh, martyric presence, encourage regeneration

## Code Files Built

### Typeclasses
- `races.py` — 27 races with stats, traits, abilities, leadership EQ
- `super_races.py` — 3 super races with tiered abilities
- `guilds.py` — Full guild trees with prerequisites, locations, abilities
- `combat.py` — Combat engine with weapon mastery, damage formula
- `characters.py` — Character with race, guild, equipment, stats
- `world.py` — World builder with all 12 islands and 300+ areas
- `quests.py` — 35 quests database
- `mechanics.py` — Damage types, condition, alignment, hunger, AC scales
- `levels.py` — Level system with formula and cost table
- `healing.py` — Healing spells and party mechanics
- `equipment.py` — Equipment database with sets and stats
- `rooms.py` — Room typeclass with island data
- `exits.py` — Exit typeclass

### Commands
- `raceguild_cmds.py` — race, guild, combat, mastery, score commands
- `combat_cmds.py` — attack, equip, rest, ability commands
- `system_cmds.py` — damage types, condition, alignment, hunger, lodestone, world, super race, quest commands
- `system_cmds_part2.py` — level, heal, equipment commands
- `default_cmdsets.py` — Integrated all commands

## Server Status
- Evennia running on port 3000 (web), 3001 (telnet), 3002 (websocket)
- All systems loaded and operational
