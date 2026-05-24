"""
Red Dragon MUD - Hunger Tick Script
Runs hunger decrease and starvation damage every few minutes
"""

from evennia import DefaultScript

class HungerTickScript(DefaultScript):
    """
    Script that periodically decreases hunger and applies effects.
    
    In IOM, hunger slowly decreases over time.
    Starvation causes HP damage.
    """
    
    key = "hunger_tick"
    desc = "Decreases hunger over time"
    interval = 120  # Every 2 minutes (IOM hunger ticks are fairly slow)
    persistent = True
    
    def at_script_creation(self):
        """Initialize."""
        pass
        
    def at_repeat(self):
        """Called every interval."""
        from evennia import search_object
        
        # Get all characters in the game
        from typeclasses.characters import Character
        characters = search_object("_", typeclass=Character)
        
        for char in characters:
            if not char or not char.location:
                continue
            
            # Skip if not a player puppet
            if not char.sessions.count():
                continue
            
            # Get current hunger (stored as percentage 0-100)
            hunger_pct = getattr(char.db, 'hunger_pct', 75)
            
            # Decrease hunger by 1-3% per tick
            import random
            decrease = random.randint(1, 3)
            hunger_pct = max(0, hunger_pct - decrease)
            char.db.hunger_pct = hunger_pct
            
            # Get hunger state
            from world.hunger import get_hunger_state
            state = get_hunger_state(hunger_pct)
            
            # Show message on significant state changes
            old_state = getattr(char.db, 'hunger_state', 'content')
            if state['state'] != old_state:
                char.msg(f"|y{state['message']}|n")
                char.db.hunger_state = state['state']
            
            # Starvation damage at very low hunger
            if hunger_pct <= 2:
                # Take HP damage
                starve_dmg = random.randint(1, 5)
                char.db.hp = max(1, char.db.hp - starve_dmg)
                char.msg(f"|rYou are starving! You take {starve_dmg} damage.|n")
            
            # Update the legacy hunger string for compatibility
            char.db.hunger = state['desc']
    
    def at_stop(self):
        """Clean up."""
        pass


def start_hunger_tick():
    """Start the hunger tick script if not already running."""
    from evennia import create_script
    existing = [s for s in DefaultScript.objects.all() if s.key == "hunger_tick"]
    if existing:
        return existing[0]
    return create_script(HungerTickScript)
