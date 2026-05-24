"""
Red Dragon MUD - Wilderness Maps
Ocean travel and wilderness exploration for Islands of Myth
"""

from evennia.contrib.grid import wilderness

class OceanMapProvider(wilderness.WildernessMapProvider):
    """
    Ocean wilderness map for sailing between islands.
    Mostly open water with occasional islands.
    """
    
    def get_location_name(self, wilderness, coordinates):
        """Return room name based on coordinates."""
        x, y = coordinates
        
        # Some named islands at specific coordinates
        named_locations = {
            (0, 0): "Port of Ilium",
            (10, 5): "Yensid Island",
            (-5, 8): "Gossamer Shore",
            (15, -3): "Mystic Atoll",
        }
        
        if coordinates in named_locations:
            return named_locations[coordinates]
        
        # Random island chance
        import random
        random.seed(x * 1000 + y)
        if random.random() < 0.05:
            return "Uncharted Island"
        
        return "Open Ocean"
    
    def get_location_desc(self, wilderness, coordinates):
        """Return room description."""
        x, y = coordinates
        name = self.get_location_name(wilderness, coordinates)
        
        if "Island" in name or "Port" in name or "Shore" in name:
            return f"Land! You have reached {name}. The waves lap gently at the shore."
        
        import random
        random.seed(x * 1000 + y)
        conditions = [
            "The ocean stretches endlessly in all directions. Waves roll gently.",
            "Salty spray fills the air. Seabirds cry overhead.",
            "The water is calm and clear. You can see fish swimming below.",
            "A strong wind blows from the east, filling the sails.",
            "Dark clouds gather on the horizon. A storm may be coming.",
        ]
        return random.choice(conditions)


def create_ocean_wilderness():
    """Create the ocean wilderness map."""
    return wilderness.create_wilderness(
        name="ocean",
        mapprovider=OceanMapProvider()
    )


def enter_ocean_wilderness(character, coordinates=(0, 0)):
    """Move a character into the ocean wilderness."""
    return wilderness.enter_wilderness(character, name="ocean", coordinates=coordinates)
