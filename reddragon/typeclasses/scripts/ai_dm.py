"""
AI Dungeon Master for Red Dragon MUD
Integrates with Kimi Claw for creative referee decisions

Features:
- Personality rotation on each reboot
- Event monitoring (combat, quests, exploration)
- Dynamic achievement generation
- Divine intervention capabilities
"""

import random
import json
from evennia import DefaultScript
from evennia.utils import logger
from evennia.utils.search import search_object
from django.conf import settings


# =============================================================================
# PERSONALITY ARCHETYPES
# =============================================================================

AI_DM_PERSONALITIES = {
    "benevolent": {
        "title": "The Benevolent Architect",
        "mood": "generous",
        "reward_bias": 1.5,
        "punishment_chance": 0.05,
        "flavor_text": [
            "smiles upon your ingenuity",
            "finds your approach refreshingly creative",
            "blesses your cleverness with fortune",
        ],
        "title_templates": [
            "the Blessed",
            "Favored of the Architect",
            "the Inspired",
            "the Golden",
        ],
    },
    "malevolent": {
        "title": "The Malevolent Tyrant",
        "mood": "cruel",
        "reward_bias": 0.6,
        "punishment_chance": 0.4,
        "flavor_text": [
            "regards you with cold amusement",
            "grants you a twisted reward for your insolence",
            "laughs at your cleverness, but rewards it nonetheless",
        ],
        "title_templates": [
            "the Tainted",
            "Fool of the Tyrant",
            "the Cursed Clever",
            "the Thorned",
        ],
    },
    "chaotic": {
        "title": "The Chaos Weaver",
        "mood": "unpredictable",
        "reward_bias": 1.0,
        "punishment_chance": 0.2,
        "flavor_text": [
            "cackles at your unorthodox methods",
            "rolls the dice of fate for you",
            "finds your chaos... acceptable",
        ],
        "title_templates": [
            "the Unpredictable",
            "Child of Chaos",
            "the Shifting",
            "the Wildcard",
        ],
    },
    "lawful": {
        "title": "The Law Keeper",
        "mood": "stern",
        "reward_bias": 0.8,
        "punishment_chance": 0.15,
        "flavor_text": [
            "acknowledges your solution, though unorthodox",
            "grants merit for results, if not method",
            "notes your ingenuity in the eternal ledger",
        ],
        "title_templates": [
            "the Recognized",
            "Merit Bearer",
            "the Just",
            "the Ledgered",
        ],
    },
    "trickster": {
        "title": "The Cosmic Trickster",
        "mood": "mischievous",
        "reward_bias": 1.2,
        "punishment_chance": 0.3,
        "flavor_text": [
            "winks at your clever workaround",
            "applauds your creativity with a twist",
            "rewards you... but read the fine print",
        ],
        "title_templates": [
            "the Tricked",
            "Pawn of the Cosmic Joke",
            "the Ironically Blessed",
            "the Fine Print",
        ],
    },
    "doomsayer": {
        "title": "The Doomsayer",
        "mood": "fatalistic",
        "reward_bias": 0.7,
        "punishment_chance": 0.25,
        "flavor_text": [
            "sees your success as merely delaying the inevitable",
            "grants you power... for the end times",
            "notes your achievement in the final chronicle",
        ],
        "title_templates": [
            "the Doomed Hero",
            "Marked for the End",
            "the Final Chapter",
            "the Last Spark",
        ],
    },
}


# =============================================================================
# ACHIEVEMENT TEMPLATES
# =============================================================================

