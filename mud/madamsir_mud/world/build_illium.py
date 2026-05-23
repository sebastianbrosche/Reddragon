#!/usr/bin/env python3
"""
Illium City Map Builder for Myth of Islands MUD
Parses the ASCII map from IOM and builds all rooms with exits.
Run with: @py from world.build_illium import build_illium_city; build_illium_city()
"""

from evennia import create_object, search_object
from typeclasses.rooms import Room
from typeclasses.exits import Exit

# Room definitions: (key, alias, description, island)
ROOMS = {
    # Main grid rooms
    "Adventurer Guild": ("Adventurer's Guild of Illium", "adv", 
        "The grand Adventurer's Guild of Illium. Tall wooden beams support a vaulted ceiling, "
        "and the walls are lined with notices of quests and bounties. A large hearth crackles "
        "with a warm fire, and several adventurers lounge about, swapping tales of their "
        "latest exploits. A worn counter stands against the north wall where guildmasters "
        "can assist you with your journey.\n\n"
        "A plaque on the wall reads: 'All new adventurers start here. Type LOOK for help.'",
        "illium"),
    
    "Central Square": ("Central Square", "c",
        "The bustling heart of Illium City. Cobblestones worn smooth by centuries of foot "
        "traffic stretch out in every direction. Merchants hawk their wares from wooden stalls, "
        "children chase pigeons, and the sound of a nearby fountain provides a soothing backdrop. "
        "A great clock tower rises to the east, its bells marking the hours for the entire city. "
        "This is where all roads in Illium meet.\n\n"
        "A weathered signpost points in every direction toward the city's many districts.",
        "illium"),
    
    "Weaponsmith": ("Weaponsmith", "wea",
        "The clang of hammer on anvil rings out as you enter the weaponsmith's shop. Heat "
        "waves shimmer from the forge, and the walls are lined with blades of every description "
        "— from simple daggers to great two-handed swords. The smith, a burly dwarf with soot-"
        "stained arms, barely looks up from his work. Racks of spears, axes, and maces fill the "
        "remaining space, each weapon tagged with a price in gold coins.",
        "illium"),
    
    "Armorer": ("Armorer", "ar",
        "Racks of leather, chain, and plate armor line the walls of this well-organized shop. "
        "The smell of leather treatment oil and polish hangs in the air. A half-elf attendant "
        "helps a nervous young warrior try on his first set of chainmail. Shields of all shapes "
        "and sizes hang from the ceiling, and a small selection of helms and gauntlets are "
        "displayed on a central table.",
        "illium"),
    
    "Pawnshop": ("Pawnshop", "p",
        "A cramped, cluttered shop filled with the cast-off possessions of desperate adventurers. "
        "The pawnbroker, a shifty-eyed gnome, peers at you over a mountain of unpaid pledges. "
        "Shelves overflow with odd trinkets, rusty weapons, and mysterious artifacts of dubious "
        "origin. A sign behind the counter reads 'No haggling — prices are final.' The smell of "
        "dust and old cloth permeates the room.",
        "illium"),
    
    "Pavilion of Gods": ("Pavilion of Gods", "pv",
        "An open-air pavilion with marble columns supporting a domed roof of shimmering crystal. "
        "The air here feels charged with divine energy. Shrines to the various gods of the realm "
        "line the perimeter, each attended by a minor acolyte. In the center, a pool of "
        "mercury-like liquid reflects starlight even during the day. Devotees come here to pray, "
        "make offerings, or seek divine guidance for their quests.",
        "illium"),
    
    "Music Hall": ("Music Hall", "mh",
        "A grand hall with exceptional acoustics, its walls adorned with tapestries depicting "
        "famous bards and their instruments. A small stage occupies the far end, where performers "
        "of all races gather to share their craft. The wooden floor is worn smooth by dancers, "
        "and the balcony above provides seating for those who prefer to listen in comfort. The "
        "sound of a lute being tuned drifts from somewhere backstage.",
        "illium"),
    
    "Cathedral": ("Cathedral", "ca",
        "Stained glass windows cast rainbow patterns across the marble floor of this magnificent "
        "cathedral. Rows of pews stretch toward an ornate altar where high priests conduct services. "
        "The silence here is profound, broken only by the occasional whispered prayer or the "
        "shuffling of vestments. Great pillars rise to support a vaulted ceiling painted with "
        "scenes from the creation myths. Candles flicker in niches along the walls, lending a "
        "warm, sacred glow to the space.",
        "illium"),
    
    "Veldren Tower": ("Veldren's Tower", "vt",
        "A narrow spiral staircase winds upward through this wizard's tower. Bookshelves crammed "
        "with ancient tomes line every wall, and strange magical apparatus sits on cluttered desks. "
        "The air smells of ozone and old parchment. A crystal orb on a pedestal pulses with a soft "
        "blue light. Arcane symbols have been etched into the stone floor, and a black cat watches "
        "you with suspicious yellow eyes from atop a stack of grimoires.",
        "illium"),
    
    "Bank": ("Bank of Illium", "bk",
        "A secure building of thick stone and iron grates. Tellers sit behind a long counter, "
        "counting gold coins and recording transactions in heavy leather ledgers. Guards in polished "
        "armor stand at attention near the vault door, their hands resting on the pommels of their "
        "swords. The floor is made of marble so polished you can see your reflection. A sign warns "
        "that attempted robbery will result in immediate teleportation to the detention facility.",
        "illium"),
    
    "General Store": ("General Store", "gen",
        "A cluttered shop that seems to sell a little bit of everything. Rope, lanterns, trail "
        "rations, waterskins, bedrolls, and a hundred other adventuring essentials are crammed onto "
        "overloaded shelves. The proprietor, a cheerful halfling, greets every customer with a "
        "smile and a recommendation. Barrels of pickled goods line one wall, and a selection of "
        "simple clothing hangs from a rack near the door.",
        "illium"),
    
    "Apothecary": ("Apothecary", "ap",
        "Glass jars filled with herbs, powders, and mysterious liquids cover every surface of "
        "this aromatic shop. Dried plants hang from the ceiling in bunches, and a mortar and pestle "
        "sits on a central workbench. The apothecary, an elderly elf with kind eyes, can mix "
        "potions for healing, stamina, or even magical enhancement. The smell of lavender and "
        "something more pungent wafts through the air. Labels on the jars are written in several "
        "languages, some of them quite ancient.",
        "illium"),
    
    "Food Shop": ("Food Shop", "fd",
        "The delicious aroma of fresh bread and roasting meat greets you as you enter this cozy "
        "eatery. A long counter displays today's offerings — hearty stews, crusty loaves, wheels "
        "of cheese, and freshly picked fruits. The cook, a stout human with flour on her apron, "
        "calls out greetings to regulars. Wooden tables and benches provide seating, and a pot of "
        "mulled wine simmers near the fireplace. Travelers and locals alike gather here for a "
        "hot meal and the latest gossip.",
        "illium"),
    
    "Ring Shop": ("Ring Shop", "rs",
        "A tiny shop that glitters with gold and gemstones. Velvet-lined cases display rings of "
        "every description — simple bands, elaborate signets, and magical rings that glow with inner "
        "light. The jeweler, a precise gnome with a magnifying glass permanently perched on one eye, "
        "examines a diamond through a loupe. Price tags indicate that even the simplest piece here "
        "costs more than most adventurers earn in a month. A security golem stands motionless in "
        "the corner, watching.",
        "illium"),
    
    "Fighters Guild": ("Fighters Guild", "fig",
        "A spacious training hall where the sound of clashing steel echoes off stone walls. "
        "Wooden practice dummies stand in rows, many bearing the scars of thousands of sword strikes. "
        "A burly orc instructor demonstrates a parry technique to a group of eager students. The "
        "floor is covered with straw to cushion falls, and racks of practice weapons line the walls. "
        "Trophies from past tournaments hang above the mantle — banners, broken shields, and the "
        "mounted head of a dragon.",
        "illium"),
    
    "Mage Guild": ("Mage Guild", "mag",
        "A building that seems larger on the inside than the outside, thanks to spatial magic. "
        "Floating candles provide illumination, and the air shimmers with residual spell energy. "
        "Apprentices sit at desks, copying spells from ancient texts under the watchful eye of "
        "their masters. A summoning circle dominates the main chamber, its runes glowing softly. "
        "The shelves hold components for every spell imaginable — bat wings, eye of newt, powdered "
        "moonstone, and substances that defy categorization.",
        "illium"),
    
    "Fiery Flagon": ("Fiery Flagon", "ff",
        "A raucous tavern where adventurers gather to drink, gamble, and share exaggerated stories. "
        "The bar is made from a single slab of mahogany, scarred by countless tankards. A bard "
        "in the corner plays a lively tune on a lute, while patrons sing along off-key. The "
        "proprietor, a retired adventurer herself, keeps a loaded crossbow under the bar 'just "
        "in case.' The walls are decorated with maps, monster trophies, and a sign that reads "
        "'No spells indoors — last fireball cost us three tables.'",
        "illium"),
    
    "Race Museum": ("Race Museum", "rm",
        "A quiet hall dedicated to the diverse races that inhabit the world. Detailed dioramas "
        "show each race in their native environments, and plaques describe their cultures, abilities, "
        "and histories. A particularly impressive display shows a full-size dragon skeleton suspended "
        "from the ceiling. Interactive exhibits allow visitors to compare racial traits and "
        "abilities. A scholarly dwarf sits in the corner, annotating a thick book about entish "
        "migration patterns.",
        "illium"),
    
    "Auction House": ("Auction House", "a",
        "A grand hall with tiered seating surrounding a central podium where the auctioneer "
        "conducts sales. Today the room is filled with collectors, merchants, and curious onlookers "
        "examining the lots on display — rare weapons, magical artifacts, property deeds, and even "
        "the occasional exotic pet. Bidding paddles are stacked near the entrance, and a clerk "
        "registers new bidders in a leather-bound book. The air is thick with anticipation and "
        "the smell of expensive perfume.",
        "illium"),
    
    "Blacksmith": ("Blacksmith", "blk",
        "A forge that never seems to cool. The blacksmith, a towering half-giant with arms like "
        "tree trunks, hammers glowing metal into horseshoes, nails, and simple tools. Sparks fly "
        "with every strike, illuminating the soot-darkened walls. Barrels of coal and water stand "
        "ready, and a selection of farm implements and hardware hangs from pegs. The heat is "
        "intense, but the smith barely seems to notice, his focus entirely on his craft.",
        "illium"),
    
    "Greasy Spoon": ("Greasy Spoon", "gsp",
        "A no-frills eatery where the food is cheap, filling, and surprisingly good. The floor "
        "is sticky, the tables are wobbly, and the menu is written on a chalkboard that hasn't been "
        "fully erased in years. But the portions are enormous, and the cook somehow makes the best "
        "fried potatoes in the city. Truck drivers, dock workers, and adventurers on a budget "
        "fill the benches, trading stories over plates piled high with comfort food.",
        "illium"),
    
    "Toy Store": ("Toy Store", "toy",
        "A whimsical shop filled with carved wooden animals, spinning tops, dolls in miniature "
        "armor, and puzzles that challenge the mind. The toymaker, an elderly gnome with paint-"
        "stained fingers, sits at a workbench carving a block of wood into what might become a "
        "dragon. Shelves overflow with colorful merchandise, and the sound of a music box plays "
        "softly in the background. A sign in the window advertises 'Toys for children of all "
        "ages — including the young at heart.'",
        "illium"),
    
    "EQ Trader": ("Equipment Trader", "tr",
        "A secondhand equipment shop where adventurers sell their old gear and buy upgrades. "
        "The inventory changes daily based on what people have traded in. Today there are several "
        "serviceable leather jerkins, a dented helm with an interesting enchantment, and a sword "
        "that the previous owner claimed was 'cursed, but in a good way.' The trader, a sharp-"
        "eyed human, evaluates each item with a practiced eye before making an offer.",
        "illium"),
    
    "Magic Shop": ("Magic Shop", "ms",
        "A shop that smells of incense and ozone, its shelves lined with scrolls, wands, potions, "
        "and spell components. A crystal ball on the counter shows swirling mist — 'for divination "
        "practice only,' the shopkeeper insists. Bottles of colored liquids glow from within, and "
        "a broom in the corner sweeps of its own accord. The proprietor, a young wizard with ink "
        "stains on his robes, can identify magical items and sell basic scrolls to apprentices.",
        "illium"),
    
    "Blu Moon": ("Blu Moon", "bm",
        "An upscale tavern with blue-tinted glass windows that cast everything in a moonlit glow. "
        "The clientele here is more refined than at the Fiery Flagon — merchants, minor nobility, "
        "and successful adventurers. A pianist plays gentle melodies in the corner, and the wine "
        "list is extensive. The food is elegantly plated and priced accordingly. Private booths "
        "provide quiet corners for business discussions, and a bouncer at the door ensures that "
        "'troublemakers' don't disturb the atmosphere.",
        "illium"),
    
    "Circus": ("Circus", "cc",
        "A colorful tent that has been permanently erected in this square. Jugglers practice "
        "their routines outside, while acrobats stretch on ropes strung between nearby buildings. "
        "The ringmaster, a flamboyant human in a top hat, promises 'the greatest show in all the "
        "islands!' Posters advertise fire-breathers, trained animals, and a mysterious 'bearded "
        "lady' who may or may not be a dwarf in costume. The smell of popcorn and sugar-roasted "
        "nuts wafts from a nearby cart.",
        "illium"),
    
    "Hall of Clans": ("Hall of Clans", "cl",
        "A formal hall where the various player clans and guilds maintain their headquarters. "
        "Banners bearing clan crests hang from the walls, each one representing a group of allied "
        "adventurers. Meeting rooms of various sizes are available for reservation, and a clerk "
        "maintains a registry of all active clans. A large map on one wall shows territories "
        "claimed by the most powerful groups. New clans can register here for a modest fee.",
        "illium"),
    
    "Wishing Pool": ("Wishing Pool", "w",
        "A serene garden centered around a crystal-clear pool. Visitors toss coins into the "
        "water while making silent wishes. The surrounding garden is meticulously maintained, "
        "with flowers from every season somehow blooming simultaneously. A stone bench provides "
        "a place for quiet contemplation. Some say the pool has minor magical properties, and that "
        "occasionally a wish comes true — though usually not in the way the wisher intended.",
        "illium"),
    
    # Cloud Road side rooms
    "Silent Room": ("Silent Room", "0",
        "A small, soundproof chamber where adventurers can rest in perfect quiet. The walls are "
        "padded with some thick material that absorbs all noise. A single comfortable chair sits in "
        "the center, and a small table holds a selection of calming herbal teas. This room is "
        "popular with spellcasters who need to memorize complex incantations without distraction.",
        "illium"),
    
    "Plaque Room": ("Plaque Room", "1",
        "A hallway lined with commemorative plaques honoring legendary adventurers who have "
        "passed through Illium. Each plaque bears a name, a brief description of their greatest "
        "achievement, and the date of their last visit. Some are polished daily by admirers, while "
        "others have been forgotten and gather dust. Reading the plaques provides a fascinating "
        "history of the realm's greatest heroes and villains.",
        "illium"),
    
    "Level Advance": ("Level Advance", "2",
        "A grand chamber where experienced adventurers go to formalize their advancement in skill "
        "and power. A massive stone table dominates the room, its surface covered with intricate "
        "carvings that glow when someone worthy stands before them. Guildmasters from every "
        "discipline gather here to evaluate and certify those who have earned the right to advance. "
        "The atmosphere is formal and weighty with tradition.",
        "illium"),
    
    "Portal Room": ("Portal Room", "3",
        "A circular chamber with a permanently active magical portal in its center. The portal "
        "shimmers with rainbow light, and its destination changes based on the incantation spoken "
        "by the portal keeper. A schedule posted nearby lists the daily destinations and their "
        "associated costs. Guards stand ready to prevent unauthorized use, and a queue of travelers "
        "waits patiently for their turn to step through the swirling magic.",
        "illium"),
    
    "Myth Room": ("Myth Room", "4",
        "A cozy study filled with books of legends, myths, and folklore from across the islands. "
        "Comfortable armchairs invite visitors to lose themselves in tales of ancient heroes, "
        "forgotten gods, and legendary treasures. A fireplace burns with a fire that never seems to "
        "need fuel. The librarian, an old sage with spectacles perched on his nose, can answer "
        "questions about almost any legend — or at least point you to the right book.",
        "illium"),
    
    "Newbie Guild": ("Newbie Guild", "5",
        "A welcoming space designed for newcomers to the world. Friendly instructors offer basic "
        "training in combat, magic, and survival skills. Practice dummies, spell targets, and "
        "climbing walls provide safe environments to learn. Free equipment is available for those "
        "who need it, and a bulletin board lists simple quests suitable for beginners. Veteran "
        "adventurers often volunteer here to help the next generation get started.",
        "illium"),
    
    "Maxxis Shop": ("Maxxis' Shop", "6",
        "A quirky shop run by Maxxis, a retired adventurer with an eye for the unusual. The "
        "inventory is eclectic — magical curiosities, maps to dungeons that may or may not exist, "
        "potions with unpredictable effects, and 'guaranteed authentic' monster parts. Maxxis "
        "himself is rarely seen, but his assistant, a talking raccoon named Bandit, handles all "
        "transactions with surprising business acumen.",
        "illium"),
    
    "Equipment Machine": ("Equipment Machine", "7",
        "A strange room dominated by a large mechanical contraption of gears, levers, and "
        "magical conduits. Insert the proper tokens, and the machine dispenses basic adventuring "
        "equipment — rope, torches, rations, and simple tools. The machine was built by a "
        "gnomish inventor who claimed it would 'revolutionize equipment distribution.' It works "
        "most of the time, though occasionally it jams or dispenses something unexpected.",
        "illium"),
    
    "Tree of Life": ("Tree of Life", "8",
        "A small grove where a single ancient tree stands, its branches heavy with golden leaves "
        "that never fall. The air here feels revitalizing, and minor wounds seem to heal faster. "
        "Druids and nature priests gather here for meditation and ceremony. Offerings of flowers "
        "and honey have been placed at the base of the trunk. Some say the tree is a remnant "
        "of the world before the islands formed, a living connection to something ancient and pure.",
        "illium"),
    
    "Reinc Portal": ("Reincarnation Portal", "9",
        "A solemn chamber housing a portal of shifting silver light. This is where adventurers "
        "who wish to begin anew come to be reincarnated — keeping their knowledge and experience "
        "but starting fresh in a new form. Priests of the cycle guide petitioners through the "
        "process, ensuring they understand that rebirth means leaving behind their current life. "
        "The room smells of incense and ozone, and the portal's hum resonates in your bones.",
        "illium"),
}

