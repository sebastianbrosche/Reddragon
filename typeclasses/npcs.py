"""
Red Dragon MUD - NPC / Mob Typeclass
Based on Islands of Myth combat system
"""

from evennia import DefaultCharacter
import random

class NPC(DefaultCharacter):
    """
    Non-player character / mob.
    
    Mobs in IOM:
    - Have HP, level, damage
    - Can be aggressive or passive
    - Drop loot on death
    - Give XP when killed
    """
    
    def at_object_creation(self):
        super().at_object_creation()
        
        # Mob metadata
        self.db.is_mob = True
        self.db.is_npc = True  # For talk command detection
        self.db.level = 1
        self.db.xp_value = 10
        self.db.gold_value = 0
        
        # Behavior
        self.db.aggressive = False
        self.db.aggro_level = 0  # Level difference to trigger aggression
        self.db.wandering = False
        self.db.wander_chance = 0.05
        
        # Combat stats
        self.db.hp = 50
        self.db.hp_max = 50
        self.db.damage_min = 1
        self.db.damage_max = 5
        self.db.ac = 0
        self.db.hit_chance = 0.7
        
        # Loot
        self.db.loot_table = []  # [(obj_key, probability), ...]
        self.db.corpse_edible = False
        
        # AI state
        self.db.target = None
        self.db.ai_state = "idle"  # idle, combat, flee, dead
        
    def at_talk(self, caller):
        """Called when a player uses 'talk' on this NPC. Override in subclasses."""
        caller.msg(f"{self.key} looks at you but has nothing to say.")
        
    def at_character_enter(self, character):
        """Called when a character enters the room."""
        if self.db.aggressive:
            level_diff = character.db.level - self.db.level
            if level_diff <= self.db.aggro_level:
                self.db.target = character
                self.db.ai_state = "combat"
                character.msg(f"{self.key} attacks you!")
                self.combat_attack(character)
                
    def combat_attack(self, target):
        """Attack a target."""
        import random
        
        if random.random() > self.db.hit_chance:
            target.msg(f"{self.key} misses you.")
            return
            
        damage = random.randint(self.db.damage_min, self.db.damage_max)
        target.db.hp -= damage
        target.msg(f"{self.key} hits you for {damage} damage!")
        
        if target.db.hp <= 0:
            target.db.hp = 0
            self.kill_target(target)
            
    def kill_target(self, target):
        """Handle killing a character."""
        target.msg(f"You have been killed by {self.key}!")
        # Handle death mechanics (respawn, XP loss, etc.)
        
    def take_damage(self, damage, attacker):
        """Take damage from an attacker."""
        self.db.hp -= damage
        
        if self.db.hp <= 0:
            self.die(attacker)
            return True
        return False
        
    def die(self, killer):
        """Handle mob death."""
        self.db.ai_state = "dead"
        
        # Award XP
        if killer and hasattr(killer, 'add_experience'):
            xp = int(self.db.xp_value * self.db.xp_rate if hasattr(self.db, 'xp_rate') else self.db.xp_value)
            killer.add_experience(xp)
            killer.msg(f"You gain {xp} experience from killing {self.key}.")
            
            # Track kills
            killer.db.kills += 1
        
        # Drop loot
        self.drop_loot()
        
        # Create corpse
        corpse = self.create_corpse()
        
        # Remove self from room (or move to void)
        self.move_to(None, quiet=True)
        
    def create_corpse(self):
        """Create a corpse object."""
        from evennia import create_object
        corpse = create_object("typeclasses.objects.Object", 
                               key=f"corpse of {self.key}",
                               location=self.location)
        corpse.db.desc = f"The remains of {self.key} lie here."
        corpse.db.is_corpse = True
        corpse.db.edible = self.db.corpse_edible
        corpse.db.mob_source = self.key
        return corpse
        
    def drop_loot(self):
        """Drop loot on death."""
        for item_key, probability in self.db.loot_table:
            if random.random() < probability:
                # Create and drop item
                pass
                
    def tick_ai(self):
        """AI tick - called periodically."""
        if self.db.ai_state == "combat" and self.db.target:
            if self.db.target.location == self.location:
                self.combat_attack(self.db.target)
            else:
                self.db.target = None
                self.db.ai_state = "idle"
                
        elif self.db.wandering and self.db.ai_state == "idle":
            if random.random() < self.db.wander_chance:
                self.wander()
                
    def wander(self):
        """Random movement."""
        import random
        exits = [ex for ex in self.location.exits if ex.access(self, "traverse")]
        if exits:
            exit = random.choice(exits)
            self.move_to(exit.destination)


