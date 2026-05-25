"""
Red Dragon Reborn - IOM-style Who Command

Replaces Evennia's default who with the classic Islands of Myth format:

------------------------------------------
--         Islands of Myth
--
--  17 players (0 wizards, 17 mortals), 4 friends, 3 clanmates
--
------------------------------------------
{1732} Nailman     [ 613].Zlame       [ 520].Temuthril   [ 305].Dritthil
{ 243}.Wildchild   [ 213].Lyrion      [ 203].Fraziw      { 201} Moose
[ 175].Daran       [ 160].Seth        [ 157] Sebbe       [ 155].Korthrun
[ 140].Rossano     [ 123].Grasfer     [ 120].Frodo       [ 104].Monkey
[  53] Sloppy
------------------------------------------
-- . = idle, () = dead, {} = race leader, * = edit, ~ = wiztest, ^ = builder
--
------------------------------------------
"""

from evennia import Command, CmdSet
from evennia.accounts.models import AccountDB
from evennia.server.sessionhandler import SESSIONS
from django.conf import settings
import time

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SERVER_NAME = getattr(settings, "SERVERNAME", "Darkstaff MUD")
RACE_NAMES = [
    "Human", "Elf", "Dwarf", "Hobbit", "Gnome", "Halfelf",
    "Drow", "Goblin", "Troll", "Ogre", "Orc", "Lizardman",
    "Snakeman", "Kobold", "Giant", "Ent", "Faerie", "Vampire",
    "Phoenix", "Mindflayer", "Minotaur", "Gargoyle", "Thrikhren",
    "Xorn", "Vinnipier", "Grorrark", "Leprechaun", "Cromagnon",
]


def _get_race_leader_levels():
    """Find the highest level player per race currently online."""
    race_leaders = {}
    sessions = SESSIONS.get_sessions()
    
    for sess in sessions:
        pup = getattr(sess, "puppet", None)
        if not pup:
            continue
        
        race = getattr(pup.db, "race", None)
        level = getattr(pup.db, "level", 1)
        
        if race:
            if race not in race_leaders or level > race_leaders[race]:
                race_leaders[race] = level
    
    return race_leaders


def _format_level(level, is_race_leader, is_dead):
    """Format level number with appropriate brackets."""
    level_str = f"{level:>5}"
    if is_dead:
        return f"({level_str})"
    elif is_race_leader:
        return f"{{{level_str}}}"
    else:
        return f"[{level_str}]"


def _format_name(name, is_idle, is_dead, is_race_leader, is_builder, is_wiztest, is_editing):
    """Format name with IOM status markers."""
    if is_dead:
        return f"({name})"
    elif is_editing:
        return f"*{name}*"
    elif is_wiztest:
        return f"~{name}~"
    elif is_builder:
        return f"^{name}^"
    elif is_idle:
        return f".{name}"
    else:
        return f" {name}"


def _is_idle(session):
    """Check if session has been idle for 5+ minutes."""
    last_cmd = getattr(session, "cmd_last", 0)
    if not last_cmd:
        return False
    return (time.time() - last_cmd) > 300  # 5 minutes


def _build_who_table(players, race_leaders, viewer_account=None):
    """Build the 4-column player list table."""
    if not players:
        return []
    
    rows = []
    row = []
    
    for sess in players:
        pup = getattr(sess, "puppet", None)
        if not pup:
            continue
        
        name = pup.key
        level = getattr(pup.db, "level", 1)
        race = getattr(pup.db, "race", None)
        
        is_race_leader = race and race in race_leaders and level == race_leaders[race]
        is_idle = _is_idle(sess)
        is_dead = getattr(pup.db, "is_dead", False)
        is_builder = pup.locks.check_lockstring(pup, "Builder")
        is_wiztest = getattr(pup.db, "wiztest", False)
        is_editing = getattr(pup.db, "is_editing", False)
        
        level_str = _format_level(level, is_race_leader, is_dead)
        name_str = _format_name(name, is_idle, is_dead, is_race_leader, is_builder, is_wiztest, is_editing)
        
        entry = f"{level_str}{name_str}"
        row.append(entry)
        
        if len(row) == 4:
            # Format row with proper spacing
            formatted = "  ".join(f"{cell:<22}" for cell in row)
            rows.append(formatted)
            row = []
    
    # Handle remaining entries
    if row:
        formatted = "  ".join(f"{cell:<22}" for cell in row)
        rows.append(formatted)
    
    return rows


def _get_who_output(viewer=None, viewer_account=None):
    """Generate the full IOM-style who output."""
    sessions = SESSIONS.get_sessions()
    
    # Filter to active puppeted sessions
    players = []
    wizards = 0
    mortals = 0
    
    for sess in sessions:
        pup = getattr(sess, "puppet", None)
        if pup:
            players.append(sess)
            # Count wizards vs mortals (simplified: check permissions)
            if pup.locks.check_lockstring(pup, "Admin"):
                wizards += 1
            else:
                mortals += 1
    
    total = len(players)
    race_leaders = _get_race_leader_levels()
    
    # Build output
    lines = []
    
    # Top border
    lines.append("-" * 42)
    lines.append("-" * 42)
    lines.append(f"--{SERVER_NAME:^38}--")
    lines.append("--")
    
    # Count line
    friends = 0  # Not implemented yet
    clanmates = 0  # Not implemented yet
    lines.append(f"--  {total} players ({wizards} wizards, {mortals} mortals), {friends} friends, {clanmates} clanmates")
    lines.append("--")
    lines.append("-" * 42)
    lines.append("-" * 42)
    
    # Player table
    table_rows = _build_who_table(players, race_leaders, viewer_account)
    lines.extend(table_rows)
    
    # Bottom border + legend
    lines.append("-" * 42)
    lines.append("-" * 42)
    lines.append("-- . = idle, () = dead, {} = race leader, * = edit, ~ = wiztest, ^ = builder")
    lines.append("--")
    lines.append("-" * 42)
    lines.append("-" * 42)
    
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

class CmdWho(Command):
    """
    Show who is online in IOM format.
    
    Usage:
      who
      w
    """
    key = "who"
    aliases = ["w", "users"]
    locks = "cmd:all()"
    help_category = "General"
    
    def func(self):
        output = _get_who_output(
            viewer=self.caller,
            viewer_account=getattr(self.caller, "account", None)
        )
        self.caller.msg(output)


class CmdWhoUnloggedin(Command):
    """
    Show who is online (available before login).
    
    Usage:
      w
      who
    """
    key = "w"
    aliases = ["who"]
    locks = "cmd:all()"
    
    def func(self):
        output = _get_who_output()
        self.caller.msg(output)


# ---------------------------------------------------------------------------
# CmdSets
# ---------------------------------------------------------------------------

class WhoCmdSet(CmdSet):
    """Add who command to character cmdset."""
    key = "who"
    priority = 1
    
    def at_cmdset_creation(self):
        self.add(CmdWho)


# Keep unloggedin version for the login screen
__all__ = ["CmdWho", "CmdWhoUnloggedin", "WhoCmdSet", "_get_who_output"]
