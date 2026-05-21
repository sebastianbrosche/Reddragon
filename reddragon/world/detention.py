"""
Red Dragon MUD - Detention Facility
Based on Islands of Myth admin moderation system
"""

from evennia import create_object
from typeclasses.rooms import Room

def create_detention_facility():
    """Create the admin detention/jail area."""
    
    detention = create_object("typeclasses.rooms.Room", key="Detention Facility")
    detention.db.desc = (
        "This facility has been established to uphold a standard of "
        "accountability. Within these walls, individuals who engage "
        "in disruptive and unacceptable behavior find themselves "
        "facing the consequences of their actions. Placement in this "
        "facility is a result of actions such as botting, harassment, "
        "sexism, racism, griefing, and excessive spamming, among others. "
        "It is important to note that this list is not exhaustive, and "
        "any behaviors that contravene the principles of this realm "
        "may lead to confinement within this detention facility. It is "
        "worth emphasizing that those who adhere to the established "
        "norms and guidelines of this realm will never find themselves "
        "within these confines. However, failure to do so has brought "
        "you here."
    )
    detention.db.area = "Admin"
    detention.db.indoors = True
    detention.db.no_recall = True
    detention.db.no_magic = True
    detention.db.no_summon = True
    detention.db.no_flee = True
    detention.db.pkill = False
    detention.db.danger_level = 0
    
    # No exits - this is a prison cell
    # Admins can teleport players here for violations
    
    return detention
