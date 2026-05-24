"""
Red Dragon MUD - Character Typeclass
Based on Islands of Myth reverse-engineering
Uses Evennia's TraitHandler, BuffHandler, and RP system.
"""

from evennia import DefaultCharacter
from evennia.utils import lazy_property
from evennia.contrib.rpg.traits import TraitHandler
from evennia.contrib.rpg.buffs import BuffHandler
from evennia.contrib.rpg.rpsystem.rpsystem import ContribRPCharacter

# Stat tier mapping from IOM data
STAT_TIERS = {
    "Terrible": 1, "Bad": 2, "Poor": 3, "Below Ave": 4,
    "Average": 5, "Above Ave": 6, "Good": 7, "Very Good": 8,
    "Excellent": 9
}

# IOM racial stat bases (from captured data)
RACE_STAT_BASES = {
    "Human": {"str": 50, "dex": 50, "con": 50, "sta": 50, "int": 50, "wis": 50, "cha": 50},
    "Dwarf": {"str": 65, "dex": 40, "con": 70, "sta": 60, "int": 45, "wis": 55, "cha": 40},
    "Elf": {"str": 40, "dex": 65, "con": 35, "sta": 45, "int": 60, "wis": 60, "cha": 60},
    "Orc": {"str": 70, "dex": 45, "con": 65, "sta": 60, "int": 30, "wis": 30, "cha": 25},
    "Gnome": {"str": 35, "dex": 55, "con": 40, "sta": 40, "int": 70, "wis": 60, "cha": 50},
    "Halfling": {"str": 35, "dex": 70, "con": 40, "sta": 45, "int": 50, "wis": 50, "cha": 55},
    "Half-Orc": {"str": 60, "dex": 50, "con": 60, "sta": 55, "int": 35, "wis": 35, "cha": 30},
    "Half-Elf": {"str": 45, "dex": 60, "con": 45, "sta": 50, "int": 55, "wis": 55, "cha": 60},
    "Troll": {"str": 80, "dex": 30, "con": 80, "sta": 70, "int": 20, "wis": 20, "cha": 15},
    "Kobold": {"str": 30, "dex": 60, "con": 35, "sta": 40, "int": 45, "wis": 40, "cha": 30},
}

