"""
Red Dragon MUD - Formula/Scroll Item Type
Based on Islands of Myth - "Formula: Head: Lesser Wisdoms"
"""

from evennia import DefaultObject

class Formula(DefaultObject):
    """
    A formula/scroll item that teaches a spell or ability when used.
    
    Example from IOM: "Formula: Head: Lesser Wisdoms"
    """
    
    def at_object_creation(self):
        super().at_object_creation()
        self.db.slot = "head"  # Equipment slot: head, body, arms, legs, etc.
        self.db.stat = "wisdom"  # Stat modified
        self.db.magnitude = "lesser"  # lesser, greater, supreme, etc.
        self.db.spell_name = None  # If it teaches a spell
        self.db.learned = False
        self.db.value = 50
        
    def at_use(self, user):
        """Called when a player uses/tries to learn from this formula."""
        if self.db.learned:
            user.msg("You have already learned this formula.")
            return
            
        if self.db.spell_name:
            # Teach the spell
            user.msg(f"You study the formula and learn {self.db.spell_name}!")
            # Add to user's known spells
            if not hasattr(user.db, 'known_spells'):
                user.db.known_spells = []
            user.db.known_spells.append(self.db.spell_name)
            self.db.learned = True
        else:
            user.msg(f"You study the formula for {self.db.magnitude} {self.db.stat} enchantment.")
            
    def get_display_name(self, looker, **kwargs):
        """Return the formatted name."""
        return f"Formula: {self.db.slot.capitalize()}: {self.db.magnitude.capitalize()} {self.db.stat.capitalize()}"
        
    def return_appearance(self, looker):
        """Custom description."""
        desc = super().return_appearance(looker)
        if self.db.learned:
            desc += "\n(You have already learned this formula.)"
        return desc
