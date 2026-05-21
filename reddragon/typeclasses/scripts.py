"""
Red Dragon MUD - Script Typeclass
Based on Islands of Myth game systems
"""

from evennia import DefaultScript

class Script(DefaultScript):
    """
    Custom script typeclass for Red Dragon MUD.
    
    Scripts handle:
    - Game ticks (combat, regeneration, mob AI)
    - Mob spawning
    - Weather effects
    - Quest timers
    """
    
    def at_script_creation(self):
        super().at_script_creation()
        self.db.script_type = "general"
        self.db.interval = 60  # Default tick interval in seconds
        
    def at_start(self):
        """Called when script starts."""
        pass
        
    def at_stop(self):
        """Called when script stops."""
        pass
        
    def at_repeat(self):
        """Called every interval."""
        pass
