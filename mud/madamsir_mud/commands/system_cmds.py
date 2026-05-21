"""
Red Dragon MUD — System Commands
Commands for mechanics, quests, lodestones, and world info.
"""

from evennia import Command
from typeclasses.mechanics import (
    DAMAGE_TYPES, DAMAGE_SCALE, CONDITION_LEVELS, ALIGNMENT_SCALE,
    HUNGER_LEVELS, AC_SCALE, LODESTONE_DESTINATIONS,
    get_damage_type_info, get_condition_info, get_alignment_info,
    get_hunger_info, get_lodestone_info
)
from typeclasses.quests import QUESTS, get_quest_detail, get_quest_list
from typeclasses.world import ISLANDS, CITY_OF_ILLIUM


class CmdDamageTypes(Command):
    """
    View damage types and their effects.

    Usage:
      damagetypes
      damagetypes <type>
    """
    key = "damagetypes"
    aliases = ["dtype", "damage"]
    locks = "cmd:all()"

    def func(self):
        if not self.args:
            lines = ["{cDamage Types (11){n", "-" * 40]
            for dtype, data in DAMAGE_TYPES.items():
                resist = data['resistance_stat'] or "None"
                lines.append(f"  {dtype:<12} Resist: {resist}")
            lines.append("-" * 40)
            lines.append("Use 'damagetypes <type>' for details.")
            self.caller.msg("\n".join(lines))
        else:
            self.caller.msg(get_damage_type_info(self.args.strip().lower()))


class CmdCondition(Command):
    """
    View equipment condition scale.

    Usage:
      condition
      condition <level>
    """
    key = "condition"
    aliases = ["cond"]
    locks = "cmd:all()"

    def func(self):
        if not self.args:
            lines = ["{cEquipment Condition Scale (13 levels){n", "-" * 50]
            for level, (name, color, desc) in CONDITION_LEVELS.items():
                stat_mod = ""
                if level < 6:
                    stat_mod = f"-{(6-level)*10}%"
                elif level > 6:
                    stat_mod = f"+{(level-6)*10}%"
                lines.append(f"  {level:>2}. {name:<12} {stat_mod:<8} {desc}")
            lines.append("-" * 50)
            self.caller.msg("\n".join(lines))
        else:
            try:
                level = int(self.args.strip())
                self.caller.msg(get_condition_info(level))
            except ValueError:
                self.caller.msg("Usage: condition <number 0-12>")


class CmdAlignment(Command):
    """
    View alignment scale or your current alignment.

    Usage:
      alignment           — view scale
      alignment check     — check your alignment
    """
    key = "alignment"
    aliases = ["align"]
    locks = "cmd:all()"

    def func(self):
        if "check" in self.args.lower():
            score = getattr(self.caller.db, "alignment", 0)
            name = get_alignment_info(score)
            self.caller.msg(f"Your alignment: {score} ({name})")
        else:
            lines = ["{cAlignment Scale{n", "-" * 40]
            for tier, (name, threshold) in sorted(ALIGNMENT_SCALE.items()):
                marker = " <-" if tier == 0 else ""
                lines.append(f"  {threshold:>6}  {name}{marker}")
            lines.append("-" * 40)
            lines.append("Perform evil acts to go negative, good acts to go positive.")
            self.caller.msg("\n".join(lines))


class CmdHunger(Command):
    """
    Check your hunger status.

    Usage:
      hunger
    """
    key = "hunger"
    locks = "cmd:all()"

    def func(self):
        level = getattr(self.caller.db, "hunger", 4)
        self.caller.msg(get_hunger_info(level))


class CmdLodestone(Command):
    """
    Use a lodestone to teleport.

    Usage:
      lodestone         — list destinations
      lodestone <dest>  — teleport to destination
    """
    key = "lodestone"
    aliases = ["lode", "recall", "home"]
    locks = "cmd:all()"

    def func(self):
        if not self.args:
            self.caller.msg(get_lodestone_info())
            return

        dest = self.args.strip().lower()
        if dest not in LODESTONE_DESTINATIONS:
            self.caller.msg(f"Unknown destination: {dest}")
            self.caller.msg("Use 'lodestone' to see available destinations.")
            return

        # Check if player has a lodestone
        has_lodestone = getattr(self.caller.db, "lodestones", {})
        if dest not in has_lodestone:
            self.caller.msg(f"You have not attuned to {dest} yet!")
            self.caller.msg("Visit a lodestone merchant to attune to new destinations.")
            return

        # Teleport (simplified — in real implementation, move to room)
        self.caller.msg(f"{C.c}The lodestone glows and you are pulled through space...{C.n}")
        self.caller.msg(f"You arrive at {dest.title()}.")


