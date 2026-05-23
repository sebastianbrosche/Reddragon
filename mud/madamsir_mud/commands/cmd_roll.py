#!/usr/bin/env python3
"""
Roll command for Myth of Islands MUD
Usage: roll <race>
Rolls 1d6 for each stat. Roll 1 = -20%, Roll 6 = +20%.
"""

import random
from evennia.commands.command import Command
from typeclasses.races import RACES

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
            # Try partial match
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
        
        self._roll_race(args, race)
    
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
    
    def _roll_race(self, race_key, race):
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
        
        for stat in all_stats:
            tier = stats.get(stat, 0)
            base = TIER_BASE.get(tier, 60)
            roll = random.randint(1, 6)
            mod = DICE_MOD[roll]
            final = int(base * mod)
            final_stats[stat] = final
            
            name = STAT_NAMES.get(stat, stat.upper())
            mod_str = f"{((mod-1)*100):+.0f}%"
            
            # Color the roll
            if roll == 6:
                roll_str = f"|g{roll}|n"
            elif roll == 1:
                roll_str = f"|r{roll}|n"
            else:
                roll_str = f"{roll}"
            
            lines.append(f"{name:<12} {base:>6} {roll_str:>6} {final:>6} {mod_str:>8}")
        
        lines.append("-" * 55)
        lines.append(f"|yXP Rate:|n {race['xp_rate']*100:.0f}%  |ySkill Cap:|n {race['skill_cap']*100:.0f}%  |ySpell Cap:|n {race['spell_cap']*100:.0f}%")
        lines.append("|c" + "="*55 + "|n")
        lines.append("Type |yaccept|n to create this character, |yroll <race>|n to reroll.")
        
        self.caller.msg("\n".join(lines))
        
        # Store rolled stats on the caller for potential acceptance
        self.caller.db._rolled_stats = final_stats
        self.caller.db._rolled_race = race_key
