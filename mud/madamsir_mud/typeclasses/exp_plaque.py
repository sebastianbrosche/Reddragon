"""
EXP Plaque — Shows player experience standings
"""

from evennia import DefaultObject

class ExpPlaque(DefaultObject):
    """
    A golden plaque that displays all players ranked by experience.
    """
    
    def at_object_creation(self):
        super().at_object_creation()
        self.db.desc = (
            "A massive golden plaque engraved with magical runes. The names of all "
            "active adventurers shimmer in the metal, ranked by their experience and "
            "achievements. The list updates itself as the world turns."
        )
    
    def return_appearance(self, looker):
        """Show the experience standings when looked at."""
        from evennia import search_object
        from typeclasses.characters import Character
        
        text = "|c" + "="*55 + "|n\n"
        text += "|G         EXPERIENCE PLAQUE — Hall of Legends|n\n"
        text += "|c" + "="*55 + "|n\n\n"
        
        # Find all characters with XP data
        chars = search_object("", typeclass="typeclasses.characters.Character")
        standings = []
        
        for char in chars:
            if not char or char.key in ("Guest", "Superuser"):
                continue
            xp = getattr(char.db, "xp", 0) or getattr(char.db, "experience", 0) or 0
            level = getattr(char.db, "level", 1) or 1
            race = getattr(char.db, "race_name", getattr(char.db, "race", "Unknown")) or "Unknown"
            standings.append((char.key, xp, level, race))
        
        # Sort by XP descending
        standings.sort(key=lambda x: x[1], reverse=True)
        
        if not standings:
            text += "  |yNo adventurers have yet made their mark...|n\n"
            text += "\n|c" + "="*55 + "|n"
            return text
        
        text += f"  {'Rank':<6} {'Name':<18} {'Level':<7} {'Race':<12} {'XP':<12}\n"
        text += "  " + "-"*53 + "\n"
        
        for i, (name, xp, level, race) in enumerate(standings[:20], 1):
            rank_color = "|y" if i == 1 else "|w" if i <= 3 else "|x"
            text += f"  {rank_color}{i:<6}|n {name:<18} {level:<7} {race:<12} {xp:<12,}\n"
        
        text += "\n|c" + "="*55 + "|n"
        return text
