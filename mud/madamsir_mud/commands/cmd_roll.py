#!/usr/bin/env python3
"""
Roll, Accept, and Reroll commands for Red Dragon MUD character creation.
Usage: roll <race> → shows rolled stats
       accept → applies rolled stats and enters world
       reroll → rerolls stats for currently selected race
"""

import random
from evennia.commands.command import Command
from evennia import search_object
from typeclasses.races import RACES, apply_race

# Base stat mapping from IOM tier to numeric base value
TIER_BASE = {
    -3: 30,   # Terrible
    -2: 40,   # Bad
    -1: 50,   # Below Ave
     0: 60,   # Average
     1: 70,   # Above Ave
     2: 80,   # Good
     3: 90,   # Very Good
     4: 100,  # Excellent
}

# Dice roll modifiers: roll 1 = -20%, roll 6 = +20%, linear scale
DICE_MOD = {
    1: 0.80,
    2: 0.88,
    3: 0.96,
    4: 1.04,
    5: 1.12,
    6: 1.20,
}

STAT_NAMES = {
    "strength": "STR",
    "constitution": "CON",
    "dexterity": "DEX",
    "stamina": "STA",
    "intelligence": "INT",
    "wisdom": "WIS",
    "charisma": "CHA",
    "hp_max": "HP Max",
    "hp_regen": "HP Regen",
    "ep_max": "EP Max",
    "ep_regen": "EP Regen",
    "sp_max": "SP Max",
    "sp_regen": "SP Regen",
}


def _do_roll(caller, race_key, race):
    """Perform a stat roll and return formatted output + final stats dict."""
    stats = race.get("stats", {})
    lines = []
    lines.append("|c" + "="*55 + "|n")
    lines.append(f"|G Rolling Stats: {race['name']}|n")
    lines.append("|c" + "="*55 + "|n")
    lines.append(f"{'Stat':<12} {'Base':>6} {'Roll':>6} {'Final':>6} {'Mod':>8}")
    lines.append("-" * 55)
    
    all_stats = ["strength", "constitution", "dexterity", "stamina",
                 "intelligence", "wisdom", "charisma",
                 "hp_max", "ep_max", "sp_max", 
                 "hp_regen", "ep_regen", "sp_regen"]
    
    final_stats = {}
    total_mod = 0
    
    for stat in all_stats:
        tier = stats.get(stat, 0)
        base = TIER_BASE.get(tier, 60)
        roll = random.randint(1, 6)
        mod = DICE_MOD[roll]
        final = int(base * mod)
        final_stats[stat] = final
        total_mod += (mod - 1)
        
        name = STAT_NAMES.get(stat, stat.upper())
        mod_str = f"{((mod-1)*100):+.0f}%"
        
        if roll == 6:
            roll_str = f"|g{roll}|n"
        elif roll == 1:
            roll_str = f"|r{roll}|n"
        else:
            roll_str = f"{roll}"
        
        lines.append(f"{name:<12} {base:>6} {roll_str:>6} {final:>6} {mod_str:>8}")
    
    lines.append("-" * 55)
    avg_mod = total_mod / len(all_stats) * 100
    mod_color = "g" if avg_mod >= 0 else "r"
    lines.append(f"|yXP Rate:|n {race['xp_rate']*100:.0f}%  |ySkill Cap:|n {race['skill_cap']*100:.0f}%  |ySpell Cap:|n {race['spell_cap']*100:.0f}%")
    lines.append(f"|{mod_color}Average modifier: {avg_mod:+.1f}%|n")
    lines.append("|c" + "="*55 + "|n")
    
    rerolls_left = max(0, 2 - getattr(caller.db, "_reroll_count", 0))
    lines.append(f"Type |yaccept|n to enter the world with these stats.")
    if rerolls_left > 0:
        lines.append(f"Type |yreroll|n to try again ({rerolls_left} left).")
    else:
        lines.append("|rNo rerolls remaining.|n")
    
    return "\n".join(lines), final_stats


