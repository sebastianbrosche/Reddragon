"""
Darkstaff MUD - Command Parser
"""

def cmdparser(raw_string, cmdset, session, player):
    """
    Parse a command string.
    
    Args:
        raw_string: The raw command string
        cmdset: The current command set
        session: The current session
        player: The current player
        
    Returns:
        list: List of matching commands
    """
    return cmdset.match(raw_string, session, player)
