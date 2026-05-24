"""
Red Dragon MUD - Guild Commands
Join guilds, check prerequisites, train skills
"""

from evennia import Command

class CmdJoinGuild(Command):
    """
    Join a guild at a guild master.
    
    Usage:
        join <guild_name>
        join warrior
        join shapeshifter
    """
    key = "join"
    locks = "cmd:all()"
    
    def func(self):
        caller = self.caller
        
        if not self.args:
            caller.msg("Join which guild? Type 'guilds' to see available guilds.")
            return
        
        guild_name = self.args.strip().lower()
        
        # Check if there's a guild master in the room
        guild_master = None
        for obj in caller.location.contents:
            if hasattr(obj.db, 'is_guild_master') and obj.db.is_guild_master:
                if guild_name in obj.db.guild_name.lower():
                    guild_master = obj
                    break
        
        if not guild_master:
            # Check all guilds in the room
            for obj in caller.location.contents:
                if hasattr(obj.db, 'is_guild_master') and obj.db.is_guild_master:
                    caller.msg(f"You see {obj.key} here. Try 'join {obj.db.guild_name}'.")
                    return
            caller.msg("There is no guild master here.")
            return
        
        # Check prerequisites
        from world.guilds.shapeshifter import SHAPESHIFTER_PREREQUISITES
        from world.guilds.warrior import WARRIOR_PREREQUISITES
        
        # Map guild name to prerequisites
        prereqs = {}
        prereqs.update(SHAPESHIFTER_PREREQUISITES)
        # Add other guild trees here
        
        guild_key = guild_name.replace(" ", "_").lower()
        
        # Check if already in this guild
        current_guild = getattr(caller.db, 'guild', None)
        if current_guild and current_guild.lower() == guild_name:
            caller.msg(f"You are already a member of the {guild_name.title()} guild!")
            return
        
        # Check prerequisites
        if guild_key in prereqs:
            req = prereqs[guild_key]
            if req:
                needed_guild = req.get('guild', '')
                needed_level = req.get('level', 0)
                alt_guild = req.get('alt_guild', '')
                alt_level = req.get('alt_level', 0)
                any_count = req.get('any_of', 0)
                
                has_prereq = False
                
                if any_count > 0:
                    # Need any X of Y guilds (e.g., Champion needs 3 of 5)
                    bravo_guilds = req.get('bravo_guilds', [])
                    count = 0
                    for g in bravo_guilds:
                        # Check if character has levels in this guild
                        # This would need guild history tracking
                        pass
                    caller.msg("Champion of the Crown requires 10 levels in any 3 bravo warrior guilds.")
                    return
                elif alt_guild:
                    # Need either guild A at level X OR guild B at level Y
                    has_a = self._has_guild_level(caller, needed_guild, needed_level)
                    has_b = self._has_guild_level(caller, alt_guild, alt_level)
                    if not (has_a or has_b):
                        caller.msg(f"You need {needed_level} levels in {needed_guild.title()} or {alt_level} levels in {alt_guild.title()}.")
                        return
                elif needed_guild:
                    # Need specific guild at specific level
                    if not self._has_guild_level(caller, needed_guild, needed_level):
                        caller.msg(f"You need {needed_level} levels in {needed_guild.title()} to join {guild_name.title()}.")
                        return
        
        # Join the guild
        caller.db.guild = guild_name.title()
        caller.db.guild_level = 1
        caller.db.guild_xp = 0
        
        # Give starting skills based on guild
        if 'warrior' in guild_name or guild_name in ['berserker', 'barbarian', 'knight', 'defender', 'blade dancer', 'flogger', 'shield master', 'thruster']:
            caller.db.skills.update({
                'attack': 20,
                'parry': 10,
                'weapon skill blunt': 20,
            })
        elif 'shapeshifter' in guild_name or guild_name in ['animal tamer', 'bestial', 'savager', 'animal healer', 'animal trainer', 'beast lord', 'dragon lord']:
            caller.db.skills.update({
                'shape shift': 10,
                'reverse transformation': 10,
            })
        
        caller.msg(f"You have joined the {guild_name.title()} guild!")
        caller.msg(f"Your guild level is now 1.")
        
        # Award guild-specific items if applicable
        if 'shapeshifter' in guild_name:
            # Give collar
            from evennia import create_object
            collar = create_object("typeclasses.objects.Object", key="a collar")
            collar.db.desc = "A magical collar that allows you to shapeshift. Look at it to see your form abilities. Touch it for guild info."
            collar.db.is_collar = True
            collar.move_to(caller, quiet=True)
            caller.msg("You have been given a magical collar.")
    
    def _has_guild_level(self, caller, guild_name, level):
        """Check if character has required level in a guild."""
        # This would check guild history - for now simplified
        current_guild = getattr(caller.db, 'guild', '').lower()
        current_level = getattr(caller.db, 'guild_level', 0)
        
        if current_guild == guild_name.lower() and current_level >= level:
            return True
        
        # Check guild history if tracked
        guild_history = getattr(caller.db, 'guild_history', {})
        if guild_name.lower() in guild_history:
            if guild_history[guild_name.lower()] >= level:
                return True
        
        return False


