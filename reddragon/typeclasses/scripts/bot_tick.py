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
        pass
        
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
    from evennia import DefaultScript
    
    existing = [s for s in DefaultScript.objects.all() if s.key == "bot_tick"]
    if existing:
        return existing[0]
    
    return create_script(BotTickScript)


def stop_bot_tick():
    """Stop the bot tick script."""
    from evennia import DefaultScript
    existing = [s for s in DefaultScript.objects.all() if s.key == "bot_tick"]
    for script in existing:
        script.stop()
