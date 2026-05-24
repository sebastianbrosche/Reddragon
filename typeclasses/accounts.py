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
        
        # Check if this is a new character that needs race selection
        from evennia import search_object
        from typeclasses.rooms import IOMRoom
        
        puppet = self.get_puppet(session)
        if puppet and getattr(puppet.db, "needs_race_selection", True):
            # Move to race selection hall
            race_room = search_object("Race Selection Hall", typeclass=IOMRoom)
            if race_room:
                puppet.move_to(race_room[0])
                puppet.msg("|cWelcome! Please |yselect <race>|n before entering the world.")
                puppet.msg("Type |yread sign|n for instructions.")
            puppet.db.needs_race_selection = False
        
    def at_disconnect(self, **kwargs):
        """Called when disconnecting."""
        super().at_disconnect(**kwargs)
        
    def at_post_disconnect(self, **kwargs):
        """Called after disconnecting."""
        super().at_post_disconnect(**kwargs)