# Exit connections: (from_room_key, exit_name, to_room_key, reverse_exit_name)
# This is the grid layout based on the ASCII map
EXITS = [
    # Cloud Road connections (right side of map)
    ("Adventurer Guild", "east", "Silent Room", "west"),
    ("Silent Room", "east", "Plaque Room", "west"),
    ("Plaque Room", "east", "Level Advance", "west"),
    ("Plaque Room", "south", "Portal Room", "north"),
    ("Level Advance", "south", "Myth Room", "north"),
    ("Portal Room", "east", "Myth Room", "west"),
    ("Level Advance", "east", "Newbie Guild", "west"),
    ("Myth Room", "east", "Maxxis Shop", "west"),
    ("Newbie Guild", "south", "Maxxis Shop", "north"),
    ("Newbie Guild", "east", "Equipment Machine", "west"),
    ("Equipment Machine", "south", "Tree of Life", "north"),
    ("Maxxis Shop", "east", "Tree of Life", "west"),
    ("Tree of Life", "south", "Reinc Portal", "north"),
    
    # Main grid - row by row connections
    # Top row: Weaponsmith -> Armorer -> Pawnshop area
    ("Weaponsmith", "east", "Armorer", "west"),
    ("Armorer", "east", "Pawnshop", "west"),
    
    # Pavilion of Gods -> Music Hall -> Mage Guild
    ("Pavilion of Gods", "east", "Music Hall", "west"),
    ("Music Hall", "east", "Mage Guild", "west"),
    
    # Cathedral connections
    ("Cathedral", "west", "Central Square", "east"),
    ("Cathedral", "north", "Music Hall", "south"),
    
    # Veldren Tower area
    ("Veldren Tower", "west", "Central Square", "east"),
    ("Veldren Tower", "north", "Music Hall", "south"),
    ("Veldren Tower", "south", "Bank", "north"),
    
    # Bank area
    ("Bank", "west", "General Store", "east"),
    ("Bank", "south", "Apothecary", "north"),
    
    # General Store -> Food Shop -> Ring Shop
    ("General Store", "south", "Food Shop", "north"),
    ("Food Shop", "east", "Ring Shop", "west"),
    
    # Central Square (hub)
    ("Central Square", "north", "Music Hall", "south"),
    ("Central Square", "south", "Race Museum", "north"),
    ("Central Square", "west", "Food Shop", "east"),
    ("Central Square", "east", "Wishing Pool", "west"),
    
    # Race Museum connections
    ("Race Museum", "west", "Toy Store", "east"),
    ("Race Museum", "east", "Auction House", "west"),
    ("Race Museum", "south", "Blacksmith", "north"),
    
    # Auction House -> Fighters Guild
    ("Auction House", "east", "Fighters Guild", "west"),
    
    # Blacksmith area
    ("Blacksmith", "west", "Greasy Spoon", "east"),
    ("Blacksmith", "south", "Equipment Trader", "north"),
    
    # Greasy Spoon -> Toy Store
    ("Greasy Spoon", "south", "Toy Store", "north"),
    
    # Equipment Trader -> Magic Shop -> Hall of Clans -> Circus -> Blu Moon
    ("Equipment Trader", "east", "Magic Shop", "west"),
    ("Magic Shop", "east", "Hall of Clans", "west"),
    ("Hall of Clans", "east", "Circus", "west"),
    ("Circus", "east", "Blu Moon", "west"),
    
    # Blu Moon -> Wishing Pool
    ("Blu Moon", "north", "Wishing Pool", "south"),
    ("Blu Moon", "east", "Adventurer Guild", "west"),
    
    # Wishing Pool -> Mage Guild
    ("Wishing Pool", "north", "Mage Guild", "south"),
    ("Wishing Pool", "east", "Adventurer Guild", "west"),
    
    # Fiery Flagon
    ("Fiery Flagon", "west", "Wishing Pool", "east"),
    ("Fiery Flagon", "north", "Cathedral", "south"),
    
    # Adventurer Guild connections to main city
    ("Adventurer Guild", "south", "Blu Moon", "north"),
    ("Adventurer Guild", "west", "Wishing Pool", "east"),
]


