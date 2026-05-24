"""
Red Dragon MUD - Object Typeclasses
Items, containers, portals, and other objects
Uses Evennia's RP system for poses and sdescs.
"""

from evennia import DefaultObject
from evennia.contrib.rpg.rpsystem.rpsystem import ContribRPObject
from evennia.contrib.game_systems.containers import ContribContainer

class Object(ContribRPObject):
    """
    Generic object with IOM-style properties.
    """
    
    def at_object_creation(self):
        super().at_object_creation()
        self.db.edible = False
        self.db.is_corpse = False
        self.db.is_formula = False
        self.db.is_portal = False
        self.db.is_container = False
        
    def get_display_name(self, looker, **kwargs):
        """Return display name."""
        name = self.key
        if self.db.is_corpse:
            name = f"corpse of {self.db.get('mob_source', 'unknown')}"
        return name


class Formula(Object):
    """
    Crafting formula item (like IOM's "Formula: Head: Lesser Wisdoms").
    Used to learn or craft equipment.
    """
    
    def at_object_creation(self):
        super().at_object_creation()
        self.db.is_formula = True
        self.db.formula_type = "head"  # head, body, arms, legs, etc.
        self.db.formula_name = "Lesser Wisdoms"
        self.db.desc = "A mysterious formula that can be used to create something."
        

class GoldCoins(Object):
    """
    Stack of gold coins (currency).
    """
    
    def at_object_creation(self):
        super().at_object_creation()
        self.key = "gold coins"
        self.db.amount = 0
        self.db.desc = "Shiny gold coins."
        
    def get_display_name(self, looker, **kwargs):
        return f"{self.db.amount} gold coins"
        

class Portal(Object):
    """
    A portal/teleporter to another location.
    """
    
    def at_object_creation(self):
        super().at_object_creation()
        self.db.is_portal = True
        self.db.destination = None  # Room key or dbref
        self.db.portal_type = "magic"  # magic, physical, guild
        self.db.one_way = False
        
    def at_use(self, user):
        """Called when user interacts with portal."""
        if not self.db.destination:
            user.msg("The portal is inactive.")
            return
            
        from evennia import search_object
        dest = search_object(self.db.destination)
        if dest:
            user.msg(f"You step through {self.key}...")
            user.move_to(dest[0])
        else:
            user.msg("The portal leads nowhere.")
            

class Container(ContribContainer, Object):
    """
    Container that can hold items.
    Uses Evennia's ContribContainer for proper get_from/put_in support.
    """
    
    def at_object_creation(self):
        super().at_object_creation()
        self.db.is_container = True
        self.db.capacity = 10  # Max items
        self.db.locked = False
        self.db.key_required = None
        
    def can_hold(self, obj):
        """Check if container can hold more items."""
        return len(self.contents) < self.db.capacity
        
    def at_object_receive(self, obj, source_location):
        """Called when an object is put in container."""
        if not self.can_hold(obj):
            obj.move_to(source_location)
            source_location.msg(f"{self.key} is full.")
            

class Corpse(Object):
    """
    A mob corpse that can be looted and eaten.
    """
    
    def at_object_creation(self):
        super().at_object_creation()
        self.db.is_corpse = True
        self.db.edible = True
        self.db.heal_hp = 20
        self.db.heal_ep = 10
        self.db.mob_source = "unknown"
        self.db.looted = False
        
    def get_display_name(self, looker, **kwargs):
        return f"corpse of {self.db.mob_source}"
        
    def at_get(self, getter):
        """Called when someone tries to get the corpse."""
        getter.msg("You can't carry corpses. Try eating or looting them.")
        return False  # Prevent picking up
