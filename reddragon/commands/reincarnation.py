"""
Red Dragon MUD - Reincarnation Commands
Sacrifice items and gold to reduce reincarnation tax
"""

from evennia import Command

class CmdSacrifice(Command):
    """
    Sacrifice an item or gold to Eje to reduce reincarnation tax.
    
    Usage:
        sacrifice <item>
        sacrifice <amount> gold
        sacrifice all gold
    """
    key = "sacrifice"
    locks = "cmd:all()"
    
    def func(self):
        caller = self.caller
        
        # Check if at Illium Church
        if not (hasattr(caller.location.db, 'is_church') and caller.location.db.is_church):
            caller.msg("You must be at Illium Church to sacrifice to Eje.")
            return
        
        if not self.args:
            # Show current tax and help
            tax = getattr(caller.db, 'reinc_tax', 0.0)
            caller.msg(f"Current reincarnation tax: {tax:.2f}%")
            caller.msg("Usage: sacrifice <item>  or  sacrifice <amount> gold")
            return
        
        args = self.args.strip().lower()
        
        if 'gold' in args:
            # Sacrifice gold
            amount_str = args.replace('gold', '').replace('all', '').strip()
            if 'all' in args:
                amount = getattr(caller.db, 'gold', 0)
            else:
                try:
                    amount = int(amount_str)
                except ValueError:
                    caller.msg("Usage: sacrifice <amount> gold  or  sacrifice all gold")
                    return
            
            if amount <= 0:
                caller.msg("You have no gold to sacrifice.")
                return
            
            if caller.db.gold < amount:
                caller.msg(f"You only have {caller.db.gold:,} gold.")
                return
            
            # Calculate tax reduction
            from world.reincarnation import calculate_gold_sacrifice_tax_reduction
            old_tax = getattr(caller.db, 'reinc_tax', 0.0)
            new_tax = calculate_gold_sacrifice_tax_reduction(old_tax, amount)
            
            caller.db.gold -= amount
            caller.db.reinc_tax = new_tax
            
            reduction = old_tax - new_tax
            caller.msg(f"You sacrifice {amount:,} gold to Eje.")
            caller.msg(f"Your reincarnation tax decreases from {old_tax:.3f}% to {new_tax:.3f}% (-{reduction:.3f}%)")
            
        else:
            # Sacrifice item
            item_name = self.args.strip()
            item = caller.search(item_name, location=caller)
            if not item:
                return
            
            # Check if item meets sacrifice requirements
            from world.reincarnation import ITEM_SACRIFICE_REQUIREMENTS
            
            meets_req = False
            best_stat = getattr(item.db, 'best_stat_bonus', 0)
            best_resist = getattr(item.db, 'best_resistance', 0)
            alpha_bonus = getattr(item.db, 'best_alpha_bonus', 0)
            bravo_bonus = getattr(item.db, 'best_bravo_bonus', 0)
            
            if best_stat >= ITEM_SACRIFICE_REQUIREMENTS['stat_bonus']:
                meets_req = True
            if best_resist >= ITEM_SACRIFICE_REQUIREMENTS['resistance']:
                meets_req = True
            if alpha_bonus >= ITEM_SACRIFICE_REQUIREMENTS['alpha_spell_skill']:
                meets_req = True
            if bravo_bonus >= ITEM_SACRIFICE_REQUIREMENTS['bravo_spell_skill']:
                meets_req = True
            
            if not meets_req:
                caller.msg("Eje refuses the item. It must have +8 to a stat, +3 resistance, +5% alpha, or +3% bravo.")
                return
            
            # Calculate worth in task points
            tps = getattr(item.db, 'task_points', 0)
            from world.reincarnation import get_item_worth_gold
            gold_equiv = get_item_worth_gold(tps)
            
            from world.reincarnation import calculate_gold_sacrifice_tax_reduction
            old_tax = getattr(caller.db, 'reinc_tax', 0.0)
            new_tax = calculate_gold_sacrifice_tax_reduction(old_tax, gold_equiv)
            
            item.delete()
            caller.db.reinc_tax = new_tax
            
            reduction = old_tax - new_tax
            caller.msg(f"You sacrifice {item.key} to Eje. (Worth ~{gold_equiv:,} gold equivalent)")
            caller.msg(f"Your reincarnation tax decreases from {old_tax:.3f}% to {new_tax:.3f}% (-{reduction:.3f}%)")


class CmdReincarnate(Command):
    """
    Reincarnate - reset your character while keeping some progress.
    
    Usage:
        reincarnate
        reincarnate confirm
    """
    key = "reincarnate"
    locks = "cmd:all()"
    
    def func(self):
        caller = self.caller
        
        tax = getattr(caller.db, 'reinc_tax', 0.0)
        
        if not self.args or self.args.strip().lower() != 'confirm':
            caller.msg(f"Reincarnation tax: {tax:.2f}%")
            caller.msg("This will reset your level and guild progress but preserve some bonuses.")
            caller.msg("Type 'reincarnate confirm' to proceed.")
            return
        
        # Calculate what is preserved based on tax
        # Lower tax = more preserved
        preserve_pct = max(0, 100 - tax) / 100.0
        
        # Store what to preserve
        old_stats = {
            'strength': caller.db.strength,
            'dexterity': caller.db.dexterity,
            'constitution': caller.db.constitution,
            'stamina': caller.db.stamina,
            'intelligence': caller.db.intelligence,
            'wisdom': caller.db.wisdom,
            'charisma': caller.db.charisma,
        }
        
        # Reset level
        caller.db.level = 1
        caller.db.experience = 0
        caller.db.training_level = 1
        
        # Reset guilds
        caller.db.guild = None
        caller.db.guild_level = 0
        caller.db.guild_xp = 0
        
        # Reset skills
        caller.db.skills = {}
        
        # Apply preserved stats
        for stat, val in old_stats.items():
            preserved = int(val * preserve_pct)
            base = getattr(caller.db, f'{stat}_base', 50)
            new_val = max(base, preserved)
            setattr(caller.db, stat, new_val)
        
        # Recalculate
        if hasattr(caller, 'recalculate_stats'):
            caller.recalculate_stats()
        
        # Increase tax for next reinc
        caller.db.reinc_tax = min(100, tax + 10)
        
        caller.msg("You have been reincarnated!")
        caller.msg(f"Your stats were preserved at {preserve_pct*100:.0f}% due to {tax:.2f}% tax.")
        caller.msg(f"Your new reincarnation tax is {caller.db.reinc_tax:.2f}%.")
        caller.msg("Visit Eje at Illium Church to reduce your tax before next reincarnation.")
