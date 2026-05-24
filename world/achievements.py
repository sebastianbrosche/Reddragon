#!/usr/bin/env python3
"""
Red Dragon MUD - IOM Achievement Definitions
Uses Evennia's contrib.game_systems.achievements system.

Achievements are tracked on characters and can trigger rewards.
Format follows Evennia's achievement dict specification.
"""

# Achievement categories
CAT_COMBAT = "Combat"
CAT_EXPLORATION = "Exploration"
CAT_PROGRESSION = "Progression"
CAT_SOCIAL = "Social"
CAT_DEATH = "Death"
CAT_ECONOMY = "Economy"
CAT_RP = "Roleplay"

# Achievement definitions for IOM
ACHIEVEMENTS = {
    # Combat achievements
    "first_blood": {
        "name": "First Blood",
        "category": CAT_COMBAT,
        "desc": "Kill your first monster.",
        "tracking": "separate",
        "num": 1,
        "rewards": [("xp", 50)],
    },
    "rat_slayer": {
        "name": "Rat Slayer",
        "category": CAT_COMBAT,
        "desc": "Kill 10 rats.",
        "tracking": "separate",
        "num": 10,
        "prereqs": [("first_blood", 1)],
        "rewards": [("xp", 100), ("gold", 50)],
    },
    "dire_rat_slayer": {
        "name": "Once More, But Bigger",
        "category": CAT_COMBAT,
        "desc": "Kill 10 dire rats.",
        "tracking": "separate",
        "num": 10,
        "prereqs": [("rat_slayer", 10)],
        "rewards": [("xp", 200)],
    },
    "kill_100": {
        "name": "Hundred Slayer",
        "category": CAT_COMBAT,
        "desc": "Kill 100 monsters.",
        "tracking": "separate",
        "num": 100,
        "rewards": [("xp", 500), ("title", "the Bloodstained")],
    },
    "kill_1000": {
        "name": "Thousand Slayer",
        "category": CAT_COMBAT,
        "desc": "Kill 1,000 monsters.",
        "tracking": "separate",
        "num": 1000,
        "prereqs": [("kill_100", 100)],
        "rewards": [("xp", 5000), ("title", "the Destroyer")],
    },
    
    # Exploration achievements
    "first_step": {
        "name": "First Step",
        "category": CAT_EXPLORATION,
        "desc": "Explore your first room.",
        "tracking": "separate",
        "num": 1,
        "rewards": [("xp", 25)],
    },
    "wanderer": {
        "name": "Wanderer",
        "category": CAT_EXPLORATION,
        "desc": "Explore 100 rooms.",
        "tracking": "separate",
        "num": 100,
        "rewards": [("xp", 200)],
    },
    "explorer": {
        "name": "Explorer",
        "category": CAT_EXPLORATION,
        "desc": "Explore 1,000 rooms.",
        "tracking": "separate",
        "num": 1000,
        "prereqs": [("wanderer", 100)],
        "rewards": [("xp", 1000), ("title", "the Explorer")],
    },
    "cartographer": {
        "name": "Cartographer",
        "category": CAT_EXPLORATION,
        "desc": "Explore 5,000 rooms.",
        "tracking": "separate",
        "num": 5000,
        "prereqs": [("explorer", 1000)],
        "rewards": [("xp", 5000), ("title", "the Cartographer")],
    },
    "ilium_visitor": {
        "name": "Visitor to Illium",
        "category": CAT_EXPLORATION,
        "desc": "Visit Ilium City.",
        "tracking": "separate",
        "num": 1,
        "rewards": [("xp", 50)],
    },
    
    # Progression achievements
    "novice": {
        "name": "Novice Adventurer",
        "category": CAT_PROGRESSION,
        "desc": "Reach level 10.",
        "tracking": "separate",
        "num": 10,
        "rewards": [("xp", 100)],
    },
    "seasoned": {
        "name": "Seasoned Warrior",
        "category": CAT_PROGRESSION,
        "desc": "Reach level 50.",
        "tracking": "separate",
        "num": 50,
        "prereqs": [("novice", 10)],
        "rewards": [("xp", 500), ("title", "the Seasoned")],
    },
    "veteran": {
        "name": "Veteran",
        "category": CAT_PROGRESSION,
        "desc": "Reach level 100.",
        "tracking": "separate",
        "num": 100,
        "prereqs": [("seasoned", 50)],
        "rewards": [("xp", 2000), ("title", "the Veteran")],
    },
    "master": {
        "name": "Master Adventurer",
        "category": CAT_PROGRESSION,
        "desc": "Reach level 200.",
        "tracking": "separate",
        "num": 200,
        "prereqs": [("veteran", 100)],
        "rewards": [("xp", 10000), ("title", "the Master")],
    },
    "guild_initiate": {
        "name": "Guild Initiate",
        "category": CAT_PROGRESSION,
        "desc": "Reach guild level 5.",
        "tracking": "separate",
        "num": 5,
        "rewards": [("xp", 100)],
    },
    "guild_master": {
        "name": "Guild Master",
        "category": CAT_PROGRESSION,
        "desc": "Reach guild level 50.",
        "tracking": "separate",
        "num": 50,
        "prereqs": [("guild_initiate", 5)],
        "rewards": [("xp", 2000), ("title", "the Guildmaster")],
    },
    
    # Death achievements
    "first_death": {
        "name": "First Death",
        "category": CAT_DEATH,
        "desc": "Die for the first time.",
        "tracking": "separate",
        "num": 1,
        "rewards": [],
    },
    "persistent": {
        "name": "Persistent",
        "category": CAT_DEATH,
        "desc": "Die 10 times.",
        "tracking": "separate",
        "num": 10,
        "prereqs": [("first_death", 1)],
        "rewards": [("xp", 50), ("title", "the Persistent")],
    },
    "immortal": {
        "name": "Immortal?",
        "category": CAT_DEATH,
        "desc": "Die 100 times.",
        "tracking": "separate",
        "num": 100,
        "prereqs": [("persistent", 10)],
        "rewards": [("xp", 500), ("title", "the Undying")],
    },
    
    # Economy achievements
    "first_gold": {
        "name": "First Gold",
        "category": CAT_ECONOMY,
        "desc": "Earn your first gold piece.",
        "tracking": "separate",
        "num": 1,
        "rewards": [("xp", 25)],
    },
    "wealthy": {
        "name": "Wealthy",
        "category": CAT_ECONOMY,
        "desc": "Accumulate 10,000 gold.",
        "tracking": "separate",
        "num": 10000,
        "prereqs": [("first_gold", 1)],
        "rewards": [("xp", 500), ("title", "the Wealthy")],
    },
    "first_purchase": {
        "name": "First Purchase",
        "category": CAT_ECONOMY,
        "desc": "Buy your first item.",
        "tracking": "separate",
        "num": 1,
        "rewards": [("xp", 25)],
    },
    
    # Social achievements
    "first_chat": {
        "name": "First Words",
        "category": CAT_SOCIAL,
        "desc": "Send your first chat message.",
        "tracking": "separate",
        "num": 1,
        "rewards": [("xp", 10)],
    },
    "socialite": {
        "name": "Socialite",
        "category": CAT_SOCIAL,
        "desc": "Send 1,000 chat messages.",
        "tracking": "separate",
        "num": 1000,
        "prereqs": [("first_chat", 1)],
        "rewards": [("xp", 200), ("title", "the Chatty")],
    },
    "mail_sent": {
        "name": "Correspondent",
        "category": CAT_SOCIAL,
        "desc": "Send your first mail.",
        "tracking": "separate",
        "num": 1,
        "rewards": [("xp", 25)],
    },
    
    # RP achievements
    "first_emote": {
        "name": "Expressive",
        "category": CAT_RP,
        "desc": "Use your first emote.",
        "tracking": "separate",
        "num": 1,
        "rewards": [("xp", 10)],
    },
    "first_pose": {
        "name": "Poser",
        "category": CAT_RP,
        "desc": "Set your first pose.",
        "tracking": "separate",
        "num": 1,
        "rewards": [("xp", 10)],
    },
}

# Achievement reward handlers
def reward_xp(character, amount):
    """Grant XP reward."""
    if hasattr(character, 'add_experience'):
        character.add_experience(amount)
    else:
        character.db.experience = character.db.experience + amount

def reward_gold(character, amount):
    """Grant gold reward."""
    character.db.gold = character.db.gold + amount
    character.msg(f"|yYou received {amount} gold!|n")

def reward_title(character, title):
    """Grant title reward."""
    if not hasattr(character.db, 'titles'):
        character.db.titles = []
    if title not in character.db.titles:
        character.db.titles.append(title)
        character.msg(f"|yYou earned the title '{title}'!|n")

REWARD_HANDLERS = {
    "xp": reward_xp,
    "gold": reward_gold,
    "title": reward_title,
}

def grant_rewards(character, rewards):
    """Grant a list of rewards to a character."""
    for reward_type, value in rewards:
        handler = REWARD_HANDLERS.get(reward_type)
        if handler:
            handler(character, value)

# Export for Evennia achievement system
__all__ = ["ACHIEVEMENTS"]
