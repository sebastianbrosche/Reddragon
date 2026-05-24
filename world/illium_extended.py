"""
Red Dragon MUD - Complete Ilium City Grid
Based on Islands of Myth ASCII map (memorized_media/20260524_illium_city_map_full.png)

Legend:
  A=Auction House, Adv=Adventurer Guild, Ap=Apothecary, Ar=Armorer,
  Bk=Bank, Bm=Blu Moon, C=Central Square, Ca=Cathedral, Cc=Circus,
  Cl=Hall of Clans, Fd=Food Shop, Ff=Fiery Flagon, Fig=Fighters Guild,
  Gen=General Store, Gsp=Greasy Spoon, Mag=Mage Guild, Mh=Music Hall,
  Ms=Magic Shop, P=Pawnshop, Pv=Pavilion of Gods, Rm=Race Museum,
  Rs=Ring Shop, Toy=Toy Store, Tr=EQ Trader, Vt=Veldrens Tower,
  Wea=Weaponsmith, Blk=Blacksmith
"""

from evennia import create_object, search_object
from world.ilium import create_exit


# =============================================================================
# ROOM DEFINITIONS
# =============================================================================

ROOMS = {
    # Building rooms
    "weaponsmith": {
        "key": "Weaponsmith",
        "desc": (
            "The clang of hammer on anvil rings out as you enter the weaponsmith's shop. "
            "Heat waves shimmer from the forge, and the walls are lined with blades of every "
            "description. The smith, a burly dwarf with soot-stained arms, barely looks up "
            "from his work."
        ),
        "type": "typeclasses.rooms.ShopRoom",
    },
    "armorer": {
        "key": "Armorer",
        "desc": (
            "Racks of leather, chain, and plate armor line the walls of this well-organized "
            "shop. The smell of leather treatment oil and polish hangs in the air. A half-elf "
            "attendant helps a nervous young warrior try on his first set of chainmail."
        ),
        "type": "typeclasses.rooms.ShopRoom",
    },
    "pawnshop": {
        "key": "Pawnshop",
        "desc": (
            "A cramped, cluttered shop filled with the cast-off possessions of desperate "
            "adventurers. The pawnbroker, a shifty-eyed gnome, peers at you over a mountain "
            "of unpaid pledges."
        ),
        "type": "typeclasses.rooms.ShopRoom",
    },
    "pavilion": {
        "key": "Pavilion of Gods",
        "desc": (
            "An open-air pavilion with marble columns supporting a domed roof of shimmering "
            "crystal. Shrines to the various gods of the realm line the perimeter. In the "
            "center, a pool of mercury-like liquid reflects starlight even during the day."
        ),
        "type": "typeclasses.rooms.Room",
    },
    "music_hall": {
        "key": "Music Hall",
        "desc": (
            "A grand hall with exceptional acoustics, its walls adorned with tapestries "
            "depicting famous bards and their instruments. A small stage occupies the far end, "
            "where performers of all races gather to share their craft."
        ),
        "type": "typeclasses.rooms.Room",
    },
    "mage_guild": {
        "key": "Mage Guild",
        "desc": (
            "A building that seems larger on the inside than the outside, thanks to spatial "
            "magic. Floating candles provide illumination, and the air shimmers with residual "
            "spell energy. Apprentices sit at desks, copying spells from ancient texts."
        ),
        "type": "typeclasses.rooms.Room",
    },
    "cathedral": {
        "key": "Cathedral",
        "desc": (
            "Stained glass windows cast rainbow patterns across the marble floor of this "
            "magnificent cathedral. Rows of pews stretch toward an ornate altar where high "
            "priests conduct services. Great pillars rise to support a vaulted ceiling."
        ),
        "type": "typeclasses.rooms.Room",
    },
    "veldrens_tower": {
        "key": "Veldrens Tower",
        "desc": (
            "A narrow spiral staircase winds upward through this wizard's tower. Bookshelves "
            "crammed with ancient tomes line every wall. The air smells of ozone and old parchment. "
            "A crystal orb on a pedestal pulses with soft blue light."
        ),
        "type": "typeclasses.rooms.Room",
    },
    "bank": {
        "key": "Bank of Illium",
        "desc": (
            "A secure building of thick stone and iron grates. Tellers sit behind a long counter, "
            "counting gold coins and recording transactions in heavy leather ledgers. Guards in "
            "polished armor stand at attention near the vault door."
        ),
        "type": "typeclasses.rooms.ShopRoom",
    },
    "general_store": {
        "key": "General Store",
        "desc": (
            "A cluttered shop that seems to sell a little bit of everything. Rope, lanterns, trail "
            "rations, waterskins, bedrolls, and a hundred other adventuring essentials are crammed "
            "onto overloaded shelves."
        ),
        "type": "typeclasses.rooms.ShopRoom",
    },
    "apothecary": {
        "key": "Apothecary",
        "desc": (
            "Glass jars filled with herbs, powders, and mysterious liquids cover every surface "
            "of this aromatic shop. Dried plants hang from the ceiling in bunches, and a mortar "
            "and pestle sits on a central workbench."
        ),
        "type": "typeclasses.rooms.ShopRoom",
    },
    "food_shop": {
        "key": "Food Shop",
        "desc": (
            "The delicious aroma of fresh bread and roasting meat greets you as you enter this "
            "cozy eatery. A long counter displays today's offerings — hearty stews, crusty loaves, "
            "wheels of cheese, and freshly picked fruits."
        ),
        "type": "typeclasses.rooms.ShopRoom",
    },
    "ring_shop": {
        "key": "Ring Shop",
        "desc": (
            "A tiny shop that glitters with gold and gemstones. Velvet-lined cases display rings "
            "of every description — simple bands, elaborate signets, and magical rings that glow "
            "with inner light."
        ),
        "type": "typeclasses.rooms.ShopRoom",
    },
    "central_square": {
        "key": "Central Square",
        "desc": (
            "The bustling heart of Illium City. Cobblestones worn smooth by centuries of foot "
            "traffic stretch out in every direction. This is where all roads in Illium meet. "
            "A great clock tower rises nearby, its bells marking the hours."
        ),
        "type": "typeclasses.rooms.Room",
    },
    "fighters_guild": {
        "key": "Fighters Guild",
        "desc": (
            "A spacious training hall where the sound of clashing steel echoes off stone walls. "
            "Wooden practice dummies stand in rows. A burly orc instructor demonstrates a parry "
            "technique to a group of eager students."
        ),
        "type": "typeclasses.rooms.Room",
    },
    "fiery_flagon": {
        "key": "Fiery Flagon",
        "desc": (
            "A raucous tavern where adventurers gather to drink, gamble, and share exaggerated "
            "stories. The bar is made from a single slab of mahogany, scarred by countless tankards. "
            "A bard in the corner plays a lively tune on a lute."
        ),
        "type": "typeclasses.rooms.ShopRoom",
    },
    "race_museum": {
        "key": "Race Museum",
        "desc": (
            "A quiet hall dedicated to the diverse races that inhabit the world. Detailed dioramas "
            "show each race in their native environments, and plaques describe their cultures, "
            "abilities, and histories."
        ),
        "type": "typeclasses.rooms.Room",
    },
    "auction_house": {
        "key": "Auction House",
        "desc": (
            "A grand hall with tiered seating surrounding a central podium where the auctioneer "
            "conducts sales. Today the room is filled with collectors, merchants, and curious "
            "onlookers examining the lots on display."
        ),
        "type": "typeclasses.rooms.Room",
    },
    "blacksmith": {
        "key": "Blacksmith",
        "desc": (
            "A forge that never seems to cool. The blacksmith, a towering half-giant with arms "
            "like tree trunks, hammers glowing metal into horseshoes, nails, and simple tools. "
            "Sparks fly with every strike."
        ),
        "type": "typeclasses.rooms.ShopRoom",
    },
    "greasy_spoon": {
        "key": "Greasy Spoon",
        "desc": (
            "A no-frills eatery where the food is cheap, filling, and surprisingly good. The floor "
            "is sticky, the tables are wobbly, and the menu is written on a chalkboard. But the "
            "portions are enormous."
        ),
        "type": "typeclasses.rooms.ShopRoom",
    },
    "toy_store": {
        "key": "Toy Store",
        "desc": (
            "A whimsical shop filled with carved wooden animals, spinning tops, dolls in miniature "
            "armor, and puzzles that challenge the mind. The toymaker sits at a workbench carving "
            "a block of wood into what might become a dragon."
        ),
        "type": "typeclasses.rooms.ShopRoom",
    },
    "eq_trader": {
        "key": "EQ Trader",
        "desc": (
            "A secondhand equipment shop where adventurers sell their old gear and buy upgrades. "
            "The inventory changes daily based on what people have traded in."
        ),
        "type": "typeclasses.rooms.ShopRoom",
    },
    "magic_shop": {
        "key": "Magic Shop",
        "desc": (
            "A shop that smells of incense and ozone, its shelves lined with scrolls, wands, potions, "
            "and spell components. A crystal ball on the counter shows swirling mist."
        ),
        "type": "typeclasses.rooms.ShopRoom",
    },
    "circus": {
        "key": "Circus",
        "desc": (
            "A colorful tent that has been permanently erected in this square. Jugglers practice "
            "their routines outside, while acrobats stretch on ropes strung between nearby buildings. "
            "The ringmaster promises 'the greatest show in all the islands!'"
        ),
        "type": "typeclasses.rooms.Room",
    },
    "hall_of_clans": {
        "key": "Hall of Clans",
        "desc": (
            "A formal hall where the various player clans and guilds maintain their headquarters. "
            "Banners bearing clan crests hang from the walls. A large map on one wall shows "
            "territories claimed by the most powerful groups."
        ),
        "type": "typeclasses.rooms.Room",
    },
    "blu_moon": {
        "key": "Blu Moon",
        "desc": (
            "An upscale tavern with blue-tinted glass windows that cast everything in a moonlit glow. "
            "The clientele here is more refined than at the Fiery Flagon — merchants, minor nobility, "
            "and successful adventurers."
        ),
        "type": "typeclasses.rooms.ShopRoom",
    },
    
    # Street/road rooms
    "north_street_west": {
        "key": "North Street West",
        "desc": "A wide cobblestone street running along the northern edge of the city center. Shops and workshops line both sides.",
        "type": "typeclasses.rooms.Room",
    },
    "north_street_east": {
        "key": "North Street East",
        "desc": "The eastern stretch of North Street, where the buildings grow taller and the merchants more affluent.",
        "type": "typeclasses.rooms.Room",
    },
    "market_street_west": {
        "key": "Market Street West",
        "desc": "Market Street bustles with vendors and shoppers. Stalls line both sides of the road, selling everything from fresh produce to enchanted trinkets.",
        "type": "typeclasses.rooms.Room",
    },
    "market_street_east": {
        "key": "Market Street East",
        "desc": "The eastern end of Market Street, where the food vendors give way to more permanent shops and guild houses.",
        "type": "typeclasses.rooms.Room",
    },
    "south_street_west": {
        "key": "South Street West",
        "desc": "South Street runs along the southern edge of the city center. The buildings here are older, their facades decorated with faded murals.",
        "type": "typeclasses.rooms.Room",
    },
    "south_street_east": {
        "key": "South Street East",
        "desc": "The eastern stretch of South Street, past the cathedral's shadow. The buildings are a mix of residences and small shops.",
        "type": "typeclasses.rooms.Room",
    },
    "bottom_street_west": {
        "key": "Bottom Street West",
        "desc": "The western end of the city's southernmost street, near the guild houses and training halls.",
        "type": "typeclasses.rooms.Room",
    },
    "bottom_street_east": {
        "key": "Bottom Street East",
        "desc": "The eastern stretch of Bottom Street, where the entertainment venues and specialized shops cluster together.",
        "type": "typeclasses.rooms.Room",
    },
    "west_road": {
        "key": "West Road",
        "desc": "West Road is quieter than the main thoroughfares. Small houses and local businesses line the road.",
        "type": "typeclasses.rooms.Room",
    },
    "east_road": {
        "key": "East Road",
        "desc": "East Road runs past the Cathedral's shadow. The buildings are well-maintained, with flower boxes on the windowsills.",
        "type": "typeclasses.rooms.Room",
    },
    "central_north": {
        "key": "Central North Road",
        "desc": "The road running north from Central Square, toward the Pavilion and Music Hall.",
        "type": "typeclasses.rooms.Room",
    },
    "central_south": {
        "key": "Central South Road",
        "desc": "The road running south from Central Square, toward the Race Museum and southern districts.",
        "type": "typeclasses.rooms.Room",
    },
    "cloud_road_mid": {
        "key": "Cloud Road Mid",
        "desc": "Cloud Road continues here, the cobblestones well-worn by countless adventurer feet.",
        "type": "typeclasses.rooms.Room",
    },
}


