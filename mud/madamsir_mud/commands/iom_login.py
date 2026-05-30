#!/usr/bin/env python3
"""
IOM-Style Login Commands for Myth of Islands MUD
Overrides Evennia's default unloggedin commands for password-less login.

Usage:
  connect <name>      - Login (no password needed)
  create <name>       - Create new character (auto-generates password)
  c <name>            - Short alias for create
  look / l            - Show connection screen
  help                - Show help
  quit                - Disconnect
"""

import re
from django.conf import settings
from evennia.utils import class_from_module
from evennia.commands.command import Command
from evennia import create_account, search_account
from evennia.commands.cmdhandler import CMD_LOGINSTART

COMMAND_DEFAULT_CLASS = class_from_module(settings.COMMAND_DEFAULT_CLASS)


class CmdIOMConnect(COMMAND_DEFAULT_CLASS):
    """
    Login to the game (no password required for testing)

    Usage:
      connect <character_name>

    Type your character name to log in.
    """
    key = "connect"
    aliases = ["conn", "con", "co", "login", "log", "l"]
    locks = "cmd:all()"
    arg_regex = r"\s.*?|$"

    def func(self):
        session = self.caller
        name = self.args.strip()

        # Auto-relogin after reboot: if no name given but auto_character stored
        if not name and session.db.auto_character:
            name = session.db.auto_character
            session.msg(f"|gAuto-reconnecting as {name}...|n")

        if not name:
            session.msg("\n|yUsage: connect <character_name>|n")
            return

        # Remove quotes if present
        name = name.strip('"').strip("'")

        Account = class_from_module(settings.BASE_ACCOUNT_TYPECLASS)

        # Try to find account
        accounts = search_account(name)
        if accounts:
            account = accounts[0]
            # Auto-login without password check (testing mode)
            session.sessionhandler.login(session, account)
            session.msg(f"\n|gWelcome back, {account.key}!|n\n")
            # Clear auto_character after successful login
            if session.db.auto_character:
                del session.db.auto_character
            return

        # Account not found - offer to create
        session.msg(f"\n|yCharacter '{name}' not found.|n")
        session.msg("|yType 'create {name}' to create a new character.|n\n")


