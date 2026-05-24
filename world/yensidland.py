"""
Red Dragon MUD - Yensidland and LobeLands World Building
Based on Islands of Myth reverse-engineering
Area: Yensidland - Newbie hunting grounds
"""

from evennia import create_object
from typeclasses.rooms import Room
from typeclasses.npcs import Earwig

def create_yensidland():
    """Create the Yensidland area with LobeLands hunting grounds."""
    
    # -------------------------------------------------------------------------
    # YENSIDLAND ENTRY POINT (arrive here from Sisong teleport or portal)
    # -------------------------------------------------------------------------
    yensid_entry = create_object("typeclasses.rooms.Room", key="Welcome to YENSIDLAND")
    yensid_entry.db.desc = (
        "This is such a jolly place!! You think you might just pop out a jolly "
        "fart or two just to show everyone how jolly you feel about being in "
        "the jolliest land in jolly old Red Dragon!!!"
    )
    yensid_entry.db.area = "Yensidland"
    yensid_entry.db.danger_level = 1
    yensid_entry.db.is_outdoors = True
    
    # Portal back to Newbie Guild
    portal = create_object("typeclasses.objects.Object", key="a portal to the Newbie Guild",
                           location=yensid_entry)
    portal.db.desc = "A shimmering portal that leads back to the Newbie Guild."
    
    # Jolly sign
    sign = create_object("typeclasses.objects.Object", key="a jolly sign",
                         location=yensid_entry)
    sign.db.desc = "A cheerful sign sits beside the path, covered in whimsical writing."
    
    # -------------------------------------------------------------------------
    # LOBELANDS ROOM 1 (nw from Yensid entry)
    # -------------------------------------------------------------------------
    lobelands_1 = create_object("typeclasses.rooms.Room", key="LobeLands")
    lobelands_1.db.desc = (
        "The terrain around you is completely black. The ground beneath your feet "
        "is soft and flexible, and seems to quiver with every sound you make. "
        "Huge piles of waxy buildup lie before you."
    )
    lobelands_1.db.area = "Yensidland"
    lobelands_1.db.danger_level = 1
    lobelands_1.db.is_outdoors = True
    lobelands_1.db.ambient_msgs = [
        (0.05, "The waxy ground quivers beneath your feet."),
    ]
    
    # Gold coins on ground
    gold = create_object("typeclasses.objects.Object", key="210 gold coins",
                         location=lobelands_1)
    gold.db.value = 210
    gold.db.desc = "A pile of gold coins glints on the dark ground."
    
    # Spawn earwigs (if present in this room)
    for i in range(3):
        earwig = create_object("typeclasses.npcs.Earwig", 
                              key=f"earwig_{i}_{lobelands_1.id}",
                              location=lobelands_1)
    
    create_exit(yensid_entry, lobelands_1, "northwest", "southeast")
    
    # -------------------------------------------------------------------------
    # LOBELANDS ROOM 2 (n from lobelands_1)
    # -------------------------------------------------------------------------
    lobelands_2 = create_object("typeclasses.rooms.Room", key="LobeLands")
    lobelands_2.db.desc = (
        "The terrain around you is completely black. The ground beneath your feet "
        "is soft and flexible, and seems to quiver with every sound you make. "
        "Huge piles of waxy buildup lie before you."
    )
    lobelands_2.db.area = "Yensidland"
    lobelands_2.db.danger_level = 1
    lobelands_2.db.is_outdoors = True
    lobelands_2.db.ambient_msgs = [
        (0.05, "The waxy ground quivers beneath your feet."),
    ]
    
    # Gold coins on ground
    gold2 = create_object("typeclasses.objects.Object", key="210 gold coins",
                          location=lobelands_2)
    gold2.db.value = 210
    gold2.db.desc = "A pile of gold coins glints on the dark ground."
    
    # Spawn earwigs
    for i in range(3):
        earwig = create_object("typeclasses.npcs.Earwig",
                              key=f"earwig_{i}_{lobelands_2.id}",
                              location=lobelands_2)
    
    create_exit(lobelands_1, lobelands_2, "north", "south")
    
    # -------------------------------------------------------------------------
    # YENSIDLAND PATHS (other directions from entry for expansion)
    # -------------------------------------------------------------------------
    
    # North from entry
    yensid_north = create_object("typeclasses.rooms.Room", key="Yensidland - Whispering Fields")
    yensid_north.db.desc = (
        "Tall grass stretches in all directions, swaying even when there is "
        "no wind. The blades whisper against each other, sounding almost like "
        "voices speaking in a language just beyond comprehension."
    )
    yensid_north.db.area = "Yensidland"
    yensid_north.db.danger_level = 1
    yensid_north.db.is_outdoors = True
    create_exit(yensid_entry, yensid_north, "north", "south")
    
    # Northeast from entry
    yensid_ne = create_object("typeclasses.rooms.Room", key="Yensidland - Crystal Brook")
    yensid_ne.db.desc = (
        "A shallow brook cuts through the landscape, its waters so clear "
        "that the stones at the bottom seem to glow with their own inner light. "
        "The water tastes of copper and something sweet."
    )
    yensid_ne.db.area = "Yensidland"
    yensid_ne.db.danger_level = 1
    yensid_ne.db.is_outdoors = True
    create_exit(yensid_entry, yensid_ne, "northeast", "southwest")
    
    # East from entry
    yensid_east = create_object("typeclasses.rooms.Room", key="Yensidland - Sunken Path")
    yensid_east.db.desc = (
        "The ground here has sunk into a natural trench, worn smooth by "
        "countless footsteps over centuries. The walls of the trench are "
        "covered in creeping vines that drip with moisture."
    )
    yensid_east.db.area = "Yensidland"
    yensid_east.db.danger_level = 1
    yensid_east.db.is_outdoors = True
    create_exit(yensid_entry, yensid_east, "east", "west")
    
    # South from entry
    yensid_south = create_object("typeclasses.rooms.Room", key="Yensidland - Briar Thicket")
    yensid_south.db.desc = (
        "Thorny briars form walls on either side of the narrow path, their "
        "thorns glistening with some kind of sap. The passage is tight, and "
        "you must move carefully to avoid being scratched."
    )
    yensid_south.db.area = "Yensidland"
    yensid_south.db.danger_level = 2
    yensid_south.db.is_outdoors = True
    create_exit(yensid_entry, yensid_south, "south", "north")
    
    # Southeast from entry
    yensid_se = create_object("typeclasses.rooms.Room", key="Yensidland - Red Clearing")
    yensid_se.db.desc = (
        "A small clearing where the grass grows red instead of green. The "
        "soil here is dark and rich, and the air smells of iron. Something "
        "about this place makes the hair on your neck stand up."
    )
    yensid_se.db.area = "Yensidland"
    yensid_se.db.danger_level = 2
    yensid_se.db.is_outdoors = True
    create_exit(yensid_entry, yensid_se, "southeast", "northwest")
    
    return yensid_entry


def create_exit(origin, destination, exit_name, return_name=None):
    """Helper to create bidirectional exits."""
    from evennia import create_object
    
    forward = create_object("typeclasses.exits.Exit", key=exit_name,
                           location=origin, destination=destination)
    if return_name:
        backward = create_object("typeclasses.exits.Exit", key=return_name,
                                  location=destination, destination=origin)
    return forward


def build_yensidland():
    """Build the complete Yensidland area."""
    entry = create_yensidland()
    return entry
