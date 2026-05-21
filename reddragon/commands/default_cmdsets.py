"""
Darkstaff MUD - Default Command Sets
"""

from evennia.commands.cmdset import CmdSet
from evennia.commands.default import unloggedin, account
from commands import unloggedin as custom_unloggedin

class UnloggedinCmdSet(CmdSet):
    """
    Command set for unlogged-in users.
    IOM-style login menu: [n] Name, [p] Password, [c] Create, [w] Who, [s] Status, [d] Disconnect
    """
    key = "DefaultUnloggedin"
    priority = 0

    def at_cmdset_creation(self):
        "Populate the cmdset with IOM-style commands"
        # IOM single-letter commands
        self.add(custom_unloggedin.CmdUnconnectedName())
        self.add(custom_unloggedin.CmdUnconnectedPassword())
        self.add(custom_unloggedin.CmdUnconnectedWho())
        self.add(custom_unloggedin.CmdUnconnectedStatus())
        self.add(custom_unloggedin.CmdUnconnectedDisconnect())
        self.add(custom_unloggedin.CmdUnconnectedCreateChar())
        # Also keep standard Evennia commands as fallbacks
        self.add(unloggedin.CmdUnconnectedConnect())
        self.add(unloggedin.CmdUnconnectedCreate())
        self.add(unloggedin.CmdUnconnectedQuit())
        self.add(unloggedin.CmdUnconnectedLook())
        self.add(unloggedin.CmdUnconnectedHelp())
        self.add(unloggedin.CmdUnconnectedEncoding())
        self.add(unloggedin.CmdUnconnectedScreenreader())
        self.add(unloggedin.CmdUnconnectedInfo())

class SessionCmdSet(CmdSet):
    """
    Session-level command set.
    """
    key = "DefaultSession"
    priority = -20

    def at_cmdset_creation(self):
        "Populate the cmdset"
        self.add(account.CmdSessions())