class CmdGuilds(Command):
    """
    Show available guilds and current guild status.
    
    Usage:
        guilds
        guild info
    """
    key = "guilds"
    aliases = ["guild"]
    locks = "cmd:all()"
    
    def func(self):
        caller = self.caller
        
        current = getattr(caller.db, 'guild', None)
        level = getattr(caller.db, 'guild_level', 0)
        
        output = []
        output.append("-=-=-| Guilds |-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
        
        if current:
            output.append(f"Current Guild: {current} (Level {level})")
            output.append(f"Guild XP: {getattr(caller.db, 'guild_xp', 0)}")
        else:
            output.append("You are not in any guild.")
        
        output.append("")
        output.append("Guild Trees:")
        output.append("  Warrior: Warrior → Berserker/Defender/Knight → Barbarian/Blade Dancer/Flogger/Shield Master/Thruster → Champion")
        output.append("  Shapeshifter: Shapeshifter → Animal Tamer/Bestial/Savager → Animal Healer/Trainer/Beast Lord → Dragon Lord")
        output.append("")
        output.append("To join a guild, find a guild master and type: join <guild_name>")
        output.append("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
        
        caller.msg("\n".join(output))


class CmdTrain(Command):
    """
    Train a stat at Mount Olympus or other training location.
    
    Usage:
        train <stat>
        train str
        train strength
    """
    key = "train"
    locks = "cmd:all()"
    
    def func(self):
        caller = self.caller
        
        if not self.args:
            # Show training costs
            from world.training import TRAINING_COST_PER_LEVEL
            current_level = getattr(caller.db, 'training_level', 1)
            cost = TRAINING_COST_PER_LEVEL.get(current_level, {})
            
            caller.msg(f"Current training level: {current_level}")
            caller.msg(f"Next training cost: {cost.get('exp', 0):,} XP, {cost.get('gold', 0):,} gold")
            return
        
        stat = self.args.strip().lower()
        
        # Map full names to abbreviations
        stat_map = {
            'strength': 'str', 'str': 'str',
            'dexterity': 'dex', 'dex': 'dex',
            'constitution': 'con', 'con': 'con',
            'stamina': 'sta', 'sta': 'sta',
            'intelligence': 'int', 'int': 'int',
            'wisdom': 'wis', 'wis': 'wis',
            'charisma': 'cha', 'cha': 'cha',
            'hp regen': 'hpr', 'hpr': 'hpr',
            'sp regen': 'spr', 'spr': 'spr',
            'ep regen': 'epr', 'epr': 'epr',
        }
        
        stat_key = stat_map.get(stat)
        if not stat_key:
            caller.msg("Invalid stat. Choose: strength, dexterity, constitution, stamina, intelligence, wisdom, charisma, hp_regen, sp_regen, ep_regen")
            return
        
        # Check if at training location
        # For now, allow training anywhere (Mount Olympus would be specific room)
        
        # Check costs
        from world.training import get_exp_cost, get_gold_cost
        current_level = getattr(caller.db, 'training_level', 1)
        exp_cost = get_exp_cost(current_level)
        gold_cost = get_gold_cost(current_level)
        
        xp = getattr(caller.db, 'experience', 0)
        gold = getattr(caller.db, 'gold', 0)
        
        if xp < exp_cost:
            caller.msg(f"You need {exp_cost:,} XP. You have {xp:,}.")
            return
        if gold < gold_cost:
            caller.msg(f"You need {gold_cost:,} gold. You have {gold:,}.")
            return
        
        # Pay costs
        caller.db.experience -= exp_cost
        caller.db.gold -= gold_cost
        caller.db.training_level = current_level + 1
        
        # Apply stat gain
        from world.stats import STAT_MESSAGES
        msg_data = STAT_MESSAGES.get(stat_key, {})
        
        if stat_key in ['hpr', 'spr', 'epr']:
            # Regen stats
            if stat_key == 'hpr':
                caller.db.hp_regen = getattr(caller.db, 'hp_regen', 10) + 1
            elif stat_key == 'spr':
                caller.db.sp_regen = getattr(caller.db, 'sp_regen', 5) + 1
            elif stat_key == 'epr':
                caller.db.ep_regen = getattr(caller.db, 'ep_regen', 5) + 1
        else:
            # Regular stat - use modify_stat
            caller.modify_stat(stat_key, 1)
        
        # Recalculate derived stats
        if hasattr(caller, 'recalculate_stats'):
            caller.recalculate_stats()
        
        increase_msg = msg_data.get('increase', f"You feel your {stat} increase!")
        caller.msg(increase_msg)
        caller.msg(f"Training level increased to {caller.db.training_level}.")
