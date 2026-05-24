# -*- coding: utf-8 -*-
"""
IOM Guild Master System

Places all guild masters in Illium City with proper ordering and prerequisites.
Bot-compatible: guild masters give clear instructions when talked to.
"""

import json
from pathlib import Path
from evennia import DefaultObject, create_object, search_object
from typeclasses.rooms import IOMRoom

# Load guild data
GUILD_DATA_PATH = Path(__file__).parent / "guild_trees.py"

class GuildMaster(DefaultObject):
    """
    A guild master NPC that players can talk to join guilds.
    """
    
    def at_object_creation(self):
        super().at_object_creation()
        self.db.guild_key = None
        self.db.guild_name = None
        self.db.guild_tier = None  # alpha, bravo, charlie, delta, etc.
        self.db.guild_tree = None  # warrior, mage, cleric, etc.
        self.db.prerequisites = []  # List of required guilds
        self.db.skills_taught = []  # List of skills this guild teaches
        self.db.spells_taught = []  # List of spells this guild teaches
        self.db.is_guild_master = True
        self.db.max_skill_percent = 100  # Max training percentage
        
    def at_init(self):
        """Set up appearance."""
        if self.db.guild_name:
            self.key = f"{self.db.guild_name} Guild Master"
    
    def return_appearance(self, looker):
        if self.db.guild_name:
            return f"|y{self.db.guild_name} Guild Master|n stands here, ready to train adventurers.\nType |wtalk {self.key.lower().replace(' ', '_')}|n to speak with them."
        return "A guild master stands here."


def load_guild_data():
    """Load guild data from the database."""
    # Try to import from guild_trees.py
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("guild_trees", GUILD_DATA_PATH)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return getattr(module, 'GUILD_DATABASE', {})
    except Exception as e:
        print(f"Could not load guild database: {e}")
        return {}


def get_tier_order(tier_name):
    """Return numeric order for tier names."""
    tiers = {
        "alpha": 1, "bravo": 2, "charlie": 3, "delta": 4,
        "echo": 5, "foxtrot": 6, "golf": 7, "hotel": 8,
        "india": 9, "juliet": 10, "kilo": 11, "lima": 12,
        "mike": 13, "november": 14, "oscar": 15, "papa": 16,
        "quebec": 17, "romeo": 18, "sierra": 19, "tango": 20,
        "uniform": 21, "victor": 22, "whiskey": 23, "x-ray": 24,
        "yankee": 25, "zulu": 26,
    }
    return tiers.get(tier_name.lower(), 99)


def place_guild_masters():
    """Place all guild masters in Illium City."""
    
    # Find Illium City hub or central square
    central = search_object("Central Square", typeclass=IOMRoom)
    if not central:
        print("Central Square not found! Creating...")
        central = create_object(IOMRoom, key="Central Square")
        central.db.desc = "The bustling center of Illium City."
        central.db.domain = "gossamer"
        central.db.area = "Illium City"
    else:
        central = central[0]
    
    # Find or create Guild Hall
    guild_hall = search_object("Guild Hall", typeclass=IOMRoom)
    if not guild_hall:
        guild_hall = create_object(IOMRoom, key="Guild Hall")
        guild_hall.db.desc = "A grand hall where guild masters gather to train adventurers."
        guild_hall.db.domain = "gossamer"
        guild_hall.db.area = "Illium City"
        
        # Connect guild hall to central square
        from typeclasses.exits import IOMExit
        to_hall = create_object(IOMExit, key="guild hall")
        to_hall.aliases.add("hall")
        to_hall.location = central
        to_hall.destination = guild_hall
        
        to_square = create_object(IOMExit, key="square")
        to_square.aliases.add("out")
        to_square.location = guild_hall
        to_square.destination = central
    else:
        guild_hall = guild_hall[0]
    
    # Load guild data
    guild_db = load_guild_data()
    
    if not guild_db:
        print("No guild data found. Creating sample guild masters...")
        # Create basic warrior guilds as fallback
        sample_guilds = [
            {"key": "warrior", "name": "Warrior", "tier": "alpha", "tree": "warrior"},
            {"key": "berserker", "name": "Berserker", "tier": "bravo", "tree": "warrior"},
            {"key": "knight", "name": "Knight", "tier": "bravo", "tree": "warrior"},
            {"key": "champion_of_the_crown", "name": "Champion of the Crown", "tier": "omicron", "tree": "warrior"},
        ]
        for guild_info in sample_guilds:
            master = create_object(GuildMaster, key=f"{guild_info['name']} Guild Master")
            master.db.guild_key = guild_info['key']
            master.db.guild_name = guild_info['name']
            master.db.guild_tier = guild_info['tier']
            master.db.guild_tree = guild_info['tree']
            master.location = guild_hall
            print(f"  Created: {guild_info['name']} ({guild_info['tier']})")
        return
    
    # Place guild masters organized by tier
    guilds_by_tier = {}
    for guild_key, guild_info in guild_db.items():
        if isinstance(guild_info, dict):
            tier = guild_info.get("tier", "unknown")
            tier_order = get_tier_order(tier)
            if tier_order not in guilds_by_tier:
                guilds_by_tier[tier_order] = []
            guilds_by_tier[tier_order].append((guild_key, guild_info))
    
    placed = 0
    for tier_order in sorted(guilds_by_tier.keys()):
        tier_guilds = guilds_by_tier[tier_order]
        for guild_key, guild_info in tier_guilds:
            tier_name = guild_info.get("tier", "unknown")
            guild_name = guild_info.get("name", guild_key.replace("_", " ").title())
            
            master = create_object(GuildMaster, key=f"{guild_name} Guild Master")
            master.db.guild_key = guild_key
            master.db.guild_name = guild_name
            master.db.guild_tier = tier_name
            master.db.guild_tree = guild_info.get("tree", "general")
            master.db.prerequisites = guild_info.get("prerequisites", [])
            master.db.skills_taught = list(guild_info.get("skills", {}).keys())
            master.db.spells_taught = list(guild_info.get("spells", {}).keys())
            master.location = guild_hall
            
            placed += 1
    
    print(f"\n{'='*60}")
    print(f"GUILD MASTERS PLACED: {placed}")
    print(f"Location: Guild Hall (connected to Central Square)")
    print(f"{'='*60}")
    print("\nBot navigation:")
    print("  1. From Central Square: go |wguild hall|n")
    print("  2. In Guild Hall: |wtalk <master name>|n")
    print("  3. Join guilds in tier order (alpha → bravo → charlie → ...)")


if __name__ == "__main__":
    print("Run this from within Evennia with:")
    print("  @py from world.guild_masters import place_guild_masters; place_guild_masters()")
