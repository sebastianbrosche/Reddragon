"""
Red Dragon MUD — Quest System
=============================
35 quests based on Islands of Myth content.
"""

from evennia import Command

QUESTS = {
    "avenge_death": {
        "name": "Avenge Player's Death",
        "type": "solo",
        "level": "any",
        "reward": 1,
        "start": "Anywhere — avenge a fallen player",
        "hint": "Avenge the death of a fellow player by slaying their killer.",
        "description": "When a player falls in combat, their killer must be brought to justice."
    },
    "avert_orc_invasion": {
        "name": "Avert Orc Invasion",
        "type": "solo",
        "level": "midbie",
        "reward": (0, 5),
        "start": "Orc Castle (Darkcaverns)",
        "hint": "Travel to the gloomy fort carved from a mountain. Find and help the elves inside carry out a vital task.",
        "description": "An orc invasion threatens the islands. Infiltrate their fortress and stop them."
    },
    "banish_jesrael": {
        "name": "Banish Jesrael",
        "type": "party",
        "level": "highbie",
        "reward": (0, 20),
        "start": "South Twin Islands",
        "hint": "Lord Jesrael has been gathering a large army of demons on South Twin Islands. Seek out and banish Jesrael before he can unleash his terror upon us.",
        "description": "The demon lord Jesrael prepares to invade. Only a strong party can stop him."
    },
    "blackavar_quest": {
        "name": "Blackavar Quest",
        "type": "solo",
        "level": ">20",
        "reward": (0, 2),
        "start": "Queen Vrille (Blackavar)",
        "hint": "Return Prince Forrester to his mother Queen Vrille.",
        "description": "Prince Forrester has gone missing. The Queen offers a reward for his safe return."
    },
    "defeat_zatea": {
        "name": "Defeat Zatea",
        "type": "party",
        "level": "highbie",
        "reward": (0, 10),
        "start": "The Pales (Darkcaverns)",
        "hint": "Help the old adventurer Adrian on Darkcavern isle to locate his son.",
        "description": "Adrian's son has been taken by the demon Zatea. A party must venture into The Pales to rescue him."
    },
    "destroy_schizomycetes": {
        "name": "Destroy Schizomycetes",
        "type": "party",
        "level": "highbie",
        "reward": (0, 20),
        "start": "Sslaath (Mists)",
        "hint": "Find Sslaath and help him destroy Schizomycetes. This is a highbie party oriented quest. Newbies stay away!!",
        "description": "A fungal demon threatens to consume the world. Sslaath the demonologist needs help."
    },
    "destroy_tiamat": {
        "name": "Destroy Tiamat",
        "type": "party",
        "level": "highbie",
        "reward": (0, 20),
        "start": "The library in Aquilonia",
        "hint": "Currently disabled.",
        "description": "The five-headed dragon Tiamat slumbers in her lair. [QUEST DISABLED]"
    },
    "discover_mermaid_city": {
        "name": "Discover Mermaid City",
        "type": "either",
        "level": "any",
        "reward": 1,
        "start": "Twin Islands waters",
        "hint": "Hidden deep within the waters of the Twin Islands is rumored to be a lost city of mermaids. Discover the mermaid city with your own eyes.",
        "description": "A castaway claims to have found a lost mermaid civilization beneath the waves."
    },
    "discover_nimrodel": {
        "name": "Discover Nimrodel",
        "type": "solo",
        "level": "newbie",
        "reward": (0, 2),
        "start": "Lothlorien (Hyboria)",
        "hint": "Nimrodel has gone missing. Help her son find her.",
        "description": "Nimrodel of Lothlorien has vanished. Her son seeks someone to help find her."
    },
    "discover_dreamers": {
        "name": "Discover the Dreamers",
        "type": "solo",
        "level": "midbie",
        "reward": 1,
        "start": "Draconne Village",
        "hint": "Hidden deep within the draconne village is a circle of dream worshippers. Find the hidden entrance and seek your inner peace.",
        "description": "A secret cult of dreamers hides within the draconne village. Find them."
    },
    "elven_secret": {
        "name": "Elven Secret",
        "type": "solo",
        "level": "midbie",
        "reward": (0, 1),
        "start": "Among the elves (Blackavar)",
        "hint": "The elves of Blackavar have a secret. Find it.",
        "description": "The Blackavar elves guard an ancient secret. Discover what they hide."
    },
    "feline_puzzle": {
        "name": "Feline Puzzle",
        "type": "solo",
        "level": "newbie",
        "reward": (0, 1),
        "start": "Catworld",
        "hint": "A puzzle in the feline kingdom is rumored to open up for a hermit.",
        "description": "The cats of Catworld guard a puzzle that only the worthy can solve."
    },
    "goodwin_treasure": {
        "name": "Goodwin's Treasure",
        "type": "party",
        "level": "newbie",
        "reward": (0, 2),
        "start": "Goodwin's Castle (Blackavar)",
        "hint": "Break the curse in Castle Goodwin and find its treasure!",
        "description": "Castle Goodwin is cursed. A party must break the curse and claim the treasure within."
    },
    "hefnoin_duties": {
        "name": "Hefnoin Civic Duties",
        "type": "solo_reward_party_req",
        "level": "midbie",
        "reward": 10,
        "start": "Hefnoin",
        "hint": "Talk to the wiseman in Hefnoin; he has a task for you.",
        "description": "The wiseman of Hefnoin needs help with civic duties. Party recommended for combat portions."
    },
    "help_breeder_bob": {
        "name": "Help Breeder Bob",
        "type": "solo",
        "level": "newbie",
        "reward": (0, 1),
        "start": "Breeder Bob's Caves (Everrest)",
        "hint": "Find and help Breeder Bob. He seeks to add to his collection of exotic creatures.",
        "description": "Breeder Bob on Everrest needs help collecting exotic creatures for his menagerie."
    },
    "help_farmer_joe": {
        "name": "Help Farmer Joe",
        "type": "solo",
        "level": "newbie",
        "reward": (0, 2),
        "start": "Farmer Joe (Newbie Garden)",
        "hint": "Help Farmer Joe find his most prized possession.",
        "description": "Farmer Joe in the Newbie Garden has lost something precious. Help him find it."
    },
    "help_helga": {
        "name": "Help Helga",
        "type": "solo",
        "level": "newbie",
        "reward": (0, 2),
        "start": "Newbie Valley",
        "hint": "Helga, the kind old witch, is working on a new magical potion. She needs your help in finding the remaining ingredients.",
        "description": "Helga the witch needs rare ingredients for her potion. Gather them from the valley."
    },
    "help_janriella": {
        "name": "Help Janriella",
        "type": "solo",
        "level": "low/mid",
        "reward": 2,
        "start": "Wandering Ghost, Blackavar Forest",
        "hint": "Look to the spirit of Janriella for clues.",
        "description": "The ghost of Janriella wanders the forest seeking closure. Help her find peace."
    },
    "help_miss_cromwell": {
        "name": "Help Miss Cromwell",
        "type": "solo",
        "level": 1,
        "reward": 1,
        "start": "Valmoria",
        "hint": "Young Miss Cromwell seems to have lost her engagement ring, again. Please come to Valmoria and help her find it.",
        "description": "Miss Cromwell has lost her ring. Again. Find it in Valmoria."
    },
    "light_lighthouse": {
        "name": "Light the Lighthouse Lamp",
        "type": "solo",
        "level": "any",
        "reward": 2,
        "start": "North Twin Island Lighthouse",
        "hint": "The lighthouse is very run down. You need to light the lamp before a passing ship runs into the rocks and sinks.",
        "description": "The North Twin Island lighthouse has gone dark. Light it before disaster strikes."
    },
    "mischief_machinations": {
        "name": "Mischief, Machinations, and Morals",
        "type": "solo",
        "level": 20,
        "reward": 1,
        "start": "Strangest cave in the lands",
        "hint": "A senile cleric needs your help with a ritual. Collect his ritualistic implements and stand ready to receive a reward below your wildest expectations.",
        "description": "A senile cleric in a strange cave performs odd rituals. Help him... if you dare."
    },
    "naval_warfare": {
        "name": "Naval Warfare",
        "type": "solo",
        "level": 10,
        "reward": (0, 2),
        "start": "Heavenly Smiles Hotel",
        "hint": "A captain from lands forgotten has arrived to challenge players to the classic game of Battleship! He prefers to play in relative quietness.",
        "description": "A mysterious captain at the Heavenly Smiles Hotel challenges adventurers to a game of Battleship."
    },
    "newbie_explore": {
        "name": "Newbie Explore",
        "type": "solo",
        "level": "newbie",
        "reward": 2,
        "start": "Newbie Guild",
        "hint": "Receive your Exploration Card from the free equipment machine. Look at the card to get started.",
        "description": "The Newbie Guild issues Exploration Cards. Visit all listed locations to complete the quest."
    },
    "nuvo_school": {
        "name": "Nuvo City Newbie School",
        "type": "solo",
        "level": "newbie",
        "reward": 1,
        "start": "Nuvo City",
        "hint": "Find Nuvo City near the newbie guild and talk to the teacher. Earn your reward by proving your knowledge.",
        "description": "Nuvo City's school for new adventurers tests your knowledge of the world."
    },
    "obsessive_collector": {
        "name": "Obsessive Collector",
        "type": "solo",
        "level": "newbie",
        "reward": (0, 1),
        "start": "Toy Shop, Illium",
        "hint": "'SnotMarbles' is a game originally played by bored imps. Visit the toy shop to begin your collection. Collect a full set!",
        "description": "The SnotMarbles craze has hit Illium. Collect all the marbles from the toy shop."
    },
    "peace_in_dig": {
        "name": "Peace in the Dig",
        "type": "party",
        "level": "highbie",
        "reward": (0, 5),
        "start": "Ancient Burial Ground (Oddworld)",
        "hint": "Down in the dig a horrible war is taking place. Find the keys to end it. Beware, this is a dangerous task.",
        "description": "An ancient war rages beneath Oddworld. A party must find the keys to end the conflict."
    },
    "proof_royal_lineage": {
        "name": "Proof of Royal Lineage",
        "type": "solo",
        "level": "midbie",
        "reward": (0, 1),
        "start": "Unknown",
        "hint": "Find a less than honest individual hidden in the sewers of a once great city and make use of his services.",
        "description": "A forger in the sewers can create proof of royal lineage... for a price."
    },
    "fall_of_rdc": {
        "name": "Read about the Fall of RDC",
        "type": "solo",
        "level": "any",
        "reward": (0, 1),
        "start": "Illium",
        "hint": "Find the fountain in the city of Illium and read about the 'Fall of RDC'.",
        "description": "The fountain in Illium bears an inscription about the Fall of the Red Dragon Clan."
    },
    "rescue_clara": {
        "name": "Rescue Clara",
        "type": "solo",
        "level": ">30",
        "reward": (0, 2),
        "start": "Forlorn Merchant (Southern Wastes)",
        "hint": "Rescue Clara from the necropolis.",
        "description": "A merchant's daughter Clara has been taken to the necropolis. Rescue her."
    },
    "shikon_shards": {
        "name": "Retrieve the Shikon Shards",
        "type": "party",
        "level": "highbie",
        "reward": (0, 15),
        "start": "Dangerous Castle (Everrest)",
        "hint": "The Shikon no Tama was destroyed and pieces spread all over the world. Help Kagome the miko collect the pieces.",
        "description": "A powerful jewel shattered. Its shards are scattered across the world. A party must help gather them."
    },
    "return_clayborn": {
        "name": "Return Clayborn Necklace",
        "type": "solo_reward_party_req",
        "level": "highbie",
        "reward": (0, 20),
        "start": "The Old Man (Emerald)",
        "hint": "Someone has lost something very important in the land of the hag. Find this person and return the missing item.",
        "description": "An old man on Emerald lost a precious necklace to the hag. A party can help retrieve it."
    },
    "satisfy_chilperic": {
        "name": "Satisfy Chilperic",
        "type": "party",
        "level": "highbie",
        "reward": (2, 20),
        "start": "Chilperic's Menagerie (Everrest)",
        "hint": "Chilperic the Biomancer needs something and doesn't know it. Find him, alert him to his problem, and solve it.",
        "description": "Chilperic the Biomancer on Everrest has a problem he doesn't realize. A party must help him."
    },
    "save_safari": {
        "name": "Save the Safari Camp",
        "type": "solo",
        "level": "midbie (max 50)",
        "reward": (0, 3),
        "start": "Safari Camp (South Twin Islands)",
        "hint": "The safari camp is running critically low on water and they are too scared of the lions to leave. Talk to the camp leader.",
        "description": "A safari camp on South Twin Islands is dying of thirst. Help them find water without becoming lion food."
    },
    "save_uforia": {
        "name": "Save Uforia",
        "type": "party",
        "level": "highbie",
        "reward": (0, 10),
        "start": "Uforia (Mists)",
        "hint": "An evil plague has ruined the world of Uforia. Find this evil and destroy it.",
        "description": "The plague-ravaged world of Uforia bleeds into reality. A party must find and destroy the source."
    },
    "shaman_staff": {
        "name": "Shaman's Staff",
        "type": "party",
        "level": "mid/high",
        "reward": (0, 1),
        "start": "Prehistoric Cave People (Hyboria)",
        "hint": "The Shaman of the cave people possesses a Staff of awesome power. Obtain the staff and unravel its secrets.",
        "description": "A powerful staff is guarded by Hyboria's cave shaman. A party must retrieve it."
    },
    "green_monkey": {
        "name": "The Great Green Monkey Heist & Other Adventures",
        "type": "solo",
        "level": "all",
        "reward": 5,
        "start": "Anker Village (Oddworld)",
        "hint": "Anker village entertains visitors once more... but a greater threat lies beneath. Meet Pirates! Whores! The undead! Monkeys!",
        "description": "Anker village seems peaceful, but dark secrets fester beneath. Pirates, the undead, and monkeys await."
    },
    "slay_god": {
        "name": "To Slay a God",
        "type": "party",
        "level": 75,
        "reward": (0, 20),
        "start": "Tarantia",
        "hint": "A route has been discovered to Mordulak's former home. Gather a party, unseal this route, and slay the demigod before he rises again!",
        "description": "The demigod Mordulak stirs in his sealed prison. Only a level 75+ party can stop his return."
    },
    "unlock_gnoll_secrets": {
        "name": "Unlock the Secrets of the Gnolls",
        "type": "solo",
        "level": ">70",
        "reward": 4,
        "start": "Dark Caverns",
        "hint": "The magic that creates this race is held secret by the Gnolls themselves. Visit them on Dark Caverns and they might reveal some secrets. Can only be unlocked once per boot.",
        "description": "The Gnoll creation magic is a closely guarded secret. Only those over level 70 can attempt to learn it."
    },
}


