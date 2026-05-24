"""
Red Dragon MUD - Newbie Areas World Building
Based on Islands of Myth newbie area system (19 areas via Sisong)
"""

from evennia import create_object
from typeclasses.rooms import Room

def create_newbie_garden():
    """Create the Newbie Garden area."""
    
    entrance = create_object("typeclasses.rooms.Room", key="Entrance to the Newbie Garden")
    entrance.db.desc = (
        "A peaceful garden with colorful flowers and gentle fountains. "
        "This is a safe place for new adventurers to learn the basics."
    )
    entrance.db.area = "Newbie Garden"
    entrance.db.healing = True
    entrance.db.danger_level = 0
    
    # Add some decorative objects
    fountain = create_object("typeclasses.objects.Object", key="a gentle fountain",
                            location=entrance)
    fountain.db.desc = "Crystal clear water flows from an ornate stone fountain."
    
    return entrance

def create_spider_cave():
    """Create the Spider Cave area."""
    
    entrance = create_object("typeclasses.rooms.Room", key="Mouth of Spider Cave")
    entrance.db.desc = (
        "The dark maw of a cave opens before you. Cobwebs cling to the "
        "walls and an acrid smell fills the air."
    )
    entrance.db.area = "Spider Cave"
    entrance.db.indoors = True
    entrance.db.danger_level = 1
    
    # Spawn spiders
    entrance.db.spawn_mobs = [("a small spider", 0.3, 3)]
    
    return entrance

def create_circus():
    """Create The Circus area."""
    
    entrance = create_object("typeclasses.rooms.Room", key="The Circus Entrance")
    entrance.db.desc = (
        "Colorful tents and the sound of carnival music surround you. "
        "Performers practice their acts while vendors sell treats."
    )
    entrance.db.area = "The Circus"
    entrance.db.danger_level = 0
    
    return entrance

def create_monster_daycare():
    """Create the Monster Daycare area."""
    
    entrance = create_object("typeclasses.rooms.Room", key="Monster Daycare")
    entrance.db.desc = (
        "A bizarre facility where young monsters are cared for. "
        "The creatures here are docile and perfect for practice combat."
    )
    entrance.db.area = "Monster Daycare"
    entrance.db.danger_level = 1
    
    return entrance

def create_church():
    """Create the Church area."""
    
    entrance = create_object("typeclasses.rooms.Room", key="A Small Church")
    entrance.db.desc = (
        "A modest stone church with stained glass windows. "
        "The air feels holy and protective."
    )
    entrance.db.area = "Church"
    entrance.db.healing = True
    entrance.db.danger_level = 0
    
    return entrance

def create_ocean():
    """Create the Ocean area."""
    
    entrance = create_object("typeclasses.rooms.Room", key="Ocean Shore")
    entrance.db.desc = (
        "Waves crash against a sandy shore. The ocean stretches "
        "endlessly to the horizon."
    )
    entrance.db.area = "Ocean"
    entrance.db.danger_level = 2
    
    return entrance

def create_strawberry_fields():
    """Create the Strawberry Fields area."""
    
    entrance = create_object("typeclasses.rooms.Room", key="Strawberry Fields")
    entrance.db.desc = (
        "Endless rows of strawberry plants stretch in every direction. "
        "The sweet aroma fills the air."
    )
    entrance.db.area = "Strawberry Fields"
    entrance.db.danger_level = 0
    
    return entrance

def create_fire_world():
    """Create the Fire World area."""
    
    entrance = create_object("typeclasses.rooms.Room", key="Fire World Entrance")
    entrance.db.desc = (
        "A realm of eternal flames and molten rock. The heat is "
        "intense but somehow survivable."
    )
    entrance.db.area = "Fire World"
    entrance.db.danger_level = 3
    
    return entrance

def create_ice_world():
    """Create the Ice World area."""
    
    entrance = create_object("typeclasses.rooms.Room", key="Ice World Entrance")
    entrance.db.desc = (
        "A frozen landscape of ice and snow. Your breath turns to "
        "frost instantly in the bitter cold."
    )
    entrance.db.area = "Ice World"
    entrance.db.danger_level = 3
    
    return entrance