class CmdRoll(Command):
    """
    Roll stats for a race. Classic tabletop style — 1d6 per stat.
    
    Usage:
      roll <race>        — Roll stats for a race
      roll               — Show available races
      
    Dice mechanic:
      Roll 1: base stat -20%
      Roll 2: base stat -12%
      Roll 3: base stat -4%
      Roll 4: base stat +4%
      Roll 5: base stat +12%
      Roll 6: base stat +20%
      
    You get up to 2 rerolls. Type 'accept' to finalize.
    """
    key = "roll"
    locks = "cmd:all()"

    def func(self):
        args = self.args.strip().lower()
        
        if not args or args in ("help", "list", "races"):
            self._show_races()
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
                self.caller.msg(f"|rUnknown race: '{args}'. Type 'roll' for list.|n")
                return
        
        # Reset reroll count when rolling a new race
        if getattr(self.caller.db, "_rolled_race", None) != args:
            self.caller.db._reroll_count = 0
        
        text, final_stats = _do_roll(self.caller, args, race)
        self.caller.msg(text)
        
        self.caller.db._rolled_stats = final_stats
        self.caller.db._rolled_race = args
    
    def _show_races(self):
        lines = []
        lines.append("|c" + "="*55 + "|n")
        lines.append("|GAvailable Races (27)|n")
        lines.append("|c" + "="*55 + "|n")
        for key, data in sorted(RACES.items()):
            xp = data['xp_rate']
            xp_str = f"|g{xp*100:.0f}%|n" if xp <= 1.0 else f"|r{xp*100:.0f}%|n"
            lines.append(f"  |g{data['name']:<14}|n — XP: {xp_str}")
        lines.append("|c" + "="*55 + "|n")
        lines.append("Usage: |yroll <race>|n — e.g. |yroll human|n, |yroll drow|n")
        self.caller.msg("\n".join(lines))


class CmdAccept(Command):
    """
    Accept your rolled stats and enter the world.
    
    Usage:
      accept
      
    This applies the race and stats from your last roll and
    teleports you from the Hall of Races into the world.
    """
    key = "accept"
    locks = "cmd:all()"

    def func(self):
        caller = self.caller
        rolled_race = getattr(caller.db, "_rolled_race", None)
        rolled_stats = getattr(caller.db, "_rolled_stats", None)
        
        if not rolled_race or not rolled_stats:
            caller.msg("|rYou have no rolled stats to accept. Type 'roll <race>' first.|n")
            return
        
        # Apply race
        if not apply_race(caller, rolled_race):
            caller.msg(f"|rFailed to apply race '{rolled_race}'.|n")
            return
        
        # Apply rolled stats
        for stat, value in rolled_stats.items():
            caller.attributes.add(stat, value)
        
        # Set current HP/EP/SP to max
        caller.db.hp = rolled_stats.get("hp_max", 60)
        caller.db.ep = rolled_stats.get("ep_max", 60)
        caller.db.sp = rolled_stats.get("sp_max", 60)
        
        # Find Adventurer's Guild as destination
        adv_guild = search_object("Adventurer's Guild of Illium", typeclass="typeclasses.rooms.Room")
        if not adv_guild:
            adv_guild = search_object("Adventurer Guild", typeclass="typeclasses.rooms.Room")
        if not adv_guild:
            adv_guild = search_object("Guild", typeclass="typeclasses.rooms.Room")
        
        if adv_guild:
            dest = adv_guild[0]
            caller.move_to(dest)
            caller.msg(f"|gYou have chosen the {RACES[rolled_race]['name']} race!|n")
            caller.msg(f"|gYou step through the portal and find yourself in {dest.key}.|n")
            caller.msg("|gType 'look' to see your surroundings, or 'score' to view your stats.|n")
        else:
            caller.msg("|gRace and stats applied!|n")
        
        # Clean up chargen state
        caller.db._reroll_count = None
        caller.db._rolled_stats = None
        caller.db._rolled_race = None


class CmdReroll(Command):
    """
    Reroll stats for your currently selected race.
    
    Usage:
      reroll
      
    You get up to 2 rerolls. Each reroll costs one charge.
    """
    key = "reroll"
    locks = "cmd:all()"

    def func(self):
        caller = self.caller
        rolled_race = getattr(caller.db, "_rolled_race", None)
        
        if not rolled_race:
            caller.msg("|rYou have no race selected. Type 'roll <race>' first.|n")
            return
        
        reroll_count = getattr(caller.db, "_reroll_count", 0)
        if reroll_count >= 2:
            caller.msg("|rYou have used all your rerolls. Type 'accept' to proceed.|n")
            return
        
        caller.db._reroll_count = reroll_count + 1
        race = RACES[rolled_race]
        
        text, final_stats = _do_roll(caller, rolled_race, race)
        caller.msg(text)
        
        caller.db._rolled_stats = final_stats
