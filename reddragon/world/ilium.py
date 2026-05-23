"""
Red Dragon MUD - Ilium City World Building
Based on Islands of Myth reverse-engineering (Session logs from emalz exploration)
Area: Ilium City - The central hub of the world
"""

from evennia import create_object

DIRECTION_ALIASES = {
    "north": ["n"],
    "south": ["s"],
    "east": ["e"],
    "west": ["w"],
    "northeast": ["ne"],
    "northwest": ["nw"],
    "southeast": ["se"],
    "southwest": ["sw"],
    "up": ["u"],
    "down": ["d"],
}

def create_exit(origin, destination, exit_name, return_name=None):
    """Helper to create bidirectional exits with standard aliases."""
    from evennia import create_object
    
    # Create forward exit
    forward = create_object("typeclasses.exits.Exit", key=exit_name, 
                           location=origin, destination=destination)
    
    # Add aliases (n, s, e, w, ne, nw, se, sw, u, d)
    aliases = DIRECTION_ALIASES.get(exit_name.lower(), [])
    for alias in aliases:
        forward.aliases.add(alias)
    
    # Create return exit if requested
    if return_name:
        backward = create_object("typeclasses.exits.Exit", key=return_name,
                                  location=destination, destination=origin)
        # Add aliases for return direction too
        return_aliases = DIRECTION_ALIASES.get(return_name.lower(), [])
        for alias in return_aliases:
            backward.aliases.add(alias)
    
    return forward

# =============================================================================
# ILLIUM CITY - ADVENTURERS' GUILD DISTRICT
# =============================================================================

