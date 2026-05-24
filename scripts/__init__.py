"""
Red Dragon MUD - AI and Game Tick Scripts
Handles mob AI, respawning, and game events
"""

from evennia import DefaultScript

class MobAIScript(DefaultScript):
    """
    Handles mob AI behavior - combat, wandering, respawning.
    Based on Islands of Myth mob behavior.
    """
    
    def at_script_creation(self):
        self.key = "mob_ai"
        self.desc = "Mob AI handler"
        self.interval = 6  # Tick every 6 seconds (IOM combat tick)
        self.persistent = True
        
    def at_repeat(self):
        """Called every interval seconds."""
        if not self.obj:
            return
            
        mob = self.obj
        
        # Skip if dead
        if getattr(mob.db, 'ai_state', '') == 'dead':
            return
            
        # Combat AI
        if mob.db.ai_state == 'combat' and mob.db.target:
            target = mob.db.target
            if target.location == mob.location:
                mob.combat_attack(target)
            else:
                # Target left - return to wander
                mob.db.ai_state = 'wander'
                mob.db.target = None
                
        # Wandering AI
        elif mob.db.ai_state == 'wander':
            import random
            if random.random() < 0.3:  # 30% chance to move
                exits = [ex for ex in mob.location.exits if ex.access(mob, "traverse")]
                if exits:
                    exit = random.choice(exits)
                    mob.move_to(exit.destination)


class MobSpawner(DefaultScript):
    """
    Handles mob respawning after death.
    """
    
    def at_script_creation(self):
        self.key = "mob_spawner"
        self.desc = "Mob respawn handler"
        self.interval = 60  # Check every minute
        self.persistent = True
        
    def at_repeat(self):
        """Check if mob needs to respawn."""
        if not self.obj or not self.obj.db.is_mob:
            return
            
        # Check if mob is dead and needs respawn
        if self.obj.db.ai_state == 'dead':
            self.obj.db.respawn_timer -= 1
            if self.obj.db.respawn_timer <= 0:
                self.obj.respawn()


class GameTick(DefaultScript):
    """
    Global game tick - handles HP/EP/SP regeneration.
    """
    
    def at_script_creation(self):
        self.key = "game_tick"
        self.desc = "Global game tick handler"
        self.interval = 6  # 6 second tick (IOM standard)
        self.persistent = True
        
    def at_repeat(self):
        """Regenerate resources for all online characters."""
        from evennia import search_object
        
        for obj in search_object("*"):
            if hasattr(obj, 'db') and hasattr(obj.db, 'hp_regen'):
                # Regenerate HP
                if obj.db.hp < obj.db.hp_max:
                    obj.db.hp = min(obj.db.hp + obj.db.hp_regen, obj.db.hp_max)
                
                # Regenerate SP
                if obj.db.sp < obj.db.sp_max:
                    obj.db.sp = min(obj.db.sp + obj.db.sp_regen, obj.db.sp_max)
                
                # Regenerate EP
                if obj.db.ep < obj.db.ep_max:
                    obj.db.ep = min(obj.db.ep + obj.db.ep_regen, obj.db.ep_max)