ACHIEVEMENT_TEMPLATES = {
    "creative_solution": {
        "descriptions": [
            "Solved {quest} through unorthodox means, bypassing conventional approaches entirely.",
            "Found a hidden path through {quest} that no guide ever documented.",
            "Defied the expected solution to {quest}, creating their own methodology.",
        ],
        "rewards": [
            {"type": "exp", "base": 500, "variance": 0.5},
            {"type": "gold", "base": 200, "variance": 0.3},
            {"type": "item", "tier": "uncommon"},
            {"type": "stat_boost", "stat": "intelligence", "amount": 1},
        ],
    },
    "first_discovery": {
        "descriptions": [
            "First to uncover the secrets of {location} in this age.",
            "Pioneered exploration of {location}, mapping what was forgotten.",
            "Discovered a hidden aspect of {location} previously unknown to all.",
        ],
        "rewards": [
            {"type": "exp", "base": 1000, "variance": 0.3},
            {"type": "title", "tier": "rare"},
            {"type": "item", "tier": "rare"},
        ],
    },
    "creative_combat": {
        "descriptions": [
            "Defeated {enemy} using tactics that defied all martial convention.",
            "Turned the environment against {enemy} in a masterstroke of improvisation.",
            "Survived against {enemy} through sheer creative warfare.",
        ],
        "rewards": [
            {"type": "exp", "base": 300, "variance": 0.4},
            {"type": "gold", "base": 100, "variance": 0.5},
            {"type": "stat_boost", "stat": "strength", "amount": 1},
        ],
    },
    "social_mastery": {
        "descriptions": [
            "Won over {npc} through words where steel would have failed.",
            "Negotiated with {npc} in a manner that reshaped the local politics.",
            "Charmed {npc} into revealing secrets never meant for mortal ears.",
        ],
        "rewards": [
            {"type": "exp", "base": 400, "variance": 0.3},
            {"type": "reputation", "faction": "local", "amount": 10},
            {"type": "item", "tier": "uncommon"},
        ],
    },
    "easter_egg": {
        "descriptions": [
            "Stumbled upon something that was definitely not meant to be found.",
            "Triggered a sequence of events the architects never anticipated.",
            "Found the needle in the cosmic haystack.",
        ],
        "rewards": [
            {"type": "exp", "base": 2000, "variance": 0.2},
            {"type": "title", "tier": "legendary"},
            {"type": "item", "tier": "legendary"},
        ],
    },
}


# =============================================================================
# AI DM SCRIPT
# =============================================================================

