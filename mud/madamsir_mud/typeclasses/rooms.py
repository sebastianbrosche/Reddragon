"""
Red Dragon MUD — Rooms
======================
Extended room typeclass with island and level information.
"""

from evennia import DefaultRoom

class Room(DefaultRoom):
    """
    Room with island, level range, and danger info.
    """

    def at_object_creation(self):
        super().at_object_creation()
        self.db.island = "unknown"
        self.db.level_range = (1, 50)
        self.db.climate = "temperate"
        self.db.dangers = []
        self.db.is_rest_area = False

    def return_appearance(self, looker, **kwargs):
        """Show island info in room description."""
        text = super().return_appearance(looker, **kwargs)
        island = self.db.island
        if island and island not in ("unknown", "illium"):
            text += f"\n{{y[Island: {island.title()}]{{n"
        if self.db.dangers:
            text += f"\n{{rDangers: {', '.join(self.db.dangers)}{{n"
        return text
