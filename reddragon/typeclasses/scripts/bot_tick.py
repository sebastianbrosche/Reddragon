"""
Red Dragon MUD - Bot Tick Script
Periodically runs bot exploration ticks.
"""

from evennia import DefaultScript

class BotTickScript(DefaultScript):
    """
    Script that periodically runs bot exploration.
    
    Every tick, all active bots take one exploration step.
    """
    
    key = "bot_tick"
    desc = "Periodically runs bot exploration"
    interval = 15  # Every 15 seconds (bots move at human-like pace)
    persistent = True
    
    def at_script_creation(self):
        """Initialize."""
        self.interval = 15
        self.repeats = -1  # Infinite repeats
        self.persistent = True
        
    def at_repeat(self):
        """Called every interval - run bot tick."""
        from world.bots import run_bot_tick
        run_bot_tick()
    
    def at_stop(self):
        """Clean up."""
        pass


def start_bot_tick():
    """Start the bot tick script if not already running."""
    from evennia import create_script
    from evennia.scripts.models import ScriptDB
    
    existing = ScriptDB.objects.filter(db_key="bot_tick")
    if existing.exists():
        script = existing.first()
        if script.db_is_active:
            return script
        else:
            script.delete()
    
    # Create script with explicit interval - using class path string
    # and setting interval/repeats as kwargs
    return create_script(
        "typeclasses.scripts.bot_tick.BotTickScript", 
        key="bot_tick", 
        interval=15, 
        repeats=-1, 
        persistent=True,
        start_delay=False,
    )


def stop_bot_tick():
    """Stop the bot tick script."""
    from evennia.scripts.models import ScriptDB
    existing = ScriptDB.objects.filter(db_key="bot_tick")
    for script in existing:
        script.stop()
        script.delete()
