# Darkstaff MUD

A faithful recreation of the classic 1995 MUD "Red Dragon" (also known as "The Red Dragon"),
based on extensive reverse-engineering of the live **Islands of Myth** server.

## About

Red Dragon was a text-based Multi-User Dungeon that ran from 1995 and had a major community
outbreak around 2002. The new incarnation is named **Darkstaff** (after the original creator).
This project aims to preserve and recreate the exact experience using **Evennia** (Python MUD engine),
while serving as the foundation for a future 3D MMO built on Atavism + Unity.

## Islands of Myth Archive

All data in this codebase was captured from the live IOM server at `islandsofmyth.org:3000`:

- **27 Races** - Complete stat blocks, lore, skills, and racial traits
- **14 Guilds** - Warrior, Martial Artist, Druid, Woodsman, Shapeshifter, Weaver,
  Unraveller, Acrobat, Elementalist, Evoker, Abjurer, Psychic, Necromancer, Lurker
- **Ilium City** - Central hub with streets, guilds, shops, and the Adventurers Guild
- **Yensid Land** - Jolly newbie grinding area with LobeLands
- **19 Newbie Areas** - Garden, Spider Cave, Circus, Monster Daycare, Church, Ocean,
  Strawberry Fields, Fire World, Ice World, Cat World, Kobold Village, Zoo,
  Newbie Forest, Ancient Tree, Animal Nursery, Swallow Moors, Bee Hive,
  Valley of New Adventurers
- **Combat System** - Real-time round-based combat with stats, skills, corpses, loot
- **Leveling System** - Judge Achman with stat-picked advancement (strength, dexterity, etc.)
- **Admin Systems** - Detention Facility for rule enforcement

## Project Structure

```
reddragon/
├── commands/          # Game commands (combat, judge, skills, warp)
├── scripts/           # AI tick, mob spawner, game tick
├── server/conf/       # Evennia settings
├── typeclasses/       # Characters, NPCs, Rooms, Objects, Exits
├── web/               # Web client configuration
└── world/             # World builder scripts
    ├── builder.py     # Master world builder
    ├── ilium.py       # Ilium City
    ├── yensidland.py  # Yensid Land
    ├── newbie_areas.py # 19 newbie areas
    ├── detention.py   # Admin detention facility
    └── guilds.py      # Guild system
```

## Key Features

- **IOM-Style Score Display** - Exact formatting match with HP/SP/EP bars
- **27 Playable Races** - From Cromagnon to Xorn, each with unique stats
- **Round-Based Combat** - Automatic combat ticks every 3 seconds (authentic IOM feel)
- **MudOS init() Pattern** - Rooms and NPCs dynamically register commands when players enter
- **Warp/Recall System** - Return to Adventurers Guild from anywhere
- **Corpse Looting & Eating** - Essential IOM survival mechanic
- **Skill Training** - Guild-based skill advancement with gold costs
- **Mob Spawning** - Configurable spawn rates and maximum counts
- **Hidden Exits** - Search-based discovery system
- **Admin Moderation** - Detention facility for rule enforcement

## Documentation

- `docs/LPC_TO_EVENNIA.md` - Complete mapping of MudOS/LPC concepts to Evennia/Python
  (essential reading for understanding how the original MUD architecture maps to modern code)

## Running the Game

1. Install Evennia: `pip install evennia`
2. Initialize game: `evennia --init reddragon`
3. Copy these files into the game directory
4. Run: `evennia start`
5. Connect via telnet: `telnet localhost 4000`

## Credits

- **Original Red Dragon** (1995) - Unknown original authors
- **Islands of Myth** - The preservation server that keeps the flame alive
- **IOM Admins** - Zifnab, Marvin, Sigwald, Magneto, Khosan, Ixtlilton, Vor, Daneel, Saryon
- **MudOS Documentation** - https://www.lysator.liu.se/mud/MudOS-doc/ (original driver docs)
- **LPC Basics** - Descartes of Borg (1993) - https://www.lysator.liu.se/mud/BasicLPC/
- **Reverse Engineering** - Automated and manual exploration of live IOM server

## License

This is a preservation and educational project. All original Red Dragon content
remains the property of its original creators.