class Earwig(NPC):
    """Low-level mob found in Yensidland/LobeLands."""
    
    def at_object_creation(self):
        super().at_object_creation()
        
        self.key = "an earwig"
        self.db.level = 1
        self.db.xp_value = 15
        self.db.gold_value = 0
        
        self.db.hp = 30
        self.db.hp_max = 30
        self.db.damage_min = 1
        self.db.damage_max = 3
        self.db.ac = 0
        self.db.hit_chance = 0.6
        
        self.db.aggressive = False
        self.db.wandering = True
        self.db.wander_chance = 0.1
        
        self.db.corpse_edible = True
        self.db.loot_table = []


class Bat(NPC):
    """Low-level flying mob."""
    
    def at_object_creation(self):
        super().at_object_creation()
        
        self.key = "a bat"
        self.db.level = 1
        self.db.xp_value = 12
        self.db.gold_value = 0
        
        self.db.hp = 25
        self.db.hp_max = 25
        self.db.damage_min = 1
        self.db.damage_max = 4
        self.db.ac = 0
        self.db.hit_chance = 0.65
        
        self.db.aggressive = False
        self.db.wandering = True
        self.db.wander_chance = 0.15
        
        self.db.corpse_edible = True


class Snake(NPC):
    """Low-level snake mob."""
    
    def at_object_creation(self):
        super().at_object_creation()
        
        self.key = "a snake"
        self.db.level = 2
        self.db.xp_value = 20
        self.db.gold_value = 0
        
        self.db.hp = 40
        self.db.hp_max = 40
        self.db.damage_min = 2
        self.db.damage_max = 5
        self.db.ac = 0
        self.db.hit_chance = 0.7
        
        self.db.aggressive = True
        self.db.aggro_level = 2
        self.db.wandering = True
        self.db.wander_chance = 0.1
        
        self.db.corpse_edible = True
        self.db.traits = ["poisonous"]  # Chance to poison on hit


class JudgeAchman(NPC):
    """Achman the Judge - Controls leveling in the Adventurers Leveling Place."""
    
    def at_object_creation(self):
        super().at_object_creation()
        self.key = "Achman the Judge"
        self.db.is_mob = False  # Not attackable
        self.db.desc = (
            "A stern-faced figure seated in a high-backed chair built into "
            "a marble podium. He controls the levels of Red Dragon and has the "
            "power to create some of the strongest players. Talk to him if "
            "you wish to advance in your endeavors."
        )
        
    def at_talk(self, caller):
        """Open the judge menu when talked to."""
        from commands.judge import JudgeRoom
        
        if not isinstance(caller.location, JudgeRoom):
            caller.msg("Achman says, 'I can only judge you in the Level Room.'")
            return
            
        cost = caller.location.get_level_cost(caller)
        xp_needed = caller.db.next_level - caller.db.experience
        
        menu = f"""
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
Adventurers leveling place
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
  a)  General information                b)  List level costs              
  c)  Advance a level                    d)  Advance a level picking a stat
  e)  Advance several levels             q)  Quit                          
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

[abcdeq] 
        """
        caller.msg(menu)
        
        # Store state for menu handling
        caller.db.judge_menu_open = True


class NewbieNavigatorSisong(NPC):
    """Sisong the Newbie Navigator - Helps new players find newbie areas."""
    
    def at_object_creation(self):
        super().at_object_creation()
        self.key = "Sisong the Newbie Navigator"
        self.db.is_mob = False  # Not attackable
        self.db.desc = (
            "A cheerful guide who sings welcome songs to new adventurers. "
            "She can help you find your way to various newbie areas around "
            "the world."
        )
        
        self.db.newbie_areas = [
            ("Newbie Garden", 1),
            ("Valley of New Adventurers", 2),
            ("Spider Cave", 3),
            ("The Circus", 4),
            ("Monster Daycare", 5),
            ("Church", 6),
            ("Ocean", 7),
            ("Strawberry Fields", 8),
            ("Yensid Land", 9),
            ("Fire World", 10),
            ("Ice World", 11),
            ("Cat World", 12),
            ("Kobold Village", 13),
            ("Zoo", 14),
            ("Newbie Forest", 15),
            ("Ancient Tree", 16),
            ("Animal Nursery", 17),
            ("Swallow Moors", 18),
            ("Bee Hive", 19),
        ]
        
    def at_talk(self, caller):
        """Open the newbie navigator menu."""
        menu = """
Sisong's Newbie Information.
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
  1)  Misc. Information     2)  Newbie Areas          q)  Quit             

[12q] """
        caller.msg(menu)
        caller.db.sisong_menu = "main"
        
    def show_newbie_areas(self, caller):
        """Show the newbie areas submenu."""
        areas_text = "Newbie Areas\n"
        areas_text += "=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n"
        for i, (name, num) in enumerate(self.db.newbie_areas, 1):
            areas_text += f"  {i:>2})  {name:<30}\n"
        areas_text += "  m)  Return to Main Menu\n"
        areas_text += "  q)  Quit                            \n"
        areas_text += "[12345678910111213141516171819mq] "
        caller.msg(areas_text)
        caller.db.sisong_menu = "areas"