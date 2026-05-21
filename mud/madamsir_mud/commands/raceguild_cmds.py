"""
Red Dragon MUD — Race & Guild Commands
======================================
Commands for:
  - Viewing and selecting races
  - Viewing and joining guilds
  - Checking combat profile
  - Viewing weapon mastery
"""

from evennia import Command
from typeclasses.races import RACES, apply_race, get_race_detail, get_race_list
from typeclasses.guilds import GUILDS, apply_guild, get_guild_detail, get_guild_list
from typeclasses.combat import (
    get_combat_summary, get_weapon_mastery, get_mastery_tier,
    format_mastery_progress, gain_weapon_mastery_xp, WEAPON_TYPES
)


class CmdRace(Command):
    """
    View or select your character race.

    Usage:
      race              — list all available races
      race <name>       — view detailed info about a race
      race select <name>— choose your race (one-time only)
    """
    key = "race"
    locks = "cmd:all()"

    def func(self):
        args = self.args.strip().lower()
        caller = self.caller

        if not args:
            caller.msg(get_race_list())
            return

        if args.startswith("select "):
            race_name = args[7:].strip()
            if caller.db.race:
                caller.msg("You have already chosen a race. This cannot be changed.")
                return
            if apply_race(caller, race_name):
                caller.msg(f"{{gYou have chosen the {RACES[race_name]['name']} race!{{n")
                caller.msg(get_race_detail(race_name))
            else:
                caller.msg("That is not a valid race. Use 'race' to see the list.")
            return

        # View detail
        if args in RACES:
            caller.msg(get_race_detail(args))
        else:
            # Try fuzzy match
            matches = [k for k in RACES if args in k or args in RACES[k]["name"].lower()]
            if matches:
                caller.msg(get_race_detail(matches[0]))
            else:
                caller.msg("Race not found. Use 'race' to see available races.")


class CmdGuild(Command):
    """
    View or join a guild.

    Usage:
      guild             — list all available guilds
      guild <name>      — view detailed info about a guild
      guild join <name> — join a guild (one-time only)
    """
    key = "guild"
    locks = "cmd:all()"

    def func(self):
        args = self.args.strip().lower()
        caller = self.caller

        if not args:
            caller.msg(get_guild_list())
            return

        if args.startswith("join "):
            guild_name = args[5:].strip()
            if caller.db.guild:
                caller.msg("You have already joined a guild. Speak to a guild master to advance.")
                return
            if apply_guild(caller, guild_name):
                caller.msg(f"{{gYou have joined the {GUILDS[guild_name]['name']} guild!{{n")
                caller.msg(get_guild_detail(guild_name))
            else:
                caller.msg("That is not a valid guild. Use 'guild' to see the list.")
            return

        # View detail
        if args in GUILDS:
            caller.msg(get_guild_detail(args))
        else:
            matches = [k for k in GUILDS if args in k or args in GUILDS[k]["name"].lower()]
            if matches:
                caller.msg(get_guild_detail(matches[0]))
            else:
                caller.msg("Guild not found. Use 'guild' to see available guilds.")


class CmdCombatProfile(Command):
    """
    View your combat statistics and weapon masteries.

    Usage:
      combat
      combat profile
    """
    key = "combat"
    aliases = ["profile", "mastery"]
    locks = "cmd:all()"

    def func(self):
        caller = self.caller
        caller.msg(get_combat_summary(caller))


class CmdMastery(Command):
    """
    View your weapon mastery levels.

    Usage:
      mastery           — list all weapon masteries
      mastery <weapon>  — view specific weapon mastery
    """
    key = "mastery"
    locks = "cmd:all()"

    def func(self):
        caller = self.caller
        args = self.args.strip().lower()

        if not caller.db.weapon_mastery:
            caller.db.weapon_mastery = {}

        if args:
            if args in WEAPON_TYPES or args in caller.db.weapon_mastery:
                val = caller.db.weapon_mastery.get(args, 0)
                tier = get_mastery_tier(val)
                caller.msg(format_mastery_progress(args, val))
                caller.msg(f"  Damage bonus: +{int(tier['dmg_bonus']*100)}%")
                caller.msg(f"  Crit bonus: +{int(tier['crit_bonus']*100)}%")
                caller.msg(f"  Parry bonus: +{int(tier['parry_bonus']*100)}%")
                if tier["special"]:
                    caller.msg(f"  {{gSpecial unlocked: {tier['special']}{{n")
            else:
                caller.msg(f"Unknown weapon type: {args}")
            return

        lines = []
        lines.append("{cWeapon Mastery{n")
        lines.append("-" * 45)
        for wpn in WEAPON_TYPES:
            val = caller.db.weapon_mastery.get(wpn, 0)
            if val > 0:
                lines.append(format_mastery_progress(wpn, val))
        lines.append("-" * 45)
        caller.msg("\n".join(lines))


class CmdScore(Command):
    """
    View your character score sheet.

    Usage:
      score
      sc
    """
    key = "score"
    aliases = ["sc", "stats"]
    locks = "cmd:all()"

    def func(self):
        caller = self.caller

        lines = []
        lines.append("{c" + "="*50 + "{n")
        lines.append(f"{{G{caller.name}{{n")
        lines.append("{c" + "="*50 + "{n")

        race = caller.db.race_name or "None"
        guild = caller.db.guild_name or "None"
        guild_lv = caller.db.guild_level or 0
        lines.append(f"  {{yRace:{{n  {race}")
        lines.append(f"  {{yGuild:{{n {guild} (Level {guild_lv})")

        lines.append("")
        lines.append("{yAttributes:{n")
        for stat in ["strength", "constitution", "dexterity", "stamina",
                     "intelligence", "wisdom"]:
            val = caller.attributes.get(stat, 10)
            lines.append(f"  {stat.capitalize():12} {val}")

        lines.append("")
        lines.append("{yResources:{n")
        hp = caller.db.hp or caller.attributes.get("hp_max", 10)
        hp_max = caller.attributes.get("hp_max", 10)
        ep = caller.db.ep or caller.attributes.get("ep_max", 10)
        ep_max = caller.attributes.get("ep_max", 10)
        sp = caller.db.sp or caller.attributes.get("sp_max", 10)
        sp_max = caller.attributes.get("sp_max", 10)
        lines.append(f"  HP: {hp}/{hp_max}")
        lines.append(f"  EP: {ep}/{ep_max}")
        lines.append(f"  SP: {sp}/{sp_max}")

        lines.append("")
        lines.append(f"{{yXP Rate:{{n {caller.db.xp_rate*100 if caller.db.xp_rate else 100:.0f}%")
        lines.append(f"{{ySkill Cap:{{n {caller.db.skill_cap*100 if caller.db.skill_cap else 95:.0f}%")
        lines.append(f"{{ySpell Cap:{{n {caller.db.spell_cap*100 if caller.db.spell_cap else 95:.0f}%")

        if caller.db.race_traits:
            lines.append("")
            lines.append("{yRacial Traits:{n")
            for trait in caller.db.race_traits:
                lines.append(f"  • {trait}")

        lines.append("{c" + "="*50 + "{n")
        caller.msg("\n".join(lines))
