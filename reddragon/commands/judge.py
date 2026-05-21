"""
Red Dragon MUD - Judge / Leveling System
Based on Islands of Myth "Adventurers leveling place"
"""

from evennia import Command
from typeclasses.rooms import Room

class JudgeRoom(Room):
    """
    The Judge room where characters level up.
    Based on IOM's "Adventurers leveling place".
    """
    
    def at_object_creation(self):
        super().at_object_creation()
        self.key = "Adventurers Leveling Place"
        self.db.desc = (
            "A grand hall of marble and gold, where adventurers come to have "
            "their deeds judged and their power measured. A stern-faced judge "
            "sits behind a high desk, quill in hand, ready to record your "
            "advancement in the great book of heroes."
        )
        self.db.area = "Ilium City"
        self.db.danger_level = 0
        self.db.is_outdoors = False
        
    def get_level_cost(self, character):
        """Calculate gold cost to advance a level."""
        return character.db.level * 50
        
    def can_advance(self, character):
        """Check if character can advance."""
        if character.db.experience < character.db.next_level:
            character.msg("You do not have enough experience to advance.")
            return False
            
        cost = self.get_level_cost(character)
        gold = getattr(character.db, 'gold', 0)
        if gold < cost:
            character.msg(f"You need {cost} gold to advance. You have {gold}.")
            return False
            
        return True
        
    def advance_level(self, character, stat=None, times=1):
        """Advance character by one or more levels."""
        for i in range(times):
            if not self.can_advance(character):
                return False
                
            cost = self.get_level_cost(character)
            character.db.gold -= cost
            
            # Level up
            old_level = character.db.level
            character.db.level += 1
            
            # ALL stats increase on every level up (from IOM log)
            character.modify_stat('strength', 2)
            character.modify_stat('dexterity', 2)
            character.modify_stat('constitution', 1)
            character.modify_stat('intelligence', 1)
            character.modify_stat('wisdom', 1)
            character.modify_stat('stamina', 2)
            
            # Regen bonuses
            character.db.hp_regen_bonus = getattr(character.db, 'hp_regen_bonus', 0) + 2
            character.db.sp_regen_bonus = getattr(character.db, 'sp_regen_bonus', 0) + 1
            character.db.ep_regen_bonus = getattr(character.db, 'ep_regen_bonus', 0) + 1
            
            # Max resources
            character.db.hp_max += 1
            character.db.ep_max += 1
            character.db.sp_max += 1
            
            # Full heal on level up
            character.db.hp = character.db.hp_max
            character.db.ep = character.db.ep_max
            character.db.sp = character.db.sp_max
            
            # Chosen stat gets extra bonus
            if stat:
                if stat in ['strength', 'constitution', 'dexterity', 'stamina', 
                           'intelligence', 'wisdom', 'charisma']:
                    character.modify_stat(stat, 2)  # Extra +2 on chosen stat
                    character.msg(f"You feel like you gained extra {stat}!")
                elif stat == 'hp_regen':
                    character.db.hp_regen_bonus = getattr(character.db, 'hp_regen_bonus', 0) + 2
                    character.msg("Your health regeneration greatly improves!")
                elif stat == 'sp_regen':
                    character.db.sp_regen_bonus = getattr(character.db, 'sp_regen_bonus', 0) + 2
                    character.msg("Your spell regeneration greatly improves!")
                elif stat == 'ep_regen':
                    character.db.ep_regen_bonus = getattr(character.db, 'ep_regen_bonus', 0) + 2
                    character.msg("Your endurance regeneration greatly improves!")
            
            # Increase next level threshold
            character.db.next_level = int(character.db.next_level * 1.5)
            
            # Newbie blessing message (first few levels)
            if character.db.level <= 5:
                character.msg("As you get more powerful, you feel some of the Gods newbie blessing going away.")
            
            character.msg(f"You are now level {character.db.level} with {character.db.experience} experience points remaining.")
            
            # Open guild levels
            open_guild = getattr(character.db, 'open_guild_levels', 0)
            character.db.open_guild_levels = open_guild + 1
        
        character.msg(f"You have advanced to level {character.db.level}!")
        return True


class CmdAdvance(Command):
    """
    Advance a level at the judge.
    
    Usage:
        advance
        advance <stat>
    """
    key = "advance"
    aliases = ["adv"]
    locks = "cmd:all()"
    
    def func(self):
        caller = self.caller
        
        # Check if in judge room
        if not isinstance(caller.location, JudgeRoom):
            caller.msg("You can only advance at the Adventurers Leveling Place.")
            return
            
        stat = self.args.strip().lower() if self.args else None
        
        caller.location.advance_level(caller, stat)


class CmdJudgeMenu(Command):
    """
    Open the judge menu.
    
    Usage:
        judge
    """
    key = "judge"
    locks = "cmd:all()"
    
    def func(self):
        caller = self.caller
        
        if not isinstance(caller.location, JudgeRoom):
            caller.msg("There is no judge here.")
            return
            
        cost = caller.location.get_level_cost(caller)
        xp_needed = caller.db.next_level - caller.db.experience
        
        menu = f"""
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
Adventurers leveling place
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
  a)  General information
  b)  List level costs
  c)  Advance a level
  d)  Advance a level picking a stat
  e)  Advance several levels
  q)  Quit
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

Your current level: {caller.db.level}
Next level cost: {cost} gold
XP needed: {xp_needed}
Gold on hand: {getattr(caller.db, 'gold', 0)}
        """
        caller.msg(menu)
        
        # Note: In a real implementation, we'd use a menu system
        # For now, direct commands work
        
class CmdPickStat(Command):
    """
    Pick a stat to advance when leveling.
    
    Usage:
        pick <stat>
    """
    key = "pick"
    locks = "cmd:all()"
    
    def func(self):
        caller = self.caller
        
        if not isinstance(caller.location, JudgeRoom):
            caller.msg("You can only pick stats at the judge.")
            return
            
        stat = self.args.strip().lower()
        
        valid_stats = [
            'strength', 'constitution', 'dexterity', 'stamina',
            'intelligence', 'wisdom', 'charisma',
            'hp_regen', 'sp_regen', 'ep_regen'
        ]
        
        if stat not in valid_stats:
            caller.msg(f"Invalid stat. Choose from: {', '.join(valid_stats)}")
            return
            
        caller.location.advance_level(caller, stat)


class CmdTalk(Command):
    """
    Talk to an NPC to open their interaction menu.
    
    Usage:
        talk <npc_name>
    """
    key = "talk"
    locks = "cmd:all()"
    
    def func(self):
        if not self.args:
            self.caller.msg("Talk to whom?")
            return
            
        target_name = self.args.strip().lower()
        
        # Find NPC in room
        npc = None
        for obj in self.caller.location.contents:
            if hasattr(obj, 'db') and hasattr(obj.db, 'is_npc') and obj.db.is_npc:
                if target_name in obj.key.lower():
                    npc = obj
                    break
                    
        if not npc:
            self.caller.msg(f"There is no {target_name} here to talk to.")
            return
            
        # Check if NPC has a custom talk handler
        if hasattr(npc, 'at_talk'):
            npc.at_talk(self.caller)
        else:
            self.caller.msg(f"{npc.key} doesn't seem interested in talking.")
