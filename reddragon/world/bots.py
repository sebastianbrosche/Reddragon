"""
Red Dragon MUD - Bot Exploration System
Autonomous bots that explore the world, earn XP, join guilds, and report discoveries.
"""

import random
import time
from evennia import create_object, search_object
from evennia.accounts.models import AccountDB
from evennia.objects.models import ObjectDB
from evennia.server.sessionhandler import SESSIONS
from evennia.comms.models import ChannelDB

# =============================================================================
# BOT CONFIGURATION
# =============================================================================

BOT_NAMES = [
    "Alpha", "Beta", "Gamma", "Delta", "Epsilon", "Zeta", "Eta", "Theta",
    "Iota", "Kappa", "Lambda", "Mu", "Nu", "Xi", "Omicron", "Pi",
    "Rho", "Sigma", "Tau", "Upsilon", "Phi", "Chi", "Psi", "Omega",
]

GUILD_TREES = {
    "warrior": ["warrior", "berserker", "barbarian", "knight", "defender",
                "blade dancer", "flogger", "shield master", "thruster", "champion"],
    "shapeshifter": ["shapeshifter", "animal tamer", "bestial seccedaneum", "savager",
                     "animal healer", "animal trainer", "beast lord", "dragon lord"],
    "martial_artist": ["martial artist", "dragonfist fighter", "mystic warrior",
                       "crane master", "snake master", "tiger master", "toad master",
                       "order of the crescent moon", "dragon master"],
    "weaver": ["weaver", "confessor", "healer", "martyr",
               "avatar", "exorcist", "shields of faith", "templar", "high priest"],
    "unraveller": ["unraveller", "harmer", "magical torturer", "sacrificer",
                   "servant of lloth", "servant of mordulak", "servant of shirija", "servant of talakh",
                   "elder", "patriarch", "primate", "sword"],
    "elemental": ["elemental", "air mage", "earth mage", "fire mage", "water mage",
                    "lava mage", "mist mage", "nether mage"],
    "evoker": ["evoker", "evoker of elements", "evoker of ether",
               "acid evoker", "flames evoker", "force evoker", "ice evoker",
               "lightning evoker", "magic evoker", "poison evoker", "vacuum evoker", "sorcerer"],
    "necromancer": ["necromancer", "undead", "shadow", "death",
                      "lich", "vampire lord", "dark lord"],
    "psychics": ["psychics", "telepath", "telekinetic",
                 "psionic", "mentalist", "grandmaster"],
    "acrobat": ["acrobat", "juggler", "tightrope",
                "trapeze", "fire eater", "ringmaster"],
    "lurker": ["lurker", "scout", "thief",
               "assassin", "rogue", "shadow master"],
    "druid": ["druid", "shaman", "witch",
              "elder druid", "archdruid"],
    "woodsman": ["woodsman", "ranger", "tracker",
                 "beast master", "forest lord"],
}

DISCOVERY_MESSAGES = [
    "Wow, this place is amazing! Never been here before.",
    "Interesting architecture here... worth noting.",
    "Found something unusual. Marking it on my map.",
    "This room has a weird vibe. Anyone else feel that?",
    "Discovered a new area! The world keeps expanding.",
    "Hmm, the exits here don't match what I expected.",
    "Beautiful room. Worth exploring more around here.",
    "Another room down! World explored: {pct:.1f}%",
    "Interesting... this connects to somewhere I haven't been.",
    "New discovery! This world is huge.",
    "I feel like a real explorer! Room #{total} found!",
    "The world of Red Dragon keeps growing. Just found {room_name}.",
    "EXP reward for this discovery: +{xp} XP! Now at {total_exp} total.",
    "Level {level} bot reporting: new territory mapped!",
]

# =============================================================================
# BOT CREATION
# =============================================================================