class CmdWorld(Command):
    """
    View world information.

    Usage:
      world             — list all islands
      world <island>    — view island details
    """
    key = "world"
    locks = "cmd:all()"

    def func(self):
        if not self.args:
            lines = ["{cThe World of Red Dragon{n", "=" * 50]
            lines.append(f"\n{{CCity:{n}")
            lines.append(f"  Illium — {CITY_OF_ILLIUM['desc'][:60]}...")
            lines.append(f"\n{{CIslands (11):{n}")
            for key, data in ISLANDS.items():
                low, high = data['level_range']
                lines.append(f"  {key.title():<15} Lv {low}-{high}  {data['climate']}")
            lines.append("\n" + "=" * 50)
            lines.append("Use 'world <island>' for details.")
            self.caller.msg("\n".join(lines))
        else:
            island = self.args.strip().lower()
            if island in ISLANDS:
                data = ISLANDS[island]
                low, high = data['level_range']
                lines = [f"{C.c}{'='*50}{C.n}",
                         f"{C.G}{island.title()}{C.n}",
                         f"{C.c}{'='*50}{C.n}",
                         f"Level Range: {low}-{high}",
                         f"Climate: {data['climate']}",
                         f"\nDescription:",
                         f"  {data['desc']}",
                         f"\nKey Areas:",
                         *[f"  - {area}" for area in data['key_areas']],
                         f"\nDangers:",
                         *[f"  ⚠ {danger.title()}" for danger in data['dangers']]]
                self.caller.msg("\n".join(lines))
            else:
                self.caller.msg(f"Island not found: {island}")


class CmdSuperRace(Command):
    """
    View super race information or select one.

    Usage:
      superrace             — list super races
      superrace <race>      — view super race details
      superrace select <race>  — choose super race (one-time)
    """
    key = "superrace"
    aliases = ["super", "superrace"]
    locks = "cmd:all()"

    def func(self):
        from typeclasses.super_races import SUPER_RACES, apply_super_race

        args = self.args.strip().lower()

        if not args:
            lines = ["{cSuper Races (3){n", "-" * 50]
            for key, data in SUPER_RACES.items():
                lines.append(f"  {C.G}{data['name']}{C.n} — {data['desc'][:50]}...")
            lines.append("-" * 50)
            lines.append("Use 'superrace <name>' for details.")
            lines.append("Use 'superrace select <name>' to choose (ONE TIME ONLY).")
            self.caller.msg("\n".join(lines))
            return

        if args.startswith("select "):
            race_name = args[7:].strip().replace(" ", "_")
            if getattr(self.caller.db, "race_selected", False):
                self.caller.msg("You have already chosen a race!")
                return
            if race_name not in SUPER_RACES:
                self.caller.msg(f"Unknown super race: {race_name}")
                return
            apply_super_race(self.caller, race_name)
            self.caller.db.race_selected = True
            self.caller.msg(f"{C.G}You have ascended as a {SUPER_RACES[race_name]['name']}!{C.n}")
            return

        # Show details
        race_name = args.replace(" ", "_")
        if race_name in SUPER_RACES:
            data = SUPER_RACES[race_name]
            lines = [f"{C.c}{'='*50}{C.n}",
                     f"{C.G}{data['name']}{C.n}",
                     f"{C.c}{'='*50}{C.n}",
                     f"\nDescription:",
                     f"  {data['desc']}",
                     f"\nStats:",
                     *[f"  {stat.title()}: {mod:+d}" for stat, mod in data['stats'].items()],
                     f"\nSpecial: {C.y}{data['special']}{C.n}",
                     f"  {data['special_desc']}",
                     f"\nPassives:",
                     *[f"  • {p}" for p in data['passives']],
                     f"\nAbilities:",
                     *[f"  Lv{lv}: {abil}" for lv, abil in sorted(data['abilities'].items())],
                     f"\nXP Rate: {data['xp_rate']}% (standard = 100)",
                     f"Max Skills: {data['skills']['max']}+{data['skills']['bonus']}",
                     f"Max Spells: {data['skills']['spells']['max']}+{data['skills']['spells']['bonus']}"]
            self.caller.msg("\n".join(lines))
        else:
            self.caller.msg(f"Unknown super race: {args}")


class CmdQuest(Command):
    """
    View quest information.

    Usage:
      quest             — list all quests
      quest <name>      — view quest details
    """
    key = "quest"
    aliases = ["quests"]
    locks = "cmd:all()"

    def func(self):
        args = self.args.strip().lower().replace(" ", "_")

        if not args:
            self.caller.msg(get_quest_list())
            return

        # Try exact match
        if args in QUESTS:
            self.caller.msg(get_quest_detail(args))
            return

        # Try fuzzy
        matches = [k for k in QUESTS if args in k or args in QUESTS[k]["name"].lower().replace(" ", "_")]
        if matches:
            self.caller.msg(get_quest_detail(matches[0]))
        else:
            self.caller.msg("Quest not found. Use 'quest' to see available quests.")


# Color helper
class C:
    c = "{c"
    n = "{n"
    G = "{G"
    y = "{y"
    r = "{r"
