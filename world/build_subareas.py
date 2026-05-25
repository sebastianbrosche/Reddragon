"""
Red Dragon MUD - Sub-Area Builder
Builds all 195 sub-areas from islandsofmyth.org maps
"""

import os
import re
from bs4 import BeautifulSoup
import evennia
from evennia import create_object, search_object
from evennia.utils import logger
from typeclasses.rooms import Room
from typeclasses.exits import Exit

# Island data with sub-areas from the HTML maps
ISLANDS = {
    "gossamer": {
        "name": "Gossamer",
        "ferry_room": "Cloud Road between Gossamer and Titan",  # Connection to world
        "sub_areas": [
            ("Illium City", "The heart of Gossamer Island, a bustling metropolis"),
            ("Newbie Ocean", "Gentle waters for new adventurers to learn"),
            ("North Forest", "A dense woodland filled with wildlife"),
            ("Kobold Village", "A small settlement of kobold traders"),
            ("Goblin Mounds", "Hilly terrain riddled with goblin tunnels"),
            ("Kreativ's Pool & Memorial Park", "A serene park with a memorial fountain"),
            ("Cat World", "A whimsical realm of oversized felines"),
            ("Small Glade", "A peaceful clearing in the woods"),
            ("Red Dragon City Ruins", "Ancient ruins of a once-great city"),
            ("Undercity", "The dark tunnels beneath Illium"),
            ("Peaceful Wood", "A tranquil forest path"),
            ("Player Castles", "Grand castles built by adventurers"),
            ("Tidy Farm", "A well-kept farm with crops and livestock"),
            ("Private Beach", "A secluded sandy shore"),
            ("Small Village", "A quiet hamlet of friendly folk"),
            ("Yensidland", "A magical land of wonder"),
            ("Newbie Garden", "A safe area for learning basics"),
            ("Prima Market", "A bustling marketplace for trade"),
            ("Beanstalk", "A giant beanstalk reaching to the clouds"),
            ("Troll Cave", "A dark cave inhabited by trolls"),
            ("Small Clearing", "An open area in the forest"),
            ("Spidranox Swamp", "A murky swamp with giant spiders"),
            ("Swamp Mansion", "An old mansion deep in the swamp"),
            ("Forest Trail", "A worn path through the woods"),
            ("Crystal Dragon Cave", "A sparkling cave of crystal formations"),
            ("Evoker Tower", "A tower for practitioners of evocation"),
            ("Aviary", "A sanctuary for exotic birds"),
            ("Forest Grove", "A sacred grove of ancient trees"),
            ("Zun Zoo", "A zoo housing exotic creatures"),
            ("Thieves Network", "A hidden network for rogues"),
            ("Larssi's Island", "A private island retreat"),
            ("Chuck's Bait Shop", "A shop selling fishing supplies"),
        ]
    },
    "blackavar": {
        "name": "Blackavar",
        "ferry_room": None,  # Will connect to gossamer ferry
        "sub_areas": [
            ("Abandoned Tower", "A crumbling tower of forgotten magic"),
            ("Ankh-Morpork City", "A city inspired by a famous disc"),
            ("Blackavar City", "The main city of Blackavar Island"),
            ("City of Bakhgrul", "An ancient city of dark stone"),
            ("Curly Grubb Inn", "A cozy inn with good ale"),
            ("Desert Storm", "A harsh desert with sandstorms"),
            ("Dracula's Castle", "A gothic castle of vampire legend"),
            ("Draejar's Tower", "A tower belonging to an archmage"),
            ("Dryad Forest", "A forest inhabited by tree spirits"),
            ("Forlorn Forest", "A gloomy wood of whispers"),
            ("Goodwin Castle", "A fortress of noble knights"),
            ("Highland Keep", "A sturdy keep in the highlands"),
            ("Insect Mound", "A hill swarming with giant insects"),
            ("Lynne Mine", "An abandoned mine with secrets"),
            ("Merlin's Keep", "The tower of a legendary wizard"),
            ("Mindflayer City", "A city of psionic creatures"),
            ("Mountain Dungeon", "A deep dungeon in the mountains"),
            ("Mountain Path", "A treacherous mountain trail"),
            ("Mt Nevermind", "A volcano of unpredictable temper"),
            ("Mt Olympus", "The legendary home of gods"),
            ("Newbie Valley", "A safe valley for beginners"),
            ("Old Church", "A ruined place of worship"),
            ("Ruo Gen City", "An oriental city of mystery"),
            ("Southern Wastes", "A barren wasteland of ash"),
            ("Spirit Temple", "A temple for communing with spirits"),
            ("Stony Brook Forest", "A forest with a bubbling brook"),
            ("Tavern", "A lively drinking establishment"),
            ("Tower of Arabidopsis", "A botanical tower of plants"),
            ("Tower Ruins", "The remains of a fallen tower"),
            ("Tunnel", "A dark passage underground"),
            ("Underworld", "The realm of the dead"),
            ("Valley of Giants", "A valley where giants roam"),
            ("Valley of Magic", "A valley crackling with arcane energy"),
        ]
    },
    "emerald": {
        "name": "Emerald",
        "ferry_room": None,
        "sub_areas": [
            ("Bugbear Forest", "A forest stalked by bugbears"),
            ("Celtica", "A land of ancient Celtic magic"),
            ("Coramonde", "A realm of knights and quests"),
            ("Crystal Caverns", "Shimmering caves of crystal"),
            ("Emerald Island Ocean Pier", "A pier extending into the ocean"),
            ("Emerald Mines", "Mines rich with gems"),
            ("Forest of a Thousand Dreams", "A mystical forest of visions"),
            ("Hag's Forest", "A wood haunted by hags"),
            ("Ice Mountain", "A frozen peak of ice"),
            ("Kobold Village", "A village of scaly kobolds"),
            ("Minotaur Temple", "A temple to the minotaur gods"),
            ("Mossflower Forest", "A forest covered in thick moss"),
            ("Mountain of Flowers and Fruits", "A fertile mountain paradise"),
            ("Newbie Forest", "A safe forest for training"),
            ("Ogre Villages", "Crude villages of ogre tribes"),
            ("Passage", "A narrow pass between cliffs"),
            ("Princess Bride", "A romantic castle setting"),
            ("Small Farm", "A modest farming homestead"),
            ("Small Grove", "A quiet grove of trees"),
            ("Small Manor", "An elegant country manor"),
            ("Spamalot", "A silly realm of knights"),
            ("Swamp Castle", "A castle surrounded by swamp"),
        ]
    },
    "everrest": {
        "name": "Everrest",
        "ferry_room": None,
        "sub_areas": [
            ("Arctic Tundra", "A frozen wasteland of ice"),
            ("Chilperic's Menagerie", "A collection of exotic beasts"),
            ("Dante's Inferno", "A hellish realm of fire"),
            ("Demonologist's Castle", "A castle of dark summoners"),
            ("Desert Wasteland", "A scorched desert of heat"),
            ("Elven Camp", "A camp of woodland elves"),
            ("Enchanted Forest", "A forest of magical creatures"),
            ("Evermore", "A land of eternal twilight"),
            ("Naraku", "A cursed valley of demons"),
            ("Quin-Jas Swamp", "A swamp of toxic gases"),
            ("Sacred Grove", "A holy grove of nature"),
            ("Snafu", "A chaotic realm of confusion"),
            ("Spider Cave", "A cave of webs and spiders"),
            ("Trading Post", "A hub for merchants"),
        ]
    },
    "hyboria": {
        "name": "Hyboria",
        "ferry_room": None,
        "sub_areas": [
            ("Aquilonia", "A kingdom of noble warriors"),
            ("Arenjun Mines", "Dangerous mines of Arenjun"),
            ("Convent", "A secluded place of worship"),
            ("Fire World", "A realm of eternal flame"),
            ("Ice World", "A frozen dimension"),
            ("Kozaki Desert", "A desert of nomadic tribes"),
            ("Lizardman Temple", "A temple of reptilian gods"),
            ("Lorien Forest", "An elven forest of beauty"),
            ("Mordulak's Realm", "The domain of a dark lord"),
            ("Mountain Temple", "A temple high in the peaks"),
            ("Mountain Trolls", "Peaks infested with trolls"),
            ("Prehistoric Hunters", "A land of ancient beasts"),
            ("Strawberry Fields", "Fields of sweet berries"),
            ("Triangle", "A mysterious geometric zone"),
            ("Valley Fortress", "A fortress in a valley"),
            ("Veldt Lost Vale", "A lost valley of grasslands"),
        ]
    },
    "mists": {
        "name": "Mists",
        "ferry_room": None,
        "sub_areas": [
            ("Army of Darkness", "A realm of undead armies"),
            ("Blight", "A diseased and dying land"),
            ("Daycare Center", "A safe place for young adventurers"),
            ("Dwarf Village", "A settlement of stout dwarves"),
            ("Elf Forest", "An elegant forest of elves"),
            ("Hall of Guildmasters", "A hall honoring guild leaders"),
            ("Lizardman Swamp", "A swamp of lizard folk"),
            ("Mist Valley", "A valley shrouded in fog"),
            ("Mists Harbor", "A port city of foggy docks"),
            ("Murkwood Forest", "A dark and gloomy wood"),
            ("Old Castle", "A decaying fortress"),
            ("Paladin Camp", "A camp of holy warriors"),
            ("Pirate Ship", "A vessel of seafaring pirates"),
            ("Plants", "A realm of sentient flora"),
            ("Shadow Castle", "A castle of darkness"),
            ("Stage", "A theatrical arena"),
            ("Uforia", "A realm of happiness"),
        ]
    },
    "oddworld": {
        "name": "Oddworld",
        "ferry_room": None,
        "sub_areas": [
            ("Asylum", "A place of madness"),
            ("Beaver Pond", "A peaceful pond habitat"),
            ("Chessboard", "A giant chessboard realm"),
            ("Demon Motel", "A motel for dark travelers"),
            ("Dig Site", "An archaeological excavation"),
            ("Hoppy Tunnels", "Tunnels filled with jumping creatures"),
            ("Obelisk", "A mysterious standing stone"),
            ("Oddworld Harbor", "A strange port town"),
            ("Pouch", "A small pocket dimension"),
            ("Stargate Pyramids", "Pyramids with star portals"),
            ("Wonderland", "A realm of nonsense and wonder"),
        ]
    },
    "sombre": {
        "name": "Sombre",
        "ferry_room": None,
        "sub_areas": [
            ("Anker Village", "A village of fishermen"),
            ("Dragon Races", "An arena for dragon racing"),
            ("Frozen Forest", "A forest encased in ice"),
            ("Geologist's Cave", "A cave of rare minerals"),
            ("Grakhna City", "A city of dark magic"),
            ("Icarus Kingdom", "A kingdom in the sky"),
            ("Mugak Swamp", "A swamp of mud and muck"),
            ("Sand Worm Temple", "A temple to giant worms"),
            ("Skjarl's Valley", "A valley of ancient warriors"),
            ("Sombre City", "The main city of Sombre Island"),
            ("Strange Valley", "A valley of odd phenomena"),
            ("Stronglight Castle", "A castle of brilliant light"),
            ("Termite Forest", "A forest of giant insects"),
            ("Valmoria City", "A city of scholars and mages"),
        ]
    },
    "southcape": {
        "name": "Southcape",
        "ferry_room": None,
        "sub_areas": [
            ("Ancient Tree", "A tree as old as time"),
            ("Bee Hive", "A giant hive of bees"),
            ("Catacombs", "Underground burial chambers"),
            ("Docks & Heavenly Smiles Hotel", "A port with a cheerful inn"),
            ("Heracleion", "A sunken city of legend"),
            ("Icy Peaks", "Frozen mountain peaks"),
            ("Mountain Passage Mines", "Mines in a mountain passage"),
            ("Mountain Tunnel", "A tunnel through stone"),
            ("Pygmy Tribe", "A village of small warriors"),
            ("Shifting Sands", "Desert sands that move"),
            ("Swamp Village", "A village in the wetlands"),
        ]
    },
    "twin_islands": {
        "name": "Twin Islands",
        "ferry_room": None,
        "sub_areas": [
            ("Animal Nursery", "A place for raising creatures"),
            ("Beach Hut", "A shack on the shore"),
            ("City of Hefnoin", "A city of twin islands"),
            ("Correctional Facility", "A place for lawbreakers"),
            ("Demon Cave", "A cave of demons"),
            ("Desert", "A barren desert"),
            ("Lighthouse", "A beacon on the coast"),
            ("North Dock", "A northern port"),
            ("Safari Camp", "A camp for hunters"),
            ("Slime Cave", "A cave of oozes"),
            ("Tunnels", "Underground passages"),
            ("Volcano", "A mountain of fire"),
            ("Xillion's Tower", "A tower of a mad wizard"),
        ]
    },
    "darkcaverns": {
        "name": "Darkcaverns",
        "ferry_room": None,
        "sub_areas": [
            ("Draconne Village", "A village of dragon kin"),
            ("Dragon Caves", "Caves of sleeping dragons"),
            ("Dragon Lord", "The lair of a dragon lord"),
            ("El Tajin Pyramid", "An ancient pyramid"),
            ("Kobold Cave", "A cave of kobold miners"),
            ("Main Path", "The main route through"),
            ("Netherworld", "A realm of shadows"),
            ("Orc Fort", "A fortress of orcs"),
            ("Pales", "Pale lands of undead"),
            ("Rifts", "Dimensional tears"),
            ("Swamp", "A dark swamp"),
        ]
    }
}


