"""
Red Dragon MUD - Account Typeclass
"""

from evennia import DefaultAccount

class Account(DefaultAccount):
    """
    Custom account typeclass.
    
    Features:
    - Tracks account-wide statistics
    - Handles multi-character support
    - Stores account preferences
    """
    
    def at_account_creation(self):
        """Called when a new account is created."""
        super().at_account_creation()
        
        # Account-wide stats
        self.db.total_playtime = 0
        self.db.characters_created = 0
        self.db.total_kills = 0
        self.db.highest_level = 0
        
        # Preferences
        self.db.color_enabled = True
        self.db.brief_mode = False
        self.db.auto_loot = False
        
    def at_pre_login(self):
        """Called just before logging in."""
        pass
        
    def at_post_login(self, session=None, **kwargs):
        """Called after logging in."""
        super().at_post_login(session=session, **kwargs)
        
    def at_disconnect(self, **kwargs):
        """Called when disconnecting."""
        super().at_disconnect(**kwargs)
        
    def at_post_disconnect(self, **kwargs):
        """Called after disconnecting."""
        super().at_post_disconnect(**kwargs)
