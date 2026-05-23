"""
Darkstaff MUD - Custom Unlogged-in Login Flow

Simple IOM-style login:
  - Type your name → password prompt → login
  - Type 'c' → create new character
  - Type 'w' → who list
  - Type 's' → server status  
  - Type 'd' → disconnect
"""

from evennia import Command, CmdSet
from evennia.accounts.models import AccountDB
from evennia.objects.models import ObjectDB
from evennia.server.sessionhandler import SESSIONS
from evennia.utils import class_from_module, create, logger
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
import re

# ---------------------------------------------------------------------------
# Login state manager (stored on session)
# ---------------------------------------------------------------------------

class LoginState:
    """Track where a player is in the login flow."""
    def __init__(self, session):
        self.session = session
        if not hasattr(session.db, "_login_state"):
            session.db._login_state = {}
        self.state = session.db._login_state
    
    def get(self, key, default=None):
        return self.state.get(key, default)
    
    def set(self, key, value):
        self.state[key] = value
        self.session.db._login_state = self.state
    
    def clear(self):
        self.state = {}
        self.session.db._login_state = {}

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def _validate_name(name):
    """Check if name is valid for use."""
    if not name or len(name) < 2:
        return False, "Name must be at least 2 characters long."
    if len(name) > 30:
        return False, "Name must be less than 30 characters."
    if not re.match(r"^[A-Za-z][A-Za-z0-9_-]*$", name):
        return False, "Name must start with a letter and contain only letters, numbers, underscores, and hyphens."
    # Check if name exists as account or character
    if AccountDB.objects.filter(username__iexact=name).exists():
        return False, "That name is already taken."
    if ObjectDB.objects.filter(db_typeclass_path=settings.BASE_CHARACTER_TYPECLASS, db_key__iexact=name).exists():
        return False, "That name is already taken."
    return True, None


def _who_list(session):
    """Show who is online."""
    sessions = SESSIONS.get_sessions()
    count = len(sessions)
    if count == 0:
        session.msg("|yNo players are currently online.|n")
        return
    
    lines = ["|b___________________________________________________________________________|n"]
    lines.append("|b  Who is online|n")
    lines.append("|b___________________________________________________________________________|n")
    
    for sess in sessions:
        if sess.account:
            name = sess.account.username
            pup = sess.puppet
            loc = pup.location.key if pup and pup.location else "Unknown"
            lines.append(f"  |c{name}|n - {loc}")
        else:
            lines.append("  |x(connecting...)|n")
    
    lines.append("|b___________________________________________________________________________|n")
    session.msg("\n".join(lines))


def _server_status(session):
    """Show server status."""
    from evennia.server.server import EVENNIA
    lines = [
        "|b___________________________________________________________________________|n",
        "|b  Server Status|n",
        "|b___________________________________________________________________________|n",
        f"  Server name: |c{settings.SERVERNAME}|n",
        f"  Uptime: {EVENNIA.uptime}",
        f"  Players online: {SESSIONS.account_count()}",
        f"  Total accounts: {AccountDB.objects.count()}",
        "|b___________________________________________________________________________|n",
    ]
    session.msg("\n".join(lines))


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

class CmdDisconnect(Command):
    """
    Disconnect from the server.
    Usage: d
    """
    key = "d"
    locks = "cmd:all()"
    
    def func(self):
        self.caller.msg("|gGoodbye!|n")
        self.caller.sessionhandler.disconnect(self.caller)


class CmdWho(Command):
    """
    See who is online.
    Usage: w
    """
    key = "w"
    aliases = ["who"]
    locks = "cmd:all()"
    
    def func(self):
        _who_list(self.caller)


class CmdServerStatus(Command):
    """
    Show server status.
    Usage: s
    """
    key = "s"
    locks = "cmd:all()"
    
    def func(self):
        _server_status(self.caller)


