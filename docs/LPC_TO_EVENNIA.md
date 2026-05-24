# LPC-to-Evennia Architecture Mapping

This document maps MudOS/LPC concepts (used by original Islands of Myth)
to their Evennia/Python equivalents. Use this as a reference when porting
original LPC code or designing new systems that feel authentically "MUD-like."

## Core Philosophy

MudOS driver theory (from LPC Basics, Descartes of Borg, 1993):
> "The driver should in no way define the nature of the game, that the
> nature of the game is to be decided by the individuals involved, and that
> you should be able to add to the game as it is being played."

Evennia follows this same philosophy - the server provides the framework,
the typeclasses and commands define the game world.

## Object Lifecycle

| MudOS/LPC | Evennia/Python | Notes |
|-----------|---------------|-------|
| `create()` | `at_object_creation()` | Initialize variables on first load. Called once per object lifetime. |
| `reset()` | `at_reset()` or `at_server_reload()` | Return object to base state. In compat mode, also used for initialization. |
| `init()` | `at_init()` | Called when object enters another object's inventory. Used to register commands. |
| `clean_up()` | `at_object_delete()` | Called before object destruction. |
| `net_dead()` | `at_disconnect()` | Called when player connection drops. |
| `catch_tell()` | `msg()` | Receive messages from other objects. |

## Command System

| MudOS/LPC | Evennia/Python | Notes |
|-----------|---------------|-------|
| `add_action("function", "verb")` | Command class in CmdSet | In LPC, objects call add_action() in init() to register commands. In Evennia, Commands are classes grouped in CmdSets. |
| `init()` | `at_init()` + `cmdset.add()` | When a player enters a room, the room's init() adds room-specific commands. Evennia: room adds its CmdSet to the player. |
| `remove_action("verb")` | `cmdset.remove()` | Remove a command from a living object. |
| `this_player()` | `caller` in Command | The player who issued the command. |
| `living(obj)` | `obj.account` or `obj.has_account` | Check if object is a player/living being. |

## LPC init() Deep Dive

MudOS init() apply (from MudOS documentation):

When move_object() moves object A into object B:
1. If A is living, A calls init() in B
2. Each living object in B's inventory calls init() in A
3. If A is living, A calls init() in each object in B's inventory

An object is "living" if enable_commands() has been called.

**Evennia equivalent:**
- `DefaultObject.at_object_receive(moved_obj, source_location)` ≈ step 1
- Living objects in room add their CmdSets to moved_obj ≈ step 2
- moved_obj (if player) adds its CmdSets to room objects ≈ step 3

## Object Types (IOM originals → Evennia)

| LPC Object | Evennia Typeclass | Description |
|------------|-------------------|-------------|
| `/std/room.c` | `typeclasses.rooms.Room` | Base room with exits, descriptions, light |
| `/std/monster.c` | `typeclasses.npcs.NPC` | Mobile NPC with combat AI |
| `/std/object.c` | `typeclasses.objects.Object` | Generic item |
| `/std/weapon.c` | `typeclasses.objects.Weapon` | Wieldable weapon |
| `/std/armour.c` | `typeclasses.objects.Armour` | Wearable armor |
| `/std/living.c` | `typeclasses.characters.Character` | Living being (player or NPC) |
| `/std/player.c` | `typeclasses.characters.Character` | Player character |
| `/std/ghost.c` | `typeclasses.characters.GhostCharacter` | Dead player ghost |
| `/std/shop.c` | `typeclasses.shops.Shopkeeper` | NPC shopkeeper |
| `/std/bank.c` | `typeclasses.shops.Bank` | Bank NPC |
| `/std/formula.c` | `typeclasses.objects.FormulaItem` | Spell formula item |
| `/std/guild_room.c` | `world.guilds.GuildRoom` | Guild training room |
| `/std/judge_room.c` | `world.ilium.JudgeRoom` | Level advancement room |

## LPC Data Types → Python