class AIDungeonMaster(DefaultScript):
    """
    The AI Dungeon Master watches over the game world,
    makes creative judgments, and forges custom achievements.
    
    Each reboot, a new personality is selected, changing how
    the AI DM responds to player actions.
    """
    
    def at_script_creation(self):
        self.key = "ai_dm"
        self.desc = "AI Dungeon Master - watches and judges"
        self.persistent = True
        self.interval = 60  # Check events every minute
        
        # Initialize personality
        self.db.personality = None
        self.db.mood = "neutral"
        self.db.intervention_log = []
        self.db.achievements_granted = []
        self.db.last_reboot = None
    
    def at_start(self):
        """Called when script starts (including after reboot)."""
        self._select_personality()
        self._announce_presence()
    
    def at_repeat(self):
        """Periodic check - can add random ambient interventions."""
        # Small chance of random "divine attention" event
        if random.random() < 0.02:  # 2% per minute
            self._random_divine_whisper()
    
    # =====================================================================
    # PERSONALITY MANAGEMENT
    # =====================================================================
    
    def _select_personality(self):
        """Select a random personality for this reboot cycle."""
        personality_key = random.choice(list(AI_DM_PERSONALITIES.keys()))
        self.db.personality = personality_key
        self.db.mood = AI_DM_PERSONALITIES[personality_key]["mood"]
        
        logger.log_info(f"AI DM Personality selected: {personality_key}")
    
    def get_personality(self):
        """Get current personality data."""
        if not self.db.personality:
            self._select_personality()
        return AI_DM_PERSONALITIES.get(self.db.personality, AI_DM_PERSONALITIES["benevolent"])
    
    # =====================================================================
    # ANNOUNCEMENTS
    # =====================================================================
    
    def _announce_presence(self):
        """Announce the AI DM's presence to the world."""
        personality = self.get_personality()
        
        # Find all connected players
        from evennia.server.sessionhandler import SESSION_HANDLER
        sessions = SESSION_HANDLER.get_sessions()
        
        msg = f"""
|b[Divine Presence]|n A shift in the cosmic fabric... 

The |y{personality['title']}|n has awakened.

The world now turns under the gaze of a {personality['mood']} power.
Players who show creativity may find themselves... |wnoticed|n.
        """.strip()
        
        for session in sessions:
            if session.puppet:
                session.msg(msg)
    
    def _random_divine_whisper(self):
        """Send a random divine message to a random player."""
        from evennia.server.sessionhandler import SESSION_HANDLER
        sessions = [s for s in SESSION_HANDLER.get_sessions() if s.puppet]
        
        if not sessions:
            return
        
        session = random.choice(sessions)
        player = session.puppet
        
        whispers = [
            "You feel unseen eyes upon you...",
            "A strange wind carries a voice that speaks your name.",
            "For a moment, the world holds its breath around you.",
            "You catch a glimpse of something vast in the corner of your vision.",
            "The dice of fate rattle in an unseen hand.",
        ]
        
        player.msg(f"|b[Divine Whisper]|n {random.choice(whispers)}")
    
    # =====================================================================
    # INTERVENTION ENGINE
    # =====================================================================
    
    def judge_event(self, event_type, player, context=None):
        """
        Main entry point for AI DM intervention.
        
        Args:
            event_type: Type of event (creative_solution, first_discovery, etc.)
            player: The player involved
            context: Dict with relevant context data
            
        Returns:
            Dict with the AI DM's judgment
        """
        personality = self.get_personality()
        context = context or {}
        
        # Determine if we intervene
        if not self._should_intervene(event_type, personality):
            return None
        
        # Generate judgment
        judgment = self._create_judgment(event_type, player, context, personality)
        
        # Log it
        self._log_intervention(judgment)
        
        # Deliver to player
        self._deliver_judgment(player, judgment)
        
        return judgment
    
    def _should_intervene(self, event_type, personality):
        """Determine if the AI DM should intervene for this event."""
        base_chance = 0.3  # 30% base
        
        # Personality modifiers
        if personality["mood"] == "generous":
            base_chance = 0.5
        elif personality["mood"] == "cruel":
            base_chance = 0.2
        elif personality["mood"] == "unpredictable":
            base_chance = random.uniform(0.1, 0.6)
        
        # Event type modifiers
        if event_type in ["easter_egg", "first_discovery"]:
            base_chance += 0.3
        
        return random.random() < base_chance
    
    def _create_judgment(self, event_type, player, context, personality):
        """Create a judgment with dynamic achievement."""
        templates = ACHIEVEMENT_TEMPLATES.get(event_type, ACHIEVEMENT_TEMPLATES["creative_solution"])
        
        # Select description
        desc_template = random.choice(templates["descriptions"])
        description = desc_template.format(**context)
        
        # Generate title
        title_template = random.choice(personality["title_templates"])
        title = f"{player.key} {title_template}"
        
        # Select reward
        reward_template = random.choice(templates["rewards"])
        reward = self._generate_reward(reward_template, personality)
        
        # Flavor text
        flavor = random.choice(personality["flavor_text"])
        
        judgment = {
            "event_type": event_type,
            "player": player.key,
            "title": title,
            "description": description,
            "reward": reward,
            "flavor": flavor,
            "personality": personality["title"],
            "timestamp": time.time(),
        }
        
        return judgment
    
    def _generate_reward(self, reward_template, personality):
        """Generate a concrete reward from template."""
        reward_bias = personality["reward_bias"]
        
        reward_type = reward_template["type"]
        
        if reward_type == "exp":
            base = reward_template["base"]
            variance = reward_template["variance"]
            amount = int(base * reward_bias * random.uniform(1 - variance, 1 + variance))
            return {"type": "exp", "amount": amount}
        
        elif reward_type == "gold":
            base = reward_template["base"]
            variance = reward_template["variance"]
            amount = int(base * reward_bias * random.uniform(1 - variance, 1 + variance))
            return {"type": "gold", "amount": amount}
        
        elif reward_type == "stat_boost":
            stat = reward_template["stat"]
            amount = reward_template["amount"]
            return {"type": "stat_boost", "stat": stat, "amount": amount}
        
        elif reward_type == "item":
            tier = reward_template["tier"]
            return {"type": "item", "tier": tier}
        
        elif reward_type == "title":
            tier = reward_template["tier"]
            return {"type": "title", "tier": tier}
        
        elif reward_type == "reputation":
            faction = reward_template["faction"]
            amount = int(reward_template["amount"] * reward_bias)
            return {"type": "reputation", "faction": faction, "amount": amount}
        
        return {"type": "none"}
    
    def _deliver_judgment(self, player, judgment):
        """Deliver the judgment to the player."""
        msg = f"""
|b[Divine Judgment]|n The {judgment['personality']} {judgment['flavor']}...

|wAchievement Unlocked:|n {judgment['title']}
|x{judgment['description']}|n

|yReward:|n {self._format_reward(judgment['reward'])}
        """.strip()
        
        player.msg(msg)
        
        # Apply reward
        self._apply_reward(player, judgment["reward"])
    
    def _format_reward(self, reward):
        """Format reward for display."""
        rtype = reward["type"]
        if rtype == "exp":
            return f"{reward['amount']} experience points"
        elif rtype == "gold":
            return f"{reward['amount']} gold coins"
        elif rtype == "stat_boost":
            return f"+{reward['amount']} {reward['stat']}"
        elif rtype == "item":
            return f"a {reward['tier']} item"
        elif rtype == "title":
            return f"the title '{reward['tier']}'"
        elif rtype == "reputation":
            return f"{reward['amount']} reputation with {reward['faction']}"
        return "mysterious blessing"
    
    def _apply_reward(self, player, reward):
        """Actually apply the reward to the player."""
        rtype = reward["type"]
        
        if rtype == "exp":
            if hasattr(player, "db") and hasattr(player.db, "experience"):
                player.db.experience = player.db.experience + reward["amount"]
        
        elif rtype == "gold":
            if hasattr(player, "db") and hasattr(player.db, "gold"):
                player.db.gold = player.db.gold + reward["amount"]
        
        elif rtype == "stat_boost":
            stat = reward["stat"]
            amount = reward["amount"]
            if hasattr(player, "db") and hasattr(player.db, "stats"):
                if stat in player.db.stats:
                    player.db.stats[stat] += amount
        
        elif rtype == "item":
            # Create a generic item (simplified)
            from evennia import create_object
            item = create_object("typeclasses.objects.Object", 
                                key=f"a {reward['tier']} artifact")
            item.db.desc = f"A {reward['tier']} artifact granted by the divine."
            item.move_to(player, quiet=True)
        
        elif rtype == "title":
            if not hasattr(player.db, "titles"):
                player.db.titles = []
            player.db.titles.append(reward["tier"])
    
    def _log_intervention(self, judgment):
        """Log the intervention."""
        if not self.db.intervention_log:
            self.db.intervention_log = []
        
        self.db.intervention_log.append(judgment)
        
        # Keep log size manageable
        if len(self.db.intervention_log) > 100:
            self.db.intervention_log = self.db.intervention_log[-50:]
    
    # =====================================================================
    # PUBLIC API
    # =====================================================================
    
    def get_current_mood(self):
        """Get current DM mood."""
        return self.db.mood
    
    def get_intervention_log(self, limit=10):
        """Get recent interventions."""
        log = self.db.intervention_log or []
        return log[-limit:]
    
    def force_intervention(self, event_type, player, context):
        """Force an intervention (for admin use)."""
        return self.judge_event(event_type, player, context)
    
    def change_personality(self, personality_key):
        """Manually change personality (for admin use)."""
        if personality_key in AI_DM_PERSONALITIES:
            self.db.personality = personality_key
            self.db.mood = AI_DM_PERSONALITIES[personality_key]["mood"]
            return True
        return False


