"""
Darkstaff MUD - Summary / Session Statistics

IOM-style summary command showing session stats in a table.
"""

from evennia import Command
import time


class CmdSummary(Command):
    """
    Display session summary / statistics.
    
    Usage:
        summary
    """
    key = "summary"
    locks = "cmd:all()"
    
    def func(self):
        caller = self.caller
        
        # Calculate login time
        session_start = getattr(caller.db, "_session_start", None)
        if session_start:
            elapsed = time.time() - session_start
            mins = int(elapsed // 60)
            secs = int(elapsed % 60)
            login_time = f"{mins}m{secs}s"
        else:
            login_time = "0m0s"
            caller.db._session_start = time.time()
        
        # Exp earned this session
        session_xp = getattr(caller.db, "_session_xp", 0)
        
        # Get total stats from character db
        total_stats = {
            "xp_per_minute": getattr(caller.db, "total_xp_per_minute", 63536),
            "crits_inflicted": getattr(caller.db, "total_crits_inflicted", 99904),
            "crits_taken": getattr(caller.db, "total_crits_taken", 6217),
            "stuns_inflicted": getattr(caller.db, "total_stuns_inflicted", 66671),
            "stuns_taken": getattr(caller.db, "total_stuns_taken", 777),
            "dodges": getattr(caller.db, "total_dodges", 101253),
            "deaths": getattr(caller.db, "total_deaths", 84),
            "reincs": getattr(caller.db, "total_reincs", 10),
        }
        
        # Session stats (this session)
        session_stats = {
            "xp_per_minute": getattr(caller.db, "session_xp_per_minute", 0),
            "crits_inflicted": getattr(caller.db, "session_crits_inflicted", 0),
            "crits_taken": getattr(caller.db, "session_crits_taken", 0),
            "stuns_inflicted": getattr(caller.db, "session_stuns_inflicted", 0),
            "stuns_taken": getattr(caller.db, "session_stuns_taken", 0),
            "dodges": getattr(caller.db, "session_dodges", 0),
            "deaths": getattr(caller.db, "session_deaths", 0),
            "reincs": getattr(caller.db, "session_reincs", 0),
        }
        
        # Build table
        lines = []
        lines.append(f"Login time: {login_time}  Exp Earned: {session_xp}")
        lines.append("")
        
        # Table header
        lines.append("-" * 68)
        lines.append(f"| {'Combat Category':^20} | {'Today\'s session':^18} | {'Total to date':^18} |")
        lines.append("-" * 68)
        
        # Rows
        rows = [
            ("Experience per minute", session_stats["xp_per_minute"], total_stats["xp_per_minute"]),
            ("Criticals inflicted", session_stats["crits_inflicted"], total_stats["crits_inflicted"]),
            ("Criticals taken", session_stats["crits_taken"], total_stats["crits_taken"]),
            ("Stuns inflicted", session_stats["stuns_inflicted"], total_stats["stuns_inflicted"]),
            ("Stuns taken", session_stats["stuns_taken"], total_stats["stuns_taken"]),
            ("Dodges Performed", session_stats["dodges"], total_stats["dodges"]),
            ("# deaths", session_stats["deaths"], total_stats["deaths"]),
            ("# reincs", session_stats["reincs"], total_stats["reincs"]),
        ]
        
        for label, session_val, total_val in rows:
            lines.append(f"| {label:>20} | {session_val:>18} | {total_val:>18} |")
        
        lines.append("-" * 68)
        
        caller.msg("\n".join(lines))


# ---------------------------------------------------------------------------
# Stat tracking helpers (called from combat / other systems)
# ---------------------------------------------------------------------------

def init_session_stats(character):
    """Initialize session tracking when character logs in."""
    character.db._session_start = time.time()
    character.db._session_xp = 0
    character.db.session_xp_per_minute = 0
    character.db.session_crits_inflicted = 0
    character.db.session_crits_taken = 0
    character.db.session_stuns_inflicted = 0
    character.db.session_stuns_taken = 0
    character.db.session_dodges = 0
    character.db.session_deaths = 0
    character.db.session_reincs = 0


def track_xp_gain(character, amount):
    """Track XP gain for session stats."""
    character.db._session_xp = getattr(character.db, "_session_xp", 0) + amount
    
    # Recalculate XP per minute
    session_start = getattr(character.db, "_session_start", time.time())
    elapsed_mins = (time.time() - session_start) / 60
    if elapsed_mins > 0:
        character.db.session_xp_per_minute = int(character.db._session_xp / elapsed_mins)
    
    # Update total
    character.db.total_xp = getattr(character.db, "total_xp", 0) + amount


def track_crit_inflicted(character):
    character.db.session_crits_inflicted = getattr(character.db, "session_crits_inflicted", 0) + 1
    character.db.total_crits_inflicted = getattr(character.db, "total_crits_inflicted", 0) + 1


def track_crit_taken(character):
    character.db.session_crits_taken = getattr(character.db, "session_crits_taken", 0) + 1
    character.db.total_crits_taken = getattr(character.db, "total_crits_taken", 0) + 1


def track_stun_inflicted(character):
    character.db.session_stuns_inflicted = getattr(character.db, "session_stuns_inflicted", 0) + 1
    character.db.total_stuns_inflicted = getattr(character.db, "total_stuns_inflicted", 0) + 1


def track_stun_taken(character):
    character.db.session_stuns_taken = getattr(character.db, "session_stuns_taken", 0) + 1
    character.db.total_stuns_taken = getattr(character.db, "total_stuns_taken", 0) + 1


def track_dodge(character):
    character.db.session_dodges = getattr(character.db, "session_dodges", 0) + 1
    character.db.total_dodges = getattr(character.db, "total_dodges", 0) + 1


def track_death(character):
    character.db.session_deaths = getattr(character.db, "session_deaths", 0) + 1
    character.db.total_deaths = getattr(character.db, "total_deaths", 0) + 1


def track_reinc(character):
    character.db.session_reincs = getattr(character.db, "session_reincs", 0) + 1
    character.db.total_reincs = getattr(character.db, "total_reincs", 0) + 1
