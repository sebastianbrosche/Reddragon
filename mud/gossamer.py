"""
gossamer.py - Islands of Myth Gossamer Wilderness Area
Evennia room definitions for the gossamer map

Room types: Sandy Beach, Ghastly Swamp, Badlands, Forest, Plains
All rooms have 8 exits (n, e, s, w, ne, nw, se, sw)
"""

from evennia import DefaultRoom

class GossamerRoom(DefaultRoom):
    """Base class for all gossamer wilderness rooms"""
    
    def at_object_creation(self):
        """Called when room is first created"""
        self.db.terrain = "unknown"
        self.db.is_wilderness = True
    
    def return_appearance(self, looker):
        """Custom appearance with map symbol"""
        desc = self.db.desc or "You are in an indistinct area."
        return desc

class SandyBeach(GossamerRoom):
    """SE corner beach terrain"""
    def at_object_creation(self):
        super().at_object_creation()
        self.db.key = "Sandy Beach"
        self.db.desc = "You are on a long sandy beach. Waves gently lap at the sand, covering the footprints that you are making."
        self.db.terrain = "beach"
        self.db.map_symbol = "b"

class GhastlySwamp(GossamerRoom):
    """Swamp terrain with hideous odor"""
    def at_object_creation(self):
        super().at_object_creation()
        self.db.key = "Ghastly Swamp"
        self.db.desc = "Your footsteps squish as you struggle through this ghastly swamp. The odor is hideous."
        self.db.terrain = "swamp"
        self.db.map_symbol = "s"

class Badlands(GossamerRoom):
    """Tortured barren lands"""
    def at_object_creation(self):
        super().at_object_creation()
        self.db.key = "Badlands"
        self.db.desc = "These tortured lands never know any respite from the cruel winds."
        self.db.terrain = "badlands"
        self.db.map_symbol = "x"

class Forest(GossamerRoom):
    """Dense forest with canopy"""
    def at_object_creation(self):
        super().at_object_creation()
        self.db.key = "Forest"
        self.db.desc = "You are in a forest. Large trees form a canopy overhead. The ground is moist and fertile."
        self.db.terrain = "forest"
        self.db.map_symbol = "f"

class Plains(GossamerRoom):
    """Open rolling grassland"""
    def at_object_creation(self):
        super().at_object_creation()
        self.db.key = "Plains"
        self.db.desc = "You are on a long rolling plain. You can see for miles in every direction. The grass is green, the breeze is cool."
        self.db.terrain = "plains"
        self.db.map_symbol = "p"

# Room type mapping for procedural generation
ROOM_TYPES = {
    'beach': SandyBeach,
    'swamp': GhastlySwamp,
    'badlands': Badlands,
    'forest': Forest,
    'plains': Plains
}

# Default exit configuration (all 8 directions)
EXIT_NAMES = ['north', 'east', 'south', 'west', 
              'northeast', 'southeast', 'southwest', 'northwest']
EXIT_ALIASES = {
    'north': ['n'],
    'east': ['e'],
    'south': ['s'],
    'west': ['w'],
    'northeast': ['ne'],
    'southeast': ['se'],
    'southwest': ['sw'],
    'northwest': ['nw']
}