def create_cat_world():
    """Create the Cat World area."""
    
    entrance = create_object("typeclasses.rooms.Room", key="Cat World")
    entrance.db.desc = (
        "A whimsical realm ruled by feline creatures. Catnip grows "
        "wild and yarn balls roll across the landscape."
    )
    entrance.db.area = "Cat World"
    entrance.db.danger_level = 1
    
    return entrance

def create_kobold_village():
    """Create the Kobold Village area."""
    
    entrance = create_object("typeclasses.rooms.Room", key="Kobold Village Entrance")
    entrance.db.desc = (
        "A crude village of mud huts and tents. Small kobolds "
        "scurry about their daily business, eyeing you warily."
    )
    entrance.db.area = "Kobold Village"
    entrance.db.danger_level = 2
    
    # Spawn kobolds
    entrance.db.spawn_mobs = [("a kobold", 0.4, 4)]
    
    return entrance

def create_zoo():
    """Create the Zoo area."""
    
    entrance = create_object("typeclasses.rooms.Room", key="The Zoo Entrance")
    entrance.db.desc = (
        "Cages and enclosures house exotic creatures from across "
        "the realm. A zookeeper maintains order."
    )
    entrance.db.area = "Zoo"
    entrance.db.danger_level = 1
    
    return entrance

def create_newbie_forest():
    """Create the Newbie Forest area."""
    
    entrance = create_object("typeclasses.rooms.Room", key="Edge of Newbie Forest")
    entrance.db.desc = (
        "A gentle forest with well-worn paths. Sunlight filters "
        "through the canopy, creating dappled patterns on the ground."
    )
    entrance.db.area = "Newbie Forest"
    entrance.db.danger_level = 1
    
    return entrance

def create_ancient_tree():
    """Create the Ancient Tree area."""
    
    entrance = create_object("typeclasses.rooms.Room", key="Base of the Ancient Tree")
    entrance.db.desc = (
        "An impossibly large tree towers above you. Its roots form "
        "natural stairways leading up into the canopy."
    )
    entrance.db.area = "Ancient Tree"
    entrance.db.danger_level = 2
    
    return entrance

def create_animal_nursery():
    """Create the Animal Nursery area."""
    
    entrance = create_object("typeclasses.rooms.Room", key="Animal Nursery")
    entrance.db.desc = (
        "Young animals of all kinds play in a protected enclosure. "
        "This is a safe place to practice gentle combat."
    )
    entrance.db.area = "Animal Nursery"
    entrance.db.danger_level = 0
    
    return entrance

def create_swallow_moors():
    """Create the Swallow Moors area."""
    
    entrance = create_object("typeclasses.rooms.Room", key="Swallow Moors")
    entrance.db.desc = (
        "Misty marshlands stretch in every direction. The ground is "
        "soft and treacherous, with hidden pools of murky water."
    )
    entrance.db.area = "Swallow Moors"
    entrance.db.danger_level = 2
    
    return entrance

def create_bee_hive():
    """Create the Bee Hive area."""
    
    entrance = create_object("typeclasses.rooms.Room", key="Entrance to the Bee Hive")
    entrance.db.desc = (
        "A massive hive constructed from wax and honeycomb. The "
        "buzz of thousands of bees fills the air."
    )
    entrance.db.area = "Bee Hive"
    entrance.db.indoors = True
    entrance.db.danger_level = 2
    
    return entrance

def create_valley_new_adventurers():
    """Create the Valley of New Adventurers area."""
    
    entrance = create_object("typeclasses.rooms.Room", key="Valley of New Adventurers")
    entrance.db.desc = (
        "A welcoming valley where new heroes begin their journey. "
        "Training dummies and helpful signs guide the way."
    )
    entrance.db.area = "Valley of New Adventurers"
    entrance.db.healing = True
    entrance.db.danger_level = 0
    
    return entrance
