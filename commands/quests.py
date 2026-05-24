"""
Red Dragon MUD - Quest Commands
Player commands for quest management
"""

from evennia import Command, CmdSet
from evennia.utils import search
from world.quests import (
    QUESTS, get_quest_log, get_active_quests, get_completed_quests,
    can_start_quest, start_quest, update_quest_progress, complete_quest,
    QUEST_ACTIVE, QUEST_COMPLETED, QUEST_FAILED
)

class CmdQuestLog(Command):
    """
    View your quest log
    
    Usage:
        quest
        quest log
        quest active
        quest completed
    """
    
    key = "quest"
    aliases = ["quests", "q"]
    locks = "cmd:all()"
    
    def func(self):
        if not self.args:
            self.show_quest_summary()
        elif self.args.strip().lower() in ["log", "active", "completed"]:
            if "active" in self.args.lower():
                self.show_active_quests()
            elif "completed" in self.args.lower():
                self.show_completed_quests()
            else:
                self.show_quest_summary()
        else:
            self.caller.msg("Usage: quest [log/active/completed]")
    
    def show_quest_summary(self):
        """Show summary of all quest activity."""
        active = get_active_quests(self.caller)
        completed = get_completed_quests(self.caller)
        
        self.caller.msg("|c" + "="*50 + "|n")
        self.caller.msg("|yQuest Log|n")
        self.caller.msg("|c" + "="*50 + "|n")
        
        self.caller.msg(f"|wActive quests: {len(active)}|n")
        self.caller.msg(f"|wCompleted quests: {len(completed)}|n")
        
        if active:
            self.caller.msg("\n|yActive Quests:|n")
            for qid in active:
                quest = QUESTS.get(qid)
                if quest:
                    log = get_quest_log(self.caller)
                    progress = log[qid]["objectives"]
                    completed_obj = sum(1 for o in progress if o["completed"])
                    total_obj = len(progress)
                    self.caller.msg(f"  |w{quest.title}|n [{completed_obj}/{total_obj}]")
        
        if completed:
            self.caller.msg("\n|gRecently Completed:|n")
            for qid in completed[-5:]:  # Show last 5
                quest = QUESTS.get(qid)
                if quest:
                    self.caller.msg(f"  |g✓ {quest.title}|n")
        
        self.caller.msg("|c" + "="*50 + "|n")
    
    def show_active_quests(self):
        """Show detailed active quest information."""
        active = get_active_quests(self.caller)
        
        if not active:
            self.caller.msg("|yYou have no active quests.|n")
            return
        
        for qid in active:
            quest = QUESTS.get(qid)
            if not quest:
                continue
            
            log = get_quest_log(self.caller)
            objectives = log[qid]["objectives"]
            
            self.caller.msg(f"\n|c{'='*40}|n")
            self.caller.msg(f"|y{quest.title}|n")
            self.caller.msg(f"|w{quest.description}|n")
            self.caller.msg(f"|cType:|n {quest.quest_type}")
            
            self.caller.msg("\n|wObjectives:|n")
            for i, obj in enumerate(objectives):
                status = "|g✓|n" if obj["completed"] else "|r○|n"
                progress = f" ({obj['current']}/{obj.get('target', 1)})" if not obj["completed"] else ""
                self.caller.msg(f"  {status} {obj['desc']}{progress}")
    
    def show_completed_quests(self):
        """Show completed quests."""
        completed = get_completed_quests(self.caller)
        
        if not completed:
            self.caller.msg("|yYou haven't completed any quests yet.|n")
            return
        
        self.caller.msg("\n|gCompleted Quests:|n")
        for qid in completed:
            quest = QUESTS.get(qid)
            if quest:
                rewards = quest.rewards
                reward_str = []
                if "exp" in rewards:
                    reward_str.append(f"{rewards['exp']} XP")
                if "gold" in rewards:
                    reward_str.append(f"{rewards['gold']} gold")
                if "item" in rewards and rewards["item"]:
                    reward_str.append(rewards["item"])
                
                reward_text = ", ".join(reward_str) if reward_str else "None"
                self.caller.msg(f"  |g✓ {quest.title}|n |w(Rewards: {reward_text})|n")


class CmdQuestStart(Command):
    """
    Start a quest from a quest giver
    
    Usage:
        quest start <quest_name>
        
    Must be near the appropriate quest giver.
    """
    
    key = "quest start"
    aliases = ["accept quest", "take quest"]
    locks = "cmd:all()"
    
    def func(self):
        if not self.args:
            self.caller.msg("Usage: quest start <quest_name>")
            return
        
        quest_name = self.args.strip().lower()
        
        # Find quest by name or ID
        quest_id = None
        for qid, quest in QUESTS.items():
            if quest_name in qid.lower() or quest_name in quest.title.lower():
                quest_id = qid
                break
        
        if not quest_id:
            self.caller.msg(f"|rNo quest found matching '{quest_name}'.|n")
            return
        
        # Check if near quest giver
        quest = QUESTS[quest_id]
        if quest.giver:
            # Check if quest giver is in room
            giver_found = False
            for obj in self.caller.location.contents:
                if hasattr(obj, 'db') and getattr(obj.db, 'is_quest_giver', False):
                    if getattr(obj.db, 'quest_id', None) == quest_id:
                        giver_found = True
                        break
            
            if not giver_found:
                self.caller.msg(f"|rYou must find the quest giver for '{quest.title}' to start this quest.|n")
                return
        
        # Start quest
        success, message = start_quest(self.caller, quest_id)
        if success:
            self.caller.msg(f"|g{message}|n")
            self.caller.msg(f"\n|w{quest.title}|n")
            self.caller.msg(f"{quest.description}\n")
            self.caller.msg("|wObjectives:|n")
            for obj in quest.objectives:
                self.caller.msg(f"  |r○|n {obj['desc']}")
        else:
            self.caller.msg(f"|r{message}|n")


class QuestCmdSet(CmdSet):
    """CmdSet with quest commands."""
    
    key = "QuestCmdSet"
    priority = 1
    
    def at_cmdset_creation(self):
        self.add(CmdQuestLog())
        self.add(CmdQuestStart())


# Quest giver NPC setup
def setup_quest_giver(npc, quest_id):
    """
    Setup an NPC as a quest giver.
    
    Args:
        npc: The NPC object
        quest_id: The quest this NPC gives
    """
    npc.db.is_quest_giver = True
    npc.db.quest_id = quest_id
    
    quest = QUESTS.get(quest_id)
    if quest:
        # Add quest info to NPC description
        desc = getattr(npc.db, 'desc', "")
        if desc:
            npc.db.desc = desc + f"\n\n|cQuest Available:|n {quest.title}\n|w{quest.description}|n\n|yType 'quest start {quest_id}' to accept.|n"
