"""
Darkstaff MUD - IOM-Style Unloggedin Commands

Custom login commands matching Islands of Myth menu style:
[n] Enter name, [c] Create character, [w] Who, [s] Status, [d] Disconnect
"""

from evennia.commands.default import unloggedin
from evennia.commands.command import Command

class CmdUnconnectedName(Command):
    """
    Enter your account name to begin login.
    
    Usage:
      n <accountname>
      name <accountname>
    """
    key = "n"
    aliases = ["name"]
    locks = "cmd:all()"
    arg_regex = r".+"

    def func(self):
        "Handle the command"
        if not self.args:
            self.msg("Usage: n <accountname>")
            return
        # Pass through to the connect command with just the name
        self.caller.msg("Enter your password:")
        # Store the name for the next step
        self.caller.ndb.login_name = self.args.strip()

class CmdUnconnectedPassword(Command):
    """
    Enter your password to complete login.
    
    Usage:
      p <password>
      password <password>
    """
    key = "p"
    aliases = ["password"]
    locks = "cmd:all()"
    arg_regex = r".+"

    def func(self):
        "Handle the command"
        if not hasattr(self.caller.ndb, 'login_name') or not self.caller.ndb.login_name:
            self.msg("Please enter your name first (n <name>).")
            return
        if not self.args:
            self.msg("Usage: p <password>")
            return
        # Call the connect command with name and password
        name = self.caller.ndb.login_name
        password = self.args.strip()
        # Use Evennia's connect command logic
        cmd = unloggedin.CmdUnconnectedConnect()
        cmd.caller = self.caller
        cmd.args = f"{name} {password}"
        cmd.session = self.session
        cmd.func()

class CmdUnconnectedWho(Command):
    """
    See who is currently playing.
    
    Usage:
      w
      who
    """
    key = "w"
    aliases = ["who"]
    locks = "cmd:all()"

    def func(self):
        "Show who is online"
        cmd = unloggedin.CmdUnconnectedInfo()
        cmd.caller = self.caller
        cmd.args = ""
        cmd.session = self.session
        cmd.func()

class CmdUnconnectedStatus(Command):
    """
    Show server status.
    
    Usage:
      s
      status
    """
    key = "s"
    aliases = ["status"]
    locks = "cmd:all()"

    def func(self):
        "Show server status"
        from django.conf import settings
        from evennia import get_evennia_version
        from evennia.server.sessionhandler import SESSION_HANDLER
        
        nplayers = len(SESSION_HANDLER.get_logged_in_accounts())
        
        self.msg(f"|bServer Status|n")
        self.msg(f"  Server: {settings.SERVERNAME}")
        self.msg(f"  Version: Evennia {get_evennia_version()}")
        self.msg(f"  Players online: {nplayers}")
        self.msg(f"  Telnet port: {settings.TELNET_PORTS[0] if settings.TELNET_ENABLED else 'Disabled'}")

class CmdUnconnectedDisconnect(Command):
    """
    Disconnect from the server.
    
    Usage:
      d
      disconnect
      quit
      q
    """
    key = "d"
    aliases = ["disconnect", "quit", "q"]
    locks = "cmd:all()"

    def func(self):
        "Disconnect the session"
        self.msg("Goodbye! Come back soon, adventurer.")
        self.session.disconnect()

class CmdUnconnectedCreateChar(Command):
    """
    Create a new character.
    
    Usage:
      c <accountname> <password>
      create <accountname> <password>
    """
    key = "c"
    aliases = ["create"]
    locks = "cmd:all()"
    arg_regex = r".+"

    def func(self):
        "Handle character creation"
        if not self.args:
            self.msg("Usage: c <accountname> <password>")
            return
        cmd = unloggedin.CmdUnconnectedCreate()
        cmd.caller = self.caller
        cmd.args = self.args
        cmd.session = self.session
        cmd.func()
