"""
Commands for interacting with the AI Dungeon Master
"""

from evennia import Command
from typeclasses.scripts.ai_dm import get_ai_dm


class CmdDivineStatus(Command):
    """
    Check the current divine presence and mood
    
    Usage:
        divine status
        gods mood
    """
    
    key = "divine status"
    aliases = ["gods mood", "divine mood", "dm status"]
    locks = "cmd:all()"
    help_category = "Divine"
    
    def func(self):
        ai_dm = get_ai_dm()
        if not ai_dm:
            self.caller.msg("No divine presence detected.")
            return
        
        personality = ai_dm.get_personality()
        
        msg = f"""
|b[Divine Presence]|n

Current Aspect: |y{personality['title']}|n
Mood: |w{ai_dm.db.mood}|n
Bias: {'Generous' if personality['reward_bias'] > 1.0 else 'Stingy' if personality['reward_bias'] < 1.0 else 'Balanced'}
        """.strip()
        
        self.caller.msg(msg)


class CmdPray(Command):
    """
    Pray to the AI Dungeon Master
    
    Usage:
        pray [message]
        
    Example:
        pray please bless my journey
    """
    
    key = "pray"
    locks = "cmd:all()"
    help_category = "Divine"
    
    def func(self):
        ai_dm = get_ai_dm()
        if not ai_dm:
            self.caller.msg("Your prayers echo in an empty void.")
            return
        
        prayer = self.args.strip()
        
        if not prayer:
            self.caller.msg("You kneel in silent prayer...")
            # Small chance of random response
            import random
            if random.random() < 0.3:
                personality = ai_dm.get_personality()
                responses = [
                    f"The {personality['title']} seems to notice your silence.",
                    "A distant rumble suggests something heard you.",
                    "The world holds its breath for a moment.",
                ]
                self.caller.msg(f"|b[Divine Whisper]|n {random.choice(responses)}")
            return
        
        # Log the prayer
        self.caller.msg(f"You pray: '{prayer}'")
        
        # Small chance of divine response to specific prayers
        import random
        if random.random() < 0.1:
            personality = ai_dm.get_personality()
            self.caller.msg(f"|b[Divine Whisper]|n The {personality['title']} heard your words...")


class CmdAchievements(Command):
    """
    View your divine achievements
    
    Usage:
        achievements
        divine achievements
    """
    
    key = "achievements"
    aliases = ["divine achievements", "my achievements"]
    locks = "cmd:all()"
    help_category = "Divine"
    
    def func(self):
        if not hasattr(self.caller.db, "titles") or not self.caller.db.titles:
            self.caller.msg("You have no divine achievements yet.")
            return
        
        msg = "|b[Your Divine Titles]|n\n\n"
        for title in self.caller.db.titles:
            msg += f"  |y{title}|n\n"
        
        self.caller.msg(msg)


class CmdDivineLog(Command):
    """
    View recent divine interventions (admin only)
    
    Usage:
        divine log [number]
    """
    
    key = "divine log"
    locks = "cmd:perm(Admin)"
    help_category = "Admin"
    
    def func(self):
        ai_dm = get_ai_dm()
        if not ai_dm:
            self.caller.msg("No AI DM active.")
            return
        
        limit = 10
        if self.args.strip().isdigit():
            limit = int(self.args.strip())
        
        log = ai_dm.get_intervention_log(limit)
        
        if not log:
            self.caller.msg("No divine interventions recorded yet.")
            return
        
        msg = f"|b[Divine Intervention Log - Last {len(log)}]|n\n\n"
        
        for entry in log:
            msg += f"  |y{entry['player']}|n - {entry['title']}\n"
            msg += f"  {entry['description'][:60]}...\n"
            msg += f"  Reward: {entry['reward']['type']} | Personality: {entry['personality']}\n\n"
        
        self.caller.msg(msg)


class CmdForceDivine(Command):
    """
    Force a divine intervention (admin only)
    
    Usage:
        divine force <player> <event_type>
        
    Event types:
        creative_solution, first_discovery, creative_combat,
        social_mastery, easter_egg
    """
    
    key = "divine force"
    locks = "cmd:perm(Admin)"
    help_category = "Admin"
    
    def func(self):
        if not self.args:
            self.caller.msg("Usage: divine force <player> <event_type>")
            return
        
        parts = self.args.split()
        if len(parts) < 2:
            self.caller.msg("Usage: divine force <player> <event_type>")
            return
        
        player_name = parts[0]
        event_type = parts[1]
        
        # Find player
        from evennia import search_object
        players = search_object(player_name, typeclass="typeclasses.characters.Character")
        
        if not players:
            self.caller.msg(f"Player '{player_name}' not found.")
            return
        
        player = players[0]
        
        ai_dm = get_ai_dm()
        if not ai_dm:
            self.caller.msg("No AI DM active.")
            return
        
        context = {
            "quest": "admin-triggered",
            "location": "admin-triggered",
            "enemy": "admin-triggered",
            "npc": "admin-triggered",
            "discovery": "admin-triggered",
        }
        
        judgment = ai_dm.force_intervention(event_type, player, context)
        
        if judgment:
            self.caller.msg(f"Divine intervention triggered for {player_name}.")
        else:
            self.caller.msg("The divine chose not to intervene.")


class CmdSetDivinePersonality(Command):
    """
    Manually set the AI DM personality (admin only)
    
    Usage:
        divine personality <type>
        
    Types: benevolent, malevolent, chaotic, lawful, trickster, doomsayer
    """
    
    key = "divine personality"
    locks = "cmd:perm(Admin)"
    help_category = "Admin"
    
    def func(self):
        if not self.args:
            self.caller.msg("Usage: divine personality <type>")
            return
        
        personality = self.args.strip().lower()
        
        ai_dm = get_ai_dm()
        if not ai_dm:
            self.caller.msg("No AI DM active.")
            return
        
        if ai_dm.change_personality(personality):
            self.caller.msg(f"AI DM personality changed to: {personality}")
        else:
            self.caller.msg(f"Invalid personality: {personality}")


# =============================================================================
# COMMAND SET
# =============================================================================

from evennia import CmdSet

class DivineCmdSet(CmdSet):
    """Command set for divine/AI DM commands."""
    
    key = "DivineCmdSet"
    
    def at_cmdset_creation(self):
        self.add(CmdDivineStatus)
        self.add(CmdPray)
        self.add(CmdAchievements)
        self.add(CmdDivineLog)
        self.add(CmdForceDivine)
        self.add(CmdSetDivinePersonality)
