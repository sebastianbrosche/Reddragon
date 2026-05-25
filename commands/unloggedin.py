"""
Red Dragon Reborn - Unlogged-in Command Set
Uses Evennia's native login commands with IOM-style presentation.
"""

# Connection screen displayed to unlogged-in users
CONNECTION_SCREEN = """
|b___________________________________________________________________________|n
|y
                     R E D   D R A G O N   R E B O R N
|n
|b___________________________________________________________________________|n
|g
   The original 1995 MUD, reborn. Enter a world of adventure where
   heroes are forged in battle and legends are written in blood.

   |yNEW PLAYER?|n  Type |wcreate <name> <password>|n to make an account.
   |yRETURNING?|n   Type |wconnect <name> <password>|n to enter the realm.

   Type |whelp|n for more information.
|n
|b___________________________________________________________________________|n
"""

from evennia import Command, CmdSet
from evennia.commands.default.unloggedin import (
    CmdUnconnectedConnect,
    CmdUnconnectedCreate,
    CmdUnconnectedQuit,
    CmdUnconnectedLook,
    CmdUnconnectedHelp,
)
from evennia.server.sessionhandler import SESSIONS
from evennia.utils import logger

# ---------------------------------------------------------------------------
# Evennia Native Login Commands (no password restrictions)
# ---------------------------------------------------------------------------

class CmdConnect(CmdUnconnectedConnect):
    """
    Connect to an existing account.
    
    Usage:
        connect <name> <password>
    """
    key = "connect"
    aliases = ["conn", "con"]
    # Use Evennia's native func() - no override


class CmdCreate(CmdUnconnectedCreate):
    """
    Create a new account.
    
    Usage:
        create <name> <password>
    
    No password restrictions - any length is accepted.
    """
    key = "create"
    aliases = ["cre", "new"]
    # Use Evennia's native func() - password validators already disabled in settings.py


class CmdQuit(CmdUnconnectedQuit):
    """Quit the connection."""
    key = "quit"
    aliases = ["q", "disconnect", "dc"]


class CmdHelp(CmdUnconnectedHelp):
    """Get help."""
    key = "help"
    aliases = ["h", "?"]


# ---------------------------------------------------------------------------
# IOM-style Who List (unlogged-in)
# ---------------------------------------------------------------------------

class CmdWhoUnlogged(Command):
    """
    Show who is online.

    Usage:
        who
        w
    """
    key = "who"
    aliases = ["w"]
    locks = "cmd:all()"

    def func(self):
        session = self.caller
        sessions = SESSIONS.get_sessions()

        count = len(sessions)
        if count == 0:
            session.msg("|yNo players are currently online.|n")
            return

        lines = []
        lines.append("|b___________________________________________________________________________|n")
        lines.append("|b  Who is online|n")
        lines.append("|b___________________________________________________________________________|n")

        # Categorize
        gods = []
        wizards = []
        mortals = []

        for sess in sessions:
            if not sess.account:
                continue

            account = sess.account
            pup = sess.puppet

            # Check permissions
            if account.check_permstring("Immortals") or account.check_permstring("Wizards"):
                if account.check_permstring("Immortals"):
                    gods.append(account)
                else:
                    wizards.append(account)
            else:
                mortals.append((account, pup))

        # Show gods
        if gods:
            lines.append("|cGods Online:|n")
            for god in gods:
                lines.append(f"  |c{god.username}|n")

        # Show wizards
        if wizards:
            lines.append("|yWizards Online:|n")
            for wiz in wizards:
                lines.append(f"  |y{wiz.username}|n")

        # Show mortals
        if mortals:
            lines.append("")
            lines.append(f"|gMortals Online ({len(mortals)}):|n")
            for account, pup in mortals:
                name = account.username
                if pup and pup.db.level:
                    lines.append(f"  |g{name}|n (Level {pup.db.level})")
                else:
                    lines.append(f"  |g{name}|n")

        lines.append("|b___________________________________________________________________________|n")
        lines.append(f"|b  {count} players online|n")
        lines.append("|b___________________________________________________________________________|n")

        session.msg("\n".join(lines))


# ---------------------------------------------------------------------------
# Server Status
# ---------------------------------------------------------------------------

class CmdServerStatusUnlogged(Command):
    """
    Show server status.

    Usage:
        status
        s
    """
    key = "status"
    aliases = ["s", "stat"]
    locks = "cmd:all()"

    def func(self):
        session = self.caller

        import datetime
        from evennia import SERVER_START_TIME

        now = datetime.datetime.now()
        uptime = now - SERVER_START_TIME if SERVER_START_TIME else datetime.timedelta(0)

        lines = []
        lines.append("|b___________________________________________________________________________|n")
        lines.append("|b  Server Status|n")
        lines.append("|b___________________________________________________________________________|n")
        lines.append(f"  Server Time: {now.strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"  Uptime: {str(uptime).split('.')[0]}")

        # Count online
        sessions = SESSIONS.get_sessions()
        lines.append(f"  Players Online: {len(sessions)}")

        # Count accounts
        total_accounts = AccountDB.objects.count()
        lines.append(f"  Total Accounts: {total_accounts}")

        lines.append("|b___________________________________________________________________________|n")

        session.msg("\n".join(lines))


# ---------------------------------------------------------------------------
# Command Set
# ---------------------------------------------------------------------------

class UnloggedinCmdSet(CmdSet):
    """Command set for unlogged-in players. Uses Evennia's native login."""

    key = "Unloggedin"
    priority = 0

    def at_cmdset_creation(self):
        self.add(CmdConnect)
        self.add(CmdCreate)
        self.add(CmdQuit)
        self.add(CmdUnconnectedLook)
        self.add(CmdHelp)
        self.add(CmdWhoUnlogged)
        self.add(CmdServerStatusUnlogged)
