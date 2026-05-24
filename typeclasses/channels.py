"""
Red Dragon MUD - Channel Typeclass
Based on Islands of Myth communication channels
"""

from evennia import DefaultChannel

class Channel(DefaultChannel):
    """
    Custom channel typeclass for Red Dragon MUD.
    
    IOM has multiple channels:
    - chat (general chat)
    - tell (private messaging)
    - newbie (help channel)
    - guild (guild-specific)
    - auction (trading)
    """
    
    def at_channel_creation(self):
        super().at_channel_creation()
        self.db.channel_type = "general"
        self.db.color_code = "|w"  # White default
        self.db.log_messages = True
        
    def channel_prefix(self, msg, emit=False):
        """Add channel prefix to messages."""
        if emit:
            return f"[{self.key}] {msg}"
        return f"[{self.key}] {msg}"
        
    def format_message(self, msg, sender, emit=False):
        """Format a channel message."""
        if emit:
            return f"[{self.key}] {msg}"
        return f"[{self.key}] {sender.key}: {msg}"
