"""
Red Dragon MUD - Character Roll System
Handles random stat generation and rerolls for character creation
"""

import random
from evennia import Command, CmdSet, create_object
from evennia.commands.default.muxcommand import MuxCommand

# Stat configuration with base values and roll ranges
# Format: (base_value, min_roll, max_roll, exp_rate_mod)
# Higher rolls = better stats but may affect exp rate
STAT_CONFIG = {
    "strength":     {"base": 10, "min": 3, "max": 18, "weight": 1.0},
    "intelligence": {"base": 10, "min": 3, "max": 18, "weight": 1.0},
    "wisdom":       {"base": 10, "min": 3, "max": 18, "weight": 1.0},
    "constitution": {"base": 10, "min": 3, "max": 18, "weight": 1.0},
    "dexterity":    {"base": 10, "min": 3, "max": 18, "weight": 1.0},
    "charisma":     {"base": 10, "min": 3, "max": 18, "weight": 0.8},
}

# Exp rate calculation based on total stats
# Higher total stats = lower exp rate (harder to level)
# Lower total stats = higher exp rate (easier to level)
def calculate_exp_rate(stats):
    """
    Calculate experience gain rate based on rolled stats.
    
    Formula:
    - Base rate: 100%
    - For every point above average (10), rate drops by 2%
    - For every point below average (10), rate increases by 2%
    - Minimum: 50%, Maximum: 150%
    
    This makes high-stat characters slower to level (they're already powerful)
    and low-stat characters faster to level (compensating for weakness)
    """
    total_stats = sum(stats.values())
    average_total = len(stats) * 10  # 60 for 6 stats
    
    diff = total_stats - average_total
    rate = 100 - (diff * 2)  # Each point diff = 2% change
    
    # Clamp between 50% and 150%
    return max(50, min(150, rate))


def roll_stats():
    """
    Roll random stats for a new character.
    
    Returns:
        dict: {stat_name: rolled_value}
    """
    stats = {}
    for stat_name, config in STAT_CONFIG.items():
        # Roll stat value
        roll = random.randint(config["min"], config["max"])
        stats[stat_name] = roll
    
    return stats


def format_stats_for_display(stats, exp_rate):
    """Format stats and exp rate for display to player."""
    output = []
    output.append("|c" + "="*40 + "|n")
    output.append("|yCharacter Stats|n")
    output.append("|c" + "="*40 + "|n")
    
    for stat_name, value in stats.items():
        # Color code based on quality
        if value >= 16:
            color = "|g"  # Excellent - green
        elif value >= 12:
            color = "|y"  # Good - yellow
        elif value >= 8:
            color = "|w"  # Average - white
        else:
            color = "|r"  # Poor - red
        
        output.append(f"  {stat_name.capitalize():15s} : {color}{value:2d}|n")
    
    output.append("|c" + "-"*40 + "|n")
    
    # Total
    total = sum(stats.values())
    output.append(f"  {'Total':15s} : |w{total}|n")
    
    # Exp rate
    if exp_rate >= 120:
        rate_color = "|g"  # Fast leveling
    elif exp_rate >= 90:
        rate_color = "|y"  # Normal
    else:
        rate_color = "|r"  # Slow leveling
    
    output.append(f"  {'Exp Rate':15s} : {rate_color}{exp_rate}%|n")
    output.append("|c" + "="*40 + "|n")
    
    return "\n".join(output)


class CmdRoll(MuxCommand):
    """
    Roll character stats
    
    Usage:
        roll
        roll reroll
        roll accept
        
    Rolls random stats for your character. Unlimited rerolls.
    Once you accept, stats are permanent.
    """
    
    key = "roll"
    aliases = ["reroll", "accept"]
    locks = "cmd:all()"
    
    def func(self):
        # Check if character already has rolled stats
        if hasattr(self.caller.db, 'stats_finalized') and self.caller.db.stats_finalized:
            self.caller.msg("|rYour stats have already been finalized.|n")
            return
        
        # Handle "accept" alias
        if self.cmdstring == "accept":
            if not hasattr(self.caller.db, 'current_roll'):
                self.caller.msg("|rYou haven't rolled any stats yet. Type 'roll' first.|n")
                return
            
            # Finalize stats
            self.caller.db.stats = self.caller.db.current_roll
            self.caller.db.exp_rate = self.caller.db.current_exp_rate
            self.caller.db.stats_finalized = True
            
            self.caller.msg("|gStats accepted and finalized!|n")
            self.caller.msg(format_stats_for_display(self.caller.db.stats, self.caller.db.exp_rate))
            
            # Apply stats to traits system if available
            self._apply_to_traits()
            return
        
        # Handle reroll count - UNLIMITED REROLLS
        reroll_count = getattr(self.caller.db, 'reroll_count', 0)
        
        if self.cmdstring == "reroll" or "reroll" in self.switches:
            reroll_count += 1
        elif reroll_count == 0 and hasattr(self.caller.db, 'current_roll'):
            # First time but already has stats - they're trying to reroll without saying so
            reroll_count += 1
        
        # Roll new stats
        stats = roll_stats()
        exp_rate = calculate_exp_rate(stats)
        
        # Store current roll
        self.caller.db.current_roll = stats
        self.caller.db.current_exp_rate = exp_rate
        self.caller.db.reroll_count = reroll_count
        
        # Display
        self.caller.msg(format_stats_for_display(stats, exp_rate))
        
        self.caller.msg(f"\n|wRoll number: {reroll_count}|n")
        self.caller.msg("|yType 'roll' or 'reroll' to roll again (unlimited).|n")
        self.caller.msg("|gType 'accept' to keep these stats.|n")
    
    def _apply_to_traits(self):
        """Apply rolled stats to the Evennia traits system if available."""
        try:
            from evennia.contrib.rpg.traits import TraitHandler
            
            if hasattr(self.caller, 'traits'):
                traits = self.caller.traits
                
                # Map stat names to trait names
                stat_map = {
                    "strength": "strength",
                    "intelligence": "intelligence", 
                    "wisdom": "wisdom",
                    "constitution": "constitution",
                    "dexterity": "dexterity",
                    "charisma": "charisma",
                }
                
                for stat_name, trait_name in stat_map.items():
                    value = self.caller.db.stats.get(stat_name, 10)
                    if trait_name in traits.all:
                        traits.all[trait_name].base = value
                    else:
                        traits.add(
                            trait_name,
                            name=stat_name.capitalize(),
                            trait_type="static",
                            base=value,
                        )
                
                self.caller.msg("|gStats applied to trait system.|n")
        except Exception as e:
            self.caller.msg(f"|yNote: Could not apply to traits system: {e}|n")


class RollCmdSet(CmdSet):
    """CmdSet for character rolling."""
    
    key = "RollCmdSet"
    priority = 1
    
    def at_cmdset_creation(self):
        self.add(CmdRoll())


# Integration with Chargen
def setup_rolling_for_character(character):
    """
    Setup rolling system for a new character.
    Call this during character creation.
    """
    from evennia import CmdSet
    
    # Add roll commands
    character.cmdset.add(RollCmdSet())
    
    # Initialize roll tracking
    character.db.reroll_count = 0
    character.db.stats_finalized = False
    
    character.msg("|cWelcome to character creation!|n")
    character.msg("|wType 'roll' to generate your character's stats.|n")
    character.msg("|wUnlimited rerolls - keep rolling until you're happy!|n")