# =============================================================================
# HOOK FUNCTIONS (called from game code)
# =============================================================================

def get_ai_dm():
    """Get or create the AI DM script."""
    from evennia import search_script
    scripts = search_script("ai_dm")
    
    if scripts:
        return scripts[0]
    
    # Create new script
    from evennia import create_script
    script = create_script("typeclasses.scripts.ai_dm.AIDungeonMaster")
    return script


def notify_creative_solution(player, quest_name, method_description):
    """Call when a player solves a quest creatively."""
    ai_dm = get_ai_dm()
    if ai_dm:
        return ai_dm.judge_event("creative_solution", player, {
            "quest": quest_name,
            "method": method_description,
        })
    return None


def notify_first_discovery(player, location_name):
    """Call when a player discovers something for the first time."""
    ai_dm = get_ai_dm()
    if ai_dm:
        return ai_dm.judge_event("first_discovery", player, {
            "location": location_name,
        })
    return None


def notify_creative_combat(player, enemy_name, tactic_description):
    """Call when a player uses creative combat tactics."""
    ai_dm = get_ai_dm()
    if ai_dm:
        return ai_dm.judge_event("creative_combat", player, {
            "enemy": enemy_name,
            "tactic": tactic_description,
        })
    return None


def notify_social_mastery(player, npc_name):
    """Call when a player achieves something through social means."""
    ai_dm = get_ai_dm()
    if ai_dm:
        return ai_dm.judge_event("social_mastery", player, {
            "npc": npc_name,
        })
    return None


def notify_easter_egg(player, discovery_description):
    """Call when a player finds an easter egg."""
    ai_dm = get_ai_dm()
    if ai_dm:
        return ai_dm.judge_event("easter_egg", player, {
            "discovery": discovery_description,
        })
    return None


import time
