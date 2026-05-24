"""
Red Dragon MUD - Quest System
Handles quest definitions, progress tracking, and rewards
"""

from evennia import Command, CmdSet, create_object
from evennia.utils import search
from evennia.utils.utils import delay
import random

# Quest types
QUEST_TYPE_KILL = "kill"
QUEST_TYPE_FETCH = "fetch"
QUEST_TYPE_DELIVER = "deliver"
QUEST_TYPE_EXPLORE = "explore"
QUEST_TYPE_TALK = "talk"
QUEST_TYPE_GUILD = "guild"  # Guild-specific advancement quests

# Quest states
QUEST_NOT_STARTED = "not_started"
QUEST_ACTIVE = "active"
QUEST_COMPLETED = "completed"
QUEST_FAILED = "failed"

class Quest:
    """Represents a single quest definition."""
    
    def __init__(self, quest_id, title, description, quest_type, objectives, rewards, 
                 giver=None, required_level=1, required_guild=None, prerequisites=None):
        """
        Args:
            quest_id: Unique identifier
            title: Quest name
            description: Quest description text
            quest_type: QUEST_TYPE_* constant
            objectives: List of dicts with objective data
            rewards: Dict with reward data
            giver: NPC or room that gives the quest
            required_level: Minimum level to start
            required_guild: Guild required (None for all)
            prerequisites: List of quest_ids that must be completed first
        """
        self.quest_id = quest_id
        self.title = title
        self.description = description
        self.quest_type = quest_type
        self.objectives = objectives
        self.rewards = rewards
        self.giver = giver
        self.required_level = required_level
        self.required_guild = required_guild
        self.prerequisites = prerequisites or []

