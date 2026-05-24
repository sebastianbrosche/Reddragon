#!/usr/bin/env python3
"""
Red Dragon MUD - IOM Buff/Debuff Definitions
Uses Evennia's contrib.rpg.buffs system.

Each buff class defines an IOM-specific status effect.
Buffs can tick, stack, refresh, and trigger on events.
"""

from evennia.contrib.rpg.buffs import Buff

class PoisonBuff(Buff):
    """
    Poison effect - ticking damage over time.
    IOM: Caused by certain monsters, weapons, or traps.
    """
    key = "poison"
    name = "Poisoned"
    flava = "Your veins burn with venom."
    duration = 30  # 30 seconds
    tickrate = 5   # tick every 5 seconds
    stacks = 1     # doesn't stack, refreshes
    refreshes = True
    
    def on_tick(self, *args, **kwargs):
        """Apply poison damage each tick."""
        target = self.owner
        damage = 5 * self.stacks
        # Apply damage to target
        if hasattr(target, 'traits') and hasattr(target.traits, 'hp'):
            target.traits.hp.current -= damage
            target.msg(f"|rYou take {damage} poison damage!|n")
            # Sync legacy db
            target.db.hp = target.traits.hp.value
            if target.traits.hp.value <= 0:
                target.msg("|rThe poison has killed you!|n")
                # Handle death
                from commands.combat import death_drop
                death_drop(target)
        else:
            # Legacy fallback
            target.db.hp = max(0, target.db.hp - damage)
            target.msg(f"|rYou take {damage} poison damage!|n")
            if target.db.hp <= 0:
                target.msg("|rThe poison has killed you!|n")

class RegenerationBuff(Buff):
    """
    Regeneration - ticking heal over time.
    IOM: Natural regen, clerical spells, potions.
    """
    key = "regen"
    name = "Regeneration"
    flava = "Your wounds close of their own accord."
    duration = 60  # 60 seconds
    tickrate = 3   # tick every 3 seconds
    stacks = 1
    refreshes = True
    
    def on_tick(self, *args, **kwargs):
        """Heal each tick."""
        target = self.owner
        heal = 3 * self.stacks
        if hasattr(target, 'traits') and hasattr(target.traits, 'hp'):
            target.traits.hp.current = min(target.traits.hp.base, target.traits.hp.value + heal)
            target.db.hp = target.traits.hp.value
        else:
            target.db.hp = min(target.db.hp_max, target.db.hp + heal)
        
class BlessBuff(Buff):
    """
    Bless - increases Strength.
    IOM: Clerical blessing, divine favor.
    """
    key = "bless"
    name = "Blessed"
    flava = "The gods smile upon you."
    duration = 300  # 5 minutes
    stacks = 1
    refreshes = True
    
    def on_apply(self, *args, **kwargs):
        """Apply STR modifier."""
        if hasattr(self.owner, 'traits') and hasattr(self.owner.traits, 'str'):
            self.owner.traits.str.mod += 10 * self.stacks
    
    def on_remove(self, *args, **kwargs):
        """Remove STR modifier."""
        if hasattr(self.owner, 'traits') and hasattr(self.owner.traits, 'str'):
            self.owner.traits.str.mod -= 10 * self.stacks

class CurseDebuff(Buff):
    """
    Curse - decreases Dexterity.
    IOM: Necromancer spell, cursed items.
    """
    key = "curse"
    name = "Cursed"
    flava = "Dark energies sap your agility."
    duration = 300
    stacks = 1
    refreshes = True
    
    def on_apply(self, *args, **kwargs):
        if hasattr(self.owner, 'traits') and hasattr(self.owner.traits, 'dex'):
            self.owner.traits.dex.mod -= 10 * self.stacks
    
    def on_remove(self, *args, **kwargs):
        if hasattr(self.owner, 'traits') and hasattr(self.owner.traits, 'dex'):
            self.owner.traits.dex.mod += 10 * self.stacks

class ShockDebuff(Buff):
    """
    Shock - paralysis/decreased stats from fear.
    IOM: Giants can shout "Fee fie fo fum!" to break out.
    """
    key = "shock"
    name = "Shocked"
    flava = "You are frozen in terror!"
    duration = 10
    stacks = 1
    refreshes = False
    
    def on_apply(self, *args, **kwargs):
        if hasattr(self.owner, 'traits'):
            if hasattr(self.owner.traits, 'dex'):
                self.owner.traits.dex.mod -= 20
            if hasattr(self.owner.traits, 'str'):
                self.owner.traits.str.mod -= 10
    
    def on_remove(self, *args, **kwargs):
        if hasattr(self.owner, 'traits'):
            if hasattr(self.owner.traits, 'dex'):
                self.owner.traits.dex.mod += 20
            if hasattr(self.owner.traits, 'str'):
                self.owner.traits.str.mod += 10

class VampireSunlightDebuff(Buff):
    """
    Vampire Sunlight - damage in light rooms.
    IOM: Vampires only heal in dark places. Sunlight hurts them.
    """
    key = "sunlight"
    name = "Sunlight Burns"
    flava = "The sun sears your undead flesh!"
    duration = -1  # Permanent while in light
    tickrate = 5
    stacks = 1
    refreshes = True
    
    def on_tick(self, *args, **kwargs):
        target = self.owner
        damage = 8
        if hasattr(target, 'traits') and hasattr(target.traits, 'hp'):
            target.traits.hp.current -= damage
            target.db.hp = target.traits.hp.value
            target.msg("|rThe sunlight burns your skin!|n")
        else:
            target.db.hp = max(0, target.db.hp - damage)
            target.msg("|rThe sunlight burns your skin!|n")

class GiantRoarBuff(Buff):
    """
    Giant's "Fee fie fo fum!" - breaks out of shock.
    IOM: Giants shout this to break shock.
    Self-buff that removes shock.
    """
    key = "giant_roar"
    name = "Roaring"
    flava = "Fee, fie, fo, fum!"
    duration = 5
    stacks = 1
    
    def on_apply(self, *args, **kwargs):
        """Remove shock if present."""
        if hasattr(self.owner, 'buffs'):
            shock = self.owner.buffs.get("shock")
            if shock:
                self.owner.buffs.remove("shock")
                self.owner.msg("|yYour roar breaks the shock!|n")

# All buff classes for easy import
IOM_BUFFS = {
    "poison": PoisonBuff,
    "regen": RegenerationBuff,
    "bless": BlessBuff,
    "curse": CurseDebuff,
    "shock": ShockDebuff,
    "sunlight": VampireSunlightDebuff,
    "giant_roar": GiantRoarBuff,
}

def apply_buff(character, buff_key, stacks=1):
    """Convenience function to apply an IOM buff to a character."""
    if not hasattr(character, 'buffs'):
        return False
    buff_class = IOM_BUFFS.get(buff_key)
    if not buff_class:
        return False
    character.buffs.add(buff_class)
    return True

def remove_buff(character, buff_key):
    """Convenience function to remove an IOM buff."""
    if not hasattr(character, 'buffs'):
        return False
    character.buffs.remove(buff_key)
    return True
