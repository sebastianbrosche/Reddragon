"""
Red Dragon MUD — System Commands (Part 2)
Commands for levels, healing, and equipment.
"""

from evennia import Command
from typeclasses.levels import LEVEL_TABLE, get_level_title, get_xp_for_level, get_total_xp_to_level, get_level_progress
from typeclasses.healing import HEALING_SPELLS, HEALER_PROGRESSION, PARTY_ROLES, get_heal_amount, get_party_heal_priority
from typeclasses.equipment import EQUIPMENT_DATABASE, EQUIPMENT_SLOTS, get_equipment_stats, get_set_bonus

class CmdLevel(Command):
    """
    View level information or your progress.

    Usage:
      level             — view level table
      level check       — check your current level/XP
      level <number>    — view specific level cost
    """
    key = "level"
    aliases = ["levels", "xp"]
    locks = "cmd:all()"

    def func(self):
        args = self.args.strip()
        
        if not args or args == "check":
            # Show player's current level info
            level = getattr(self.caller.db, "level", 1)
            xp = getattr(self.caller.db, "xp", 0)
            title = get_level_title(level)
            next_level_cost = get_xp_for_level(level + 1) if level < 200 else 0
            total_to_next = get_total_xp_to_level(level)
            progress = get_level_progress(xp, level)
            
            lines = [
                f"{C.c}{'='*50}{C.n}",
                f"  {C.G}Level: {level}{C.n} ({title})",
                f"  XP: {xp:,}",
                f"  Next Level: {level + 1} (needs {next_level_cost:,} XP)",
                f"  Progress: {progress:.1f}%",
                f"{C.c}{'='*50}{C.n}",
            ]
            self.caller.msg("\n".join(lines))
        elif args.isdigit():
            target = int(args)
            if 1 <= target <= 200:
                cost = get_xp_for_level(target)
                total = get_total_xp_to_level(target)
                title = get_level_title(target)
                lines = [
                    f"{C.c}Level {target}{C.n} ({title})",
                    f"  Cost for this level: {cost:,} XP",
                    f"  Total XP to reach: {total:,} XP",
                ]
                self.caller.msg("\n".join(lines))
            else:
                self.caller.msg("Level must be between 1 and 200.")
        else:
            self.caller.msg("Usage: level | level check | level <1-200>")

class CmdHeal(Command):
    """
    Healing and party support commands.

    Usage:
      heal              — view healing guide
      heal spells       — list all healing spells
      heal <spell>      — view specific spell
      heal party        — view party role guide
      heal priority     — view healing priority
    """
    key = "heal"
    aliases = ["healing", "partyheal"]
    locks = "cmd:all()"

    def func(self):
        args = self.args.strip().lower()
        
        if not args:
            # Show healing guide overview
            lines = [
                f"{C.c}Party Healing Guide{C.n}",
                f"{C.c}{'='*50}{C.n}",
                "",
                "{C}Guild Progression for Healers:{n}",
                "  1. {y}Weaver{n} — cure serious/minor refresh",
                "  2. {y}Healer{n} — heal, major refresh, mastery",
                "  3. {y}Martyr/Confessor{n} — party support",
                "  4. {y}Avatar{n} — encourage regeneration (game-changer)",
                "",
                "{C}Key Principles:{n}",
                "  • Heal spell MUST be at 100% for parties",
                "  • Max martyric presence at level 5",
                "  • Encourage regeneration > refresh (SP > EP)",
                "  • Re-cast enreg immediately when it falls",
                "",
                "{C}Use 'heal spells', 'heal party', 'heal priority' for more.{n}",
            ]
            self.caller.msg("\n".join(lines))
        elif args == "spells":
            lines = [f"{C.c}Healing Spells Database{C.n}", f"{C.c}{'='*50}{C.n}"]
            for name, spell in sorted(HEALING_SPELLS.items()):
                lines.append(f"  {C.G}{name}{C.n}")
                lines.append(f"    Guild: {spell['guild']} | Type: {spell['type']} | Target: {spell['target']}")
                if 'base_heal' in spell:
                    lines.append(f"    Base Heal: {spell['base_heal']} | SP Cost: {spell['sp_cost']}")
                if 'base_refresh' in spell:
                    lines.append(f"    Base Refresh: {spell['base_refresh']} | SP Cost: {spell['sp_cost']}")
                if 'mastery' in spell:
                    lines.append(f"    Mastery: {spell['mastery']}")
                lines.append(f"    {spell['description']}")
                lines.append("")
            self.caller.msg("\n".join(lines))
        elif args == "party":
            lines = [f"{C.c}Party Roles{C.n}", f"{C.c}{'='*50}{C.n}"]
            for role, info in PARTY_ROLES.items():
                lines.append(f"\n{C.G}{role.upper()}{C.n}")
                lines.append(f"  {info['description']}")
                lines.append(f"  Consumes: {info['consumes']}")
                lines.append(f"  Needs: {', '.join(info['needs'])}")
            self.caller.msg("\n".join(lines))
        elif args == "priority":
            lines = [
                f"{C.c}Party Healing Priority{C.n}",
                f"{C.c}{'='*50}{C.n}",
                "  1. Cast {y}encourage regeneration{n} on blasters FIRST",
                "  2. Keep {y}martyric presence{n} always active",
                "  3. {y}heal{n} tank when HP drops below 50%",
                "  4. {y}refresh{n} damagers when EP low",
                "  5. Re-cast {y}enreg{n} immediately when it falls",
                "",
                "  Why blasters first? They do the most damage.",
                "  Why enreg over refresh? SP > EP for damage output.",
            ]
            self.caller.msg("\n".join(lines))
        elif args in HEALING_SPELLS:
            spell = HEALING_SPELLS[args]
            lines = [
                f"{C.c}{spell['name']}{C.n}",
                f"  Guild: {spell['guild']}",
                f"  Type: {spell['type']}",
                f"  Target: {spell['target']}",
                f"  SP Cost: {spell['sp_cost']}",
            ]
            if 'base_heal' in spell:
                lines.append(f"  Base Heal: {spell['base_heal']}")
            if 'base_refresh' in spell:
                lines.append(f"  Base Refresh: {spell['base_refresh']}")
            if 'mastery' in spell:
                lines.append(f"  Mastery: {spell['mastery']}")
            lines.append(f"\n  {spell['description']}")
            self.caller.msg("\n".join(lines))
        else:
            self.caller.msg(f"Unknown: {args}. Use 'heal spells' to see available spells.")

