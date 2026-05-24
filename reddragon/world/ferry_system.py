# -*- coding: utf-8 -*-
"""
IOM Ferry System with Delays

Ferry exits that take approximately 1 minute each way.
Implements cooldowns and countdown messages.
"""

import random
from evennia import Command, CmdSet, DefaultExit
from evennia.utils import delay

FERRY_DELAY_MIN = 45  # seconds
FERRY_DELAY_MAX = 75  # seconds

class FerryExit(DefaultExit):
    """
    A ferry exit that takes time to travel.
    Shows countdown messages and has a delay before arriving.
    """
    
    def at_object_creation(self):
        super().at_object_creation()
        self.db.is_ferry = True
        self.db.ferry_name = "ferry"
        self.db.travel_time = random.randint(FERRY_DELAY_MIN, FERRY_DELAY_MAX)
        self.db.in_transit = False
    
    def at_traverse(self, traversing_object, target_location, **kwargs):
        """
        Called when an object tries to traverse this exit.
        Implements the ferry delay.
        """
        if self.db.in_transit:
            traversing_object.msg("The ferry is already in transit. Please wait.")
            return False
        
        # Start ferry journey
        self.db.in_transit = True
        travel_time = self.db.travel_time
        
        # Message to departing location
        self.location.msg_contents(
            f"{{traversing_object}} boards the ferry to {target_location.key}.",
            exclude=traversing_object,
            mapping={"traversing_object": traversing_object}
        )
        
        # Message to traveler
        traversing_object.msg(
            f"|cYou board the ferry to {target_location.key}.|n\n"
            f"The journey will take approximately {travel_time} seconds..."
        )
        
        # Countdown messages
        def send_countdown(seconds_left):
            if seconds_left > 0:
                if seconds_left % 15 == 0 or seconds_left <= 5:
                    traversing_object.msg(f"|y...{seconds_left} seconds remaining...|n")
                delay(1, lambda: send_countdown(seconds_left - 1))
            else:
                # Arrive
                arrive_at_destination(traversing_object, target_location, self)
        
        # Start countdown
        delay(1, lambda: send_countdown(travel_time - 1))
        
        # Schedule arrival
        delay(travel_time, lambda: None)  # Just to mark the time
        
        return False  # Don't move immediately - we'll move them in arrive_at_destination


def arrive_at_destination(traveler, destination, ferry_exit):
    """Move traveler to destination after ferry delay."""
    # Actually move the traveler
    traveler.move_to(destination, quiet=True)
    
    # Arrival messages
    traveler.msg(
        f"|gYou have arrived at {destination.key}!|n\n"
        f"{destination.return_appearance(traveler)}"
    )
    
    destination.msg_contents(
        f"{{traveler}} arrives by ferry.",
        exclude=traveler,
        mapping={"traveler": traveler}
    )
    
    # Reset ferry
    ferry_exit.db.in_transit = False


class InstantFerryExit(DefaultExit):
    """
    A ferry exit for bots and testing that completes quickly.
    Normal ferries take 1 minute; instant ferries take 5 seconds.
    """
    
    def at_object_creation(self):
        super().at_object_creation()
        self.db.is_ferry = True
        self.db.is_instant = True
        self.db.travel_time = 5
    
    def at_traverse(self, traversing_object, target_location, **kwargs):
        """Quick ferry for bots."""
        traversing_object.msg(
            f"|cYou board the ferry to {target_location.key}...|n"
        )
        
        def arrive():
            traversing_object.move_to(target_location, quiet=True)
            traversing_object.msg(
                f"|gYou have arrived at {target_location.key}!|n"
            )
        
        delay(self.db.travel_time, arrive)
        return False


def upgrade_ferries_to_delayed(world_builder_ferries=None):
    """
    Upgrade existing ferry exits to use the delayed system.
    Call this after building the world.
    """
    from evennia import search_object
    from typeclasses.exits import IOMExit
    
    # Find all ferry exits
    all_exits = search_object("ferry", typeclass=IOMExit)
    
    upgraded = 0
    for exit_obj in all_exits:
        if hasattr(exit_obj.db, "is_ferry"):
            # Already a ferry exit
            continue
        
        # Convert to delayed ferry
        exit_obj.db.is_ferry = True
        exit_obj.db.travel_time = random.randint(FERRY_DELAY_MIN, FERRY_DELAY_MAX)
        
        upgraded += 1
    
    print(f"Upgraded {upgraded} ferries to delayed travel.")
    print(f"Travel time: {FERRY_DELAY_MIN}-{FERRY_DELAY_MAX} seconds each way.")


if __name__ == "__main__":
    print("Run this from within Evennia with:")
    print("  @py from world.ferry_system import upgrade_ferries_to_delayed; upgrade_ferries_to_delayed()")