def build_illium_city():
    """Build all rooms and exits for Illium City."""
    created_rooms = {}
    
    # Create all rooms
    for key, (name, alias, desc, island) in ROOMS.items():
        # Check if room already exists
        existing = search_object(name, typeclass="typeclasses.rooms.Room")
        if existing:
            room = existing[0]
            print(f"  Using existing room: {name}")
        else:
            room = create_object(Room, key=name, location=None)
            print(f"  Created room: {name}")
        
        room.db.desc = desc
        room.db.island = island
        room.db.level_range = (1, 50)
        created_rooms[key] = room
    
    # Create all exits
    for from_key, exit_name, to_key, reverse_name in EXITS:
        from_room = created_rooms.get(from_key)
        to_room = created_rooms.get(to_key)
        
        if not from_room or not to_room:
            print(f"  SKIP: Missing room for exit {from_key} -> {to_key}")
            continue
        
        # Check if exit already exists
        existing_exits = [ex for ex in from_room.exits if ex.key == exit_name]
        if existing_exits:
            print(f"  Exit exists: {from_room.key} -> {exit_name}")
            continue
        
        # Create exit
        exit_obj = create_object(Exit, key=exit_name, location=from_room, destination=to_room)
        print(f"  Created exit: {from_room.key} --{exit_name}--> {to_room.key}")
    
    # Set Adventurer Guild as starting location
    adv_guild = created_rooms.get("Adventurer Guild")
    if adv_guild:
        # Try to set as default home
        from evennia import DefaultCharacter
        DefaultCharacter.db.home = adv_guild
        print(f"\n  Set Adventurer's Guild as default starting location.")
    
    print(f"\n=== Illium City built: {len(created_rooms)} rooms ===")
    return created_rooms


if __name__ == "__main__":
    build_illium_city()