class CmdCreateMenu(Command):
    """
    Start character creation.
    Usage: c
    """
    key = "c"
    locks = "cmd:all()"
    
    def func(self):
        state = LoginState(self.caller)
        state.clear()
        state.set("step", "create_name")
        self.caller.msg("\n|yWhat name would you like for your new character?|n")
        self.caller.msg("|x(Or type 'back' to return to the login screen)|n\n")


class CmdBack(Command):
    """
    Go back to login screen.
    Usage: back
    """
    key = "back"
    locks = "cmd:all()"
    
    def func(self):
        state = LoginState(self.caller)
        state.clear()
        self.caller.msg(_get_login_screen())


class CmdLoginInput(Command):
    """
    Main login handler - catches name input and password input.
    This is the default command that catches anything not matched above.
    """
    key = ""
    aliases = []
    locks = "cmd:all()"
    
    def parse(self):
        self.raw = self.args.strip()
    
    def func(self):
        session = self.caller
        raw = self.raw.strip()
        
        if not raw:
            session.msg("|rPlease enter your name, or type 'c' to create a new character.|n")
            return
        
        state = LoginState(session)
        step = state.get("step")
        
        # ---------------------------------------------------------------
        # Character creation flow
        # ---------------------------------------------------------------
        if step == "create_name":
            if raw.lower() == "back":
                state.clear()
                session.msg(_get_login_screen())
                return
            
            valid, err = _validate_name(raw)
            if not valid:
                session.msg(f"|r{err}|n")
                session.msg("|yWhat name would you like?|n")
                return
            
            state.set("create_name", raw)
            state.set("step", "create_password")
            session.msg(f"\n|yName accepted: |c{raw}|n")
            session.msg("|yChoose a password (min 4 characters):|n")
            return
        
        if step == "create_password":
            if len(raw) < 4:
                session.msg("|rPassword must be at least 4 characters.|n")
                session.msg("|yChoose a password:|n")
                return
            
            state.set("create_password", raw)
            state.set("step", "create_confirm")
            session.msg("|yConfirm your password:|n")
            return
        
        if step == "create_confirm":
            if raw != state.get("create_password"):
                session.msg("|rPasswords do not match. Let's start over.|n")
                state.clear()
                state.set("step", "create_name")
                session.msg("|yWhat name would you like for your new character?|n")
                return
            
            name = state.get("create_name")
            password = raw
            
            # Create account and character
            try:
                _create_account_and_character(session, name, password)
                state.clear()
            except Exception as e:
                logger.log_err(f"Character creation failed: {e}")
                session.msg("|rSomething went wrong creating your character. Please try again.|n")
                state.clear()
                session.msg(_get_login_screen())
            return
        
        if step == "select_char":
            char_ids = state.get("chars", [])
            if raw.lower() == "new":
                state.set("step", "create_name")
                session.msg("|yWhat name would you like for your new character?|n")
                return
            
            try:
                idx = int(raw) - 1
                if 0 <= idx < len(char_ids):
                    char = ObjectDB.objects.get_id(char_ids[idx])
                    account = session.account
                    if account:
                        session.msg(f"\n|gEntering the world as |c{char.key}|n|g...|n\n")
                        account.puppet_object(session, char)
                        state.clear()
                    else:
                        session.msg("|rSession not linked to account. Please log in again.|n")
                        state.clear()
                        session.msg(_get_login_screen())
                else:
                    session.msg(f"|rInvalid selection. Choose 1-{len(char_ids)} or type 'new'.|n")
            except ValueError:
                session.msg("|rPlease enter a number or type 'new'.|n")
            return
        
        # ---------------------------------------------------------------
        # Password entry for existing account
        # ---------------------------------------------------------------
        if step == "password":
            name = state.get("login_name")
            try:
                account = AccountDB.objects.get(username__iexact=name)
                if account.check_password(raw):
                    # Success - login
                    session.sessionhandler.login(session, account)
                    state.clear()
                    # After login, show character selection or enter world
                    _post_login(session, account)
                else:
                    session.msg("|rIncorrect password.|n")
                    session.msg("|yPassword:|n")
            except ObjectDoesNotExist:
                session.msg("|rAccount no longer exists.|n")
                state.clear()
                session.msg(_get_login_screen())
            return
        
        # ---------------------------------------------------------------
        # New name entered - check if exists
        # ---------------------------------------------------------------
        if not step:
            # Check if it's an existing account name
            try:
                account = AccountDB.objects.get(username__iexact=raw)
                # Found - ask for password
                state.set("login_name", raw)
                state.set("step", "password")
                session.msg(f"\n|yWelcome back, |c{account.username}|n|y!|n")
                session.msg("|yEnter your password:|n")
                return
            except ObjectDoesNotExist:
                pass
            
            # Check if it's a character name attached to an account
            try:
                char = ObjectDB.objects.get(
                    db_typeclass_path=settings.BASE_CHARACTER_TYPECLASS,
                    db_key__iexact=raw
                )
                if char.account:
                    state.set("login_name", char.account.username)
                    state.set("step", "password")
                    session.msg(f"\n|yWelcome back, |c{char.key}|n|y!|n")
                    session.msg(f"|y(Account: |c{char.account.username}|n|y)|n")
                    session.msg("|yEnter your password:|n")
                    return
            except ObjectDoesNotExist:
                pass
            
            # Name not found - ask if they want to create
            session.msg(f"\n|yThe name '|c{raw}|n|y' was not found.|n")
            session.msg("|yWould you like to create a new character? |n[|gy|n/|rn|n]")
            state.set("pending_name", raw)
            state.set("step", "confirm_create")
            return
        
        # ---------------------------------------------------------------
        # Confirm create from name entry
        # ---------------------------------------------------------------
        if step == "confirm_create":
            if raw.lower() in ("y", "yes"):
                name = state.get("pending_name")
                valid, err = _validate_name(name)
                if not valid:
                    session.msg(f"|r{err}|n")
                    state.clear()
                    session.msg(_get_login_screen())
                    return
                
                state.set("create_name", name)
                state.set("step", "create_password")
                session.msg(f"\n|yCreating character: |c{name}|n")
                session.msg("|yChoose a password (min 4 characters):|n")
            elif raw.lower() in ("n", "no"):
                state.clear()
                session.msg(_get_login_screen())
            else:
                session.msg("|yPlease answer |gy|n|y or |rn|n")
            return


