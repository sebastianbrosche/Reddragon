"""
Red Dragon MUD - Combat Commands
Based on Islands of Myth combat system
"""

from evennia import Command
from evennia import CmdSet
from evennia.utils import search
from commands.utility import CmdVersion, CmdChat, CmdToggleChat
from commands.ai_dm_commands import (
    CmdDivineStatus, CmdPray, CmdAchievements, CmdDivineLog,
    CmdForceDivine, CmdSetDivinePersonality
)
from evennia.contrib.game_systems.mail import mail
from evennia.contrib.rpg.rpsystem.rpsystem import RPSystemCmdSet
from evennia.contrib.grid.extended_room.extended_room import ExtendedRoomCmdSet
from evennia.contrib.grid.simpledoor.simpledoor import SimpleDoorCmdSet
from evennia.contrib.base_systems.ingame_python.commands import CmdCallback
from evennia.contrib.rpg.dice.dice import CmdDice
from evennia.contrib.game_systems.gendersub.gendersub import SetGender
from evennia.contrib.rpg.health_bar.health_bar import display_meter
from evennia.contrib.game_systems.clothing.clothing import ClothedCharacterCmdSet
from evennia.contrib.game_systems.barter.barter import CmdOffer, CmdAccept, CmdDecline, CmdEvaluate, CmdStatus
from evennia.contrib.game_systems.crafting.crafting import CraftingCmdSet
from evennia.contrib.base_systems.ingame_reports.reports import ReportsCmdSet
from evennia.contrib.game_systems.multidescer.multidescer import CmdMultiDesc
from evennia.contrib.rpg.character_creator.character_creator import ContribCmdCharCreate
from world.buffs import IOM_BUFFS, apply_buff, remove_buff

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


class CmdMove(Command):
    """
    Move in a direction.
    
    Usage:
        n, s, e, w, ne, nw, se, sw, u, d
        north, south, east, west, northeast, northwest, southeast, southwest, up, down
    """
    key = "move"
    aliases = ["n", "s", "e", "w", "ne", "nw", "se", "sw", "u", "d",
               "north", "south", "east", "west", 
               "northeast", "northwest", "southeast", "southwest",
               "up", "down"]
    locks = "cmd:all()"
    
    def func(self):
        caller = self.caller
        location = caller.location
        
        if not location:
            caller.msg("You are nowhere.")
            return
        
        # Normalize direction
        direction = self.cmdstring.lower()
        
        # Map aliases to full names for matching
        alias_map = {
            "n": "north", "s": "south", "e": "east", "w": "west",
            "ne": "northeast", "nw": "northwest", "se": "southeast", "sw": "southwest",
            "u": "up", "d": "down",
        }
        
        # Check if the typed command is an alias - search for both
        search_names = [direction]
        if direction in alias_map:
            search_names.append(alias_map[direction])
        
        # Find matching exit
        found_exit = None
        for exit_obj in location.exits:
            exit_key = exit_obj.key.lower()
            exit_aliases = [a.lower() for a in exit_obj.aliases.all()]
            
            if direction in (exit_key, *exit_aliases):
                found_exit = exit_obj
                break
            # Also check if the full name matches any alias or key
            for search_name in search_names:
                if search_name in (exit_key, *exit_aliases):
                    found_exit = exit_obj
                    break
            if found_exit:
                break
        
        if not found_exit:
            caller.msg(f"You can't go {direction}.")
            return
        
        # Try to traverse
        if found_exit.access(caller, "traverse"):
            found_exit.at_traverse(caller, found_exit.destination)
        else:
            caller.msg(f"You can't go {direction}.")


from commands.summary import CmdSummary, init_session_stats


class CmdBuffs(Command):
    """
    View and manage active buffs and debuffs.
    
    Usage:
        buffs
        affects
    """
    key = "buffs"
    aliases = ["affects", "aff", "buff"]
    locks = "cmd:all()"
    
    def func(self):
        caller = self.caller
        
        if not hasattr(caller, 'buffs') or not caller.buffs.all:
            caller.msg("You have no active buffs or debuffs.")
            return
        
        lines = []
        lines.append("|wActive Buffs & Debuffs:|n")
        lines.append("-" * 40)
        
        for buff in caller.buffs.all:
            name = buff.name
            duration = buff.timeleft
            stacks = buff.stacks
            flava = buff.flava
            
            if duration < 0:
                dur_str = "Permanent"
            else:
                dur_str = f"{duration:.0f}s"
            
            stack_str = f" x{stacks}" if stacks > 1 else ""
            lines.append(f"|y{name}{stack_str}|n ({dur_str})")
            lines.append(f"  {flava}")
        
        caller.msg("\n".join(lines))


class CmdSail(Command):
    """
    Set sail into the ocean wilderness.
    
    Usage:
        sail
        
    Enters the ocean wilderness map for sailing between islands.
    """
    key = "sail"
    locks = "cmd:all()"
    
    def func(self):
        caller = self.caller
        
        # Check if at a port or dock
        if not (hasattr(caller.location, 'db') and getattr(caller.location.db, 'is_port', False)):
            caller.msg("You need to be at a port or dock to sail.")
            return
        
        caller.msg("You cast off and set sail into the open ocean...")
        from world.wilderness_maps import enter_ocean_wilderness
        enter_ocean_wilderness(caller)