# Quest Database
QUESTS = {
    # Newbie Quests
    "newbie_tour": Quest(
        "newbie_tour",
        "Tour of the Islands",
        "Visit all 19 newbie areas to get familiar with the world.",
        QUEST_TYPE_EXPLORE,
        [
            {"area": "adventurer_guild", "desc": "Visit the Adventurer Guild"},
            {"area": "yensid_land", "desc": "Visit Yensid Land"},
            {"area": "lobelands", "desc": "Visit the LobeLands"},
        ],
        {"exp": 500, "gold": 100, "item": None},
        giver="sisong",
        required_level=1,
    ),
    
    "kill_earwigs": Quest(
        "kill_earwigs",
        "Pest Control",
        "The LobeLands are infested with earwigs. Kill 10 of them to help clear the area.",
        QUEST_TYPE_KILL,
        [
            {"target": "earwig", "count": 10, "current": 0, "desc": "Kill 10 earwigs"},
        ],
        {"exp": 300, "gold": 50, "item": "healing_potion"},
        giver="sisong",
        required_level=1,
    ),
    
    "first_blood": Quest(
        "first_blood",
        "First Blood",
        "Kill your first monster and return to the Adventurer Guild.",
        QUEST_TYPE_KILL,
        [
            {"target": "any", "count": 1, "current": 0, "desc": "Kill any monster"},
        ],
        {"exp": 200, "gold": 25, "item": "leather_armor"},
        giver="achman",
        required_level=1,
    ),
    
    # Guild Quests
    "warrior_initiation": Quest(
        "warrior_initiation",
        "Warrior's Path",
        "Prove your strength by defeating 5 monsters in combat.",
        QUEST_TYPE_GUILD,
        [
            {"target": "any", "count": 5, "current": 0, "desc": "Defeat 5 monsters in combat"},
        ],
        {"exp": 1000, "gold": 200, "guild_rank": 1, "item": "warrior_belt"},
        giver="warrior_guildmaster",
        required_level=5,
        required_guild="warrior",
    ),
    
    "mage_apprentice": Quest(
        "mage_apprentice",
        "Apprentice Mage",
        "Gather magical components for your first spell.",
        QUEST_TYPE_FETCH,
        [
            {"item": "crystal_shard", "count": 3, "current": 0, "desc": "Collect 3 crystal shards"},
            {"item": "herb_mandrake", "count": 2, "current": 0, "desc": "Collect 2 mandrake herbs"},
        ],
        {"exp": 1000, "gold": 200, "guild_rank": 1, "item": "mage_robe"},
        giver="mage_guildmaster",
        required_level=5,
        required_guild="mage",
    ),
    
    "rogue_stealth": Quest(
        "rogue_stealth",
        "Test of Stealth",
        "Sneak past the guards in the training grounds without being seen.",
        QUEST_TYPE_EXPLORE,
        [
            {"area": "training_grounds", "stealth": True, "desc": "Sneak through training grounds"},
        ],
        {"exp": 1000, "gold": 200, "guild_rank": 1, "item": "thief_tools"},
        giver="rogue_guildmaster",
        required_level=5,
        required_guild="rogue",
    ),
    
    "druid_nature": Quest(
        "druid_nature",
        "Harmony with Nature",
        "Visit the sacred grove and commune with the spirits.",
        QUEST_TYPE_EXPLORE,
        [
            {"area": "sacred_grove", "desc": "Visit the sacred grove"},
            {"action": "commune", "desc": "Commune with nature spirits"},
        ],
        {"exp": 1000, "gold": 200, "guild_rank": 1, "item": "druid_staff"},
        giver="druid_guildmaster",
        required_level=5,
        required_guild="druid",
    ),
    
    # Mid-level Quests
    "blackavar_explorer": Quest(
        "blackavar_explorer",
        "Explorer of Blackavar",
        "Explore the vast domain of Blackavar and discover its secrets.",
        QUEST_TYPE_EXPLORE,
        [
            {"area": "valley_of_magic", "desc": "Visit Valley of Magic"},
            {"area": "mt_olympus", "desc": "Climb Mt Olympus"},
            {"area": "blackavar_city", "desc": "Enter Blackavar City"},
        ],
        {"exp": 5000, "gold": 1000, "item": "explorer_map"},
        required_level=15,
    ),
    
    "dragon_slayer": Quest(
        "dragon_slayer",
        "Dragon Slayer",
        "A dragon has been terrorizing the countryside. Slay it!",
        QUEST_TYPE_KILL,
        [
            {"target": "dragon", "count": 1, "current": 0, "desc": "Slay the dragon"},
        ],
        {"exp": 10000, "gold": 5000, "item": "dragon_scale_armor"},
        required_level=25,
        prerequisites=["blackavar_explorer"],
    ),
    
    # Delivery Quests
    "deliver_message": Quest(
        "deliver_message",
        "Urgent Delivery",
        "Deliver an urgent message from the Adventurer Guild to Blackavar City.",
        QUEST_TYPE_DELIVER,
        [
            {"item": "sealed_letter", "from": "adventurer_guild", "to": "blackavar_city", "desc": "Deliver sealed letter"},
        ],
        {"exp": 400, "gold": 75, "item": None},
        giver="achman",
        required_level=2,
    ),
    
    # Fetch Quests
    "potion_ingredients": Quest(
        "potion_ingredients",
        "Potion Ingredients",
        "Gather ingredients for the guild alchemist.",
        QUEST_TYPE_FETCH,
        [
            {"item": "spider_venom", "count": 5, "current": 0, "desc": "Collect 5 spider venoms"},
            {"item": "healing_herb", "count": 10, "current": 0, "desc": "Collect 10 healing herbs"},
        ],
        {"exp": 600, "gold": 120, "item": "health_potion"},
        giver="alchemist",
        required_level=3,
    ),
}

# Active quest tracking on characters
def get_quest_log(character):
    """Get a character's quest log."""
    if not hasattr(character.db, 'quest_log'):
        character.db.quest_log = {}
    return character.db.quest_log

def get_active_quests(character):
    """Get list of active quest IDs."""
    log = get_quest_log(character)
    return [qid for qid, data in log.items() if data.get("state") == QUEST_ACTIVE]

def get_completed_quests(character):
    """Get list of completed quest IDs."""
    log = get_quest_log(character)
    return [qid for qid, data in log.items() if data.get("state") == QUEST_COMPLETED]