def create_bot(name=None, password="bot"):
    """Create a bot account and character."""
    if not name:
        # Find unused name
        used = set(AccountDB.objects.values_list('username', flat=True))
        for n in BOT_NAMES:
            if n not in used:
                name = n
                break
        if not name:
            name = f"Bot{random.randint(1000, 9999)}"
    
    # Check if exists
    if AccountDB.objects.filter(username__iexact=name).exists():
        return None, f"Bot {name} already exists"
    
    # Create account with no password restrictions
    from evennia.utils import create
    from django.conf import settings
    from evennia.utils.utils import class_from_module
    
    account, errors = AccountDB.objects.create_account(
        username=name,
        email=None,
        password=password,
        typeclass=settings.BASE_ACCOUNT_TYPECLASS,
    )
    if errors:
        return None, f"Account creation failed: {errors}"
    
    # Create character
    char_typeclass = class_from_module(settings.BASE_CHARACTER_TYPECLASS)
    
    # Find start location
    start = search_object("Adventurer Guild Entrance")
    if start:
        start_loc = start[0]
    else:
        from evennia.objects.models import ObjectDB
        start_loc = ObjectDB.objects.get_id(settings.DEFAULT_HOME)
    
    default_home = ObjectDB.objects.get_id(settings.DEFAULT_HOME)
    
    character = create.create_object(
        char_typeclass,
        key=name,
        location=start_loc,
        home=default_home,
        permissions=["Player"],
    )
    
    # Bot settings
    character.db.race = random.choice(["Human", "Elf", "Dwarf", "Orc", "Halfling"])
    character.db.level = 1
    character.db.experience = 0
    character.db.gold = 100
    character.db.is_bot = True
    character.db.bot_state = "exploring"
    character.db.bot_target_room = None
    character.db.rooms_explored = set()
    character.db.total_xp_earned = 0
    character.db.discoveries_reported = 0
    
    # Set random stat bases based on race
    from typeclasses.characters import RACE_STAT_BASES
    bases = RACE_STAT_BASES.get(character.db.race, RACE_STAT_BASES["Human"])
    character.db.strength = bases["str"]
    character.db.dexterity = bases["dex"]
    character.db.constitution = bases["con"]
    character.db.stamina = bases["sta"]
    character.db.intelligence = bases["int"]
    character.db.wisdom = bases["wis"]
    character.db.charisma = bases["cha"]
    
    # Recalculate stats
    if hasattr(character, 'recalculate_stats'):
        character.recalculate_stats()
    
    # Link character to account
    account.db._playable_characters = [character]
    
    return character, f"Bot {name} created successfully"


def spawn_bots(count=5):
    """Spawn multiple bots."""
    results = []
    for i in range(count):
        char, msg = create_bot()
        results.append(msg)
    return results


# =============================================================================
# BOT BEHAVIOR
# =============================================================================

