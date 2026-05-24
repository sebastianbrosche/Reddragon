"""
Red Dragon MUD - Task Points / Wishing Pond Commands
Spend task points earned from quests
"""

from evennia import Command

class CmdWish(Command):
    """
    Make a wish at the Wishing Pond east of Central Square.
    
    Usage:
        wish
        wish <wish_type>
    """
    key = "wish"
    locks = "cmd:all()"
    
    def func(self):
        caller = self.caller
        
        # Check if at wishing pond
        if not (hasattr(caller.location.db, 'is_wishing_pond') and caller.location.db.is_wishing_pond):
            caller.msg("You must be at the Wishing Pond (east of Central Square) to make wishes.")
            return
        
        tp = getattr(caller.db, 'task_points', 0)
        
        if not self.args:
            # Show available wishes
            output = []
            output.append("-=-=-| Wishing Pond |-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
            output.append(f"Task Points: {tp}")
            output.append("")
            output.append("Available Wishes:")
            output.append("  1 TP  - Minor blessing (+1 to any stat temporarily)")
            output.append("  3 TP  - Stat boost (+1 permanent stat)")
            output.append("  5 TP  - Regeneration boost (+1 hp/sp/ep regen)")
            output.append("  10 TP - Equipment blessing (improve one item)")
            output.append("  15 TP - Guild XP boost (+1000 guild XP)")
            output.append("  25 TP - Reset reincarnation tax to 0%")
            output.append("  50 TP - Special item (random unique)")
            output.append("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
            caller.msg("\n".join(output))
            return
        
        wish = self.args.strip().lower()
        
        # Map wish to cost and effect
        wishes = {
            'minor blessing': (1, 'minor_blessing'),
            'stat boost': (3, 'stat_boost'),
            'regeneration boost': (5, 'regen_boost'),
            'equipment blessing': (10, 'eq_blessing'),
            'guild xp': (15, 'guild_xp'),
            'reset tax': (25, 'reset_tax'),
            'special item': (50, 'special_item'),
        }
        
        # Check shorthand
        if wish == '1':
            wish_key = 'minor blessing'
        elif wish == '3':
            wish_key = 'stat boost'
        elif wish == '5':
            wish_key = 'regeneration boost'
        elif wish == '10':
            wish_key = 'equipment blessing'
        elif wish == '15':
            wish_key = 'guild xp'
        elif wish == '25':
            wish_key = 'reset tax'
        elif wish == '50':
            wish_key = 'special item'
        else:
            wish_key = None
            for k in wishes:
                if k in wish or wish in k:
                    wish_key = k
                    break
        
        if not wish_key or wish_key not in wishes:
            caller.msg("Unknown wish. Type 'wish' to see available options.")
            return
        
        cost, effect = wishes[wish_key]
        
        if tp < cost:
            caller.msg(f"You need {cost} task points. You have {tp}.")
            return
        
        # Deduct task points
        caller.db.task_points -= cost
        
        # Apply effect
        if effect == 'minor_blessing':
            caller.msg("The pond glows softly. You feel a minor blessing wash over you.")
            caller.db.hp = min(caller.db.hp + 50, caller.db.hp_max)
            caller.db.sp = min(caller.db.sp + 50, caller.db.sp_max)
            
        elif effect == 'stat_boost':
            import random
            stats = ['str', 'dex', 'con', 'sta', 'int', 'wis', 'cha']
            stat = random.choice(stats)
            caller.modify_stat(stat, 1)
            from world.stats import STAT_MESSAGES
            msg = STAT_MESSAGES.get(stat, {}).get('increase', f"Your {stat} increases!")
            caller.msg(msg)
            
        elif effect == 'regen_boost':
            import random
            regens = ['hp_regen', 'sp_regen', 'ep_regen']
            regen = random.choice(regens)
            current = getattr(caller.db, regen, 0)
            setattr(caller.db, regen, current + 1)
            from world.stats import STAT_MESSAGES
            msg = STAT_MESSAGES.get(regen, {}).get('increase', f"Your {regen} increases!")
            caller.msg(msg)
            
        elif effect == 'eq_blessing':
            caller.msg("The pond glows brightly. Pour this blessing on an item to improve it.")
            # Would need to track a 'pending blessing' on character
            caller.db.pending_wish = 'eq_blessing'
            
        elif effect == 'guild_xp':
            caller.db.guild_xp = getattr(caller.db, 'guild_xp', 0) + 1000
            caller.msg(f"You gain 1000 guild XP! (Total: {caller.db.guild_xp})")
            
        elif effect == 'reset_tax':
            caller.db.reinc_tax = 0.0
            caller.msg("Your reincarnation tax has been reset to 0%!")
            
        elif effect == 'special_item':
            from evennia import create_object
            item = create_object("typeclasses.objects.Object", key="Wished Item")
            item.db.desc = "A magical item granted by the Wishing Pond."
            item.db.magical = True
            import random
            bonuses = ['strength', 'dexterity', 'constitution', 'intelligence', 'wisdom']
            stat = random.choice(bonuses)
            item.db.stat_bonuses = {stat: random.randint(3, 8)}
            item.move_to(caller, quiet=True)
            caller.msg("The pond surges with power! A magical item appears in your hands.")
        
        caller.msg(f"Task points remaining: {caller.db.task_points}")


class CmdTaskPoints(Command):
    """
    Check your task points.
    
    Usage:
        taskpoints
        tp
    """
    key = "taskpoints"
    aliases = ["tp"]
    locks = "cmd:all()"
    
    def func(self):
        caller = self.caller
        tp = getattr(caller.db, 'task_points', 0)
        caller.msg(f"Task Points: {tp}")
        caller.msg("Earn task points by completing quests.")
        caller.msg("Spend them at the Wishing Pond (east of Central Square).")
