"""
Red Dragon MUD - Monster Commands
Player commands for monster interaction
"""

from evennia import Command, CmdSet
from world.monsters import MONSTERS, get_monster_data, create_monster, spawn_monsters_for_area

class CmdBestiary(Command):
    """
    View the monster bestiary
    
    Usage:
        bestiary
        bestiary <monster_name>
    """
    
    key = "bestiary"
    aliases = ["monsters", "mobs"]
    locks = "cmd:all()"
    
    def func(self):
        if not self.args:
            # Show list of all monsters
            self.caller.msg("|c" + "="*50 + "|n")
            self.caller.msg("|yMonster Bestiary|n")
            self.caller.msg("|c" + "="*50 + "|n")
            
            # Sort by level
            sorted_mobs = sorted(MONSTERS.items(), key=lambda x: x[1]["level"])
            
            for mob_id, data in sorted_mobs:
                level_color = "|g" if data["level"] <= 5 else "|y" if data["level"] <= 15 else "|r"
                self.caller.msg(f"  {level_color}{data['name']}|n (Lv{data['level']}) - {data['behavior']}")
            
            self.caller.msg("|c" + "="*50 + "|n")
            self.caller.msg("|wUse 'bestiary <name>' for details.|n")
        else:
            # Show specific monster details
            search_name = self.args.strip().lower()
            
            found = None
            for mob_id, data in MONSTERS.items():
                if search_name in mob_id or search_name in data["name"].lower():
                    found = (mob_id, data)
                    break
            
            if not found:
                self.caller.msg(f"|rNo monster found matching '{search_name}'.|n")
                return
            
            mob_id, data = found
            
            self.caller.msg(f"\n|c{'='*40}|n")
            self.caller.msg(f"|y{data['name'].capitalize()}|n")
            self.caller.msg(f"|cLevel:|n {data['level']}")
            self.caller.msg(f"|cHP:|n {data['hp']}")
            self.caller.msg(f"|cDamage:|n {data['damage']}")
            self.caller.msg(f"|cEXP:|n {data['exp']}")
            self.caller.msg(f"|cGold:|n {data['gold'][0]}-{data['gold'][1]}")
            self.caller.msg(f"|cBehavior:|n {data['behavior']}")
            
            if data["resistances"]:
                self.caller.msg(f"|cResistances:|n")
                for resist, val in data["resistances"].items():
                    self.caller.msg(f"  {resist}: {val}%")
            
            if data["loot"]:
                self.caller.msg(f"|cLoot:|n")
                for item in data["loot"]:
                    self.caller.msg(f"  {item['item']} ({item['chance']*100}%)")
            
            self.caller.msg(f"|cSpawn Areas:|n {', '.join(data['spawn_areas'])}")
            self.caller.msg(f"|c{'='*40}|n")


class MonsterCmdSet(CmdSet):
    """CmdSet with monster commands."""
    
    key = "MonsterCmdSet"
    priority = 1
    
    def at_cmdset_creation(self):
        self.add(CmdBestiary())