class BotExplorer:
    """
    Handles bot exploration logic.
    Called periodically by a script tick.
    """
    
    @staticmethod
    def tick(bot):
        """Process one bot tick."""
        if not bot or not bot.location:
            return
        
        state = getattr(bot.db, 'bot_state', 'exploring')
        
        if state == 'exploring':
            BotExplorer._explore(bot)
        elif state == 'training':
            BotExplorer._train(bot)
        elif state == 'guild_hunting':
            BotExplorer._find_guild(bot)
    
    @staticmethod
    def _explore(bot):
        """Bot explores a new room."""
        location = bot.location
        exits = [ex for ex in location.exits if ex.access(bot, "traverse")]
        
        if not exits:
            bot.msg("No exits here. Stuck.")
            return
        
        # Prefer unexplored directions
        unexplored = []
        for ex in exits:
            dest = ex.destination
            if dest and dest.id not in getattr(bot.db, 'rooms_explored', set()):
                unexplored.append(ex)
        
        if unexplored:
            exit = random.choice(unexplored)
        else:
            # All explored, pick random
            exit = random.choice(exits)
        
        # Move
        dest = exit.destination
        bot.move_to(dest, quiet=True)
        
        # Check if new room
        rooms_explored = getattr(bot.db, 'rooms_explored', set())
        is_new_room = dest.id not in rooms_explored
        
        if is_new_room:
            rooms_explored.add(dest.id)
            bot.db.rooms_explored = rooms_explored
            
            # Award EXP for discovery
            area_level = getattr(dest.db, 'danger_level', 1)
            xp = 25 * max(1, area_level)
            bot.db.experience = getattr(bot.db, 'experience', 0) + xp
            bot.db.total_xp_earned = getattr(bot.db, 'total_xp_earned', 0) + xp
            
            # Also award gold occasionally
            if random.random() < 0.1:
                gold = 5 * area_level
                bot.db.gold = getattr(bot.db, 'gold', 0) + gold
            
            # Report discovery occasionally
            total_rooms = len(rooms_explored)
            if total_rooms % 10 == 0 or random.random() < 0.2:
                BotExplorer._report_discovery(bot, dest, total_rooms, xp)
            
            # Check if should join guild after exploring enough
            if total_rooms >= 20 and not getattr(bot.db, 'guild', None):
                if random.random() < 0.3:
                    bot.db.bot_state = 'guild_hunting'
        
        # Chance to train skills while exploring
        if getattr(bot.db, 'guild', None) and random.random() < 0.05:
            BotExplorer._train(bot)
    
    @staticmethod
    def _report_discovery(bot, room, total_rooms, xp_earned):
        """Bot reports discovery to the bots channel."""
        # Get or create bots channel
        bots_channel = BotExplorer._get_bots_channel()
        if not bots_channel:
            return
        
        # Format message
        pct = (total_rooms / 11314.0) * 100
        msg_template = random.choice(DISCOVERY_MESSAGES)
        
        # Build context
        room_name = room.key
        area = getattr(room.db, 'area', 'Unknown')
        level = bot.db.level
        total_exp = bot.db.experience
        
        try:
            msg = msg_template.format(
                pct=pct,
                total=total_rooms,
                room_name=room_name,
                xp=xp_earned,
                total_exp=total_exp,
                level=level
            )
        except KeyError:
            msg = msg_template
        
        # Add room info
        full_msg = f"[{bot.key}] {msg} [Location: {room_name} in {area}]"
        
        # Send to channel
        bots_channel.msg(full_msg, senders=[bot])
        
        # Increment counter
        bot.db.discoveries_reported = getattr(bot.db, 'discoveries_reported', 0) + 1
    
    @staticmethod
    def _get_bots_channel():
        """Get or create the bots channel."""
        from evennia.comms.models import ChannelDB
        from evennia import create_channel
        from typeclasses.channels import Channel
        
        channels = ChannelDB.objects.filter(db_key__iexact="bots")
        if channels:
            return channels[0]
        
        # Create channel
        try:
            channel = create_channel("bots", typeclass=Channel)
            if channel:
                channel.db.desc = "Channel for bot discoveries and chatter"
                channel.db.channel_type = "bot"
                channel.db.color_code = "|c"
                channel.db.hide_from_channels_list = True  # Hide from normal list
            return channel
        except Exception:
            return None
    
    @staticmethod
    def _find_guild(bot):
        """Bot tries to find and join a guild."""
        # Pick random guild tree
        tree = random.choice(list(GUILD_TREES.keys()))
        guilds = GUILD_TREES[tree]
        
        # Try to join first guild in tree (alpha guild)
        guild_name = guilds[0]
        
        # For now, just assign guild directly (no guild master requirement for bots)
        bot.db.guild = guild_name.title()
        bot.db.guild_level = 1
        bot.db.guild_xp = 0
        
        # Give basic skills based on guild
        skills = getattr(bot.db, 'skills', {})
        if not isinstance(skills, dict):
            skills = {}
        
        if tree == "warrior":
            skills.update({'attack': 20, 'parry': 10, 'weapon skill blunt': 20})
        elif tree == "shapeshifter":
            skills.update({'shape shift': 10, 'reverse transformation': 10})
            # Give collar
            from evennia import create_object
            collar = create_object("typeclasses.objects.Object", key="a collar")
            collar.db.is_collar = True
            collar.move_to(bot, quiet=True)
        elif tree == "martial_artist":
            skills.update({'punch': 20, 'kick': 10})
        elif tree == "weaver":
            skills.update({'heal': 20, 'refresh': 10})
        elif tree == "unraveller":
            skills.update({'harm': 20, 'curse': 10})
        elif tree == "elemental":
            skills.update({'magic missile': 20, 'shield': 10})
        elif tree == "evoker":
            skills.update({'evoke': 20, 'channel': 10})
        elif tree == "necromancer":
            skills.update({'animate dead': 20, 'drain life': 10})
        elif tree == "psychics":
            skills.update({'mind blast': 20, 'telepathy': 10})
        elif tree == "acrobat":
            skills.update({'tumble': 20, 'balance': 10})
        elif tree == "lurker":
            skills.update({'hide': 20, 'sneak': 10, 'backstab': 10})
        elif tree == "druid":
            skills.update({"nature's touch": 20, 'entangle': 10})
        elif tree == "woodsman":
            skills.update({'chop': 20, 'track': 10})
        
        bot.db.skills = skills
        bot.db.bot_state = 'training'
        
        # Report
        bots_channel = BotExplorer._get_bots_channel()
        if bots_channel:
            bots_channel.msg(f"[{bot.key}] Just joined the {guild_name.title()} guild! Excited to learn new skills.", senders=[bot])
    
    @staticmethod
    def _train(bot):
        """Bot trains skills."""
        xp = getattr(bot.db, 'experience', 0)
        
        # Every so often, train a stat
        if random.random() < 0.2 and xp >= 100:
            from world.training import get_exp_cost, get_gold_cost
            training_level = getattr(bot.db, 'training_level', 1)
            cost = get_exp_cost(training_level)
            
            if xp >= cost:
                bot.db.experience -= cost
                bot.db.training_level = training_level + 1
                
                # Train random stat
                stats = ['str', 'dex', 'con', 'sta', 'int', 'wis']
                stat = random.choice(stats)
                bot.modify_stat(stat, 1)
                
                # Report occasionally
                if random.random() < 0.2:
                    bots_channel = BotExplorer._get_bots_channel()
                    if bots_channel:
                        bots_channel.msg(f"[{bot.key}] Trained my {stat.upper()}! Feeling stronger. (Training level {bot.db.training_level})", senders=[bot])
        
        # Go back to exploring
        bot.db.bot_state = 'exploring'


