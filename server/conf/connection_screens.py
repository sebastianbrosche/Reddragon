"""
Red Dragon Reborn - Connection Screen

This is the screen shown to players when they first connect.
Only DEFAULT_CONNECTION_SCREEN should be a top-level string in this module
so Evennia's random_string_from_module picks the right one.
"""

from django.conf import settings
from evennia.utils.utils import get_evennia_version

def _get_menu_screen():
    """IOM-style login menu."""
    return """
|b___________________________________________________________________________|n
|b|n
|b  Welcome to Red Dragon Reborn|n
|b___________________________________________________________________________|n
|n
  [n] - Enter your name to log in
  [c] - Create a new character
  [w] - See who is currently playing
  [s] - Server status
  [d] - Disconnect

|b___________________________________________________________________________|n
|n
"""

def _get_character_select_screen():
    """Screen shown after login but before character selection."""
    return """
|b___________________________________________________________________________|n
|b|n
|b  Character Selection|n
|b___________________________________________________________________________|n
|n
  Select a character or create a new one:

"""

def _get_new_player_screen():
    """Screen shown to new players before character creation."""
    return """
|b___________________________________________________________________________|n
|b|n
|b  Welcome, Adventurer!|n
|b___________________________________________________________________________|n
|n
  You are about to enter the world of Red Dragon Reborn, a realm of magic,
  monsters, and mystery. Choose your race wisely, for it will shape
  your destiny.

  Available races range from the common Human to the exotic Xorn.
  Each has unique strengths, weaknesses, and abilities.

|b___________________________________________________________________________|n
|n
"""

def _get_ascii_header():
    """ASCII art header for the main connection screen."""
    return """|b___________________________________________________________________________|n
|b|n
|b  _____             _               _   _                 _|n
|b |  __ \\           | |             | | | |               | ||n
|b | |  | | __ _ _ __| | _____  _   _| |_| |__   __ _ _ __ | |__   ___ _ __|n
|b | |  | |/ _` | '__| |/ / _ \\| | | | __| '_ \\ / _` | '_ \\| '_ \\ / _ \\ '__||n
|b | |__| | (_| | |  |   <  __/| |_| | |_| | | | (_| | | | | | | |  __/ |   |n
|b |_____/ \\__,_|_|  |_|\\_\\___| \\__, |\\__|_| |_|\\__,_|_| |_|_| |_|\\___|_|   |n
|b                               __/ |                                      |n
|b                              |___/                                       |n
|b___________________________________________________________________________|n|n"""

def _get_online_count():
    """Count online players."""
    try:
        from evennia.server.sessionhandler import SESSIONS
        nplayers = SESSIONS.account_count()
    except (ImportError, AttributeError):
        nplayers = 0
    if nplayers:
        return f"|y  Players currently online: {nplayers}|n"
    return "|y  No players currently online.|n"

# This is the ONLY top-level string in this module so Evennia picks it correctly
DEFAULT_CONNECTION_SCREEN = _get_ascii_header() + "|g  Based on the classic 1995 MUD \"Red Dragon\" - now reborn|n\n|g  A heavily modified LIMA mudlib running on Evennia (Python)|n\n|b___________________________________________________________________________|n|n" + _get_online_count() + "|b___________________________________________________________________________|n|n"