def _create_account_and_character(session, name, password):
    """Create a new account and character."""
    from evennia.utils.utils import callables_from_module
    
    # Create account
    account, errors = AccountDB.objects.create_account(
        username=name,
        email=None,
        password=password,
        typeclass=settings.BASE_ACCOUNT_TYPECLASS,
    )
    if errors:
        raise Exception(f"Account creation failed: {errors}")
    
    # Create character
    char_typeclass = class_from_module(settings.BASE_CHARACTER_TYPECLASS)
    start_loc = ObjectDB.objects.get_id(settings.START_LOCATION)
    default_home = ObjectDB.objects.get_id(settings.DEFAULT_HOME)
    
    character = create.create_object(
        char_typeclass,
        key=name,
        location=start_loc,
        home=default_home,
        permissions=["Player"],
    )
    character.db.race = "Human"
    character.db.level = 1
    character.db.xp = 0
    character.db.gold = 0
    
    # Link character to account
    account.db._playable_characters = [character]
    
    # Login
    session.sessionhandler.login(session, account)
    
    # Enter world
    session.msg("\n|gCharacter created successfully!|n")
    session.msg(f"|gWelcome to Darkstaff MUD, |c{name}|n|g!|n\n")
    
    # Show new player screen
    session.msg(_get_new_player_screen())
    
    # Puppet the character
    account.puppet_object(session, character)