# =============================================================================
# EXIT CONNECTIONS (from_room, exit_name, to_room, return_name)
# =============================================================================

EXITS = [
    # --- NORTHERN ROW: Weaponsmith -> Armorer -> Pawnshop ---
    ("weaponsmith", "east", "armorer", "west"),
    ("armorer", "east", "pawnshop", "west"),
    
    # --- UPPER MIDDLE: Pavilion -> Music Hall -> Mage Guild ---
    ("pavilion", "east", "music_hall", "west"),
    ("music_hall", "east", "mage_guild", "west"),
    
    # --- Connections from northern row to upper middle ---
    ("weaponsmith", "south", "pavilion", "north"),
    ("armorer", "south", "music_hall", "north"),
    ("pawnshop", "south", "mage_guild", "north"),
    
    # --- MIDDLE AREA: General Store, Apothecary, Food Shop, Bank, Ring Shop, Veldren Tower ---
    ("general_store", "east", "apothecary", "west"),
    ("apothecary", "east", "food_shop", "west"),
    ("food_shop", "east", "bank", "west"),
    ("bank", "east", "ring_shop", "west"),
    ("ring_shop", "east", "veldrens_tower", "west"),
    
    # --- Vertical connections for middle area ---
    ("general_store", "north", "pavilion", "south"),
    ("apothecary", "north", "music_hall", "south"),
    ("food_shop", "north", "cathedral", "south"),
    ("bank", "north", "veldrens_tower", "south"),
    ("ring_shop", "north", "mage_guild", "south"),
    
    # --- CENTER: Central Square connections ---
    ("central_square", "north", "food_shop", "south"),
    ("central_square", "south", "race_museum", "north"),
    ("central_square", "west", "apothecary", "east"),
    ("central_square", "east", "cathedral", "west"),
    
    # --- LOWER MIDDLE: Toy Store, Race Museum, Fiery Flagon ---
    ("toy_store", "east", "race_museum", "west"),
    ("race_museum", "east", "fiery_flagon", "west"),
    
    # --- Vertical from lower middle ---
    ("toy_store", "north", "apothecary", "south"),
    ("fiery_flagon", "north", "cathedral", "south"),
    
    # --- BOTTOM ROW: Blacksmith -> Auction House -> Fighters Guild ---
    ("blacksmith", "east", "auction_house", "west"),
    ("auction_house", "east", "fighters_guild", "west"),
    
    # --- Vertical from bottom row ---
    ("blacksmith", "north", "toy_store", "south"),
    ("auction_house", "north", "race_museum", "south"),
    ("fighters_guild", "north", "fiery_flagon", "south"),
    
    # --- SOUTHERNMOST: Circus, EQ Trader, Magic Shop, Hall of Clans, Blu Moon, Greasy Spoon ---
    ("circus", "east", "eq_trader", "west"),
    ("eq_trader", "east", "magic_shop", "west"),
    ("magic_shop", "east", "hall_of_clans", "west"),
    ("hall_of_clans", "east", "blu_moon", "west"),
    ("blu_moon", "east", "greasy_spoon", "west"),
    
    # --- Vertical from southernmost to bottom row ---
    ("circus", "north", "blacksmith", "south"),
    ("eq_trader", "north", "auction_house", "south"),
    ("magic_shop", "north", "auction_house", "south"),
    ("hall_of_clans", "north", "fighters_guild", "south"),
    ("blu_moon", "north", "fighters_guild", "south"),
    ("greasy_spoon", "north", "fighters_guild", "south"),
    
    # --- STREET/ROAD CONNECTIONS (bridging between districts) ---
    # North Street connects northern buildings
    ("weaponsmith", "west", "north_street_west", "east"),
    ("north_street_west", "east", "armorer", "west"),
    ("armorer", "east", "north_street_east", "west"),
    ("north_street_east", "east", "pawnshop", "west"),
    
    # Market Street connects middle area
    ("general_store", "west", "market_street_west", "east"),
    ("market_street_west", "east", "apothecary", "west"),
    ("apothecary", "west", "market_street_west", "east"),
    ("food_shop", "west", "market_street_west", "east"),
    ("food_shop", "east", "market_street_east", "west"),
    ("market_street_east", "west", "food_shop", "east"),
    ("bank", "east", "market_street_east", "west"),
    ("market_street_east", "east", "ring_shop", "west"),
    
    # South Street connects lower area
    ("toy_store", "west", "south_street_west", "east"),
    ("south_street_west", "east", "race_museum", "west"),
    ("race_museum", "west", "south_street_west", "east"),
    ("race_museum", "east", "south_street_east", "west"),
    ("south_street_east", "west", "race_museum", "east"),
    ("fiery_flagon", "east", "south_street_east", "west"),
    
    # Bottom Street
    ("blacksmith", "west", "bottom_street_west", "east"),
    ("bottom_street_west", "east", "auction_house", "west"),
    ("auction_house", "west", "bottom_street_west", "east"),
    ("auction_house", "east", "bottom_street_east", "west"),
    ("bottom_street_east", "west", "auction_house", "east"),
    ("fighters_guild", "east", "bottom_street_east", "west"),
    
    # Cloud Road area (connecting to Adventurer's Guild)
    ("general_store", "north", "cloud_road_mid", "south"),
    ("cloud_road_mid", "south", "general_store", "north"),
    ("cloud_road_mid", "east", "apothecary", "west"),
    ("apothecary", "west", "cloud_road_mid", "east"),
    
    # West Road
    ("blacksmith", "west", "west_road", "east"),
    ("west_road", "east", "blacksmith", "west"),
    ("west_road", "north", "greasy_spoon", "south"),
    ("greasy_spoon", "south", "west_road", "north"),
    
    # East Road
    ("cathedral", "east", "east_road", "west"),
    ("east_road", "west", "cathedral", "east"),
    ("east_road", "south", "fiery_flagon", "north"),
    ("fiery_flagon", "north", "east_road", "south"),
    
    # Central connections
    ("central_square", "north", "central_north", "south"),
    ("central_north", "south", "central_square", "north"),
    ("central_north", "north", "food_shop", "south"),
    ("food_shop", "south", "central_north", "north"),
    ("central_square", "south", "central_south", "north"),
    ("central_south", "north", "central_square", "south"),
    ("central_south", "south", "race_museum", "north"),
    ("race_museum", "north", "central_south", "south"),
]


