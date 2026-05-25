"""
Admin command to build all 195 sub-areas
Usage: @buildsubareas
"""

from evennia import Command
from evennia.utils import logger

class CmdBuildSubAreas(Command):
    """
    Build all island sub-areas from islandsofmyth.org maps

    Usage:
      @buildsubareas

    This creates all 195 sub-areas across 10 islands and connects them
    to their island hubs with proper ferry connections.
    """

    key = "@buildsubareas"
    locks = "cmd:perm(Developer)"
    help_category = "Admin"

    def func(self):
        self.caller.msg("Starting sub-area construction...")
        
        try:
            from world.build_subareas import build_all
            build_all()
            self.caller.msg("|gSub-area construction complete!|n")
            self.caller.msg("Type 'look' to see the world around you.")
        except Exception as e:
            self.caller.msg(f"|rError during construction: {e}|n")
            logger.log_err(f"Sub-area build failed: {e}")