def create_ilium_adventurers_guild():
    r"""Create the Adventurers' Guild area of Ilium City.
    
    Map layout (from IOM):
    
        | 0        [Cloud Road is north of 0]
        |/
    1-@-2 +-6
     /|\  |
    3 4 +-5-7
        |
        +-8
        |
        9
    
    0 = Silent Room
    1 = Plaque Room
    2 = Level Advance (Level Room)
    3 = Portal room
    4 = Myth room
    5 = Newbie guild
    6 = Maxxis' shop
    7 = Equipment Machine
    8 = Tree of Life
    9 = Reinc portal
    
    @ = Adventurer Guild Entrance (hub)
    """
    
    # -------------------------------------------------------------------------
    # HUB: ADVENTURER GUILD ENTRANCE (@ on map)
    # -------------------------------------------------------------------------
    guild_entrance = create_object("typeclasses.rooms.Room", key="Adventurer Guild Entrance")
    guild_entrance.db.desc = (
        "This large room is the Adventurers guild. Truly breathtaking in its "
        "architecture, the guild houses a vast amount of help for the new "
        "adventurers and the old. Its high domed ceiling swirls with blue and "
        "whites, like the sky on a very windy day. Because it is domed and "
        "there are windows all along the wall, the room seems very open and "
        "very friendly."
    )
    guild_entrance.db.area = "Ilium City"
    guild_entrance.db.room_type = "guild"
    guild_entrance.db.has_guild = True
    guild_entrance.db.danger_level = 0
    guild_entrance.db.is_outdoors = False
    
    # -------------------------------------------------------------------------
    # 0: SILENT ROOM (north of hub, via northeast from hub)
    # -------------------------------------------------------------------------
    silent_room = create_object("typeclasses.rooms.Room", key="Silent Room")
    silent_room.db.desc = (
        "This is a silent room where no channels/tells/says can reach you."
    )
    silent_room.db.area = "Ilium City"
    silent_room.db.danger_level = 0
    silent_room.db.is_outdoors = False
    silent_room.db.ambient_msgs = [
        (0.05, "The silence presses against your ears like a physical weight.")
    ]
    
    create_exit(guild_entrance, silent_room, "northeast", "southwest")
    
    # -------------------------------------------------------------------------
    # 1: PLAQUE ROOM (west of hub)
    # -------------------------------------------------------------------------
    plaque_room = create_object("typeclasses.rooms.Room", key="Plaque Rooms")
    plaque_room.db.desc = (
        "This large and marbleized room holds the famed plaques of Islands of Myth. "
        "Because it is valued among so many adventurers, its encasing is grand indeed. "
        "The walls are made of a solid white rock, lined with veins of blue. The floor "
        "is blue quartz. The numerous plaques hang on the walls."
    )
    plaque_room.db.area = "Ilium City"
    plaque_room.db.danger_level = 0
    plaque_room.db.is_outdoors = False
    
    create_exit(guild_entrance, plaque_room, "west", "east")
    
    # -------------------------------------------------------------------------
    # 2: LEVEL ROOM / JUDGE ROOM (east of hub)
    # -------------------------------------------------------------------------
    level_room = create_object("typeclasses.rooms.Room", key="Level Room")
    level_room.db.desc = (
        "This room is large, and the ceiling is high. In the center stands a "
        "large podium. Upon that podium sits Achman, the judge. He controls the "
        "levels of Islands of Myth, and has the power to create some of the strongest "
        "players. He sits in a high back chair built into the podium. Talk to him "
        "if you wish to advance in your endeavors."
    )
    level_room.db.area = "Ilium City"
    level_room.db.danger_level = 0
    level_room.db.is_outdoors = False
    
    # Create Achman NPC
    achman = create_object("typeclasses.npcs.JudgeAchman", key="Achman the Judge",
                           location=level_room)
    
    create_exit(guild_entrance, level_room, "east", "west")
    
    # -------------------------------------------------------------------------
    # 3: PORTAL ROOM (southwest of hub)
    # -------------------------------------------------------------------------
    portal_room = create_object("typeclasses.rooms.Room", key="Portal Room")
    portal_room.db.desc = (
        "This small room houses the portals to the alpha guilds of Islands of Myth "
        "for the ease and convenience of all adventurers."
    )
    portal_room.db.area = "Ilium City"
    portal_room.db.danger_level = 0
    portal_room.db.is_outdoors = False
    
    create_exit(guild_entrance, portal_room, "southwest", "northeast")
    
    # Guild portal exits (lead to guild headquarters - currently loop back as placeholders)
    guilds = [
        "shifter", "abjurer", "elemental", "woodsman", "martial_artist",
        "lurker", "druid", "acrobat", "weaver", "evoker", "unraveller",
        "psychics", "warrior"
    ]
    
    for guild in guilds:
        # Create a placeholder destination room for each guild
        guild_room = create_object("typeclasses.rooms.Room", key=f"{guild.capitalize()} Guild")
        guild_room.db.desc = f"The {guild.capitalize()} Guild headquarters. A place of training and power."
        guild_room.db.area = "Ilium City"
        guild_room.db.danger_level = 0
        guild_room.db.is_outdoors = False
        
        # Portal exit from portal room to guild (one-way portal)
        portal_exit = create_object("typeclasses.exits.Exit", key=guild,
                                     location=portal_room, destination=guild_room)
        # Return exit from guild back to portal room
        return_exit = create_object("typeclasses.exits.Exit", key="portal",
                                     location=guild_room, destination=portal_room)
    
    # -------------------------------------------------------------------------
    # 4: MYTH ROOM (south of hub)
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
    
    create_exit(guild_entrance, myth_room, "south", "north")
    
    # -------------------------------------------------------------------------
    # 6: MAXXIS' SHOP (northeast of Level Room / east of hub area)
    # -------------------------------------------------------------------------
    maxxis_shop = create_object("typeclasses.rooms.ShopRoom", key="Maxxis' Shop")
    maxxis_shop.db.desc = (
        "Shelves line every wall of this cozy shop, packed with goods for the "
        "traveling adventurer. The smell of leather, oil, and dried herbs fills "
        "the air. Maxxis, the shopkeeper, watches over his wares with a keen eye."
    )
    maxxis_shop.db.area = "Ilium City"
    maxxis_shop.db.danger_level = 0
    maxxis_shop.db.is_outdoors = False
    
    # Create shopkeeper NPC
    maxxis = create_object("typeclasses.shops.Shopkeeper", key="Maxxis the Shopkeeper",
                           location=maxxis_shop)
    maxxis.db.items_for_sale = {
        "a torch": {"price": 10, "stock": 50},
        "a healing potion": {"price": 50, "stock": 20},
        "a bread roll": {"price": 5, "stock": 100},
        "a waterskin": {"price": 15, "stock": 30},
    }
    
    create_exit(level_room, maxxis_shop, "east", "west")
    
    # -------------------------------------------------------------------------
    # CLOUD ROAD (north of guild entrance — IOM shows @ has 'north' exit)
    # -------------------------------------------------------------------------
    cloud_road = create_object("typeclasses.rooms.Room", key="On Cloud Road between Gossamer and Titan")
    cloud_road.db.desc = (
        "You stand on Cloud Road before a mighty structure! Here stands the "
        "Adventurers Guild. It contains some of the most helpful things in the "
        "world of Islands of Myth. To the east is Titan Street; to the west is "
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
    
    # Add memorial object
    memorial = create_object("typeclasses.objects.Object", key="a grand memorial",
                             location=cloud_road)
    memorial.db.desc = "A grand memorial stands here, commemorating the founding of the guild."
    
    # @ north → Cloud Road; Cloud Road south → @
    create_exit(guild_entrance, cloud_road, "north", "south")
    
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
    # GOSSAMER STREET (west of cloud road)
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
    
    # Create formula items on floor (based on IOM)
    formula1 = create_object("typeclasses.objects.Formula", key="Formula: Head: Lesser Wisdoms",
                            location=guild_entrance)
    formula1.db.formula_type = "head"
    formula1.db.formula_name = "Lesser Wisdoms"
    formula1.db.desc = "A mysterious formula that can be used to create headgear."
    
    formula2 = create_object("typeclasses.objects.Formula", key="Formula: Head: Lesser Wisdoms",
                            location=guild_entrance)
    formula2.db.formula_type = "head"
    formula2.db.formula_name = "Lesser Wisdoms"
    formula2.db.desc = "A mysterious formula that can be used to create headgear."
    
    return {
        "entrance": guild_entrance,
        "level_room": level_room,
        "silent_room": silent_room,
        "plaque_room": plaque_room,
        "portal_room": portal_room,
        "myth_room": myth_room,
        "maxxis_shop": maxxis_shop,
        "cloud_road": cloud_road,
    }


# =============================================================================
# NEWBIE GUILD DISTRICT
# =============================================================================

def create_newbie_guild():
    r"""Create the Newbie Guild area connected to Adventurers' Guild.
    
    Map layout (from IOM, positions 5-9):
        5 = Newbie guild (southeast from hub)
        7 = Equipment Machine (east of 5)
        8 = Tree of Life (south of 5)
        9 = Reinc portal (south of 8)
    """
    
    # -------------------------------------------------------------------------
    # 5: NEWBIE GUILD ENTRANCE (southeast of main guild hub)
    # -------------------------------------------------------------------------
    newbie_guild = create_object("typeclasses.rooms.Room", key="Newbie Guild")
    newbie_guild.db.desc = (
        "Welcome Newbies! This is where you can find all sorts of great "
        "information to help start you off on your adventures here at Islands of "
        "Myth. For lots of advice on getting started you should begin by "
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
    
    # -------------------------------------------------------------------------
    # 7: EQUIPMENT MACHINE (east of newbie guild)
    # -------------------------------------------------------------------------
    equipment_room = create_object("typeclasses.rooms.Room", key="Equipment Machine")
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
    
    # -------------------------------------------------------------------------
    # 8: TREE OF LIFE (south of newbie guild)
    # -------------------------------------------------------------------------
    tree_room = create_object("typeclasses.rooms.Room", key="Tree of Life")
    tree_room.db.desc = (
        "A massive tree dominates this chamber, its branches spreading out in all "
        "directions and filling the room with a gentle, warm light. The bark is "
        "smooth and silver, and small glowing motes drift lazily through the air. "
        "It is said that those who touch the tree may find new beginnings."
    )
    tree_room.db.area = "Ilium City"
    tree_room.db.danger_level = 0
    tree_room.db.is_outdoors = False
    tree_room.db.ambient_msgs = [
        (0.05, "The tree's leaves rustle softly, though there is no wind."),
        (0.03, "A glowing mote drifts past your face, warm and gentle.")
    ]
    
    create_exit(newbie_guild, tree_room, "south", "north")
    
    # -------------------------------------------------------------------------
    # 9: REINC PORTAL (south of Tree of Life)
    # -------------------------------------------------------------------------
    reinc_room = create_object("typeclasses.rooms.Room", key="Reinc Portal")
    reinc_room.db.desc = (
        "A single stone archway stands in the center of this otherwise empty room. "
        "Within the arch, a swirling vortex of silver and gold energy pulses with a "
        "rhythm like a heartbeat. The air tastes of ozone and possibility. This is "
        "the portal of reincarnation, where adventurers may begin anew."
    )
    reinc_room.db.area = "Ilium City"
    reinc_room.db.danger_level = 0
    reinc_room.db.is_outdoors = False
    
    create_exit(tree_room, reinc_room, "south", "north")
    
    return newbie_guild


def build_ilium_city():
    """Build the complete Ilium City area."""
    guild_area = create_ilium_adventurers_guild()
    newbie_guild = create_newbie_guild()
    
    guild_entrance = guild_area["entrance"]
    level_room = guild_area["level_room"]
    
    # Connect newbie guild to adventurer guild (southeast from hub, northwest from newbie)
    create_exit(guild_entrance, newbie_guild, "southeast", "northwest")
    
    # Map shows 5 (Newbie Guild) is also south of 2 (Level Room)
    create_exit(level_room, newbie_guild, "south", "north")
    
    # TODO: As the subagent maps more rooms, expand this function
    # to connect additional streets, buildings, and landmarks.
    
    return guild_entrance