class CmdIOMCreate(COMMAND_DEFAULT_CLASS):
    """
    Create a new character (auto-generates password)

    Usage:
      create <character_name>
      c <character_name>

    Creates a new character with the given name.
    A dummy password is auto-generated.
    """
    key = "create"
    aliases = ["cre", "cr", "c", "new", "n"]
    locks = "cmd:all()"
    arg_regex = r"\s.*?|$"

    def at_pre_cmd(self):
        if not settings.NEW_ACCOUNT_REGISTRATION_ENABLED:
            self.msg("Registration is currently disabled.")
            return True
        return super().at_pre_cmd()

    def func(self):
        session = self.caller
        name = self.args.strip()

        if not name:
            session.msg("\n|yUsage: create <character_name>|n")
            return

        # Remove quotes if present
        name = name.strip('"').strip("'")
        name = name.strip()

        # NO NAME RESTRICTIONS — user can call themselves anything
        # Just prevent empty strings
        if len(name) < 1:
            session.msg("|rName cannot be empty.|n")
            return

        # Check if account already exists
        from evennia.accounts.models import AccountDB
        if AccountDB.objects.filter(username__iexact=name).exists():
            session.msg(f"|rCharacter '{name}' already exists. Type 'connect {name}' to login.|n")
            return

        # Auto-generate password
        password = "password123"

        # Create account
        Account = class_from_module(settings.BASE_ACCOUNT_TYPECLASS)
        address = session.address

        try:
            account, errors = Account.create(
                username=name,
                password=password,
                ip=address,
                session=session,
            )
            if not account:
                session.msg(f"|r{' '.join(errors)}|n")
                return

            # Create a character for the account
            from evennia import create_object, search_object
            from typeclasses.characters import Character

            # Find or create Hall of Races for starting location
            from evennia import create_object
            from typeclasses.rooms import Room
            
            hall_of_races = search_object("Hall of Races", typeclass="typeclasses.rooms.Room")
            if hall_of_races:
                start_location = hall_of_races[0]
            else:
                # Create Hall of Races
                start_location = create_object(Room, key="Hall of Races")
                start_location.db.desc = (
                    "This is the Hall of Races in the space outside the world.\n"
                    "The only way out of this void is to select the race you wish\n"
                    "to represent in the world of Islands of Myth.\n\n"
                    "In this hall, every race has a statue, and you feel that you can do these things:\n"
                    "  |yall races|n      — To get a list of available races\n"
                    "  |ytouch <race>|n   — To touch the statue of <race> and enter the world\n"
                    "  |yla <race>|n     — To examine <race>'s statue and learn more info\n"
                    "  |yread poster|n   — To see which races are best for which guilds\n"
                    "  |yread sign|n     — You're lost and need additional help\n"
                )
                start_location.db.island = "chargen"
            
            char = create_object(Character, key=name, location=start_location)
            if char:
                # Don't set race yet — player must choose in Hall of Races
                char.db.race = None
                char.db.race_name = None
                char.db.island = "chargen"
                # Set home to Hall of Races initially
                char.db.home = start_location
                # Grant puppet permission — allow this account to puppet this char
                # pid() checks the puppeting account's id
                char.locks.add(f"puppet:pid({account.id}) or puppet:all()")
                # Link to account
                account.db._playable_characters = [char]

            # Login - this triggers at_post_login which auto-puppets _playable_characters[0]
            session.sessionhandler.login(session, account)

            # If auto-puppet didn't work, force it manually
            if char and not session.puppet:
                account.puppet_object(session, char)

            # Move character to starting location if not already placed
            if char and not char.location:
                if start_location:
                    char.move_to(start_location)
                else:
                    # Fallback: any room
                    fallback = search_object("Hall of Races", typeclass="typeclasses.rooms.Room")
                    if fallback:
                        char.move_to(fallback[0])
                    else:
                        # Last resort: Limbo
                        limbo = search_object("Limbo", typeclass="typeclasses.rooms.Room")
                        if limbo:
                            char.move_to(limbo[0])

            session.msg(f"\n|gWelcome, {name}! Your character has been created.|n")
            if start_location:
                session.msg(f"|gYou awaken in {start_location.key}.|n")
                session.msg("|gType LOOK to see your surroundings.|n")
                session.msg("|gUse 'all races' to see available races, then 'touch <race>' to choose.|n")
                session.msg("|gUse 'la <race>' to examine a race before choosing.|n\n")

        except Exception as e:
            import traceback
            session.msg(f"|rError creating character: {e}|n")
            session.msg(f"|r{traceback.format_exc()}|n")


class CmdIOMLook(COMMAND_DEFAULT_CLASS):
    """
    Show the connection screen. Replaces the default auto-look command.
    """
    key = CMD_LOGINSTART
    aliases = ["look", "l", "lo"]
    locks = "cmd:all()"

    def func(self):
        from server.conf import connection_screens
        session = self.caller

        # Get connection screen
        try:
            screen = connection_screens.CONNECTION_SCREEN
        except:
            screen = connection_screens.connection_screen() if hasattr(connection_screens, 'connection_screen') else "Welcome to Myth of Islands!"

        session.msg(screen)


class CmdIOMHelp(COMMAND_DEFAULT_CLASS):
    """
    Show help for unloggedin commands
    """
    key = "help"
    aliases = ["h", "?"]
    locks = "cmd:all()"

    def func(self):
        session = self.caller
        help_text = """
|b==============================================================|n
                          |gMYTH OF ISLANDS|n - Help

|wTo login:|n          connect <character_name>
|wTo create:|n        create <character_name>  (or: c <name>)
|wTo look:|n          look  (shows welcome screen)
|wTo quit:|n          quit

|yNo password needed!|n
|b==============================================================|n
"""
        session.msg(help_text)


class CmdIOMQuit(COMMAND_DEFAULT_CLASS):
    """
    Disconnect from the game
    """
    key = "quit"
    aliases = ["q", "disconnect", "dc"]
    locks = "cmd:all()"

    def func(self):
        session = self.caller
        session.msg("|rDisconnecting...|n")
        session.sessionhandler.disconnect(session, reason="Player quit")
