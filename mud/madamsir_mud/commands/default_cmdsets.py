"""
Command sets

All commands in the game must be grouped in a cmdset.  A given command
can be part of any number of cmdsets and cmdsets can be added/removed
and merged onto entities at runtime.

To create new commands to populate the cmdset, see
`commands/command.py`.

This module wraps the default command sets of Evennia; overloads them
to add/remove commands from the default lineup. You can create your
own cmdsets by inheriting from them or directly from `evennia.CmdSet`.

"""

from evennia import default_cmds
from commands.command import CmdReboot

# Wrap optional imports in try/except so cmdset loading never fails
try:
    from commands.raceguild_cmds import CmdRace, CmdGuild, CmdCombatProfile, CmdMastery, CmdScore
except Exception:
    CmdRace = CmdGuild = CmdCombatProfile = CmdMastery = CmdScore = None

try:
    from commands.combat_cmds import CombatCmdSet
except Exception:
    CombatCmdSet = None

try:
    from commands.system_cmds import CmdDamageTypes, CmdCondition, CmdAlignment, CmdHunger, CmdLodestone, CmdWorld, CmdSuperRace, CmdQuest
except Exception:
    CmdDamageTypes = CmdCondition = CmdAlignment = CmdHunger = CmdLodestone = CmdWorld = CmdSuperRace = CmdQuest = None

try:
    from commands.system_cmds_part2 import CmdLevel, CmdHeal, CmdEquipment, CmdBuildWorld
except Exception:
    CmdLevel = CmdHeal = CmdEquipment = CmdBuildWorld = None

try:
    from commands.cmd_roll import CmdRoll, CmdAccept, CmdReroll
except Exception:
    CmdRoll = CmdAccept = CmdReroll = None

try:
    from commands.chargen_cmds import CmdAllRaces, CmdTouch, CmdLa, CmdReadChargen
except Exception:
    CmdAllRaces = CmdTouch = CmdLa = CmdReadChargen = None


class CharacterCmdSet(default_cmds.CharacterCmdSet):
    """
    The `CharacterCmdSet` contains general in-game commands like `look`,
    `get`, etc available on in-game Character objects. It is merged with
    the `AccountCmdSet` when an Account puppets a Character.
    """

    key = "DefaultCharacter"

    def at_cmdset_creation(self):
        """
        Populates the cmdset
        """
        super().at_cmdset_creation()
        # Add commands only if imports succeeded
        if CmdRace: self.add(CmdRace)
        if CmdGuild: self.add(CmdGuild)
        if CmdCombatProfile: self.add(CmdCombatProfile)
        if CmdMastery: self.add(CmdMastery)
        if CmdScore: self.add(CmdScore)
        if CombatCmdSet:
            combat_set = CombatCmdSet()
            for cmd in combat_set.commands:
                self.add(cmd)
        if CmdDamageTypes: self.add(CmdDamageTypes)
        if CmdCondition: self.add(CmdCondition)
        if CmdAlignment: self.add(CmdAlignment)
        if CmdHunger: self.add(CmdHunger)
        if CmdLodestone: self.add(CmdLodestone)
        if CmdWorld: self.add(CmdWorld)
        if CmdSuperRace: self.add(CmdSuperRace)
        if CmdQuest: self.add(CmdQuest)
        if CmdLevel: self.add(CmdLevel)
        if CmdHeal: self.add(CmdHeal)
        if CmdEquipment: self.add(CmdEquipment)
        if CmdBuildWorld: self.add(CmdBuildWorld)
        if CmdRoll: self.add(CmdRoll)
        if CmdAccept: self.add(CmdAccept)
        if CmdReroll: self.add(CmdReroll)
        if CmdAllRaces: self.add(CmdAllRaces)
        if CmdTouch: self.add(CmdTouch)
        if CmdLa: self.add(CmdLa)
        if CmdReadChargen: self.add(CmdReadChargen)
        self.add(CmdReboot)


class AccountCmdSet(default_cmds.AccountCmdSet):
    """
    This is the cmdset available to the Account at all times. It is
    combined with the `CharacterCmdSet` when the Account puppets a
    Character. It holds game-account-specific commands, channel
    commands, etc.
    """

    key = "DefaultAccount"

    def at_cmdset_creation(self):
        """
        Populates the cmdset
        """
        super().at_cmdset_creation()
        #
        # any commands you add below will overload the default ones.
        #


class UnloggedinCmdSet(default_cmds.UnloggedinCmdSet):
    """
    Command set available to the Session before being logged in.  This
    holds commands like creating a new account, logging in, etc.
    """

    key = "DefaultUnloggedin"

    def at_cmdset_creation(self):
        """
        Populates the cmdset
        """
        super().at_cmdset_creation()
        # Remove default connect/create by key string (safe, no import needed)
        self.remove("connect")
        self.remove("create")
        from evennia.commands.cmdhandler import CMD_LOGINSTART
        self.remove(CMD_LOGINSTART)
        self.remove("help")
        self.remove("quit")
        # Add IOM-style login commands
        try:
            from commands.iom_login import CmdIOMConnect, CmdIOMCreate, CmdIOMLook, CmdIOMHelp, CmdIOMQuit
            self.add(CmdIOMConnect)
            self.add(CmdIOMCreate)
            self.add(CmdIOMLook)
            self.add(CmdIOMHelp)
            self.add(CmdIOMQuit)
        except Exception as e:
            import logging
            logger = logging.getLogger("evennia")
            logger.error(f"IOM login commands failed to load: {e}")
            pass


class SessionCmdSet(default_cmds.SessionCmdSet):
    """
    This cmdset is made available on Session level once logged in. It
    is empty by default.
    """

    key = "DefaultSession"

    def at_cmdset_creation(self):
        """
        This is the only method defined in a cmdset, called during
        its creation. It should populate the set with command instances.

        As and example we just add the empty base `Command` object.
        It prints some info.
        """
        super().at_cmdset_creation()
        #
        # any commands you add below will overload the default ones.
        #