def can_start_quest(character, quest_id):
    """Check if character can start a quest."""
    if quest_id not in QUESTS:
        return False, "Quest does not exist."
    
    quest = QUESTS[quest_id]
    log = get_quest_log(character)
    
    # Check if already active or completed
    if quest_id in log:
        if log[quest_id]["state"] == QUEST_ACTIVE:
            return False, "You are already on this quest."
        if log[quest_id]["state"] == QUEST_COMPLETED:
            return False, "You have already completed this quest."
    
    # Check level requirement
    if character.db.level < quest.required_level:
        return False, f"You must be level {quest.required_level} to start this quest."
    
    # Check guild requirement
    if quest.required_guild:
        if getattr(character.db, 'guild', None) != quest.required_guild:
            return False, f"This quest requires the {quest.required_guild} guild."
    
    # Check prerequisites
    for prereq_id in quest.prerequisites:
        if prereq_id not in log or log[prereq_id]["state"] != QUEST_COMPLETED:
            prereq = QUESTS.get(prereq_id)
            prereq_name = prereq.title if prereq else prereq_id
            return False, f"You must complete '{prereq_name}' first."
    
    return True, ""

def start_quest(character, quest_id):
    """Start a quest for a character."""
    can_start, reason = can_start_quest(character, quest_id)
    if not can_start:
        return False, reason
    
    quest = QUESTS[quest_id]
    log = get_quest_log(character)
    
    # Initialize quest progress
    log[quest_id] = {
        "state": QUEST_ACTIVE,
        "started_at": character.dbref,  # Use current time in practice
        "objectives": [
            {"desc": obj["desc"], "completed": False, "current": obj.get("current", 0), 
             "target": obj.get("count", 1)}
            for obj in quest.objectives
        ],
    }
    
    character.db.quest_log = log
    return True, f"Quest started: {quest.title}"

def update_quest_progress(character, quest_id, objective_index, amount=1):
    """Update progress on a quest objective."""
    log = get_quest_log(character)
    if quest_id not in log or log[quest_id]["state"] != QUEST_ACTIVE:
        return False
    
    quest = QUESTS.get(quest_id)
    if not quest:
        return False
    
    obj_data = log[quest_id]["objectives"][objective_index]
    obj_data["current"] += amount
    
    # Check if objective is complete
    target = quest.objectives[objective_index].get("count", 1)
    if obj_data["current"] >= target:
        obj_data["completed"] = True
        character.msg(f"|gQuest objective completed: {obj_data['desc']}|n")
    
    # Check if all objectives complete
    if all(o["completed"] for o in log[quest_id]["objectives"]):
        complete_quest(character, quest_id)
    
    character.db.quest_log = log
    return True

def complete_quest(character, quest_id):
    """Complete a quest and give rewards."""
    log = get_quest_log(character)
    if quest_id not in log:
        return False
    
    quest = QUESTS[quest_id]
    log[quest_id]["state"] = QUEST_COMPLETED
    
    # Give rewards
    rewards = quest.rewards
    messages = [f"|gQuest completed: {quest.title}!|n"]
    
    if "exp" in rewards:
        exp = rewards["exp"]
        # Apply exp rate modifier
        exp_rate = getattr(character.db, 'exp_rate', 100) / 100.0
        adjusted_exp = int(exp * exp_rate)
        character.db.exp = character.db.get('exp', 0) + adjusted_exp
        messages.append(f"|yExperience gained: {adjusted_exp}|n")
    
    if "gold" in rewards:
        gold = rewards["gold"]
        character.db.gold = character.db.get('gold', 0) + gold
        messages.append(f"|yGold gained: {gold}|n")
    
    if "guild_rank" in rewards:
        rank = rewards["guild_rank"]
        character.db.guild_rank = rank
        messages.append(f"|yGuild rank increased to: {rank}|n")
    
    if "item" in rewards and rewards["item"]:
        item_name = rewards["item"]
        # Create and give item (simplified - would use actual item creation)
        messages.append(f"|yItem received: {item_name}|n")
    
    character.db.quest_log = log
    
    for msg in messages:
        character.msg(msg)
    
    return True

def fail_quest(character, quest_id, reason=""):
    """Fail a quest."""
    log = get_quest_log(character)
    if quest_id in log:
        log[quest_id]["state"] = QUEST_FAILED
        character.db.quest_log = log
        character.msg(f"|rQuest failed: {QUESTS[quest_id].title}. {reason}|n")
