"""
Red Dragon MUD - Ferry System
Connects islands via ferry routes between dock locations
"""

from evennia import create_object, CmdSet, Command
from typeclasses.rooms import Room
from typeclasses.exits import Exit

class Dock(Room):
    """
    A dock room where ferries arrive and depart.
    Has ferry schedules and destinations.
    """
    
    def at_object_creation(self):
        super().at_object_creation()
        self.db.is_dock = True
        self.db.ferry_routes = {}  # {destination_name: (destination_room, cost, duration)}
        self.db.dock_name = "Unnamed Dock"
        
    def get_display_desc(self, looker, **kwargs):
        """Show ferry destinations in room description."""
        desc = super().get_display_desc(looker, **kwargs)
        
        if self.db.ferry_routes:
            desc += "\n\n|cFerry Routes:|n\n"
            for dest_name, (dest, cost, duration) in self.db.ferry_routes.items():
                desc += f"  |yferry {dest_name}|n - {cost} gold, {duration} seconds\n"
        
        return desc


class FerryExit(Exit):
    """
    A special exit that acts as a ferry route.
    Charges gold and takes time to travel.
    """
    
    def at_object_creation(self):
        super().at_object_creation()
        self.db.ferry_cost = 0
        self.db.ferry_duration = 10  # seconds
        self.db.is_ferry = True
        
    def at_traverse(self, traversing_object, target_location, **kwargs):
        """
        Handle ferry travel with cost and delay.
        """
        if not traversing_object.is_pc:
            return super().at_traverse(traversing_object, target_location, **kwargs)
        
        # Check if player has enough gold
        gold = traversing_object.db.gold or 0
        if gold < self.db.ferry_cost:
            traversing_object.msg(f"|rYou need {self.db.ferry_cost} gold for this ferry.|n")
            return None
        
        # Deduct gold
        traversing_object.db.gold = gold - self.db.ferry_cost
        
        # Send boarding message
        traversing_object.location.msg_contents(
            f"|y{traversing_object.key} boards the ferry to {target_location.key}.|n",
            exclude=traversing_object
        )
        traversing_object.msg(
            f"|yYou pay {self.db.ferry_cost} gold and board the ferry...|n"
        )
        
        # Use Evennia's delay for travel time
        from evennia.utils.utils import delay
        
        def arrive():
            if traversing_object.location == target_location:
                return  # Already there somehow
            
            # Move to destination
            traversing_object.move_to(target_location, quiet=True)
            traversing_object.msg(
                f"|gThe ferry arrives at {target_location.key}.|n"
            )
            target_location.msg_contents(
                f"|yA ferry arrives carrying {traversing_object.key}.|n",
                exclude=traversing_object
            )
        
        delay(self.db.ferry_duration, arrive)
        
        return None  # Don't traverse immediately, we handle it


class CmdFerry(Command):
    """
    Take a ferry to another island
    
    Usage:
        ferry <destination>
        
    Example:
        ferry gossamer
        ferry blackavar
    """
    
    key = "ferry"
    aliases = ["sail", "boat"]
    
    def func(self):
        if not self.args:
            # Show available destinations
            if self.caller.location.db.ferry_routes:
                self.caller.msg("|cAvailable ferry destinations:|n")
                for dest_name, (dest, cost, duration) in self.caller.location.db.ferry_routes.items():
                    self.caller.msg(f"  |y{dest_name}|n - {cost} gold")
            else:
                self.caller.msg("|rThere are no ferries available here.|n")
            return
        
        # Find destination
        dest_name = self.args.strip().lower()
        routes = getattr(self.caller.location, 'db', {}).get('ferry_routes', {})
        
        if dest_name not in routes:
            self.caller.msg(f"|rNo ferry route to '{dest_name}'.|n")
            return
        
        dest_room, cost, duration = routes[dest_name]
        
        # Check gold
        gold = self.caller.db.gold or 0
        if gold < cost:
            self.caller.msg(f"|rYou need {cost} gold for this ferry.|n")
            return
        
        # Deduct gold and travel
        self.caller.db.gold = gold - cost
        
        self.caller.location.msg_contents(
            f"|y{self.caller.key} boards the ferry to {dest_name}.|n",
            exclude=self.caller
        )
        self.caller.msg(f"|yYou pay {cost} gold and board the ferry to {dest_name}...|n")
        
        # Delayed arrival
        from evennia.utils.utils import delay
        
        def arrive():
            self.caller.move_to(dest_room, quiet=True)
            self.caller.msg(f"|gThe ferry arrives at {dest_room.key}!|n")
            dest_room.msg_contents(
                f"|yA ferry arrives from {self.caller.location.key} carrying {self.caller.key}.|n",
                exclude=self.caller
            )
        
        delay(duration, arrive)


class FerryCmdSet(CmdSet):
    """CmdSet with ferry commands."""
    
    def at_cmdset_creation(self):
        self.add(CmdFerry())


def create_ferry_route(from_dock, to_dock, cost=10, duration=15):
    """
    Create a ferry route between two docks.
    
    Args:
        from_dock: Starting Dock room
        to_dock: Destination Dock room  
        cost: Gold cost
        duration: Travel time in seconds
    """
    # Add route to from_dock
    if not from_dock.db.ferry_routes:
        from_dock.db.ferry_routes = {}
    
    dest_name = to_dock.db.dock_name or to_dock.key
    from_dock.db.ferry_routes[dest_name.lower()] = (to_dock, cost, duration)
    
    # Add return route
    if not to_dock.db.ferry_routes:
        to_dock.db.ferry_routes = {}
    
    from_name = from_dock.db.dock_name or from_dock.key
    to_dock.db.ferry_routes[from_name.lower()] = (from_dock, cost, duration)
    
    return True


# IOM Island Ferry Routes
ISLAND_FERRY_ROUTES = [
    # (from_island, to_island, cost, duration)
    ("gossamer", "blackavar", 15, 20),
    ("gossamer", "sombre", 20, 25),
    ("gossamer", "twin_islands", 10, 15),
    ("blackavar", "hyboria", 25, 30),
    ("blackavar", "everrest", 30, 35),
    ("sombre", "mists", 15, 20),
    ("sombre", "southcape", 20, 25),
    ("twin_islands", "emerald", 15, 20),
    ("twin_islands", "oddworld", 25, 30),
    ("hyboria", "darkcaverns", 20, 25),
]
