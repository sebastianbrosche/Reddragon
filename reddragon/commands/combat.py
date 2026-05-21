"""
Red Dragon MUD - Combat Commands
Based on Islands of Myth combat system
"""

from evennia import Command
from evennia import CmdSet
from evennia.utils import search
from commands.economy import CmdBuy, CmdSell, CmdList, CmdDeposit, CmdWithdraw, CmdBalance

class CmdKill(Command):
    """
    Attack a target.
    
    Usage:
        kill <target>
    """
    key = "kill"
    locks = "cmd:all()"
    
    def func(self):
        caller = self.caller
        target_name = self.args.strip()
        
        if not target_name:
            caller.msg("Kill whom?")
            return
            
        # Find target in room
        target = caller.search(target_name, location=caller.location)
        if not target:
            return
            
        if not hasattr(target.db, "is_mob") or not target.db.is_mob:
            caller.msg(f"You can't kill {target.key}.")
            return
            
        if target.db.ai_state == "dead":
            caller.msg(f"{target.key} is already dead.")
            return
            
        # Start combat using tick script
        from typeclasses.scripts.combat import start_combat
        
        caller.msg(f"You are now in combat with {target.key}.")
        caller.location.msg_contents(
            f"{caller.key} attacks {target.key}!",
            exclude=caller
        )
        
        script = start_combat(caller, target)
        if script:
            # Initial hit as part of initiating combat
            script.execute_round(caller, target)
        else:
            caller.msg("Combat could not be started.")


class CmdScore(Command):
    """
    Display character score sheet (IOM-style).
    
    Usage:
        score
        sc
    """
    key = "score"
    aliases = ["sc", "stats"]
    locks = "cmd:all()"
    
    def func(self):
        caller = self.caller
        
        if hasattr(caller, 'get_score_display'):
            caller.msg(caller.get_score_display())
        else:
            caller.msg("You have no score to display.")


class CmdSkills(Command):
    """
    Display character skills (IOM-style).
    
    Usage:
        skills
        sk
    """
    key = "skills"
    aliases = ["sk", "skill"]
    locks = "cmd:all()"
    
    def func(self):
        caller = self.caller
        
        # Get guild skills
        guild = getattr(caller.db, 'guild', None)
        guild_level = getattr(caller.db, 'guild_level', 0)
        
        if not guild:
            caller.msg("You have no guild skills yet.")
            return
            
        # Format skills display (IOM-style)
        skills = getattr(caller.db, 'skills', {})
        
        header = f"-=-=-| {guild.capitalize()} |-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-"
        footer = "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-"
        
        skill_lines = []
        skill_names = sorted(skills.keys())
        
        # Display in two columns
        for i in range(0, len(skill_names), 2):
            left = skill_names[i]
            left_pct = skills[left]
            left_str = f"  {left:<28}: {left_pct:>3}%"
            
            if i + 1 < len(skill_names):
                right = skill_names[i + 1]
                right_pct = skills[right]
                right_str = f"  {right:<28}: {right_pct:>3}%"
                skill_lines.append(f"{left_str}  |{right_str}")
            else:
                skill_lines.append(left_str)
        
        if not skill_lines:
            skill_lines.append("  (No skills learned yet)")
            
        output = f"{header}\n" + "\n".join(skill_lines) + f"\n{footer}"
        caller.msg(output)


class CmdLoot(Command):
    """
    Loot a corpse.
    
    Usage:
        loot <corpse>
    """
    key = "loot"
    locks = "cmd:all()"
    
    def func(self):
        caller = self.caller
        target_name = self.args.strip()
        
        if not target_name:
            caller.msg("Loot what?")
            return
            
        target = caller.search(target_name, location=caller.location)
        if not target:
            return
            
        if not hasattr(target.db, 'is_corpse') or not target.db.is_corpse:
            caller.msg("That's not a corpse.")
            return
            
        # Check for loot on corpse
        loot = []
        for obj in target.contents:
            obj.move_to(caller, quiet=True)
            loot.append(obj.key)
            
        if loot:
            caller.msg(f"You loot: {', '.join(loot)}")
        else:
            caller.msg("You find nothing of value.")
            
        # Remove corpse
        target.delete()


class CmdEat(Command):
    """
    Eat something (especially corpses for healing).
    
    Usage:
        eat <item>
    """
    key = "eat"
    locks = "cmd:all()"
    
    def func(self):
        caller = self.caller
        target_name = self.args.strip()
        
        if not target_name:
            caller.msg("Eat what?")
            return
            
        target = caller.search(target_name, location=caller.location)
        if not target:
            # Check inventory
            target = caller.search(target_name, location=caller)
            if not target:
                return
                
        if not hasattr(target.db, 'edible') or not target.db.edible:
            if not hasattr(target.db, 'is_corpse') or not target.db.is_corpse:
                caller.msg("You can't eat that.")
                return
            
        # Consume and heal
        heal_hp = getattr(target.db, 'heal_hp', 20)
        heal_ep = getattr(target.db, 'heal_ep', 10)
        
        old_hp = caller.db.hp
        old_ep = caller.db.ep
        
        caller.db.hp = min(caller.db.hp + heal_hp, caller.db.hp_max)
        caller.db.ep = min(caller.db.ep + heal_ep, caller.db.ep_max)
        
        hp_gained = caller.db.hp - old_hp
        ep_gained = caller.db.ep - old_ep
        
        caller.msg(f"You devour {target.key}.")
        if hp_gained > 0:
            caller.msg(f"You feel better. (+{hp_gained} HP)")
        if ep_gained > 0:
            caller.msg(f"You feel refreshed. (+{ep_gained} EP)")
            
        caller.db.hunger = "Satisfied"
        
        caller.location.msg_contents(
            f"{caller.key} eats {target.key}.",
            exclude=caller
        )
        
        target.delete()