class Character(ContribRPCharacter):
    """
    Custom character typeclass for Red Dragon.
    Uses Evennia's TraitHandler for stats, BuffHandler for effects,
    and RP system for sdescs, poses, and recognition.
    """

    @lazy_property
    def traits(self):
        return TraitHandler(self)

    @lazy_property
    def buffs(self):
        return BuffHandler(self)

    @lazy_property
    def cooldowns(self):
        from evennia.contrib.game_systems.cooldowns.cooldowns import CooldownHandler
        return CooldownHandler(self)

    def _setup_traits(self):
        """Initialize all IOM traits for this character."""
        race = getattr(self.db, "race", "Human")
        bases = RACE_STAT_BASES.get(race, RACE_STAT_BASES["Human"])

        # Static traits: core stats
        self.traits.add("str", "Strength", trait_type="static", base=bases["str"], mod=0)
        self.traits.add("dex", "Dexterity", trait_type="static", base=bases["dex"], mod=0)
        self.traits.add("con", "Constitution", trait_type="static", base=bases["con"], mod=0)
        self.traits.add("sta", "Stamina", trait_type="static", base=bases["sta"], mod=0)
        self.traits.add("int", "Intelligence", trait_type="static", base=bases["int"], mod=0)
        self.traits.add("wis", "Wisdom", trait_type="static", base=bases["wis"], mod=0)
        self.traits.add("cha", "Charisma", trait_type="static", base=bases["cha"], mod=0)

        # Gauge traits: HP, SP, EP
        con_bonus = self.traits.con.value // 10
        self.traits.add("hp", "Hit Points", trait_type="gauge", base=100 + con_bonus * 5, mod=0)
        self.traits.add("sp", "Spell Points", trait_type="gauge", base=100, mod=0)
        self.traits.add("ep", "Endurance Points", trait_type="gauge", base=100, mod=0)

        # Counter traits: guild skills
        self.traits.add("warrior", "Warrior Skill", trait_type="counter", base=0, mod=0, min=0, max=100)
        self.traits.add("thief", "Thief Skill", trait_type="counter", base=0, mod=0, min=0, max=100)
        self.traits.add("cleric", "Cleric Skill", trait_type="counter", base=0, mod=0, min=0, max=100)
        self.traits.add("mage", "Mage Skill", trait_type="counter", base=0, mod=0, min=0, max=100)
        self.traits.add("ranger", "Ranger Skill", trait_type="counter", base=0, mod=0, min=0, max=100)
        self.traits.add("bard", "Bard Skill", trait_type="counter", base=0, mod=0, min=0, max=100)
        self.traits.add("monk", "Monk Skill", trait_type="counter", base=0, mod=0, min=0, max=100)
        self.traits.add("cavalier", "Cavalier Skill", trait_type="counter", base=0, mod=0, min=0, max=100)
        self.traits.add("necromancer", "Necromancer Skill", trait_type="counter", base=0, mod=0, min=0, max=100)

    def at_object_creation(self):
        super().at_object_creation()

        # Set up RP sdesc based on race
        race = getattr(self.db, "race", "Human")
        if hasattr(self, 'sdesc'):
            self.sdesc.add(f"a {race.lower()} adventurer")

        # Set up traits via Evennia's TraitHandler
        self._setup_traits()

        # Keep legacy db attributes for backward compat until full migration
        # These will be removed once all commands use traits
        self.db.strength = self.traits.str.value
        self.db.dexterity = self.traits.dex.value
        self.db.constitution = self.traits.con.value
        self.db.stamina = self.traits.sta.value
        self.db.intelligence = self.traits.int.value
        self.db.wisdom = self.traits.wis.value
        self.db.charisma = self.traits.cha.value
        self.db.hp = self.traits.hp.value
        self.db.hp_max = self.traits.hp.base
        self.db.sp = self.traits.sp.value
        self.db.sp_max = self.traits.sp.base
        self.db.ep = self.traits.ep.value
        self.db.ep_max = self.traits.ep.base

        # Progression
        self.db.level = 1
        self.db.experience = 0
        self.db.next_level = 1000
        self.db.guild = None
        self.db.guild_level = 0
        self.db.guild_xp = 0
        self.db.guild_next = 500

        # Exploration
        self.db.rooms_explored = set()
        self.db.exploration_pct = 0.0

        # State
        self.db.alignment = "Neutral"
        self.db.hunger = "Satisfied"
        self.db.poisoned = False
        self.db.wimpy = 0
        self.db.stealth = 0
        self.db.hiding = False
        self.db.growth = "Growing"
        self.db.task_points = 0

        # Combat
        self.db.ac = "VLow"
        self.db.kills = 0
        self.db.deaths = 0

        # Size/Physical
        self.db.height = "5'8\""
        self.db.weight = 176
        self.db.size = "Medium"
        self.db.race = "Human"

        # Economy
        self.db.gold = 100
        self.db.bank_gold = 0

        # Legacy skills dict (will migrate to traits)
        self.db.skills = {
            "attack": 20,
            "flesh of stone": 20,
            "honor of the gods": 20,
            "tanking": 20,
            "weapon skill blunt": 20,
        }

        # Regeneration stats
        self.db.hp_regen = 10
        self.db.sp_regen = 5
        self.db.ep_regen = 5

        # Mail system
        self.db.mail_count = 0
        self.db.mail_unread = 0

        # Spawn location
        from evennia.utils import search
        start_room = search.search_object("Adventurer Guild Entrance", typeclass="typeclasses.rooms.Room")
        if start_room:
            self.home = start_room[0]
            self.location = start_room[0]

        # AI DM data
        self.db.titles = []
        self.db.chat_enabled = True
    
    def at_post_puppet(self, **kwargs):
        """
        Called just after puppeting (after account has connected).
        IOM-style greeting.
        """
        super().at_post_puppet(**kwargs)
        
        # Show version info
        from commands.utility import VERSION
        self.msg(f"|bWelcome to {VERSION['name']}|n |y(v{VERSION['version']})|n")
        
        # Initialize session statistics
        from commands.summary import init_session_stats
        init_session_stats(self)
        
        # Initialize AI DM if not already running
        from typeclasses.scripts.ai_dm import get_ai_dm
        get_ai_dm()
        
        # Show score on login
        self.msg(self.get_score_display())
        
        # Show room description
        if self.location:
            self.msg(self.location.return_appearance(self))
            
    def at_post_unpuppet(self, account=None, **kwargs):
        """Called just after un-puppeting."""
        super().at_post_unpuppet(**kwargs)
        
        
    def get_stat_modifier(self, stat_name):
        """Return stat value as modifier for calculations."""
        trait = self.traits.get(stat_name.lower(), None)
        if trait:
            return trait.value
        return getattr(self.db, stat_name, 50)
        
    def modify_stat(self, stat, delta):
        """Adjust a stat by delta, bounded 1-100."""
        trait = self.traits.get(stat.lower(), None)
        if trait:
            trait.base = max(1, min(100, trait.base + delta))
            # Sync legacy db for backward compat
            stat_map = {"str": "strength", "dex": "dexterity", "con": "constitution", 
                       "sta": "stamina", "int": "intelligence", "wis": "wisdom", "cha": "charisma",
                       "hp": "hp", "sp": "sp", "ep": "ep"}
            db_key = stat_map.get(stat.lower())
            if db_key:
                setattr(self.db, db_key, trait.value)
            return trait.value
        return getattr(self.db, stat, 50)
        
    def add_experience(self, amount):
        """Add XP and check for level up."""
        self.db.experience += amount
        if self.db.experience >= self.db.next_level:
            self.level_up()
            
    def level_up(self):
        """Handle level advancement (IOM formula) using traits."""
        self.db.level += 1
        
        # IOM stat gains per level - modify traits
        self.modify_stat("str", 2)
        self.modify_stat("dex", 2)
        self.modify_stat("con", 1)
        self.modify_stat("int", 1)
        self.modify_stat("wis", 1)
        self.modify_stat("sta", 2)
        
        # Regeneration increases
        self.db.hp_regen = getattr(self.db, 'hp_regen', 10) + 2
        self.db.sp_regen = getattr(self.db, 'sp_regen', 5) + 1
        self.db.ep_regen = getattr(self.db, 'ep_regen', 5) + 1
        
        # Increase max resources based on CON/STA via traits
        con_bonus = self.traits.con.value // 10
        sta_bonus = self.traits.sta.value // 10
        self.traits.hp.base += 20 + con_bonus * 5
        self.traits.ep.base += 15 + sta_bonus * 3
        self.traits.sp.base += 10 + (self.traits.int.value // 10) * 3
        
        # Sync legacy db attributes
        self.db.hp_max = self.traits.hp.base
        self.db.ep_max = self.traits.ep.base
        self.db.sp_max = self.traits.sp.base
        
        # Full heal on level up
        self.traits.hp.current = self.traits.hp.base
        self.traits.ep.current = self.traits.ep.base
        self.traits.sp.current = self.traits.sp.base
        self.db.hp = self.traits.hp.value
        self.db.ep = self.traits.ep.value
        self.db.sp = self.traits.sp.value
        
        # Increase next level threshold (exponential)
        self.db.next_level = int(self.db.next_level * 1.5)
        
        self.msg(f"You have advanced to level {self.db.level}!")
        
    def explore_room(self, room):
        """Mark a room as explored."""
        if room.id not in self.db.rooms_explored:
            self.db.rooms_explored.add(room.id)
            return True
        return False
        
    def get_score_display(self):
        """Return formatted score sheet (IOM-style) using traits."""
        race_name = self.db.race if hasattr(self.db, "race") else "Unknown"
        guild_name = self.db.guild if self.db.guild else "None"
        guild_lvl = self.db.guild_level
        
        total_rooms = 17750
        explored = len(self.db.rooms_explored)
        pct = (explored / total_rooms) * 100 if total_rooms > 0 else 0
        
        # Pull values from traits (fallback to db for backward compat)
        str_val = getattr(self.traits, 'str', None) and self.traits.str.value or self.db.strength
        dex_val = getattr(self.traits, 'dex', None) and self.traits.dex.value or self.db.dexterity
        con_val = getattr(self.traits, 'con', None) and self.traits.con.value or self.db.constitution
        sta_val = getattr(self.traits, 'sta', None) and self.traits.sta.value or self.db.stamina
        int_val = getattr(self.traits, 'int', None) and self.traits.int.value or self.db.intelligence
        wis_val = getattr(self.traits, 'wis', None) and self.traits.wis.value or self.db.wisdom
        cha_val = getattr(self.traits, 'cha', None) and self.traits.cha.value or self.db.charisma
        hp_cur = getattr(self.traits, 'hp', None) and self.traits.hp.value or self.db.hp
        hp_max = getattr(self.traits, 'hp', None) and self.traits.hp.base or self.db.hp_max
        sp_cur = getattr(self.traits, 'sp', None) and self.traits.sp.value or self.db.sp
        sp_max = getattr(self.traits, 'sp', None) and self.traits.sp.base or self.db.sp_max
        ep_cur = getattr(self.traits, 'ep', None) and self.traits.ep.value or self.db.ep
        ep_max = getattr(self.traits, 'ep', None) and self.traits.ep.base or self.db.ep_max
        
        return f"""
,----------------------------------------------------------------------------.
| {self.key} the {race_name}
| Level          : {self.db.level:>4}                Open Guild Levels : {guild_lvl:>4}              |
|                                                                            |
| Experience     : {self.db.experience:>14}     Explored          : {pct:>5.2f}% ({pct * 8.57:.2f}%)     |
| Next level     : {self.db.next_level:>14}     Rooms Explored    : {explored:>14}     |
| Guild Level    : {self.db.guild_level:>14}     Gold on hand      : {self.db.gold:>14}     |
| To Next Level  : {self.db.next_level - self.db.experience:>14}     Gold in bank      : {self.db.bank_gold:>14}     |
| To Guild Level : {self.db.guild_next - self.db.guild_xp if self.db.guild else 0:>14}                                            |
|----------------------------------------------------------------------------|
| Strength     : {str_val:>3} | Hit Points     : {hp_cur:>4} ({hp_max:>4}) | AC       : {self.db.ac}
| Dexterity    : {dex_val:>3} | Spell Points   : {sp_cur:>4} ({sp_max:>4}) | Size     : {self.db.size}
| Constitution : {con_val:>3} | Endurance Pts. : {ep_cur:>4} ({ep_max:>4}) | Weight   : {self.db.weight} lb
| Stamina      : {sta_val:>3} | Hunger         : {self.db.hunger}       | Stealth  : {self.db.stealth}%
| Intelligence : {int_val:>3} | Wimpy          : {self.db.wimpy}%            | Hiding   : {'Yes' if self.db.hiding else 'No'}
| Wisdom       : {wis_val:>3} | Alignment      : {self.db.alignment}       | Poisoned : {'Yes' if self.db.poisoned else 'No'}
| Charisma     : {cha_val:>3} | TaskPts. : {self.db.task_points}        
|----------------------------------------------------------------------------|
| alpha   : {guild_name} ({guild_lvl})                      | Mail          : {self.db.mail_unread}/{self.db.mail_count}           |
|                                            | Kills         : {self.db.kills}             |
`----------------------------------------------------------------------------'
hp({hp_cur}/{hp_max}) sp({sp_cur}/{sp_max}) ep({ep_cur}/{ep_max}) >"""