# =============================================================================
# BUILD FUNCTION
# =============================================================================

def create_illium_extended_grid(guild_entrance):
    """
    Build the extended Ilium City grid.
    
    Args:
        guild_entrance: The Adventurer Guild Entrance room (from ilium.py)
    """
    created_rooms = {}
    
    # Create all rooms
    for key, room_def in ROOMS.items():
        # Check if room already exists
        existing = search_object(room_def["key"], typeclass="typeclasses.rooms.Room")
        if existing:
            room = existing[0]
            print(f"  Using existing room: {room_def['key']}")
        else:
            room = create_object(room_def["type"], key=room_def["key"])
            print(f"  Created room: {room_def['key']}")
        
        room.db.desc = room_def["desc"]
        room.db.area = "Ilium City"
        room.db.danger_level = 0
        if room_def["type"] == "typeclasses.rooms.ShopRoom":
            room.db.is_outdoors = False
        else:
            room.db.is_outdoors = True
        
        created_rooms[key] = room
    
    # Connect to guild entrance (Cloud Road from Adventurer's Guild)
    # The guild_entrance "north" exit goes to Cloud Road (already created in ilium.py)
    cloud_road = None
    for exit_obj in guild_entrance.exits:
        if exit_obj.key == "north":
            cloud_road = exit_obj.destination
            break
    
    if cloud_road:
        # Connect Cloud Road to the city grid
        # From the map, Cloud Road connects west toward General Store area
        create_exit(cloud_road, created_rooms.get("general_store"), "west", "east")
        print(f"  Connected Cloud Road to General Store")
    
    # Create all exits
    for from_key, exit_name, to_key, return_name in EXITS:
        from_room = created_rooms.get(from_key)
        to_room = created_rooms.get(to_key)
        
        if not from_room or not to_room:
            print(f"  SKIP: Missing room for exit {from_key} -> {to_key}")
            continue
        
        # Check if exit already exists
        existing_exits = [ex for ex in from_room.exits if ex.key == exit_name]
        if existing_exits:
            continue
        
        # Create exit using helper
        create_exit(from_room, to_room, exit_name, return_name)
        print(f"  Connected: {from_room.key} --{exit_name}--> {to_room.key}")
    
    print(f"\n=== Extended Ilium City built: {len(created_rooms)} rooms ===")
    return created_rooms


if __name__ == "__main__":
    # For testing
    from evennia import search_object
    guild = search_object("Adventurer Guild Entrance", typeclass="typeclasses.rooms.Room")
    if guild:
        create_illium_extended_grid(guild[0])
    else:
        print("Adventurer Guild Entrance not found!")
