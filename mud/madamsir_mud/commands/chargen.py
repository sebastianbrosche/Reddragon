#!/usr/bin/env python3
"""
Character Creation Commands
============================
IOM-style character creation commands for the Hall of Races:
  all races       — list available races
  touch <race>    — select race and roll stats
  la <race>       — examine a race
  read poster     — race/guild compatibility
  read sign       — help for new players

Plus standalone roll/accept/reroll for D&D-style creation.
"""

from commands.chargen_cmds import CmdAllRaces, CmdTouch, CmdLa, CmdReadChargen
from commands.cmd_roll import CmdRoll, CmdAccept, CmdReroll

__all__ = [
    "CmdAllRaces",
    "CmdTouch",
    "CmdLa",
    "CmdReadChargen",
    "CmdRoll",
    "CmdAccept",
    "CmdReroll",
]
