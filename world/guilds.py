"""
Red Dragon MUD - Guild System
Based on Islands of Myth guilds
"""

from evennia import DefaultScript
from typeclasses.rooms import GuildRoom

# Warrior Guild Skills (from IOM data - captured from live server)
WARRIOR_SKILLS = {
    "attack": {"cost": 100, "max": 100, "desc": "Basic attack proficiency."},
    "flesh_of_stone": {"cost": 200, "max": 100, "desc": "Harden your body against damage."},
    "honor_of_the_gods": {"cost": 300, "max": 100, "desc": "Call upon divine favor in combat."},
    "tanking": {"cost": 250, "max": 100, "desc": "Draw enemy attention to yourself."},
    "weapon_skill_blunt": {"cost": 150, "max": 100, "desc": "Proficiency with blunt weapons."},
    "slash": {"cost": 150, "max": 100, "desc": "A basic sword attack."},
    "bash": {"cost": 150, "max": 100, "desc": "Bash an opponent with your shield."},
    "kick": {"cost": 100, "max": 100, "desc": "A powerful kick attack."},
    "rescue": {"cost": 200, "max": 100, "desc": "Rescue a party member from combat."},
    "second_attack": {"cost": 500, "max": 100, "desc": "Gain a second attack per round."},
    "third_attack": {"cost": 1000, "max": 100, "desc": "Gain a third attack per round."},
    "enhanced_damage": {"cost": 300, "max": 100, "desc": "Increase damage dealt."},
    "dual_wield": {"cost": 400, "max": 100, "desc": "Wield two weapons at once."},
    "parry": {"cost": 250, "max": 100, "desc": "Parry incoming attacks."},
    "dodge": {"cost": 250, "max": 100, "desc": "Dodge incoming attacks."},
    "shield_block": {"cost": 200, "max": 100, "desc": "Block with your shield."},
    "disarm": {"cost": 300, "max": 100, "desc": "Disarm your opponent."},
    "trip": {"cost": 200, "max": 100, "desc": "Trip your opponent."},
    "berserk": {"cost": 500, "max": 100, "desc": "Enter a berserk rage."},
}

# All guild definitions
GUILDS = {
    "warrior": {
        "name": "Warrior",
        "master": "QuinSyndrius The Great Warlord",
        "skills": WARRIOR_SKILLS,
        "desc": "The warrior guild focuses on physical combat prowess."
    },
    "martial": {
        "name": "Martial Artist",
        "master": "Master Kael",
        "skills": {},  # TODO: Fill from IOM data
        "desc": "Martial artists train their bodies as weapons."
    },
    "druid": {
        "name": "Druid",
        "master": "Druid Elder",
        "skills": {},
        "desc": "Druids draw power from nature."
    },
    "woodsman": {
        "name": "Woodsman",
        "master": "Ranger Captain",
        "skills": {},
        "desc": "Woodsmen are masters of the wilderness."
    },
    "shapeshifter": {
        "name": "Shapeshifter",
        "master": "The Changeling",
        "skills": {},
        "desc": "Shapeshifters can transform into beasts."
    },
    "weaver": {
        "name": "Weaver",
        "master": "The Weaver",
        "skills": {},
        "desc": "Weavers manipulate the threads of reality."
    },
    "unraveller": {
        "name": "Unraveller",
        "master": "The Unraveller",
        "skills": {},
        "desc": "Unravellers tear apart magic and matter."
    },
    "acrobat": {
        "name": "Acrobat",
        "master": "The Acrobat",
        "skills": {},
        "desc": "Acrobats are masters of agility."
    },
    "element": {
        "name": "Elementalist",
        "master": "The Elementalist",
        "skills": {},
        "desc": "Elementalists command fire, water, earth, and air."
    },
    "evoker": {
        "name": "Evoker",
        "master": "The Evoker",
        "skills": {},
        "desc": "Evokers summon raw magical power."
    },
    "abjurer": {
        "name": "Abjurer",
        "master": "The Abjurer",
        "skills": {},
        "desc": "Abjurers specialize in protective magic."
    },
    "psychics": {
        "name": "Psychic",
        "master": "The Psychic",
        "skills": {},
        "desc": "Psychics wield mental powers."
    },
    "necro": {
        "name": "Necromancer",
        "master": "The Necromancer",
        "skills": {},
        "desc": "Necromancers command the dead."
    },
    "lurker": {
        "name": "Lurker",
        "master": "The Lurker",
        "skills": {},
        "desc": "Lurkers strike from the shadows."
    }
}


class GuildManager(DefaultScript):
    """Global guild manager script."""
    
    def at_script_creation(self):
        self.key = "guild_manager"
        self.persistent = True
        self.db.guilds = GUILDS
        
    def get_guild(self, guild_key):
        """Get guild data by key."""
        return self.db.guilds.get(guild_key.lower())
        
    def list_guilds(self):
        """List all available guilds."""
        return [(key, data["name"]) for key, data in self.db.guilds.items()]
        
    def get_skills(self, guild_key):
        """Get skills for a guild."""
        guild = self.get_guild(guild_key)
        if guild:
            return guild.get("skills", {})
        return {}


def join_guild(character, guild_key):
    """Have a character join a guild."""
    guild = GUILDS.get(guild_key.lower())
    if not guild:
        return False
        
    character.db.guild = guild["name"]
    character.db.guild_level = 0
    character.db.guild_key = guild_key.lower()
    
    # Initialize skills dict
    if not hasattr(character.db, 'skills'):
        character.db.skills = {}
        
    return True


def train_skill(character, skill_name):
    """Train a skill at guild."""
    if not character.db.guild:
        character.msg("You must join a guild first.")
        return False
        
    guild_data = GUILDS.get(character.db.guild_key, {})
    skills = guild_data.get("skills", {})
    
    if skill_name not in skills:
        character.msg("That skill is not available in your guild.")
        return False
        
    skill_info = skills[skill_name]
    current = character.db.skills.get(skill_name, 0)
    
    if current >= skill_info["max"]:
        character.msg("You have mastered that skill.")
        return False
        
    # Check gold cost
    gold = getattr(character.db, 'gold', 0)
    cost = skill_info["cost"]
    
    if gold < cost:
        character.msg(f"You need {cost} gold to train that skill.")
        return False
        
    # Deduct gold and increase skill
    character.db.gold -= cost
    character.db.skills[skill_name] = current + 1
    
    character.msg(f"You train {skill_name} to {current + 1}%!")
    return True


def advance_guild_level(character):
    """Advance character's guild level."""
    if not character.db.guild:
        character.msg("You must join a guild first.")
        return False
        
    # Check requirements
    # In IOM, you need certain skill percentages to advance
    guild_data = GUILDS.get(character.db.guild_key, {})
    skills = guild_data.get("skills", {})
    
    # Simple check: need at least 50% in one skill per guild level
    req_skill_pct = character.db.guild_level * 50
    
    has_req = False
    for skill_name, level in character.db.skills.items():
        if level >= req_skill_pct:
            has_req = True
            break
            
    if not has_req and character.db.guild_level > 0:
        character.msg(f"You need at least {req_skill_pct}% in a skill to advance.")
        return False
        
    # Check gold
    cost = (character.db.guild_level + 1) * 100
    gold = getattr(character.db, 'gold', 0)
    
    if gold < cost:
        character.msg(f"You need {cost} gold to advance.")
        return False
        
    character.db.gold -= cost
    character.db.guild_level += 1
    
    character.msg(f"You have advanced to guild level {character.db.guild_level}!")
    return True