def build_island_sub_areas(island_key):
    """Build all sub-areas for an island."""
    island = ISLANDS[island_key]
    island_name = island["name"]
    sub_areas = island["sub_areas"]
    
    # Find or create the island hub room
    hub_name = f"{island_name} Island"
    hub = search_object(hub_name, typeclass=Room)
    if not hub:
        hub = create_object(Room, key=hub_name, 
                           attributes={"desc": f"You stand on the shores of {island_name}, a vast island with many wonders."})
        logger.log_info(f"Created island hub: {hub_name}")
    else:
        hub = hub[0]
    
    # Create each sub-area
    created = []
    for area_name, area_desc in sub_areas:
        # Check if it already exists
        existing = search_object(area_name, typeclass=Room)
        if existing:
            logger.log_info(f"Sub-area already exists: {area_name}")
            room = existing[0]
        else:
            # Create the room
            room = create_object(Room, key=area_name,
                               attributes={"desc": area_desc})
            logger.log_info(f"Created sub-area: {area_name}")
            created.append(area_name)
        
        # Connect to hub (bidirectional)
        # Check if exit already exists
        exit_name = f"to_{area_name.lower().replace(' ', '_').replace(\"'\", '').replace('&', 'and')}"
        
        # Create exit from hub to room if not exists
        existing_exits = [ex for ex in hub.exits if ex.key == area_name]
        if not existing_exits:
            hub_exit = create_object(Exit, key=area_name, 
                                   location=hub, destination=room,
                                   aliases=[area_name.lower()])
            logger.log_info(f"Created exit: {hub.key} -> {room.key}")
        
        # Create return exit
        existing_returns = [ex for ex in room.exits if ex.key == island_name or ex.key == hub_name]
        if not existing_returns:
            room_exit = create_object(Exit, key=island_name,
                                    location=room, destination=hub,
                                    aliases=[island_name.lower(), "island", "hub"])
            logger.log_info(f"Created return exit: {room.key} -> {hub.key}")
    
    return created, hub