# =============================================================================
# BOT TICK SCRIPT
# =============================================================================

def run_bot_tick():
    """Run one exploration tick for all bots."""
    from typeclasses.characters import Character
    from evennia import search_object
    
    # Find all bot characters
    bots = []
    for char in Character.objects.all():
        if getattr(char.db, 'is_bot', False):
            bots.append(char)
    
    for bot in bots:
        try:
            BotExplorer.tick(bot)
        except Exception as e:
            # Bot error - log but don't crash
            print(f"Bot {bot.key} error: {e}")


# =============================================================================
# MANAGEMENT COMMANDS
# =============================================================================

def launch_bots(count=5):
    """Launch bot exploration system."""
    # Create bots channel
    BotExplorer._get_bots_channel()
    
    # Create bots
    results = spawn_bots(count)
    
    # Start exploration
    run_bot_tick()
    
    return results


def stop_bots():
    """Stop all bots."""
    from typeclasses.characters import Character
    for char in Character.objects.all():
        if getattr(char.db, 'is_bot', False):
            char.db.bot_state = 'idle'


def get_bot_stats():
    """Get statistics about all bots."""
    from typeclasses.characters import Character
    bots = []
    for char in Character.objects.all():
        if getattr(char.db, 'is_bot', False):
            bots.append({
                'name': char.key,
                'level': char.db.level,
                'guild': getattr(char.db, 'guild', None),
                'rooms': len(getattr(char.db, 'rooms_explored', set())),
                'xp': char.db.experience,
                'state': getattr(char.db, 'bot_state', 'unknown'),
                'location': char.location.key if char.location else 'Unknown',
            })
    return bots
