"""
Red Dragon MUD - Ilium City World Building
Based on Islands of Myth reverse-engineering (Session logs from emalz exploration)
Area: Ilium City - The central hub of the world
"""

from evennia import create_object

def create_exit(origin, destination, exit_name, return_name=None):
    """Helper to create bidirectional exits."""
    from evennia import create_object
    
    # Create forward exit
    forward = create_object("typeclasses.exits.Exit", key=exit_name, 
                           location=origin, destination=destination)
    
    # Create return exit if requested
    if return_name:
        backward = create_object("typeclasses.exits.Exit", key=return_name,
                                  location=destination, destination=origin)
    
    return forward

# =============================================================================
# ILLIUM CITY - ADVENTURERS' GUILD DISTRICT
# =============================================================================

def create_ilium_adventurers_guild():
    """Create the Adventurers' Guild area of Ilium City."""
    
    # -------------------------------------------------------------------------
    # ADVENTURER GUILD ENTRANCE (hub room)
    # -------------------------------------------------------------------------
    adventurer_guild = create_object("typeclasses.rooms.Room", key="Adventurer Guild Entrance")
    adventurer_guild.db.desc = (
        "This large room is the Adventurers guild. Truly breathtaking in its "
        "architecture, the guild houses a vast amount of help for the new "
        "adventurers and the old. Its high domed ceiling swirls with blue and "
        "whites, like the sky on a very windy day. Because it is domed and "
        "there are windows all along the wall, the room seems very open and "
        "very friendly."
    )
    adventurer_guild.db.area = "Ilium City"
    adventurer_guild.db.room_type = "guild"
    adventurer_guild.db.has_guild = True
    adventurer_guild.db.danger_level = 0
    adventurer_guild.db.is_outdoors = False
    
    # -------------------------------------------------------------------------
    # LEVEL ROOM / JUDGE ROOM (east of guild entrance)
    # -------------------------------------------------------------------------
    level_room = create_object("typeclasses.rooms.Room", key="Adventurers Leveling Place")
    level_room.db.desc = (
        "This room is large, and the ceiling is high. In the center stands a "
        "large podium. Upon that podium sits Achman, the judge. He controls the "
        "levels of Red Dragon, and has the power to create some of the strongest "
        "players. He sits in a high back chair built into the podium. Talk to him "
        "if you wish to advance in your endeavors."
    )
    level_room.db.area = "Ilium City"
    level_room.db.danger_level = 0
    level_room.db.is_outdoors = False
    
    # Create Achman NPC
    achman = create_object("typeclasses.npcs.JudgeAchman", key="Achman the Judge",
                           location=level_room)
    
    create_exit(adventurer_guild, level_room, "east", "west")
    
    # -------------------------------------------------------------------------
    # MYTH ROOM (south of guild entrance)
    # -------------------------------------------------------------------------
    myth_room = create_object("typeclasses.rooms.Room", key="Myth Room")
    myth_room.db.desc = (
        "In this room, those who have been honored stand. It is a bright and open "
        "room, with plenty of light. Statues stand all along the walls. Statues of "
        "those who have contributed much to this amazing world."
    )
    myth_room.db.area = "Ilium City"
    myth_room.db.danger_level = 0
    myth_room.db.is_outdoors = False
    
    create_exit(adventurer_guild, myth_room, "south", "north")
    
    # -------------------------------------------------------------------------
    # SILENT ROOM (northeast of guild entrance)
    # -------------------------------------------------------------------------
    silent_room = create_object("typeclasses.rooms.Room", key="Silent Room")
    silent_room.db.desc = (
        "This is a silent room where no channels, tells, or says can reach you. "
        "The air feels thick and muffled, as if sound itself has been drained "
        "from the space. It is a place of refuge for those who need absolute "
        "quiet from the chatter of the world."
    )
    silent_room.db.area = "Ilium City"
    silent_room.db.danger_level = 0
    silent_room.db.is_outdoors = False
    silent_room.db.ambient_msgs = [
        (0.05, "The silence presses against your ears like a physical weight.")
    ]
    
    create_exit(adventurer_guild, silent_room, "northeast", "southwest")
    
    # -------------------------------------------------------------------------
    # PLAQUE ROOMS (west of guild entrance)
    # -------------------------------------------------------------------------
    plaque_rooms = create_object("typeclasses.rooms.Room", key="Plaque Rooms")
    plaque_rooms.db.desc = (
        "This large and marbleized room holds the famed plaques of Red Dragon. "
        "Because it is valued among so many adventurers, its encasing is grand "
        "indeed. The walls are made of a solid white rock, lined with veins of "
        "blue. The floor is blue quartz. The numerous plaques hang on the walls, "
        "each one commemorating a great deed or legendary adventurer."
    )
    plaque_rooms.db.area = "Ilium City"
    plaque_rooms.db.danger_level = 0
    plaque_rooms.db.is_outdoors = False
    
    create_exit(adventurer_guild, plaque_rooms, "west", "east")
    
    # -------------------------------------------------------------------------
    # PORTAL ROOM (southwest of guild entrance)
    # -------------------------------------------------------------------------
    portal_room = create_object("typeclasses.rooms.Room", key="Portal Room")
    portal_room.db.desc = (
        "This small room houses the portals to the alpha guilds of Red Dragon "
        "for the ease and convenience of all adventurers. A shimmering gateway "
        "stands in each direction, leading to the various guild headquarters."
    )
    portal_room.db.area = "Ilium City"
    portal_room.db.danger_level = 0
    portal_room.db.is_outdoors = False
    
    create_exit(adventurer_guild, portal_room, "southwest", "northeast")
    
    # -------------------------------------------------------------------------
    # CLOUD ROAD BETWEEN GOSSAMER AND TITAN (north of guild entrance)
    # -------------------------------------------------------------------------
    cloud_road = create_object("typeclasses.rooms.Room", key="On Cloud Road between Gossamer and Titan")
    cloud_road.db.desc = (
        "You stand on Cloud Road before a mighty structure! Here stands the "
        "Adventurers Guild. It contains some of the most helpful things in the "
        "world of Red Dragon. To the east is Titan Street; to the west is "
        "Gossamer Street. Small trees line the road, their leaves whispering "
        "in the breeze."
    )
    cloud_road.db.area = "Ilium City"
    cloud_road.db.danger_level = 0
    cloud_road.db.is_outdoors = True
    cloud_road.db.ambient_msgs = [
        (0.1, "A cart rumbles past, its driver nodding politely."),
        (0.05, "A floating moonflower vine drifts by, glowing softly.")
    ]
    
    # Add objects
    memorial = create_object("typeclasses.objects.Object", key="a grand memorial", 
                             location=cloud_road)
    memorial.db.desc = "A grand memorial stands here, commemorating the founding of the guild."
    
    create_exit(adventurer_guild, cloud_road, "north", "south")
    
    # -------------------------------------------------------------------------
    # INTERSECTION OF CLOUD AND TITAN (east of cloud road)
    # -------------------------------------------------------------------------
    cloud_titan_intersection = create_object("typeclasses.rooms.Room", key="Intersection of Cloud and Titan")
    cloud_titan_intersection.db.desc = (
        "The edge of the Illium Bazaar here blends into Cloud Road, which heads "
        "west towards the Illian Adventurers' Guild. The guild is a domed building, "
        "visible for blocks - especially over the low stalls of the marketplace. "
        "The city cathedral lies close by to the south, dominating the landscape "
        "for blocks around."
    )
    cloud_titan_intersection.db.area = "Ilium City"
    cloud_titan_intersection.db.danger_level = 0
    cloud_titan_intersection.db.is_outdoors = True
    cloud_titan_intersection.db.ambient_msgs = [
        (0.1, "A shopkeeper runs by, waving a broom, chasing a pair of young men."),
        (0.05, "The smell of cooking food wafts from the bazaar.")
    ]
    
    create_exit(cloud_road, cloud_titan_intersection, "east", "west")
    
    # -------------------------------------------------------------------------
    # ON TITAN STREET (north of intersection)
    # -------------------------------------------------------------------------
    titan_street = create_object("typeclasses.rooms.Room", key="On Titan Street")
    titan_street.db.desc = (
        "An abundance of wisps twirl around you as you step into this section of "
        "Illium City. Large and small buildings have been erected all around you, "
        "providing the necessary services to the city of Illium. The street is "
        "bustling with activity as adventurers and citizens go about their day."
    )
    titan_street.db.area = "Ilium City"
    titan_street.db.danger_level = 0
    titan_street.db.is_outdoors = True
    titan_street.db.ambient_msgs = [
        (0.1, "A floating moonflower vine drifts past, its glow pulsing gently."),
        (0.05, "A merchant calls out their wares from a nearby stall.")
    ]
    
    create_exit(cloud_titan_intersection, titan_street, "north", "south")
    
    # -------------------------------------------------------------------------
    # GOSSAMER STREET (west of cloud road - placeholder for expansion)
    # -------------------------------------------------------------------------
    gossamer_street = create_object("typeclasses.rooms.Room", key="On Gossamer Street")
    gossamer_street.db.desc = (
        "Gossamer Street stretches before you, named for the delicate silk that "
        "was once traded here in abundance. The buildings here are older, their "
        "stone facades weathered by centuries of wind and rain. Lanterns hang "
        "from iron brackets, casting warm pools of light on the cobblestones."
    )
    gossamer_street.db.area = "Ilium City"
    gossamer_street.db.danger_level = 0
    gossamer_street.db.is_outdoors = True
    
    create_exit(cloud_road, gossamer_street, "west", "east")
    
    # Create Judge Achman NPC in Level Room
    achman = create_object("typeclasses.npcs.JudgeAchman", key="Achman the Judge",
                            location=level_room)
    
    # Create formula items on floor (based on IOM)
    formula1 = create_object("typeclasses.objects.Formula", key="Formula: Head: Lesser Wisdoms",
                            location=adventurer_guild)
    formula1.db.formula_type = "head"
    formula1.db.formula_name = "Lesser Wisdoms"
    formula1.db.desc = "A mysterious formula that can be used to create headgear."
    
    formula2 = create_object("typeclasses.objects.Formula", key="Formula: Head: Lesser Wisdoms",
                            location=adventurer_guild)
    formula2.db.formula_type = "head"
    formula2.db.formula_name = "Lesser Wisdoms"
    formula2.db.desc = "A mysterious formula that can be used to create headgear."
    
    # -------------------------------------------------------------------------
    # BANK OF ILLIUM (north of titan street)
    # -------------------------------------------------------------------------
    bank_room = create_object("typeclasses.rooms.BankRoom", key="Bank of Illium")
    bank_room.db.desc = (
        "The Bank of Illium stands as a monument to commerce and trust. Massive "
        "stone columns support a vaulted ceiling painted with scenes of trade and "
        "prosperity. Tellers stand behind polished marble counters, ready to serve "
        "adventurers with their banking needs. A heavy iron vault door stands "
        "impressively at the back of the room."
    )
    bank_room.db.area = "Ilium City"
    bank_room.db.danger_level = 0
    bank_room.db.is_outdoors = False
    
    # Create banker NPC
    banker = create_object("typeclasses.shops.Bank", key="a large steel vault",
                           location=bank_room)
    
    create_exit(titan_street, bank_room, "north", "south")
    
    # -------------------------------------------------------------------------
    # GENERAL STORE (east of titan street)
    # -------------------------------------------------------------------------
    shop_room = create_object("typeclasses.rooms.ShopRoom", key="Maxxis General Store")
    shop_room.db.desc = (
        "Shelves line every wall of this cozy shop, packed with goods for the "
        "traveling adventurer. The smell of leather, oil, and dried herbs fills "
        "the air. Maxxis, the shopkeeper, watches over his wares with a keen eye."
    )
    shop_room.db.area = "Ilium City"
    shop_room.db.danger_level = 0
    shop_room.db.is_outdoors = False
    
    # Create shopkeeper NPC
    shopkeeper = create_object("typeclasses.shops.Shopkeeper", key="Maxxis the Shopkeeper",
                               location=shop_room)
    shopkeeper.db.items_for_sale = {
        "a torch": {"price": 10, "stock": 50},
        "a healing potion": {"price": 50, "stock": 20},
        "a bread roll": {"price": 5, "stock": 100},
        "a waterskin": {"price": 15, "stock": 30},
    }
    
    create_exit(titan_street, shop_room, "east", "west")
    
    return adventurer_guild