| LPC Type | Python Type | Notes |
|----------|------------|-------|
| `int` | `int` | Integer |
| `float` | `float` | Floating point |
| `string` | `str` | String |
| `object` | `ObjectDB` instance | Game object reference |
| `array` | `list` | Ordered collection |
| `mapping` | `dict` | Key-value pairs |
| `function` | `callable` | Function reference |
| `status` | `bool` | 0/1 boolean |
| `mixed` | `Any` | Any type |

## Common LPC Efuns → Evennia Utils

| LPC Efun | Evennia Equivalent | Description |
|----------|-------------------|-------------|
| `this_player()` | `caller` in commands | Current command issuer |
| `this_object()` | `self` | Current object |
| `environment(obj)` | `obj.location` | Object's container/location |
| `present(str, obj)` | `obj.search(str)` | Find object by name in inventory |
| `move_object(obj, dest)` | `obj.move_to(dest)` | Move object to destination |
| `say(str)` | `obj.msg_contents(str)` | Message to room |
| `tell_object(obj, str)` | `obj.msg(str)` | Message to specific object |
| `shout(str)` | `channels.Channel` | Broadcast to all |
| `call_other(obj, "func", args)` | `obj.func(args)` | Call function on another object |
| `find_living(str)` | `search.search_object(str)` | Find living object by name |
| `all_inventory(obj)` | `obj.contents` | All objects in inventory |
| `first_inventory(obj)` | `obj.contents[0]` | First object in inventory |
| `sizeof(arr)` | `len(arr)` | Array/mapping size |
| `explode(str, delim)` | `str.split(delim)` | Split string |
| `implode(arr, delim)` | `delim.join(arr)` | Join array |
| `capitalize(str)` | `str.capitalize()` | Capitalize string |
| `lower_case(str)` | `str.lower()` | Lowercase string |
| `upper_case(str)` | `str.upper()` | Uppercase string |
| `random(n)` | `random.randint(0, n-1)` | Random integer |
| `time()` | `time.time()` | Unix timestamp |

## IOM-Specific Systems

### Combat System (from emalz logs)

IOM uses automatic combat with rounds:
```
You are now in combat with a bat.
You hit a bat for 13 damage.
A bat hits you for 3 damage.
```

**Evennia implementation:** `commands/combat.py`
- `CmdKill` initiates combat (sets target, starts combat script)
- Combat script ticks every N seconds (IOM ~2-3s)
- Each tick: attacker hits target, target hits back (if in combat)
- Damage = weapon + str bonus - target AC
- Auto-flee at wimpy threshold

### Leveling System

IOM Judge Achman:
```
[c] Advance a level
[d] Advance a level picking a stat
[e] Advance several levels
```

**Evennia implementation:** `commands/judge.py`
- Menu-driven stat selection
- Cost increases per level
- Stat bonuses: str +2, dex +2, con +1, int +1, wis +1, sta +2
- HP/SP/EP regen increases

### Guild System

IOM guilds have:
- Guild skills (trained by practicing)
- Guild spells (learned from formulas)
- Guild XP separate from character XP
- Task points for guild advancement

**Evennia implementation:** `world/guilds.py`
- Skill dictionaries with percentage mastery
- Formula items that teach spells
- Guild XP tracking
- Task point system

### Race System

IOM races have:
- Base stat ranges (Terrible to Excellent)
- Racial traits (wings, resistances, special abilities)
- Stat caps per race
- Experience modifiers

**Evennia implementation:** `typeclasses/characters.py`
- `STAT_TIERS` mapping text to numeric values
- `modify_stat()` for stat adjustments
- Racial trait flags

## MudOS Driver Concepts

### Compat Mode vs Native Mode

MudOS has two modes:
- **Compat mode**: Uses `reset()` for both initialization and resetting
- **Native mode**: Uses `create()` for init, `reset()` for reset only

IOM likely runs in compat mode (older mudlib). The "heavily modified LIMA"
suggests native mode with custom modifications.

**Evennia equivalent:**
- `at_object_creation()` = `create()` (native)
- `at_reset()` = `reset()` (native)
- No direct compat mode equivalent - use `at_server_reload()` for resets

### Inheritance