class CmdReturn(Command):
    """
    Return from the wilderness to the nearest port.
    
    Usage:
        return
        dock
    """
    key = "return"
    aliases = ["dock"]
    locks = "cmd:all()"
    
    def func(self):
        caller = self.caller
        
        # Check if in wilderness
        from evennia.contrib.grid import wilderness
        if not wilderness.get_wilderness_script(caller):
            caller.msg("You are not at sea.")
            return
        
        caller.msg("You sail back to the nearest port...")
        wilderness.leave_wilderness(caller)


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
        self.add(CmdMove)
        self.add(CmdSail)
        self.add(CmdReturn)
        self.add(CmdWho)
        self.add(CmdSummary)
        # Version
        self.add(CmdVersion)
        # Chat
        self.add(CmdChat)
        self.add(CmdToggleChat)
        # RP System (sdescs, poses, recog, emotes)
        self.add(RPSystemCmdSet())
        self.add(CmdDivineStatus)
        self.add(CmdPray)
        self.add(CmdAchievements)
        self.add(CmdDivineLog)
        self.add(CmdForceDivine)
        self.add(CmdSetDivinePersonality)
        # Mail
        self.add(mail.CmdMail())
        # Buffs
        self.add(CmdBuffs)
        # Extended Room (weather, time-of-day, details)
        self.add(ExtendedRoomCmdSet())
        # Simple Door (open/close/lock doors)
        self.add(SimpleDoorCmdSet())
        # In-game Python (event callbacks)
        self.add(CmdCallback())
        # Dice roller (1d20 + 5, etc)
        self.add(CmdDice())
        # Clothing (wear, remove, cover, uncover)
        self.add(ClothedCharacterCmdSet())
        # Barter (trade, offer, accept, decline, evaluate, status)
        self.add(CmdOffer())
        self.add(CmdAccept())
        self.add(CmdDecline())
        self.add(CmdEvaluate())
        self.add(CmdStatus())
        # Crafting
        self.add(CraftingCmdSet())
        # Gender setting
        self.add(SetGender())
        # Containers (put, get from containers)
        from evennia.contrib.game_systems.containers import ContainerCmdSet
        self.add(ContainerCmdSet())
        # Storage (store, retrieve, list in storage rooms)
        from evennia.contrib.game_systems.storage.storage import StorageCmdSet
        self.add(StorageCmdSet())
        # In-Game Reports (bug, idea, player reports)
        self.add(ReportsCmdSet())
        # Multi-Describer (+desc command for multiple character descriptions)
        self.add(CmdMultiDesc())
        # Character Creator (interactive chargen menu)
        self.add(ContribCmdCharCreate())
        # Slow Exit (setspeed, stop commands)
        from evennia.contrib.grid.slow_exit.slow_exit import SlowExitCmdSet
        self.add(SlowExitCmdSet())
        # In-Game Map Display (ascii map command)
        from evennia.contrib.grid.ingame_map_display.ingame_map_display import MapDisplayCmdSet
        self.add(MapDisplayCmdSet())
        # Map Builder (@mapbuilder command for builders)
        from evennia.contrib.grid.mapbuilder.mapbuilder import CmdMapBuilder
        self.add(CmdMapBuilder())
        # LLM NPC talk command (requires LLM server config)
        from evennia.contrib.rpg.llm.llm_npc import CmdLLMTalk
        self.add(CmdLLMTalk())
        # Ferry system (sail between islands)
        from typeclasses.ferry import FerryCmdSet
        self.add(FerryCmdSet())
        # Character stat rolling system
        from commands.chargen_roll import RollCmdSet
        self.add(RollCmdSet())
        # Quest system
        from commands.quests import QuestCmdSet
        self.add(QuestCmdSet())
        # Monster system
        from commands.monsters import MonsterCmdSet
        self.add(MonsterCmdSet())
        self.add(CmdBuy)
        self.add(CmdSell)
        self.add(CmdList)
        self.add(CmdDeposit)
        self.add(CmdWithdraw)
        self.add(CmdBalance)
        # Guild commands (join, train, guilds)
        from commands.guild import CmdJoinGuild, CmdGuilds, CmdTrain
        self.add(CmdJoinGuild)
        self.add(CmdGuilds)
        self.add(CmdTrain)
        # Shapeshifter commands
        from commands.shapeshifter import (
            CmdShapeShift, CmdReverseTransformation, CmdMigrate,
            CmdBite, CmdClaw, CmdHerbGathering, CmdMagicalGrowth, CmdScavengeWood
        )
        self.add(CmdShapeShift)
        self.add(CmdReverseTransformation)
        self.add(CmdMigrate)
        self.add(CmdBite)
        self.add(CmdClaw)
        self.add(CmdHerbGathering)
        self.add(CmdMagicalGrowth)
        self.add(CmdScavengeWood)
        # Reincarnation commands
        from commands.reincarnation import CmdSacrifice, CmdReincarnate
        self.add(CmdSacrifice)
        self.add(CmdReincarnate)
        # Task points commands
        from commands.taskpoints import CmdWish, CmdTaskPoints
        self.add(CmdWish)
        self.add(CmdTaskPoints)
