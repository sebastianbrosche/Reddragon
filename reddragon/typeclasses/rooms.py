"""
Red Dragon MUD - Room Typeclasses
Based on Islands of Myth room system
"""

from evennia import DefaultRoom

class Room(DefaultRoom):
    """
    Base room type for Red Dragon MUD.
    
    IOM rooms have:
    - Descriptions with weather/lighting effects
    - Exits in cardinal directions
    - Mob spawn points
    - Special room flags (indoors, underwater, etc.)
    """
    
    def at_object_creation(self):
        super().at_object_creation()
        # Room properties
        self.db.indoors = False
        self.db.underwater = False
        self.db.no_magic = False
        self.db.no_recall = False
        self.db.no_summon = False
        self.db.no_flee = False
        self.db.healing = False  # Healing room (regen boost)
        self.db.pkill = False  # Player killing allowed
        
        # Spawn data
        self.db.spawn_mobs = []  # [(mob_key, probability, max_count), ...]
        self.db.spawn_interval = 300  # Seconds between spawn checks
        self.db.last_spawn = 0
        
        # Atmosphere
        self.db.day_desc = None  # Override description during day
        self.db.night_desc = None  # Override description during night
        self.db.smell = None  # Smell description
        self.db.sound = None  # Sound description
        
    def return_appearance(self, looker, **kwargs):
        """
        Return room appearance (IOM-style formatting).
        
        Format:
          Room Name [exits: west, south, ...]
          Description text...
        """
        from evennia.utils.utils import list_to_string
        
        # Get room name
        name = self.get_display_name(looker, **kwargs)
        
        # Build exits line in magenta (IOM style)
        exits = [ex for ex in self.exits if ex.access(looker, "traverse")]
        if exits:
            exit_names = [ex.key for ex in exits]
            # Format like "west, south, southeast, northeast, north, southwest and east"
            if len(exit_names) == 1:
                exit_str = exit_names[0]
            elif len(exit_names) == 2:
                exit_str = f"{exit_names[0]} and {exit_names[1]}"
            else:
                exit_str = ", ".join(exit_names[:-1]) + f" and {exit_names[-1]}"
            exits_line = f"|m[exits: {exit_str}]|n"
        else:
            exits_line = "|m[exits: none]|n"
        
        # Room name + exits on same line or adjacent
        appearance = f"{name}\n{exits_line}\n"
        
        # Description
        desc = self.db.desc or "You see nothing special."
        appearance += f"  {desc}\n"
        
        # Add atmosphere
        if self.db.smell:
            appearance += f"\nYou smell: {self.db.smell}\n"
        if self.db.sound:
            appearance += f"You hear: {self.db.sound}\n"
        
        # List objects
        objects = [obj for obj in self.contents 
                   if obj != looker and not hasattr(obj.db, 'is_mob') and not obj.destination]
        if objects:
            object_names = []
            for obj in objects:
                if hasattr(obj, 'get_display_name'):
                    object_names.append(obj.get_display_name(looker))
                else:
                    object_names.append(obj.key)
            appearance += f"\n{list_to_string(object_names)}.\n"
        
        # List characters / mobs
        characters = [char for char in self.contents 
                     if char != looker and hasattr(char.db, 'is_mob') and char.db.is_mob]
        if characters:
            char_names = [char.key for char in characters]
            appearance += f"\n{list_to_string(char_names)} is here.\n"
        
        return appearance
    
    def at_object_receive(self, obj, source_location):
        """
        Called when an object enters the room.
        
        MudOS init() equivalent: When a living object enters,
        the room and its contents register commands on the living object.
        """
        super().at_object_receive(obj, source_location)
        
        # Only register commands for characters (living objects)
        if not (hasattr(obj, 'db') and hasattr(obj.db, 'level')):
            return
        
        # Register room commands on the player (MudOS: room.init() adds actions)
        if hasattr(self, 'room_cmdset'):
            obj.cmdset.add(self.room_cmdset, permanent=False)
        
        # Register NPC commands on the player (MudOS: each living calls init() in entering obj)
        for content in self.contents:
            if content != obj and hasattr(content, 'npc_cmdset'):
                obj.cmdset.add(content.npc_cmdset, permanent=False)
            
            # Notify NPCs of character entry (aggro triggers, etc.)
            if hasattr(content, 'at_character_enter'):
                content.at_character_enter(obj)
        
        # Check mob spawns
        self.check_spawns()
    
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
            # Count existing mobs of this type
            existing = sum(1 for obj in self.contents 
                          if obj.key == mob_key and hasattr(obj.db, 'is_mob'))
            
            if existing >= max_count:
                continue
                
            if random.random() < probability:
                self.spawn_mob(mob_key)
    
    def spawn_mob(self, mob_key):
        """Spawn a mob in this room."""
        from evennia import create_object
        
        # Map mob keys to typeclass paths
        mob_types = {
            "an earwig": "typeclasses.npcs.Earwig",
            "a bat": "typeclasses.npcs.Bat",
            "a snake": "typeclasses.npcs.Snake",
        }
        
        typeclass = mob_types.get(mob_key, "typeclasses.npcs.NPC")
        mob = create_object(typeclass, key=mob_key, location=self)
        
        # Call init() equivalent on the mob so it registers with room contents
        if hasattr(mob, 'at_init'):
            mob.at_init()
        
        return mob


class IndoorsRoom(Room):
    """Room that is indoors (no weather effects)."""
    
    def at_object_creation(self):
        super().at_object_creation()
        self.db.indoors = True


class HealingRoom(Room):
    """Room that boosts HP/SP/EP regeneration."""
    
    def at_object_creation(self):
        super().at_object_creation()
        self.db.healing = True
        self.db.regen_multiplier = 2.0
        
    def at_object_receive(self, obj, source_location):
        super().at_object_receive(obj, source_location)
        if hasattr(obj, 'msg'):
            obj.msg("You feel a soothing warmth in this place.")


class PKRoom(Room):
    """Player-killing allowed room."""
    
    def at_object_creation(self):
        super().at_object_creation()
        self.db.pkill = True


class NoRecallRoom(Room):
    """Room where warp/recall doesn't work."""
    
    def at_object_creation(self):
        super().at_object_creation()
        self.db.no_recall = True
        
    def at_object_receive(self, obj, source_location):
        super().at_object_receive(obj, source_location)
        if hasattr(obj, 'msg') and source_location:
            obj.msg("You feel a strange force preventing recall here.")


class ShopRoom(Room):
    """Room with a shopkeeper NPC."""
    
    def at_object_creation(self):
        super().at_object_creation()
        self.db.is_shop = True
        self.db.shopkeeper = None
        self.db.shop_items = []  # [(item_key, price, quantity), ...]


class BankRoom(Room):
    """Room with a banker NPC for deposits/withdrawals."""
    
    def at_object_creation(self):
        super().at_object_creation()
        self.db.is_bank = True
        self.db.banker = None