def get_quest_detail(quest_key):
    """Return formatted quest information."""
    quest = QUESTS.get(quest_key)
    if not quest:
        return "Unknown quest."

    lines = []
    lines.append(f"{{c{'='*50}{{n")
    lines.append(f"{{G{quest['name']}{{n")
    lines.append(f"{{c{'='*50}{{n")
    lines.append(f"  {{yType:{{n {quest['type']}")
    lines.append(f"  {{yLevel:{{n {quest['level']}")
    reward = quest['reward']
    if isinstance(reward, tuple):
        lines.append(f"  {{yReward:{{n {reward[0]}-{reward[1]} quest points")
    else:
        lines.append(f"  {{yReward:{{n {reward} quest points")
    lines.append(f"  {{yStart:{{n {quest['start']}")
    lines.append("")
    lines.append(f"{{yDescription:{{n")
    lines.append(f"  {quest['description']}")
    lines.append("")
    lines.append(f"{{yHint:{{n")
    lines.append(f"  {quest['hint']}")
    lines.append(f"{{c{'='*50}{{n")
    return "\n".join(lines)


def get_quest_list():
    """Return formatted list of all quests."""
    lines = []
    lines.append("{cAvailable Quests (35){n")
    lines.append("-" * 50)
    for key, data in QUESTS.items():
        qtype = data['type']
        level = str(data['level'])
        reward = data['reward']
        if isinstance(reward, tuple):
            reward_str = f"{reward[0]}-{reward[1]} QP"
        else:
            reward_str = f"{reward} QP"
        lines.append(f"  {{g{data['name']:<35}{{n {qtype:<8} Lv{level:<10} {reward_str}")
    lines.append("-" * 50)
    lines.append("Use {gquest {name}{n to view details.")
    return "\n".join(lines)


class CmdQuest(Command):
    """
    View quest information.

    Usage:
      quest             — list all quests
      quest <name>      — view quest details
    """
    key = "quest"
    locks = "cmd:all()"

    def func(self):
        args = self.args.strip().lower().replace(" ", "_")
        caller = self.caller

        if not args:
            caller.msg(get_quest_list())
            return

        # Try exact match
        if args in QUESTS:
            caller.msg(get_quest_detail(args))
            return

        # Try fuzzy
        matches = [k for k in QUESTS if args in k or args in QUESTS[k]["name"].lower().replace(" ", "_")]
        if matches:
            caller.msg(get_quest_detail(matches[0]))
        else:
            caller.msg("Quest not found. Use 'quest' to see available quests.")
