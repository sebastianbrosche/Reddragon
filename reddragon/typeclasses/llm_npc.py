"""
Red Dragon MUD - LLM NPC Support
Integration with Evennia's LLM NPC contrib for AI-driven conversations
"""

from evennia.contrib.rpg.llm.llm_npc import LLMNPC as BaseLLMNPC

class LLMNPC(BaseLLMNPC):
    """
    An NPC that uses a Large Language Model to generate responses.
    
    Requires LLM server endpoint configuration in settings:
    LLM_SERVER_API_URL = "https://api.openai.com/v1/chat/completions"
    LLM_SERVER_API_KEY = "your-api-key"
    LLM_PROMPT_PREFIX = "You are roleplaying as {name}..."
    
    Usage:
        talk npc "Hello there"
    """
    
    def at_object_creation(self):
        super().at_object_creation()
        self.db.is_npc = True
        self.db.is_mob = False
        self.db.level = 1
        self.db.hp = 100
        self.db.max_hp = 100
        self.db.xp = 0
        self.db.gold = 0


class SmartMob(LLMNPC):
    """
    A mob that can fight AND talk using LLM responses.
    Combines combat capabilities with AI-driven dialogue.
    """
    
    def at_object_creation(self):
        super().at_object_creation()
        self.db.is_mob = True
        self.db.is_npc = True
        
    def at_char_entered(self, character):
        """Called when a character enters the room."""
        if self.db.is_aggressive and character.is_pc:
            self.attack(character)
        else:
            # Greet using LLM if not aggressive
            if hasattr(self, 'llm_client'):
                self.build_prompt(character, f"{character.key} has entered the room.")
