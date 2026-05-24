"""
Version and Chat Commands for Red Dragon MUD
"""

from evennia import Command, create_channel
from evennia.comms.models import ChannelDB
from evennia.utils import search

# Version info
VERSION = {
    "name": "Red Dragon MUD",
    "version": "0.4.0",
    "build": "2026-05-24",
    "features": [
        "Ilium City - Full grid with 30+ rooms",
        "AI Dungeon Master - Dynamic personality referee",
        "27 Playable Races with stat blocks",
        "Combat System - Round-based automatic combat",
        "Guild System - Warrior skills & leveling",
        "Dynamic Achievements - AI-generated rewards",
        "Chat Channel - Global player communication",
    ],
}


class CmdVersion(Command):
    """
    Show the current MUD version and features.
    
    Usage:
        version
        ver
    """
    
    key = "version"
    aliases = ["ver", "mud version"]
    locks = "cmd:all()"
    help_category = "General"
    
    def func(self):
        msg = f"""
|b[{VERSION['name']}]|n
Version: |y{VERSION['version']}|n
Build Date: |y{VERSION['build']}|n

|bActive Features:|n
""".strip()
        
        for i, feature in enumerate(VERSION['features'], 1):
            msg += f"\n  {i}. {feature}"
        
        msg += "\n\nType |whelp|n for command list."
        
        self.caller.msg(msg)


# =============================================================================
# CHAT CHANNEL
# =============================================================================

class CmdChat(Command):
    """
    Send a message to the global chat channel.
    
    Usage:
        chat <message>
        
    Example:
        chat Hello everyone!
    """
    
    key = "chat"
    locks = "cmd:all()"
    help_category = "Communication"
    
    def func(self):
        if not self.args.strip():
            self.caller.msg("Usage: chat <message>")
            return
        
        # Check if player has chat enabled
        if hasattr(self.caller.db, 'chat_enabled') and not self.caller.db.chat_enabled:
            self.caller.msg("You have chat disabled. Type 'on chat' to enable.")
            return
        
        # Get or create the chat channel
        channel = self._get_chat_channel()
        if not channel:
            self.caller.msg("Chat channel is not available.")
            return
        
        message = self.args.strip()
        
        # Send to channel
        channel.msg(f"|y[{self.caller.key}]|n {message}")
        
        # Also notify the sender
        self.caller.msg(f"|y[You]|n {message}")
    
    def _get_chat_channel(self):
        """Get or create the global chat channel."""
        channels = search.search_channel("Chat")
        if channels:
            return channels[0]
        
        # Create new channel
        channel = create_channel("Chat", 
                                desc="Global player chat",
                                locks="listen:all();send:all()")
        return channel


class CmdToggleChat(Command):
    """
    Toggle chat channel on or off.
    
    Usage:
        on chat    - Enable chat
        off chat   - Disable chat
    """
    
    key = "on chat"
    aliases = ["off chat"]
    locks = "cmd:all()"
    help_category = "Communication"
    
    def func(self):
        if not hasattr(self.caller.db, 'chat_enabled'):
            self.caller.db.chat_enabled = True
        
        is_on = self.cmdstring == "on chat"
        self.caller.db.chat_enabled = is_on
        
        if is_on:
            self.caller.msg("|gChat enabled.|n You will now see chat messages.")
        else:
            self.caller.msg("|rChat disabled.|n You will no longer see chat messages.")


# =============================================================================
# COMMAND SET
# =============================================================================

from evennia import CmdSet

class UtilityCmdSet(CmdSet):
    """Command set for version, chat, and utility commands."""
    
    key = "UtilityCmdSet"
    
    def at_cmdset_creation(self):
        self.add(CmdVersion)
        self.add(CmdChat)
        self.add(CmdToggleChat)
