"""
Red Dragon MUD - Judge / Leveling System
Based on Islands of Myth "Adventurers leveling place"
Uses real IOM training costs and level formulas.
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
        """Calculate gold cost to advance using real IOM training costs."""
        from world.training import get_gold_cost
        current_training_level = getattr(character.db, 'training_level', 1)
        return get_gold_cost(current_training_level)
        
    def get_xp_needed(self, character):
        """Get XP needed for next level using real IOM formula."""
        from world.training import get_exp_cost
        current_training_level = getattr(character.db, 'training_level', 1)
        return get_exp_cost(current_training_level)
        
    def can_advance(self, character):
        """Check if character can advance using real IOM costs."""
        xp_needed = self.get_xp_needed(character)
        xp_current = getattr(character.db, 'experience', 0)
        if xp_current < xp_needed:
            character.msg(f"You need {xp_needed:,} XP to advance. You have {xp_current:,}.")
            return False
            
        cost = self.get_level_cost(character)
        gold = getattr(character.db, 'gold', 0)
        if gold < cost:
            character.msg(f"You need {cost:,} gold to advance. You have {gold:,}.")
            return False
            
        return True
        
    def advance_level(self, character, stat=None, times=1):
        """Advance character using real IOM stat gains and costs."""
        from world.stats import STAT_EFFECTS, STAT_MESSAGES
        
        for i in range(times):
            if not self.can_advance(character):
                return False
                
            # Pay costs
            cost = self.get_level_cost(character)
            xp_needed = self.get_xp_needed(character)
            character.db.gold -= cost
            character.db.experience -= xp_needed
            
            # Level up
            old_level = character.db.level
            character.db.level += 1
            training_level = getattr(character.db, 'training_level', 1)
            character.db.training_level = training_level + 1
            
            # IOM stat gains on level up (from real data)
            # STR: .5hp per +1, melee hit power, weapon size, inventory
            # DEX: .5ep per +1, defensive, melee hits
            # CON: 2.5hp per +1
            # STA: 2.5ep per +1
            # INT: 2sp per +1, spell damage
            # WIS: 2sp per +1, healing power
            
            character.modify_stat('strength', 2)
            character.modify_stat('dexterity', 2)
            character.modify_stat('constitution', 1)
            character.modify_stat('intelligence', 1)
            character.modify_stat('wisdom', 1)
            character.modify_stat('stamina', 2)
            
            # Recalculate max HP/SP/EP based on real stat formulas
            self._recalculate_resources(character)
            
            # Regen bonuses
            character.db.hp_regen_bonus = getattr(character.db, 'hp_regen_bonus', 0) + 2
            character.db.sp_regen_bonus = getattr(character.db, 'sp_regen_bonus', 0) + 1
            character.db.ep_regen_bonus = getattr(character.db, 'ep_regen_bonus', 0) + 1
            
            # Full heal on level up
            character.db.hp = character.db.hp_max
            character.db.ep = character.db.ep_max
            character.db.sp = character.db.sp_max
            
            # Chosen stat gets extra bonus
            if stat:
                if stat in ['strength', 'constitution', 'dexterity', 'stamina', 
                           'intelligence', 'wisdom', 'charisma']:
                    character.modify_stat(stat, 2)
                    msg_key = stat[:3]
                    msg = STAT_MESSAGES.get(msg_key, {}).get('increase', f"You feel your {stat} increase!")
                    character.msg(msg)
                elif stat == 'hp_regen':
                    character.db.hp_regen_bonus = getattr(character.db, 'hp_regen_bonus', 0) + 2
                    character.msg("Your heart beats an extra beat.")
                elif stat == 'sp_regen':
                    character.db.sp_regen_bonus = getattr(character.db, 'sp_regen_bonus', 0) + 2
                    character.msg("Your brain pulses.")
                elif stat == 'ep_regen':
                    character.db.ep_regen_bonus = getattr(character.db, 'ep_regen_bonus', 0) + 2
                    character.msg("You feel refreshed.")
            
            # Newbie blessing message (first few levels)
            if character.db.level <= 5:
                character.msg("As you get more powerful, you feel some of the Gods newbie blessing going away.")
            
            character.msg(f"You are now level {character.db.level} with {character.db.experience:,} experience points remaining.")
            
            # Open guild levels (from IOM: each player level opens guild levels)
            open_guild = getattr(character.db, 'open_guild_levels', 0)
            character.db.open_guild_levels = open_guild + 1
        
        character.msg(f"You have advanced to level {character.db.level}!")
        return True
        
    def _recalculate_resources(self, character):
        """Recalculate max HP/SP/EP based on real IOM stat formulas."""
        from world.stats import STAT_EFFECTS
        
        str_val = getattr(character.db, 'strength', 50)
        con_val = getattr(character.db, 'constitution', 50)
        dex_val = getattr(character.db, 'dexterity', 50)
        sta_val = getattr(character.db, 'stamina', 50)
        int_val = getattr(character.db, 'intelligence', 50)
        wis_val = getattr(character.db, 'wisdom', 50)
        
        # HP = base + CON bonus + STR bonus
        con_hp = con_val * STAT_EFFECTS['con']['hp_bonus']
        str_hp = str_val * STAT_EFFECTS['str']['hp_bonus']
        character.db.hp_max = int(50 + con_hp + str_hp)
        
        # SP = base + INT bonus + WIS bonus
        int_sp = int_val * STAT_EFFECTS['int']['sp_bonus']
        wis_sp = wis_val * STAT_EFFECTS['wis']['sp_bonus']
        character.db.sp_max = int(50 + int_sp + wis_sp)
        
        # EP = base + DEX bonus + STA bonus
        dex_ep = dex_val * STAT_EFFECTS['dex']['ep_bonus']
        sta_ep = sta_val * STAT_EFFECTS['sta']['ep_bonus']
        character.db.ep_max = int(50 + dex_ep + sta_ep)
        
        # Apply hunger penalty to max resources
        from world.hunger import get_hunger_penalty
        penalty = get_hunger_penalty(character)
        if penalty < 1.0:
            character.db.hp_max = int(character.db.hp_max * penalty)
            character.db.sp_max = int(character.db.sp_max * penalty)
            character.db.ep_max = int(character.db.ep_max * penalty)


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
        xp_needed = caller.location.get_xp_needed(caller)
        xp_current = getattr(caller.db, 'experience', 0)
        
        from world.training import get_god_for_stat
        
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
Next level cost: {cost:,} gold
XP needed: {xp_needed:,} (you have {xp_current:,})
Gold on hand: {getattr(caller.db, 'gold', 0):,}

Mount Olympus Training Gods:
  STR: {get_god_for_stat('str')}  DEX: {get_god_for_stat('dex')}  CON: {get_god_for_stat('con')}
  STA: {get_god_for_stat('sta')}  INT: {get_god_for_stat('int')}  WIS: {get_god_for_stat('wis')}
        """
        caller.msg(menu)
        
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
