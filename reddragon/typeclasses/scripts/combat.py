"""
Darkstaff MUD - Combat Tick Script
Based on Islands of Myth automatic combat system

In IOM, combat is automatic:
1. Player initiates with 'kill <target>'
2. Combat runs in rounds (~2-3 seconds per round)
3. Each round: attacker hits, target hits back
4. Continues until death, flee, or disengagement

This script handles the periodic combat ticks.
"""

from evennia import DefaultScript
import random

class CombatTickScript(DefaultScript):
    """
    Script that runs combat rounds between two combatants.
    
    MudOS equivalent: The driver calls combat functions periodically
    for objects in combat state.
    """
    
    key = "combat_tick"
    desc = "Handles automatic combat rounds"
    interval = 3  # Seconds between rounds (IOM ~2-3s)
    persistent = True
    
    def at_script_creation(self):
        """Initialize combat state."""
        self.db.attacker = None
        self.db.target = None
        self.db.round = 0
        
    def at_repeat(self):
        """Called every interval - execute a combat round."""
        attacker = self.db.attacker
        target = self.db.target
        
        if not attacker or not target:
            self.stop()
            return
            
        # Check if either is dead or gone
        if not attacker.location or not target.location:
            self.stop()
            return
            
        if attacker.location != target.location:
            # Combatants moved apart
            attacker.db.combat_target = None
            target.db.target = None
            if hasattr(target.db, 'ai_state'):
                target.db.ai_state = "idle"
            self.stop()
            return
            
        self.db.round += 1
        self.execute_round(attacker, target)
        
    def execute_round(self, attacker, target):
        """Execute one combat round."""
        # Attacker hits target
        self.combat_hit(attacker, target)
        
        # Check if target is still alive and fighting back
        if (hasattr(target.db, 'hp') and target.db.hp > 0 and 
            getattr(target.db, 'combat_target', None) == attacker):
            self.combat_hit(target, attacker)
            
        # Check wimpy
        self.check_wimpy(attacker)
        self.check_wimpy(target)
        
    def combat_hit(self, attacker, defender):
        """One combatant hits another."""
        silence = getattr(attacker.db, 'combat_silence', False)
        
        # Calculate hit chance
        hit_chance = 0.7 + (getattr(attacker.db, 'dexterity', 50) / 200)
        hit_chance -= getattr(defender.db, 'ac', 0) / 100
        hit_chance = max(0.1, min(0.95, hit_chance))
        
        if random.random() > hit_chance:
            if not silence:
                attacker.msg(f"You miss {defender.key}.")
                defender.msg(f"{attacker.key} misses you.")
            return
            
        # Calculate damage
        str_bonus = getattr(attacker.db, 'strength', 50) // 20
        weapon_dmg = getattr(attacker.db, 'weapon_dmg', (1, 5))
        
        if hasattr(weapon_dmg, '__iter__'):
            dmg_min, dmg_max = weapon_dmg
        else:
            dmg_min, dmg_max = 1, 5
            
        damage = random.randint(dmg_min + str_bonus, dmg_max + str_bonus)
        
        # Apply damage
        if hasattr(defender.db, 'hp'):
            defender.db.hp -= damage
            
            if not silence:
                attacker.msg(f"You hit {defender.key} for {damage} damage!")
                defender.msg(f"{attacker.key} hits you for {damage} damage!")
                
                # Room message (exclude combatants)
                others = [obj for obj in attacker.location.contents 
                         if obj != attacker and obj != defender and 
                         hasattr(obj, 'msg')]
                for observer in others:
                    observer.msg(f"{attacker.key} hits {defender.key}.")
                    
            # Check death
            if defender.db.hp <= 0:
                defender.db.hp = 0
                self.handle_death(attacker, defender)
                
    def check_wimpy(self, combatant):
        """Check if combatant should flee due to wimpy setting."""
        wimpy = getattr(combatant.db, 'wimpy', 0)
        if wimpy <= 0:
            return
            
        hp_pct = (combatant.db.hp / combatant.db.hp_max) * 100
        if hp_pct <= wimpy:
            if hasattr(combatant.db, 'is_mob') and combatant.db.is_mob:
                # Mob flees
                combatant.msg("You flee in terror!")
                combatant.location.msg_contents(
                    f"{combatant.key} flees in terror!",
                    exclude=combatant
                )
                # Find a random exit and flee
                exits = [ex for ex in combatant.location.exits 
                        if ex.access(combatant, "traverse")]
                if exits:
                    import random
                    exit = random.choice(exits)
                    combatant.move_to(exit.destination)
                    combatant.db.target = None
                    combatant.db.ai_state = "idle"
            else:
                # Player wimpy flee
                combatant.msg("You flee in terror!")
                combatant.location.msg_contents(
                    f"{combatant.key} flees in terror!",
                    exclude=combatant
                )
                exits = [ex for ex in combatant.location.exits 
                        if ex.access(combatant, "traverse")]
                if exits:
                    import random
                    exit = random.choice(exits)
                    combatant.move_to(exit.destination)
                    combatant.db.combat_target = None
                    
    def handle_death(self, killer, victim):
        """Handle combat death."""
        victim.msg(f"You have been killed by {killer.key}!")
        killer.msg(f"You have killed {victim.key}!")
        
        # Award XP
        if hasattr(victim.db, 'xp_value') and hasattr(killer, 'add_experience'):
            xp = victim.db.xp_value
            killer.add_experience(xp)
            killer.msg(f"You gain {xp} experience from killing {victim.key}.")
            
        # Handle victim death
        if hasattr(victim, 'die'):
            victim.die(killer)
        else:
            # Simple death - move to void/respawn
            victim.msg("Everything goes dark...")
            
        # Stop combat script
        self.stop()
        
    def at_stop(self):
        """Clean up when script stops."""
        attacker = self.db.attacker
        target = self.db.target
        
        if attacker and hasattr(attacker.db, 'combat_target'):
            attacker.db.combat_target = None
        if target and hasattr(target.db, 'combat_target'):
            target.db.combat_target = None
            
        # Remove the script from both objects
        if attacker and self in attacker.scripts.all():
            attacker.scripts.stop(self.key)
        if target and self in target.scripts.all():
            target.scripts.stop(self.key)


def start_combat(attacker, target):
    """
    Start a combat tick script between two combatants.
    
    Args:
        attacker: The attacking character
        target: The target character
    """
    from evennia import create_script
    
    # Check if either is already in combat
    if (getattr(attacker.db, 'combat_target', None) or 
        getattr(target.db, 'combat_target', None)):
        # Already in combat
        return
        
    # Create and attach combat script
    script = create_script(CombatTickScript, 
                          key=f"combat_{attacker.id}_{target.id}",
                          obj=attacker)
    
    if script:
        script.db.attacker = attacker
        script.db.target = target
        attacker.db.combat_target = target
        target.db.combat_target = attacker
        
        if hasattr(target.db, 'ai_state'):
            target.db.ai_state = "combat"
            
    return script
