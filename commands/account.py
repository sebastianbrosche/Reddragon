"""
Darkstaff MUD - Account Commands

Commands for account-level operations (login, register, etc.).
"""

from evennia import Command, CmdSet

class AccountCmdSet(CmdSet):
    """
    Account-level commands.
    """
    key = "account"
    
    def at_cmdset_creation(self):
        pass  # Account commands are handled by Evennia's default system
