"""
Red Dragon MUD - Room Typeclasses
"""

from evennia import DefaultRoom
from evennia.contrib.grid.extended_room import ExtendedRoom as ContribExtendedRoom

class Room(DefaultRoom):
    """
    Base room typeclass for Red Dragon Reborn.
    Awards EXP when characters discover new rooms.
    """
    
    def at_object_receive(self, moved_obj, source_location):
        """
        Called when an object enters this room.
        Award EXP if it's a character discovering this room for the first time.
        """
        super().at_object_receive(moved_obj, source_location)
        
        # Only award EXP to characters with sessions (players/bots)
        if not hasattr(moved_obj, 'sessions'):
            return
        if not moved_obj.sessions.count():
            return
        
        # Check if this room is new for this character
        rooms_explored = getattr(moved_obj.db, 'rooms_explored', set())
        room_id = self.id
        
        if room_id not in rooms_explored:
            # First time in this room!
            rooms_explored.add(room_id)
            moved_obj.db.rooms_explored = rooms_explored
            
            # Calculate EXP reward based on area danger/level
            base_xp = 25
            area_level = getattr(self.db, 'danger_level', 1)
            xp_reward = base_xp * max(1, area_level)
            
            # Bonus for exploration milestones
            total_rooms = len(rooms_explored)
            milestone_bonus = 0
            if total_rooms % 100 == 0:
                milestone_bonus = total_rooms  # +100 XP at 100 rooms, +200 at 200, etc.
                moved_obj.msg(f"|y*** EXPLORATION MILESTONE: {total_rooms} rooms discovered! ***|n")
            
            total_xp = xp_reward + milestone_bonus
            
            # Add experience
            if hasattr(moved_obj, 'add_experience'):
                moved_obj.add_experience(total_xp)
            else:
                moved_obj.db.experience = getattr(moved_obj.db, 'experience', 0) + total_xp
            
            # Notify
            moved_obj.msg(f"|gYou discover a new area! (+{total_xp} XP)|n")
            
            # Update exploration percentage if we know total world size
            total_world_rooms = getattr(self.db, 'total_world_rooms', 11314)  # IOM world size
            if total_world_rooms > 0:
                pct = (total_rooms / total_world_rooms) * 100
                moved_obj.db.exploration_pct = pct
                if total_rooms % 50 == 0:
                    moved_obj.msg(f"|yWorld explored: {pct:.1f}%|n")


class IOMRoom(Room):
    """
    Islands of Myth room - used for all IOM world rooms.
    Inherits EXP reward and adds IOM-specific features.
    """
    
    def at_object_creation(self):
        super().at_object_creation()
        # IOM room flags
        self.db.indoors = False
        self.db.no_magic = False
        self.db.no_recall = False
        self.db.no_summon = False
        self.db.no_flee = False
        self.db.healing = False
        self.db.pkill = False
        self.db.danger_level = 1
        self.db.area = "Unknown"


class WeatherRoom(ContribExtendedRoom):
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