# =============================================================================
# NEWBIE GUILD DISTRICT
# =============================================================================

def create_newbie_guild():
    """Create the Newbie Guild area connected to Adventurers' Guild."""
    
    # -------------------------------------------------------------------------
    # NEWBIE GUILD ENTRANCE
    # -------------------------------------------------------------------------
    newbie_guild_entrance = create_object("typeclasses.rooms.Room", key="Newbie Guild Entrance")
    newbie_guild_entrance.db.desc = (
        "This room is large, and the ceiling is high. To the northwest is "
        "another room, while to the east is the Newbie Guild."
    )
    newbie_guild_entrance.db.area = "Ilium City"
    newbie_guild_entrance.db.danger_level = 0
    newbie_guild_entrance.db.is_outdoors = False
    
    # -------------------------------------------------------------------------
    # ENTRANCE TO THE NEWBIE GUILD
    # -------------------------------------------------------------------------
    newbie_guild = create_object("typeclasses.rooms.Room", key="Entrance to the Newbie Guild")
    newbie_guild.db.desc = (
        "Welcome Newbies! This is where you can find all sorts of great "
        "information to help start you off on your adventures here at Red "
        "Dragon. For lots of advice on getting started you should begin by "
        "speaking with Sisong. She's here especially to help you out."
    )
    newbie_guild.db.area = "Ilium City"
    newbie_guild.db.danger_level = 0
    newbie_guild.db.is_outdoors = False
    
    # Create Sisong NPC
    sisong = create_object("typeclasses.npcs.NewbieNavigatorSisong", key="Sisong the Newbie Navigator",
                           location=newbie_guild)
    
    # Create portal to Nuvo City
    nuvo_portal = create_object("typeclasses.objects.Object", key="a blue portal", 
                                location=newbie_guild)
    nuvo_portal.db.desc = "A shimmering blue portal that leads to Nuvo City."
    
    # Create gold plaque
    plaque = create_object("typeclasses.objects.Object", key="a gold plaque",
                           location=newbie_guild)
    plaque.db.desc = "A gleaming gold plaque with helpful information for newbies."
    
    create_exit(newbie_guild_entrance, newbie_guild, "east", "west")
    
    # -------------------------------------------------------------------------
    # BRIGHTLY LIT HALLWAY (north/south from newbie guild)
    # -------------------------------------------------------------------------
    hallway = create_object("typeclasses.rooms.Room", key="Brightly Lit Hallway")
    hallway.db.desc = (
        "You are wandering down a brightly lit hallway. To the east you can make "
        "out the entrance to Maxxis' Newbie Shop and to the south is the way back "
        "to the entrance of the Newbie Guild."
    )
    hallway.db.area = "Ilium City"
    hallway.db.danger_level = 0
    hallway.db.is_outdoors = False
    
    create_exit(newbie_guild, hallway, "north", "south")
    
    # -------------------------------------------------------------------------
    # USED EQUIPMENT STORAGE ROOM (east from newbie guild)
    # -------------------------------------------------------------------------
    equipment_room = create_object("typeclasses.rooms.Room", key="Used Equipment Storage Room")
    equipment_room.db.desc = (
        "This simple room is virtually empty, apart from the conspicuous machine "
        "situated in the middle of the room and humming quietly to itself. "
        "Apparently this location has been set aside to house the newbie equipment "
        "dispensing machine. It can be used to obtain a fresh set of equipment. "
        "Of course, being free, this 'eq' is probably worth just that, next to "
        "nothing."
    )
    equipment_room.db.area = "Ilium City"
    equipment_room.db.danger_level = 0
    equipment_room.db.is_outdoors = False
    
    create_exit(newbie_guild, equipment_room, "east", "west")
    
    return newbie_guild_entrance


def build_ilium_city():
    """Build the complete Ilium City area."""
    guild = create_ilium_adventurers_guild()
    newbie_entrance = create_newbie_guild()
    
    # Connect newbie guild to adventurer guild (southeast from guild, northwest from newbie)
    create_exit(guild, newbie_entrance, "southeast", "northwest")
    
    # TODO: As the subagent maps more rooms, expand this function
    # to connect additional streets, buildings, and landmarks.
    
    return guild