class CmdWarp(Command):
    """
    Warp to the Adventurers' Guild.
    
    Usage:
        warp
    """
    key = "warp"
    locks = "cmd:all()"
    
    def func(self):
        caller = self.caller
        
        # Find the guild entrance
        from evennia import search_object
        guild = search_object("Adventurer Guild Entrance", typeclass="typeclasses.rooms.Room")
        
        if not guild:
            caller.msg("You can't warp right now.")
            return
            
        guild = guild[0]
        
        caller.msg("You warp, bend and fold into a small dot which disappears!")
        caller.location.msg_contents(
            f"{caller.key} warps away in a flash of light!",
            exclude=caller
        )
        
        caller.move_to(guild, quiet=True)
        caller.msg("You arrive at the Adventure Guild.")
        
        # Trigger room look
        guild.at_object_receive(caller, caller.location)


class CmdCombatSilence(Command):
    """
    Toggle combat silence mode - suppresses combat messages for cleaner stat capture.
    
    Usage:
        combat silence
    """
    key = "combat silence"
    locks = "cmd:all()"
    
    def func(self):
        caller = self.caller
        
        current = getattr(caller.db, 'combat_silence', False)
        caller.db.combat_silence = not current
        
        if caller.db.combat_silence:
            caller.msg("Combat silence is now ON. Combat messages will be suppressed.")
        else:
            caller.msg("Combat silence is now OFF. Combat messages will show normally.")


class CmdGetAll(Command):
    """
    Get all items from a container or corpse.
    
    Usage:
        get all from <container/corpse>
        get all
    """
    key = "get all"
    locks = "cmd:all()"
    
    def func(self):
        caller = self.caller
        
        if not self.args:
            # Get all items in room
            items = [obj for obj in caller.location.contents 
                    if not hasattr(obj.db, 'is_mob') and obj != caller]
            
            if not items:
                caller.msg("There is nothing here to get.")
                return
                
            for item in items:
                item.move_to(caller, quiet=True)
                caller.msg(f"You get {item.key}.")
            return
            
        # Parse "from corpse" etc
        args = self.args.strip().lower()
        if args.startswith("from "):
            target = args[5:].strip()
            
            # Find target in room
            container = None
            for obj in caller.location.contents:
                if target in obj.key.lower():
                    container = obj
                    break
                    
            if not container:
                caller.msg(f"There is no {target} here.")
                return
                
            # Get all from container
            items = [obj for obj in container.contents]
            if not items:
                caller.msg(f"There is nothing in {container.key}.")
                return
                
            for item in items:
                item.move_to(caller, quiet=True)
                caller.msg(f"You get {item.key} from {container.key}.")
        else:
            caller.msg("Usage: get all from <container>")


class CmdWimpy(Command):
    """
    Set wimpy percentage (auto-flee when HP drops below this %).
    
    Usage:
        wimpy <percentage>
    """
    key = "wimpy"
    locks = "cmd:all()"
    
    def func(self):
        caller = self.caller
        
        if not self.args:
            current = caller.db.wimpy
            caller.msg(f"Your wimpy is set to {current}%.")
            return
            
        try:
            pct = int(self.args.strip())
            pct = max(0, min(100, pct))
            caller.db.wimpy = pct
            caller.msg(f"Wimpy set to {pct}%.")
        except ValueError:
            caller.msg("Usage: wimpy <0-100>")


class CmdWho(Command):
    """
    List who is currently playing.
    
    Usage:
        who
    """
    key = "who"
    locks = "cmd:all()"
    
    def func(self):
        from evennia import search_object
        
        players = [obj for obj in search_object("*") 
                    if hasattr(obj, 'db') and hasattr(obj.db, 'level')]
        
        output = "=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n"
        output += "  Players currently online:\n"
        output += "=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n"
        
        for player in players:
            if hasattr(player, 'sessions') and player.sessions.count() > 0:
                level = getattr(player.db, 'level', 1)
                race = getattr(player.db, 'race', 'Unknown')
                guild = getattr(player.db, 'guild', None)
                guild_str = f" ({guild})" if guild else ""
                output += f"  {player.key:15} - Level {level:3} {race}{guild_str}\n"
                
        output += "=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n"
        self.caller.msg(output)


class CombatCmdSet(CmdSet):
    """
    Holds all combat commands.
    """
    key = "combat"
    
    def at_cmdset_creation(self):
        self.add(CmdKill)
        self.add(CmdScore)
        self.add(CmdSkills)
        self.add(CmdLoot)
        self.add(CmdEat)
        self.add(CmdWarp)
        self.add(CmdCombatSilence)
        self.add(CmdGetAll)
        self.add(CmdWimpy)
        self.add(CmdWho)
        # Economy commands
        self.add(CmdBuy)
        self.add(CmdSell)
        self.add(CmdList)
        self.add(CmdDeposit)
        self.add(CmdWithdraw)
        self.add(CmdBalance)
