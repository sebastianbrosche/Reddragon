

class ExtendedRoom(ContribExtendedRoom):
    """
    Extended room with time-of-day, season, and weather descriptions.
    For outdoor areas that should feel alive.
    Also keeps IOM spawn/mob support.
    """
    
    def at_object_creation(self):
        super().at_object_creation()
        # Set up IOM-specific room flags
        self.db.indoors = False
        self.db.no_magic = False
        self.db.no_recall = False
        self.db.no_summon = False
        self.db.no_flee = False
        self.db.healing = False
        self.db.pkill = False
        self.db.spawn_mobs = []
        self.db.spawn_interval = 300
        self.db.last_spawn = 0
        
    def check_spawns(self):
        """Check if any mobs should spawn in this room."""
        import time
        import random
        
        if not self.db.spawn_mobs:
            return
            
        now = time.time()
        if now - self.db.last_spawn < self.db.spawn_interval:
            return
            
        self.db.last_spawn = now
        
        for mob_key, probability, max_count in self.db.spawn_mobs:
            existing = sum(1 for obj in self.contents 
                          if obj.key == mob_key and hasattr(obj.db, 'is_mob'))
            
            if existing >= max_count:
                continue
                
            if random.random() < probability:
                self.spawn_mob(mob_key)
    
    def spawn_mob(self, mob_key):
        """Spawn a mob in this room."""
        from evennia import create_object
        
        mob_types = {
            "an earwig": "typeclasses.npcs.Earwig",
            "a bat": "typeclasses.npcs.Bat",
            "a snake": "typeclasses.npcs.Snake",
        }
        
        typeclass = mob_types.get(mob_key, "typeclasses.npcs.NPC")
        mob = create_object(typeclass, key=mob_key, location=self)
        
        if hasattr(mob, 'at_init'):
            mob.at_init()
        
        return mob