def _post_login(session, account):
    """Handle post-login character selection / entry."""
    chars = list(account.db._playable_characters or [])
    if not chars:
        # No characters - need to create one
        session.msg("\n|yYou have no characters. Let's create one!|n")
        state = LoginState(session)
        state.set("step", "create_name")
        session.msg("|yWhat name would you like?|n")
        return
    
    if len(chars) == 1:
        # Only one character - enter world directly
        char = chars[0]
        session.msg(f"\n|gEntering the world as |c{char.key}|n|g...|n\n")
        account.puppet_object(session, char)
    else:
        # Multiple characters - show selection
        lines = [
            "\n|b___________________________________________________________________________|n",
            "|b  Select a character:|n",
            "|b___________________________________________________________________________|n",
        ]
        for i, char in enumerate(chars, 1):
            lines.append(f"  |c{i}|n - {char.key} (Lv{char.db.level or 1} {char.db.race or 'Unknown'})")
        lines.append("|b___________________________________________________________________________|n")
        lines.append("|yType the number to select, or 'new' to create a new character.|n")
        session.msg("\n".join(lines))
        
        state = LoginState(session)
        state.set("step", "select_char")
        state.set("chars", [c.id for c in chars])


# ---------------------------------------------------------------------------
# Screen text
# ---------------------------------------------------------------------------

def _get_login_screen():
    """Return the main login screen."""
    from evennia.utils.utils import get_evennia_version
    try:
        nplayers = SESSIONS.account_count()
        online_text = f"|y  Players currently online: {nplayers}|n" if nplayers else "|y  No players currently online.|n"
    except:
        online_text = ""
    
    return f"""
|b___________________________________________________________________________|n
|b|n
|b  _____             _               _   _                 _|n
|b |  __ \\           | |             | | | |               | ||n
|b | |  | | __ _ _ __| | _____  _   _| |_| |__   __ _ _ __ | |__   ___ _ __|n
|b | |  | |/ _` | '__| |/ / _ \\| | | | __| '_ \\ / _` | '_ \\| '_ \\ / _ \\ '__||n
|b | |__| | (_| | |  |   <  __/| |_| | |_| | | | (_| | | | | | | |  __/ |   |n
|b |_____/ \\__,_|_|  |_|\\_\\___| \\__, |\\__|_| |_|\\__,_|_| |_|_| |_|\\___|_|   |n
|b                               __/ |                                      |n
|b                              |___/                                       |n
|b___________________________________________________________________________|n|n
|g  Based on the classic 1995 MUD "Red Dragon" - now reborn as Darkstaff|n
|g  A heavily modified LIMA mudlib running on Evennia (Python)|n
|b___________________________________________________________________________|n|n
  [|gn|n] - Enter your name to log in
  [|gc|n] - Create a new character
  [|gw|n] - See who is currently playing
  [|gs|n] - Server status
  [|gd|n] - Disconnect

{online_text}
|b___________________________________________________________________________|n|n
"""


def _get_new_player_screen():
    """Screen shown to new players after creation."""
    return """
|b___________________________________________________________________________|n
|b|n
|b  Welcome, Adventurer!|n
|b___________________________________________________________________________|n|n
  You are about to enter the world of Darkstaff, a realm of magic,
  monsters, and mystery. Choose your race wisely, for it will shape
  your destiny.

  Available races range from the common Human to the exotic Xorn.
  Each has unique strengths, weaknesses, and abilities.

  Type '|yhelp|n' for a list of commands.

|b___________________________________________________________________________|n|n
"""


# ---------------------------------------------------------------------------
# CmdSet
# ---------------------------------------------------------------------------

class UnloggedinCmdSet(CmdSet):
    """
    This is the cmdset available to unlogged-in sessions.
    
    It provides:
      - d (disconnect)
      - w (who)
      - s (server status)
      - c (create character menu)
      - back (return to login screen)
      - <anything else> → name input handler
    """
    key = "Unloggedin"
    priority = 0
    
    def at_cmdset_creation(self):
        self.add(CmdDisconnect)
        self.add(CmdWho)
        self.add(CmdServerStatus)
        self.add(CmdCreateMenu)
        self.add(CmdBack)
        # The empty-key command catches all unmatched input
        self.add(CmdLoginInput)


# ---------------------------------------------------------------------------
# Module-level screen (for Evennia's connection screen system)
# ---------------------------------------------------------------------------

DEFAULT_CONNECTION_SCREEN = _get_login_screen()
