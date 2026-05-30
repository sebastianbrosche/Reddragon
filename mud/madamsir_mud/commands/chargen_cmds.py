"""
Red Dragon MUD — Hall of Races Commands (Chargen)
==================================================
IOM-style commands for the Hall of Races character creation area.
  all races       — list available races
  touch <race>    — select race, roll stats, and show results
  la <race>       — examine a race statue (detailed info)
  read poster     — race/guild compatibility matrix
  read sign       — help for new players
"""

from evennia import Command
from typeclasses.races import RACES, apply_race, get_race_detail, get_race_list
from commands.cmd_roll import _do_roll


# Race/Guild compatibility matrix from IOM
RACE_GUILD_MATRIX = """
    -+ This Poster gives a few hints about Races and Guilds +-
    -+ It associates some recommended races to Alpha guilds   +-

       1 - Not recommended    2 - Poor fit    3 - Decent fit    4 - Good fit (recommended)

           Warrior Martial Druid Woodsman Shapeshifter Weaver Unraveller
---------------------------------------------------------------------
Cromagnon     4       3      1      2          2         1       1
Drow          2       2      4      3          3         4       4
Dwarf         3       3      2      4          4         2       2
Elf           2       2      4      2          4         4       4
Ent           2       1      4      1          3         4       4
Faerie        1       1      4      1          2         4       4
Gargoyle      1       1      2      1          2         2       2
Giant         4       3      1      2          1         1       1
Gnome         1       1      4      1          2         4       4
Goblin        2       4      1      2          2         1       1
Grorrark      3       4      1      2          3         1       1
Halfelf       3       3      2      4          4         2       2
Hobbit        2       4      1      2          3         1       1
Human         3       3      3      4          4         3       3
Kobold        2       2      1      2          2         1       1
Leprechaun    1       1      2      1          2         2       2
Lizardman     3       3      2      4          4         2       2
Mindflayer    1       1      4      1          2         4       4
Minotaur      4       3      1      2          2         1       1
Ogier         3       4      1      2          3         1       1
Phoenix       2       2      3      2          3         3       3
Snakeman      1       1      2      1          3         2       2
Thrikhren     2       2      3      2          3         3       3
Troll         4       3      1      2          1         1       1
Vampire       2       2      3      3          4         3       3
Vinnipier     3       4      1      3          3         1       1
Xorn          4       3      1      2          1         1       1

------------------------------------------------------------------
            Acrobat Element Evoker Abjurer Psychics  Necro  Lurker
------------------------------------------------------------------
Cromagnon     2       1      1       1       1         1       2
Drow          4       3      3       4       3         3       4
Dwarf         3       1      1       2       1         1       3
Elf           4       2      2       4       2         2       4
Ent           1       3      3       4       3         3       1
Faerie        3       3      3       4       3         3       3
Gargoyle      1       4      4       2       4         4       1
Giant         2       1      1       1       1         1       2
Gnome         1       2      2       4       2         2       1
Goblin        2       1      1       1       1         1       2
Grorrark      3       1      1       1       1         1       3
Halfelf       3       2      2       3       2         2       3
Hobbit        3       1      1       1       1         1       3
Human         3       3      3       3       3         3       3
Kobold        2       1      1       1       1         1       2
Leprechaun    1       2      2       2       2         2       1
Lizardman     4       1      1       2       1         1       4
Mindflayer    1       4      4       4       4         4       1
Minotaur      2       1      1       1       1         1       2
Ogier         3       1      1       1       1         1       3
Phoenix       2       4      4       2       4         4       2
Snakeman      1       4      4       2       4         4       1
Thrikhren     2       4      4       3       4         4       2
Troll         2       1      1       1       1         1       2
Vampire       2       4      4       3       4         4       2
Vinnipier     4       1      1       1       1         1       4
Xorn          2       1      1       1       1         1       2
"""

SIGN_TEXT = """
|yThis room is where players pick their respective races.|n

Please keep in mind how you want to play, whether that is a fighter race or
are more inclined to use magic. If you are completely new to Islands of Myth,
magic using races are typically difficult to start out as — you might have more
fun in the early stages as a fighter race.

|yThe poster in this room will give you an idea of which races are suited for
which guilds.|n

You are allowed to change your race at any point in the game, however there is
a cost associated with doing that. Make your choice wisely.

|gP.S.  If you see a prompt that says --More--(XX%) that means the mud is
waiting for you to hit enter before showing you more information.|n
"""


class CmdAllRaces(Command):
    """
    List all available races.

    Usage:
      all races
      all
    """
    key = "all"
    aliases = ["races", "list races"]
    locks = "cmd:all()"

    def func(self):
        args = self.args.strip().lower()
        if args == "races" or not args:
            self.caller.msg(get_race_list())
        else:
            self.caller.msg("Usage: |yall races|n to see the list of available races.")


class CmdTouch(Command):
    """
    Touch a race statue to select it and roll your stats.
    
    Usage:
      touch <race>
      
    This selects your race and automatically rolls your stats.
    You will then see your rolled stats and can accept or reroll.
    """
    key = "touch"
    locks = "cmd:all()"

    def func(self):
        args = self.args.strip().lower()
        if not args:
            self.caller.msg("Usage: |ytouch <race>|n — e.g. |ytouch human|n, |ytouch drow|n")
            return
        
        race = RACES.get(args)
        if not race:
            matches = [k for k in RACES if args in k]
            if len(matches) == 1:
                race = RACES[matches[0]]
                args = matches[0]
            elif len(matches) > 1:
                self.caller.msg(f"|yMultiple races match '{args}': {', '.join(matches)}|n")
                return
            else:
                self.caller.msg(f"|rUnknown race: '{args}'. Type 'all races' for the list.|n")
                return
        
        # Reset reroll count when selecting a new race
        if getattr(self.caller.db, "_rolled_race", None) != args:
            self.caller.db._reroll_count = 0
        
        text, final_stats = _do_roll(self.caller, args, race)
        self.caller.msg(text)
        
        self.caller.db._rolled_stats = final_stats
        self.caller.db._rolled_race = args
        
        self.caller.msg(f"\n|gYou have touched the {race['name']} statue.|n")
        self.caller.msg("|gThe ancient magic flows through you, determining your fate...|n")


class CmdLa(Command):
    """
    Look at a race statue to examine it in detail.
    
    Usage:
      la <race>
      
    Shows full details about a race including stats, traits, and abilities.
    """
    key = "la"
    locks = "cmd:all()"

    def func(self):
        args = self.args.strip().lower()
        if not args:
            self.caller.msg("Usage: |yla <race>|n — e.g. |yla human|n, |yla drow|n")
            return
        
        if args in RACES:
            self.caller.msg(get_race_detail(args))
        else:
            matches = [k for k in RACES if args in k or args in RACES[k]["name"].lower()]
            if matches:
                self.caller.msg(get_race_detail(matches[0]))
            else:
                self.caller.msg("Race not found. Type 'all races' to see available races.")


class CmdReadChargen(Command):
    """
    Read items in the Hall of Races.
    
    Usage:
      read poster    — Race/Guild compatibility matrix
      read sign      — Help for new players
    """
    key = "read"
    locks = "cmd:all()"

    def func(self):
        args = self.args.strip().lower()
        
        if args == "poster":
            self.caller.msg(RACE_GUILD_MATRIX)
        elif args == "sign":
            self.caller.msg(SIGN_TEXT)
        else:
            self.caller.msg("You can |yread poster|n or |yread sign|n here.")