LPC uses `#include` and inheritance:
```lpc
inherit "/std/room";
```

**Evennia equivalent:**
```python
from typeclasses.rooms import Room
class MyRoom(Room):
    pass
```

### Master Object

MudOS has a "master object" that controls:
- valid_read/write (security)
- creator_file (who owns what)
- compile_object (object creation)
- epilog (startup)

**Evennia equivalent:**
- `server/conf/locks.py` or `settings.py` for security
- `Account` typeclass for ownership
- `at_server_start()` for startup

## File Paths

IOM file structure (guessed from LPC Basics and login screen):
```
/players/        Player home directories
/std/           Standard objects (room, monster, object, etc.)
/d/             Domain directories (areas)
/cmds/          Commands
/open/          Open areas
/adm/           Admin files
/doc/           Documentation
/log/           Logs
```

## Porting Strategy

When porting original IOM LPC code:

1. **Read the LPC file** - Understand what it inherits, what variables it sets, what functions it defines
2. **Map inheritance** - Find the Evennia base class that matches
3. **Map variables** - Convert LPC variables to `self.db` attributes or Python properties
4. **Map functions** - Convert LPC functions to Python methods
5. **Map init()/add_action()** - Convert to Evennia Commands and CmdSets
6. **Test incrementally** - Load in Evennia and verify behavior

## Example: Porting an LPC Room

LPC room (`/std/room.c` style):
```lpc
inherit "/std/room";

void create() {
    ::create();
    set_property("indoors", 1);
    set("short", "A dark cave");
    set("long", "The cave is damp and cold.");
    set_exits(([
        "north": "/d/cave/room2",
        "south": "/d/cave/entrance"
    ]));
    set_items(([
        "wall": "The walls are wet."
    ]));
}

void reset() {
    ::reset();
    if (!present("bat"))
        new("/std/monster/bat")->move(this_object());
}
```

Evennia equivalent:
```python
from typeclasses.rooms import Room
from evennia import create_object

class DarkCaveRoom(Room):
    def at_object_creation(self):
        super().at_object_creation()
        self.db.indoors = True
        self.db.desc = "The cave is damp and cold."
        # Exits created by world builder
        self.db.spawn_mobs = [("npcs.Bat", 1.0, 3)]
        self.db.spawn_interval = 300
        
    def at_reset(self):
        """Called periodically - spawn mobs if below max."""
        super().at_reset()
        bats = [obj for obj in self.contents 
                if hasattr(obj, 'db') and obj.db.key == "a bat"]
        if len(bats) < 3:
            create_object("typeclasses.npcs.Bat", 
                         key="a bat", location=self)
```

## Key Differences

1. **Syntax**: LPC uses C-style braces `{}`; Python uses indentation
2. **Typing**: LPC is weakly typed; Python is strongly typed
3. **Pointers**: LPC uses pointers implicitly; Python uses references
4. **Driver interaction**: LPC objects call driver efuns; Evennia objects call framework methods
5. **Security**: LPC has `valid_read`/`valid_write`; Evennia uses `locks` strings
6. **Persistence**: LPC saves to flat files; Evennia uses Django ORM + database

## Resources

- LPC Basics by Descartes of Borg (1993): https://www.lysator.liu.se/mud/BasicLPC/
- MudOS Documentation: https://www.lysator.liu.se/mud/MudOS-doc/
- Evennia Documentation: https://www.evennia.com/docs/
- IOM Login Screen: "A heavily modified LIMA mudlib"

## Notes for Darkstaff Development

When implementing new features, ask:
1. "How would this work in LPC?"
2. "What would the original IOM mudlib do?"
3. "Does this feel authentically MUD-like?"

The goal is not to replicate MudOS exactly, but to capture the same
*feel* and *flexibility* that made LP MUDs special: a world that
can be modified while it's being played, where wizards (admins) can
shape the world in real-time.

---
*Document created 2026-05-18 by Miha (Darkstaff MUD)*
*Sources: MudOS-doc, BasicLPC by Descartes of Borg, IOM reverse-engineering*