def connect_islands():
    """Connect island hubs via ferry rooms."""
    # Find Gossamer hub (main hub)
    gossamer_hub = search_object("Gossamer Island", typeclass=Room)
    if not gossamer_hub:
        logger.log_err("Gossamer Island hub not found!")
        return
    gossamer_hub = gossamer_hub[0]
    
    # Connect all other islands to Gossamer via ferry exits
    for island_key, island_data in ISLANDS.items():
        if island_key == "gossamer":
            continue
        
        island_name = island_data["name"]
        hub = search_object(f"{island_name} Island", typeclass=Room)
        if not hub:
            logger.log_warn(f"Hub not found for {island_name}")
            continue
        hub = hub[0]
        
        # Create ferry exit from Gossamer
        ferry_name = f"Ferry to {island_name}"
        existing = [ex for ex in gossamer_hub.exits if ex.key == ferry_name or ex.key == island_name]
        if not existing:
            ferry = create_object(Exit, key=ferry_name,
                               location=gossamer_hub, destination=hub,
                               aliases=[island_name.lower(), island_key])
            logger.log_info(f"Created ferry: Gossamer -> {island_name}")
        
        # Create return ferry
        return_ferry_name = "Ferry to Gossamer"
        existing_return = [ex for ex in hub.exits if ex.key == return_ferry_name or ex.key == "Gossamer"]
        if not existing_return:
            return_ferry = create_object(Exit, key=return_ferry_name,
                                        location=hub, destination=gossamer_hub,
                                        aliases=["gossamer", "return"])
            logger.log_info(f"Created return ferry: {island_name} -> Gossamer")


def build_all():
    """Build all sub-areas and connections."""
    logger.log_info("=== BUILDING ALL SUB-AREAS ===")
    
    total_created = 0
    for island_key, island_data in ISLANDS.items():
        logger.log_info(f"\nBuilding {island_data['name']}...")
        created, hub = build_island_sub_areas(island_key)
        total_created += len(created)
        logger.log_info(f"Created {len(created)} new rooms for {island_data['name']}")
    
    # Connect islands
    logger.log_info("\nConnecting islands...")
    connect_islands()
    
    logger.log_info(f"\n=== COMPLETE: {total_created} new sub-areas created ===")


if __name__ == "__main__":
    build_all()
