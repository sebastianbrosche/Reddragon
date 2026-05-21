"""
Red Dragon MUD - Exit Typeclass
Based on Islands of Myth exit system
"""

from evennia import DefaultExit

class Exit(DefaultExit):
    """
    Custom exit type for Red Dragon MUD.
    
    Features:
    - Level requirements
    - Key/lock requirements
    - One-way exits
    - Hidden exits (need search to find)
    - Special messages on traversal
    """
    
    def at_object_creation(self):
        super().at_object_creation()
        # Exit properties
        self.db.min_level = 0
        self.db.max_level = 100
        self.db.key_required = None  # Item key needed to use
        self.db.hidden = False
        self.db.search_difficulty = 0  # For hidden exits
        
        # Messages
        self.db.traverse_msg = None  # "You walk through the door..."
        self.db.arrive_msg = None    # "You arrive at..."
        self.db.fail_msg = None      # "The door is locked."
        
    def at_traverse(self, traversing_object, target_location):
        """
        Called when something tries to traverse this exit.
        Return True if traversal allowed, False to block.
        """
        # Check level requirement
        if hasattr(traversing_object.db, 'level'):
            if traversing_object.db.level < self.db.min_level:
                traversing_object.msg(
                    f"You must be at least level {self.db.min_level} to go that way."
                )
                return False
            if traversing_object.db.level > self.db.max_level:
                traversing_object.msg(
                    f"You are too high level to go that way (max: {self.db.max_level})."
                )
                return False
        
        # Check key requirement
        if self.db.key_required:
            has_key = False
            for obj in traversing_object.contents:
                if obj.key == self.db.key_required:
                    has_key = True
                    break
            if not has_key:
                traversing_object.msg(
                    f"You need a {self.db.key_required} to go that way."
                )
                return False
        
        # Check if destination exists
        if not target_location:
            traversing_object.msg("That leads nowhere.")
            return False
            
        # Check destination room restrictions
        if hasattr(target_location.db, 'no_recall') and target_location.db.no_recall:
            # Only block warp, not normal movement
            pass
            
        # Display traverse message
        if self.db.traverse_msg:
            traversing_object.msg(self.db.traverse_msg)
        else:
            traversing_object.msg(f"You go {self.key}.")
            
        # Display arrival message
        if self.db.arrive_msg:
            traversing_object.msg(self.db.arrive_msg)
            
        # Move the object
        traversing_object.move_to(target_location, quiet=True)
        
        # Show room description
        if hasattr(target_location, 'return_appearance'):
            traversing_object.msg(target_location.return_appearance(traversing_object))
        
        return True
        
    def get_display_name(self, looker, **kwargs):
        """
        Return the exit name. Hidden exits show as 'obscured exit' unless found.
        """
        if self.db.hidden:
            # Check if looker has found this exit
            found_exits = getattr(looker.db, 'found_exits', set())
            if self.id not in found_exits:
                return "obscured exit"
        return self.key
        
    def at_failed_traverse(self, traversing_object):
        """Called when traversal fails."""
        if self.db.fail_msg:
            traversing_object.msg(self.db.fail_msg)
        else:
            traversing_object.msg(f"You can't go {self.key}.")
