"""
Red Dragon MUD — Character Typeclass
====================================
Extended character with race, guild, combat, and weapon mastery support.
"""

from evennia import DefaultCharacter
from typeclasses.races import apply_race
from typeclasses.guilds import apply_guild

class Character(DefaultCharacter):
    """
    The Character typeclass for Red Dragon MUD.
    Integrates races, guilds, weapon mastery, and combat stats.
    """

    def at_object_creation(self):
        """Called when character is first created."""
        super().at_object_creation()

        # Core stats (base 10 for humans, modified by race)
        for stat in ["strength", "constitution", "dexterity", "stamina",
                     "intelligence", "wisdom", "hp_max", "hp_regen",
                     "ep_max", "ep_regen", "sp_max", "sp_regen", "armor_class",
                     "xp_rate", "skill_max", "spell_max"]:
            if not hasattr(self.db, stat):
                setattr(self.db, stat, 10)

        # Combat stats
        self.db.weapon_mastery = {}  # weapon_type -> mastery_level (0-100)
        self.db.equipped_weapon = None
        self.db.equipped_armor = None
        self.db.combat_stance = "balanced"
        self.db.temp_modifiers = {}  # active buffs/debuffs

        # Race/Guild
        self.db.race_key = None
        self.db.race_name = None
        self.db.guild_key = None
        self.db.guild_name = None
        self.db.guild_level = 1
        self.db.guild_xp = 0
        self.db.guild_abilities = []
        self.db.guild_passives = []

        # Super race
        self.db.race_type = "regular"  # or "super"

        # Quest tracking
        self.db.completed_quests = []
        self.db.active_quests = []
        self.db.quest_points = 0

        # Alignment (-1000 to 1000)
        self.db.alignment = 0

        # Hunger (0 = starving, 6 = stuffed)
        self.db.hunger = 4

        # Lodestones
        self.db.lodestones = ["illium", "newbie"]

    def at_post_unpuppet(self, account, session=None, **kwargs):
        """When player logs out, save state."""
        super().at_post_unpuppet(account, session, **kwargs)
        self.db.hp_current = getattr(self.db, "hp_current", self.db.hp_max)
        self.db.ep_current = getattr(self.db, "ep_current", self.db.ep_max)
        self.db.sp_current = getattr(self.db, "sp_current", self.db.sp_max)

    def return_appearance(self, looker, **kwargs):
        """Custom appearance showing combat info."""
        text = super().return_appearance(looker, **kwargs)
        extras = []
        if self.db.race_name:
            extras.append(f"Race: {self.db.race_name}")
        if self.db.guild_name:
            extras.append(f"Guild: {self.db.guild_name}")
        if extras:
            text += "\n{" + ",".join(extras) + "}"
        return text

    def get_display_name(self, looker=None, **kwargs):
        """Show race/guild in display name if known."""
        name = super().get_display_name(looker, **kwargs)
        if self.db.race_name and self.db.guild_name:
            return f"{name} the {self.db.race_name} {self.db.guild_name}"
        elif self.db.race_name:
            return f"{name} the {self.db.race_name}"
        return name

    def get_combat_stats(self):
        """Return current combat-relevant stats."""
        stats = {
            "str": getattr(self.db, "strength", 10),
            "con": getattr(self.db, "constitution", 10),
            "dex": getattr(self.db, "dexterity", 10),
            "sta": getattr(self.db, "stamina", 10),
            "int": getattr(self.db, "intelligence", 10),
            "wis": getattr(self.db, "wisdom", 10),
            "ac": getattr(self.db, "armor_class", 10),
        }
        return stats

    def get_mastery_level(self, weapon_type="general"):
        """Return weapon mastery level (0-100)."""
        return self.db.weapon_mastery.get(weapon_type, 0)

    def set_mastery_level(self, weapon_type, level):
        """Set weapon mastery, capped at 100."""
        self.db.weapon_mastery[weapon_type] = min(100, max(0, level))

    def add_mastery(self, weapon_type, amount):
        """Add mastery XP, return True if tier up."""
        old_level = self.get_mastery_level(weapon_type)
        new_level = min(100, old_level + amount)
        self.set_mastery_level(weapon_type, new_level)
        # Check tier boundaries
        tiers = [20, 40, 60, 80, 95]
        for tier in tiers:
            if old_level < tier <= new_level:
                return True
        return False
