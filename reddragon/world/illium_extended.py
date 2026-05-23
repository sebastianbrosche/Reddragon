"""
Red Dragon MUD - Ilium City Extended Map
Based on Islands of Myth map screenshot (2026-05-24)

Map reference: /root/.openclaw/workspace/memorized_media/20260524_illium_city_map_full.png

Key landmarks (from Legend):
  A  = Auction House      Adv= Adventure Guild   Ap = Apothecary
  Ar = Armorer            Bk = Bank              Bm = Blu Moon
  C  = Central Square     Ca = Cathedral         Cc = Circus
  Cl = Hall of Clans      Fd = Food Shop         Ff = Fiery Flagon
  Fig= Fighters Guild     Gen= General Store     Gsp= Greasy Spoon
  Mag= Mage Guild         Mh = Music Hall        Ms = Magic Shop
  P  = Pawnshop           Pv = Pavilion of Gods  Rm = Race Museum
  Rs = Ring Shop          Toy= Toy Store         Tr = EQ Trader
  Vt = Veldrens Tower     Wea= Weaponsmith       Blk= Blacksmith
"""

from evennia import create_object
from world.ilium import create_exit


def create_illium_extended_grid(guild_entrance):
    """
    Build the extended Ilium City grid based on IOM map.
    
    Grid reference (relative to Adv at origin):
      - North (+y), South (-y), East (+x), West (-x)
      - From Adv to CS: n, 3w, 3s → CS at roughly (-3, -2)
    """
    
    # ========================================================================
    # CENTRAL SQUARE AND PATH FROM ADVENTURER'S GUILD
    # ========================================================================
    
    # Step 1 from Adv: north → Cloud Road (already exists in base ilium.py)
    # We need to link west from Cloud Road towards Central Square
    
    # Find existing Cloud Road
    cloud_road = None
    for obj in guild_entrance.contents_get():
        if obj.key == "On Cloud Road between Gossamer and Titan":
            # Actually this is the room itself, not an exit destination
            pass
    
    # Better: search for it
    from evennia import search_object
    cloud_roads = search_object("On Cloud Road between Gossamer and Titan", typeclass="typeclasses.rooms.Room")
    cloud_road = cloud_roads[0] if cloud_roads else None
    
    if not cloud_road:
        # Create it if missing
        cloud_road = create_object("typeclasses.rooms.Room", key="On Cloud Road between Gossamer and Titan")
        cloud_road.db.desc = (
            "You stand on Cloud Road before a mighty structure! Here stands the "
            "Adventurers Guild."
        )
        cloud_road.db.area = "Ilium City"
        cloud_road.db.is_outdoors = True
    
    # Path from Cloud Road: 3 west
    # Step 1 west: Ring Shop area / first street segment
    ring_shop_street = create_object("typeclasses.rooms.Room", key="On Cloud Road near the Ring Shop")
    ring_shop_street.db.desc = (
        "Cloud Road continues here, passing by a small shop with glittering rings "
        "displayed in the window. The shopkeeper eyes you warily. The street is "
        "narrower here, with tall buildings casting long shadows."
    )
    ring_shop_street.db.area = "Ilium City"
    ring_shop_street.db.is_outdoors = True
    
    create_exit(cloud_road, ring_shop_street, "west", "east")
    
    # Create Ring Shop building (north of this street)
    ring_shop = create_object("typeclasses.rooms.ShopRoom", key="Ring Shop")
    ring_shop.db.desc = (
        "The Ring Shop is a small, dimly lit store filled with display cases. Rings "
        "of every description line the shelves - gold, silver, jeweled, enchanted. "
        "The owner, a wiry old man with a jeweler's loupe perpetually in one eye, "
        "nods at you."
    )
    ring_shop.db.area = "Ilium City"
    ring_shop.db.is_outdoors = False
    
    create_exit(ring_shop_street, ring_shop, "north", "south")
    
    # Step 2 west: General Store area
    general_street = create_object("typeclasses.rooms.Room", key="On Cloud Road near the General Store")
    general_street.db.desc = (
        "The smell of leather, spices, and dried meat fills the air here. A large "
        "sign creaks in the wind above a broad doorway. The street widens slightly, "
        "and a few carts are parked along the curb."
    )
    general_street.db.area = "Ilium City"
    general_street.db.is_outdoors = True
    
    create_exit(ring_shop_street, general_street, "west", "east")
    
    # Create General Store (south of this street)
    general_store = create_object("typeclasses.rooms.ShopRoom", key="General Store")
    general_store.db.desc = (
        "The General Store is a sprawling establishment with goods piled high on "
        "rough wooden shelves. Ropes, lanterns, bedrolls, rations, and a hundred "
        "other adventuring necessities fill the space. The shopkeeper haggles with "
        "a customer in the corner."
    )
    general_store.db.area = "Ilium City"
    general_store.db.is_outdoors = False
    
    create_exit(general_street, general_store, "south", "north")
    
    # Step 3 west: Veldrens Tower / approaching Central Square
    tower_street = create_object("typeclasses.rooms.Room", key="On Cloud Road near Veldrens Tower")
    tower_street.db.desc = (
        "A tall, spiraling tower rises to the north, its peak lost in the clouds. "
        "The stonework is ancient, covered in creeping vines that shimmer with a "
        "faint magical light. The street here is cleaner, the cobblestones well-maintained."
    )
    tower_street.db.area = "Ilium City"
    tower_street.db.is_outdoors = True
    
    create_exit(general_street, tower_street, "west", "east")
    
    # Create Veldrens Tower
    veldrens_tower = create_object("typeclasses.rooms.Room", key="Veldrens Tower")
    veldrens_tower.db.desc = (
        "The interior of Veldrens Tower is a single circular chamber with a vaulted "
        "ceiling that disappears into shadow. Arcane symbols glow softly on the walls, "
        "and the air hums with latent magic. A spiral staircase winds upward into darkness."
    )
    veldrens_tower.db.area = "Ilium City"
    veldrens_tower.db.is_outdoors = False
    
    create_exit(tower_street, veldrens_tower, "north", "south")
    
    # Now 3 south from tower_street to Central Square
    # Step 1 south: Cathedral area (this is the street south of Veldrens)
    cathedral_street = create_object("typeclasses.rooms.Room", key="South of Veldrens Tower")
    cathedral_street.db.desc = (
        "The street opens up here, revealing a massive cathedral to the east. Its "
        "spires pierce the sky, and the sound of chanting drifts from within. The "
        "cobblestones are worn smooth by centuries of pilgrim feet."
    )
    cathedral_street.db.area = "Ilium City"
    cathedral_street.db.is_outdoors = True
    
    create_exit(tower_street, cathedral_street, "south", "north")
    
    # Create Cathedral (east of this street)
    cathedral = create_object("typeclasses.rooms.Room", key="Cathedral")
    cathedral.db.desc = (
        "The Cathedral of Illium is a vast, awe-inspiring structure. Stained glass "
        "windows cast colored light across rows of polished pews. The air smells of "
        "incense and old stone. A massive pipe organ dominates the far wall, and a "
        "calm reverence fills the space."
    )
    cathedral.db.area = "Ilium City"
    cathedral.db.is_outdoors = False
    
    create_exit(cathedral_street, cathedral, "east", "west")
    
    # Step 2 south: Food Shop / Apothecary area
    market_street = create_object("typeclasses.rooms.Room", key="Market Street")
    market_street.db.desc = (
        "Market Street is bustling with vendors and shoppers. Stalls line both sides "
        "of the road, selling everything from fresh produce to enchanted trinkets. The "
        "smell of baked bread and exotic spices fills the air."
    )
    market_street.db.area = "Ilium City"
    market_street.db.is_outdoors = True
    
    create_exit(cathedral_street, market_street, "south", "north")
    
    # Create Food Shop (west of this street)
    food_shop = create_object("typeclasses.rooms.ShopRoom", key="Food Shop")
    food_shop.db.desc = (
        "The Food Shop is a warm, inviting place with wooden tables and the smell of "
        "freshly baked bread. Jars of preserves, wheels of cheese, and smoked meats "
        "hang from the ceiling. The baker wipes flour from her hands and greets you."
    )
    food_shop.db.area = "Ilium City"
    food_shop.db.is_outdoors = False
    
    create_exit(market_street, food_shop, "west", "east")
    
    # Create Apothecary (east of this street)
    apothecary = create_object("typeclasses.rooms.ShopRoom", key="Apothecary")
    apothecary.db.desc = (
        "The Apothecary is filled with the sharp scents of herbs and chemicals. Glass "
        "jars containing dried roots, powdered minerals, and strange liquids line the "
        "shelves. The apothecary, a thin woman with ink-stained fingers, measures "
        "ingredients with precision."
    )
    apothecary.db.area = "Ilium City"
    apothecary.db.is_outdoors = False
    
    create_exit(market_street, apothecary, "east", "west")
    
    # Step 3 south: Central Square!
    central_square = create_object("typeclasses.rooms.Room", key="Central Square")
    central_square.db.desc = (
        "This small room houses the portals to the alpha guilds of Islands of Myth "
        "for the ease and convenience of all adventurers."
    )
    central_square.db.area = "Ilium City"
    central_square.db.is_outdoors = True
    
    create_exit(market_street, central_square, "south", "north")
    
    # ========================================================================
    # SOUTHERN DISTRICT (below Central Square)
    # ========================================================================
    
    # South of Central Square: Race Museum area
    south_street = create_object("typeclasses.rooms.Room", key="South Street")
    south_street.db.desc = (
        "South Street runs along the southern edge of the city center. The buildings "
        "here are older, their facades decorated with faded murals. A museum sign "
        "catches your eye."
    )
    south_street.db.area = "Ilium City"
    south_street.db.is_outdoors = True
    
    create_exit(central_square, south_street, "south", "north")
    
    # Race Museum (east of south street)
    race_museum = create_object("typeclasses.rooms.Room", key="Race Museum")
    race_museum.db.desc = (
        "The Race Museum is a grand hall filled with dioramas and displays depicting "
        "the history of every race in Islands of Myth. Statues of famous heroes from "
        "each race stand in alcoves along the walls. Informational plaques describe "
        "their unique abilities and cultures."
    )
    race_museum.db.area = "Ilium City"
    race_museum.db.is_outdoors = False
    
    create_exit(south_street, race_museum, "east", "west")
    
    # Toy Store (west of south street)
    toy_store = create_object("typeclasses.rooms.ShopRoom", key="Toy Store")
    toy_store.db.desc = (
        "The Toy Store is a whimsical shop filled with wind-up toys, enchanted dolls, "
        "and miniature replicas of famous landmarks. Colorful streamers hang from the "
        "ceiling, and the proprietor is a jolly fellow with paint-stained apron."
    )
    toy_store.db.area = "Ilium City"
    toy_store.db.is_outdoors = False
    
    create_exit(south_street, toy_store, "west", "east")
    
    # ========================================================================
    # BOTTOM DISTRICT (southernmost part of map)
    # ========================================================================
    
    # Bottom street: Fighters Guild, Circus, EQ Trader, etc.
    bottom_street = create_object("typeclasses.rooms.Room", key="Bottom Street")
    bottom_street.db.desc = (
        "The southernmost street of Illium is quieter than the rest. The buildings here "
        "serve more specialized purposes - training halls, guild houses, and entertainment "
        "venues. The cobblestones are worn, and the street lamps flicker."
    )
    bottom_street.db.area = "Ilium City"
    bottom_street.db.is_outdoors = True
    
    create_exit(south_street, bottom_street, "south", "north")
    
    # Fighters Guild (east)
    fighters_guild = create_object("typeclasses.rooms.Room", key="Fighters Guild")
    fighters_guild.db.desc = (
        "The Fighters Guild is a rugged hall decorated with weapons and trophies from "
        "countless battles. Training dummies line one wall, and the sound of clashing "
        "steel echoes from the practice yard. A burly instructor eyes your stance."
    )
    fighters_guild.db.area = "Ilium City"
    fighters_guild.db.is_outdoors = False
    
    create_exit(bottom_street, fighters_guild, "east", "west")
    
    # Circus (southeast from bottom street - need an intermediate)
    circus_approach = create_object("typeclasses.rooms.Room", key="Circus Approach")
    circus_approach.db.desc = (
        "The sound of music and laughter draws you toward a large tent ahead. The smell "
        "of popcorn and sawdust fills the air."
    )
    circus_approach.db.area = "Ilium City"
    circus_approach.db.is_outdoors = True
    
    create_exit(bottom_street, circus_approach, "southeast", "northwest")
    
    circus = create_object("typeclasses.rooms.Room", key="Circus")
    circus.db.desc = (
        "The Circus is a riot of color and sound. Acrobats tumble through the air, "
        "clowns perform slapstick routines, and a ringmaster in a top hat bellows "
        "introductions. The big top tent is striped in red and gold."
    )
    circus.db.area = "Ilium City"
    circus.db.is_outdoors = False
    
    create_exit(circus_approach, circus, "east", "west")
    
    # EQ Trader (southwest from bottom street)
    eq_trader = create_object("typeclasses.rooms.Room", key="EQ Trader")
    eq_trader.db.desc = (
        "The EQ Trader is a specialized shop for adventuring equipment. Armor stands, "
        "weapon racks, and tool benches fill the space. A grizzled veteran sits behind "
        "the counter, evaluating gear with a practiced eye."
    )
    eq_trader.db.area = "Ilium City"
    eq_trader.db.is_outdoors = False
    
    create_exit(bottom_street, eq_trader, "southwest", "northeast")
    
    # ========================================================================
    # NORTHERN DISTRICT (above Cloud Road)
    # ========================================================================
    
    # North of Cloud Road: Weaponsmith, Pawnshop area
    north_street = create_object("typeclasses.rooms.Room", key="North Street")
    north_street.db.desc = (
        "North Street is lined with specialized craft shops. The clang of hammers on "
        "anvils and the smell of hot metal fill the air. Master craftsmen ply their "
        "trades in open-front workshops."
    )
    north_street.db.area = "Ilium City"
    north_street.db.is_outdoors = True
    
    create_exit(cloud_road, north_street, "north", "south")
    
    # Weaponsmith (west)
    weaponsmith = create_object("typeclasses.rooms.ShopRoom", key="Weaponsmith")
    weaponsmith.db.desc = (
        "The Weaponsmith is a forge and shop in one. Swords, axes, spears, and maces "
        "hang from racks, gleaming with oil. The smith, a broad-shouldered dwarf, hammers "
        "a glowing blade on his anvil. Sparks fly with each strike."
    )
    weaponsmith.db.area = "Ilium City"
    weaponsmith.db.is_outdoors = False
    
    create_exit(north_street, weaponsmith, "west", "east")
    
    # Pawnshop (east)
    pawnshop = create_object("typeclasses.rooms.ShopRoom", key="Pawnshop")
    pawnshop.db.desc = (
        "The Pawnshop is a cluttered establishment with goods piled haphazardly on "
        "shelves and in bins. A shrewd-looking man with a calculator eyes every item "
        "you carry, estimating its value."
    )
    pawnshop.db.area = "Ilium City"
    pawnshop.db.is_outdoors = False
    
    create_exit(north_street, pawnshop, "east", "west")
    
    # Music Hall (north of north street)
    music_hall = create_object("typeclasses.rooms.Room", key="Music Hall")
    music_hall.db.desc = (
        "The Music Hall is an elegant auditorium with rows of velvet seats facing a "
        "grand stage. The acoustics are perfect, and famous bards from across the realm "
        "perform here. A grand piano sits in one corner, and instruments of every kind "
        "line the walls."
    )
    music_hall.db.area = "Ilium City"
    music_hall.db.is_outdoors = False
    
    create_exit(north_street, music_hall, "north", "south")
    
    # ========================================================================
    # WESTERN DISTRICT (off General Store / Gossamer)
    # ========================================================================
    
    # West of General Store street: Greasy Spoon, etc.
    west_street = create_object("typeclasses.rooms.Room", key="West Street")
    west_street.db.desc = (
        "West Street is quieter than the main thoroughfares. Small houses and local "
        "businesses line the road. The smell of cooking drifts from a nearby diner."
    )
    west_street.db.area = "Ilium City"
    west_street.db.is_outdoors = True
    
    create_exit(general_street, west_street, "west", "east")
    
    # Greasy Spoon (south)
    greasy_spoon = create_object("typeclasses.rooms.ShopRoom", key="Greasy Spoon")
    greasy_spoon.db.desc = (
        "The Greasy Spoon is a no-nonsense diner with checkered tablecloths and "
        "comfort food. The menu is simple: meat, potatoes, bread, and ale. The cook "
        "shouts orders from the kitchen while a tired waitress refills mugs."
    )
    greasy_spoon.db.area = "Ilium City"
    greasy_spoon.db.is_outdoors = False
    
    create_exit(west_street, greasy_spoon, "south", "north")
    
    # ========================================================================
    # EASTERN DISTRICT (off Cathedral area)
    # ========================================================================
    
    # East of Cathedral: Fiery Flagon
    east_street = create_object("typeclasses.rooms.Room", key="East Street")
    east_street.db.desc = (
        "East Street runs past the Cathedral's shadow. The buildings here are a mix "
        "of residences and small shops. The street is well-maintained, with flower "
        "boxes on the windowsills."
    )
    east_street.db.area = "Ilium City"
    east_street.db.is_outdoors = True
    
    create_exit(cathedral, east_street, "east", "west")
    
    # Fiery Flagon (south)
    fiery_flagon = create_object("typeclasses.rooms.ShopRoom", key="Fiery Flagon")
    fiery_flagon.db.desc = (
        "The Fiery Flagon is a lively tavern with a roaring fireplace and long wooden "
        "tables. Patrons sing bawdy songs while tankards clink. The barkeep, a woman "
        "with a burn scar across one cheek, serves drinks with a no-nonsense attitude."
    )
    fiery_flagon.db.area = "Ilium City"
    fiery_flagon.db.is_outdoors = False
    
    create_exit(east_street, fiery_flagon, "south", "north")
    
    # ========================================================================
    # ADDITIONAL LANDMARKS
    # ========================================================================
    
    # Armorer (northwest of Ring Shop area)
    armorer = create_object("typeclasses.rooms.ShopRoom", key="Armorer")
    armorer.db.desc = (
        "The Armorer is a workshop filled with breastplates, helms, shields, and "
        "greaves. The smell of leather and oil permeates the air. A half-finished suit "
        "of plate mail stands on a wooden frame."
    )
    armorer.db.area = "Ilium City"
    armorer.db.is_outdoors = False
    
    create_exit(ring_shop_street, armorer, "northwest", "southeast")
    
    # Mage Guild (northeast of Cathedral)
    mage_guild = create_object("typeclasses.rooms.Room", key="Mage Guild")
    mage_guild.db.desc = (
        "The Mage Guild is a tower of blue stone surrounded by a garden of strange "
        "plants. Inside, the walls are lined with bookshelves, and magical apparatus "
        "bubbles and steams on workbenches. Apprentices study ancient tomes while "
        "masters conduct experiments."
    )
    mage_guild.db.area = "Ilium City"
    mage_guild.db.is_outdoors = False
    
    create_exit(cathedral_street, mage_guild, "northeast", "southwest")
    
    # Magic Shop (south of EQ Trader)
    magic_shop = create_object("typeclasses.rooms.ShopRoom", key="Magic Shop")
    magic_shop.db.desc = (
        "The Magic Shop sells spell components, scrolls, wands, and enchanted trinkets. "
        "The shelves glow faintly with stored magic. A nervous young clerk organizes "
        "vials of powdered unicorn horn and dragon scales."
    )
    magic_shop.db.area = "Ilium City"
    magic_shop.db.is_outdoors = False
    
    # Connect to bottom street area - create a south extension
    bottom_south = create_object("typeclasses.rooms.Room", key="Bottom South Street")
    bottom_south.db.desc = (
        "The street continues southward, past the main guild houses toward the city's "
        "southern wall. The buildings are sparse here, and you can see the city gates "
        "in the distance."
    )
    bottom_south.db.area = "Ilium City"
    bottom_south.db.is_outdoors = True
    
    create_exit(bottom_street, bottom_south, "south", "north")
    create_exit(bottom_south, magic_shop, "west", "east")
    
    # Hall of Clans (east of bottom south)
    hall_of_clans = create_object("typeclasses.rooms.Room", key="Hall of Clans")
    hall_of_clans.db.desc = (
        "The Hall of Clans is a vast circular chamber with banners hanging from the "
        "ceiling. Each banner represents a player clan, displaying their colors and "
        "emblems. A registration desk sits in the center where new clans can be formed."
    )
    hall_of_clans.db.area = "Ilium City"
    hall_of_clans.db.is_outdoors = False
    
    create_exit(bottom_south, hall_of_clans, "east", "west")
    
    # Blu Moon (southeast)
    blu_moon = create_object("typeclasses.rooms.ShopRoom", key="Blu Moon")
    blu_moon.db.desc = (
        "Blu Moon is an upscale establishment with blue silk curtains and silver "
        "candelabras. The clientele is well-dressed, and the conversation is hushed. "
        "Fine wines and exotic delicacies are served by impeccably dressed staff."
    )
    blu_moon.db.area = "Ilium City"
    blu_moon.db.is_outdoors = False
    
    create_exit(bottom_south, blu_moon, "southeast", "northwest")
    
    # Auction House (near Blacksmith)
    blacksmith = create_object("typeclasses.rooms.ShopRoom", key="Blacksmith")
    blacksmith.db.desc = (
        "The Blacksmith is a hot, noisy forge with multiple hearths blazing. Anvils "
        "ring with hammer blows, and the air shimmers with heat. Raw iron ingots are "
        "stacked by the door, and finished tools hang on the walls."
    )
    blacksmith.db.area = "Ilium City"
    blacksmith.db.is_outdoors = False
    
    create_exit(bottom_street, blacksmith, "west", "east")
    
    auction_house = create_object("typeclasses.rooms.Room", key="Auction House")
    auction_house.db.desc = (
        "The Auction House is a grand hall with a podium at the center and rows of "
        "seats rising in tiers. Rich merchants and adventurers gather here to bid on "
        "rare items. An auctioneer pounds a gavel, calling out prices in rapid-fire "
        "cadence."
    )
    auction_house.db.area = "Ilium City"
    auction_house.db.is_outdoors = False
    
    create_exit(bottom_street, auction_house, "south", "north")
    
    # Pavilion of Gods (north of Weaponsmith area)
    pavilion = create_object("typeclasses.rooms.Room", key="Pavilion of Gods")
    pavilion.db.desc = (
        "The Pavilion of Gods is an open-air shrine with statues of the deities of "
        "Islands of Myth arranged in a circle. Worshippers leave offerings at the feet "
        "of their chosen gods. The air is thick with incense, and a priest tends the "
        "eternal flame at the center."
    )
    pavilion.db.area = "Ilium City"
    pavilion.db.is_outdoors = True
    
    create_exit(weaponsmith, pavilion, "north", "south")
    
    return central_square
