"""
Red Dragon MUD - Character Typeclass
Based on Islands of Myth reverse-engineering
"""

from evennia import DefaultCharacter

# Stat tier mapping from IOM data
STAT_TIERS = {
    "Terrible": 1, "Bad": 2, "Poor": 3, "Below Ave": 4,
    "Average": 5, "Above Ave": 6, "Good": 7, "Very Good": 8,
    "Excellent": 9
}

class Character(DefaultCharacter):
    """
    Custom character typeclass for Red Dragon.
    
    Stats (from IOM): Strength, Dexterity, Constitution, Stamina,
    Intelligence, Wisdom, Charisma
    
    Resources: HP, SP (Spell Points), EP (Endurance Points)
    """

    def at_object_creation(self):
        super().at_object_creation()
        
        # Core stats (1-100 scale, human baseline ~50)
        self.db.strength = 50
        self.db.dexterity = 50
        self.db.constitution = 50
        self.db.stamina = 50
        self.db.intelligence = 50
        self.db.wisdom = 50
        self.db.charisma = 50
        
        # Resources
        self.db.hp = 100
        self.db.hp_max = 100
        self.db.sp = 100
        self.db.sp_max = 100
        self.db.ep = 100
        self.db.ep_max = 100
        
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
        self.db.wimpy = 0  # % to flee at
        self.db.stealth = 0  # stealth percentage
        self.db.hiding = False
        self.db.growth = "Growing"
        self.db.task_points = 0
        
        # Combat
        self.db.ac = "VLow"  # Armor Class
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
        
        # Skills (guild skills)
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
        
        # Spawn location - try to move to Adventurer Guild Entrance if it exists
        from evennia.utils import search
        start_room = search.search_object("Adventurer Guild Entrance", typeclass="typeclasses.rooms.Room")
        if start_room:
            self.home = start_room[0]
            self.location = start_room[0]
        else:
            # Will be set by at_server_start world builder
            pass
        
    def at_pre_puppet(self, account, **kwargs):
        """Called just before puppeting."""
        pass
        
    def at_post_puppet(self, **kwargs):
        """
        Called just after puppeting (after account has connected).
        IOM-style greeting.
        """
        super().at_post_puppet(**kwargs)
        
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
        return getattr(self.db, stat_name, 50)
        
    def modify_stat(self, stat, delta):
        """Adjust a stat by delta, bounded 1-100."""
        current = getattr(self.db, stat, 50)
        new_val = max(1, min(100, current + delta))
        setattr(self.db, stat, new_val)
        return new_val
        
    def add_experience(self, amount):
        """Add XP and check for level up."""
        self.db.experience += amount
        if self.db.experience >= self.db.next_level:
            self.level_up()
            
    def level_up(self):
        """Handle level advancement (IOM formula)."""
        self.db.level += 1
        
        # IOM stat gains per level
        self.db.strength += 2
        self.db.dexterity += 2
        self.db.constitution += 1
        self.db.intelligence += 1
        self.db.wisdom += 1
        self.db.stamina += 2
        
        # Regeneration increases
        self.db.hp_regen = getattr(self.db, 'hp_regen', 10) + 2
        self.db.sp_regen = getattr(self.db, 'sp_regen', 5) + 1
        self.db.ep_regen = getattr(self.db, 'ep_regen', 5) + 1
        
        # Increase max resources based on CON/STA
        con_bonus = self.db.constitution // 10
        sta_bonus = self.db.stamina // 10
        self.db.hp_max += 20 + con_bonus * 5
        self.db.ep_max += 15 + sta_bonus * 3
        self.db.sp_max += 10 + (self.db.intelligence // 10) * 3
        
        # Full heal on level up
        self.db.hp = self.db.hp_max
        self.db.ep = self.db.ep_max
        self.db.sp = self.db.sp_max
        
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
        """Return formatted score sheet (IOM-style)."""
        race_name = self.db.race if hasattr(self.db, "race") else "Unknown"
        guild_name = self.db.guild if self.db.guild else "None"
        guild_lvl = self.db.guild_level
        
        total_rooms = 17750  # IOM world size estimate
        explored = len(self.db.rooms_explored)
        pct = (explored / total_rooms) * 100 if total_rooms > 0 else 0
        
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
| Strength     : {self.db.strength:>3} | Hit Points     : {self.db.hp:>4} ({self.db.hp_max:>4}) | AC       : {self.db.ac}
| Dexterity    : {self.db.dexterity:>3} | Spell Points   : {self.db.sp:>4} ({self.db.sp_max:>4}) | Size     : {self.db.size}
| Constitution : {self.db.constitution:>3} | Endurance Pts. : {self.db.ep:>4} ({self.db.ep_max:>4}) | Weight   : {self.db.weight} lb
| Stamina      : {self.db.stamina:>3} | Hunger         : {self.db.hunger}       | Stealth  : {self.db.stealth}%
| Intelligence : {self.db.intelligence:>3} | Wimpy          : {self.db.wimpy}%            | Hiding   : {'Yes' if self.db.hiding else 'No'}
| Wisdom       : {self.db.wisdom:>3} | Alignment      : {self.db.alignment}       | Poisoned : {'Yes' if self.db.poisoned else 'No'}
| Charisma     : {self.db.charisma:>3} | TaskPts. : {self.db.task_points}        
|----------------------------------------------------------------------------|
| alpha   : {guild_name} ({guild_lvl})                      | Mail          : {self.db.mail_unread}/{self.db.mail_count}           |
|                                            | Kills         : {self.db.kills}             |
`----------------------------------------------------------------------------'
hp({self.db.hp}/{self.db.hp_max}) sp({self.db.sp}/{self.db.sp_max}) ep({self.db.ep}/{self.db.ep_max}) >"""