class CmdEquipment(Command):
    """
    View equipment database.

    Usage:
      eq                — list equipment sets
      eq <set>          — view specific set
      eq item <name>    — view specific item
      eq slots          — list equipment slots
    """
    key = "eq"
    aliases = ["equipment", "gear"]
    locks = "cmd:all()"

    def func(self):
        args = self.args.strip().lower()
        
        if not args:
            # List all sets
            sets = {}
            for key, item in EQUIPMENT_DATABASE.items():
                s = item.get("set", "misc")
                if s not in sets:
                    sets[s] = []
                sets[s].append(item["name"])
            
            lines = [f"{C.c}Equipment Sets{C.n}", f"{C.c}{'='*50}{C.n}"]
            for set_name, items in sorted(sets.items()):
                lines.append(f"\n{C.G}{set_name.title()}{C.n} ({len(items)} items)")
                for item in items[:5]:
                    lines.append(f"  • {item}")
                if len(items) > 5:
                    lines.append(f"  ... and {len(items) - 5} more")
            self.caller.msg("\n".join(lines))
        elif args == "slots":
            lines = [f"{C.c}Equipment Slots ({len(EQUIPMENT_SLOTS)}){C.n}"]
            for slot in EQUIPMENT_SLOTS:
                lines.append(f"  {slot.replace('_', ' ').title()}")
            self.caller.msg("\n".join(lines))
        elif args.startswith("item "):
            item_name = args[5:].strip().replace(" ", "_").lower()
            # Try exact match first
            if item_name in EQUIPMENT_DATABASE:
                item = get_equipment_stats(item_name)
            else:
                # Fuzzy match
                matches = [k for k in EQUIPMENT_DATABASE if item_name in k]
                item = get_equipment_stats(matches[0]) if matches else None
            
            if item:
                lines = [
                    f"{C.c}{item['name']}{C.n}",
                    f"  Slot: {item['slot']}",
                    f"  Set: {item['set'] or 'None'}",
                    f"  Level Req: {item['level_req']}",
                ]
                if item['stats']:
                    lines.append(f"  Stats: {', '.join(f'{k}: +{v}' for k, v in item['stats'].items())}")
                if item['special']:
                    lines.append(f"  Special: {', '.join(item['special'])}")
                lines.append(f"\n  {item['description']}")
                self.caller.msg("\n".join(lines))
            else:
                self.caller.msg(f"Item not found: {item_name}")
        else:
            # Try set name
            set_items = [v for v in EQUIPMENT_DATABASE.values() if v.get("set") == args]
            if set_items:
                lines = [f"{C.c}{args.title()} Set ({len(set_items)} pieces){C.n}", f"{C.c}{'='*50}{C.n}"]
                for item in sorted(set_items, key=lambda x: x["slot"]):
                    lines.append(f"\n{C.G}{item['name']}{C.n}")
                    lines.append(f"  Slot: {item['slot']}")
                    if item.get("stats"):
                        lines.append(f"  Stats: {', '.join(f'{k}: +{v}' for k, v in item['stats'].items())}")
                    if item.get("special"):
                        lines.append(f"  Special: {', '.join(item['special'])}")
                    lines.append(f"  Lv.{item['level_req']}")
                self.caller.msg("\n".join(lines))
            else:
                self.caller.msg(f"Unknown set or command: {args}")

# Color helper
class C:
    c = "{c"
    n = "{n"
    G = "{G"
    y = "{y"
    r = "{r"


# Admin command to rebuild world
class CmdBuildWorld(Command):
    """
    Build the entire game world from map data.
    Admin only.
    """
    key = "@buildworld"
    locks = "cmd:perm(Admin)"

    def func(self):
        from typeclasses.world_builder import build_world
        self.caller.msg("{yBuilding world... this may take a moment.{n")
        try:
            rooms, exits = build_world()
            self.caller.msg(f"{{gWorld build complete! {{n{rooms} rooms, {exits} exits created.")
        except Exception as e:
            self.caller.msg(f"{{rError building world: {e}{{n")
            import traceback
            self.caller.msg(traceback.format_exc())
