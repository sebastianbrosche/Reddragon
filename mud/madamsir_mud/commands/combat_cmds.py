"""
Red Dragon MUD — Combat Commands
================================
Commands for attacking, using abilities, and managing combat.
"""

from evennia import Command, CmdSet
from typeclasses.combat import calculate_damage, check_hit, gain_weapon_mastery_xp
import random


class CmdAttack(Command):
    """
    Attack a target.

    Usage:
      attack <target>
      kill <target>
    """
    key = "attack"
    aliases = ["kill", "hit", "strike"]
    locks = "cmd:all()"

    def func(self):
        caller = self.caller
        args = self.args.strip()

        if not args:
            caller.msg("Attack whom?")
            return

        target = caller.search(args)
        if not target:
            return

        # Determine weapon type
        weapon_type = caller.db.equipped_weapon or "unarmed"
        damage_type = "physical"

        # Check if attack hits
        hit_result = check_hit(caller, target, weapon_type)
        if not hit_result["is_hit"]:
            for msg in hit_result["messages"]:
                caller.msg(msg)
            return

        # Calculate damage
        dmg_result = calculate_damage(caller, target, weapon_type, damage_type)

        # Apply damage
        current_hp = target.db.hp or target.attributes.get("hp_max", 10)
        new_hp = max(0, current_hp - dmg_result["damage"])
        target.db.hp = new_hp

        # Award mastery XP
        new_tier = gain_weapon_mastery_xp(caller, weapon_type, dmg_result["mastery_xp"])
        if new_tier:
            caller.msg(f"{{gYour {weapon_type} mastery advances to: {new_tier}!{{n")

        # Messages
        caller.msg(f"You attack {target.name} with your {weapon_type}!")
        for msg in dmg_result["messages"]:
            caller.msg(msg)

        target.msg(f"{caller.name} attacks you!")
        for msg in dmg_result["messages"]:
            if "deal" in msg.lower():
                target.msg(msg.replace("You deal", f"{caller.name} deals"))

        # Check death
        if new_hp <= 0:
            caller.msg(f"{{rYou have slain {target.name}!{{n")
            target.msg(f"{{rYou have been slain by {caller.name}!{{n")
            # Award kill mastery XP
            gain_weapon_mastery_xp(caller, weapon_type, 10)


class CmdEquip(Command):
    """
    Equip a weapon.

    Usage:
      equip <weapon_type>
      wield <weapon_type>
    """
    key = "equip"
    aliases = ["wield", "weapon"]
    locks = "cmd:all()"

    def func(self):
        caller = self.caller
        args = self.args.strip().lower()

        if not args:
            current = caller.db.equipped_weapon or "unarmed"
            caller.msg(f"You are wielding: {current}")
            return

        from typeclasses.combat import WEAPON_TYPES
        if args not in WEAPON_TYPES:
            caller.msg(f"Unknown weapon type. Available: {', '.join(WEAPON_TYPES)}")
            return

        caller.db.equipped_weapon = args
        caller.msg(f"You ready your {args}.")


class CmdRest(Command):
    """
    Rest to recover HP, EP, and SP.

    Usage:
      rest
      sleep
    """
    key = "rest"
    aliases = ["sleep", "recover"]
    locks = "cmd:all()"

    def func(self):
        caller = self.caller

        # Regeneration rates
        hp_regen = caller.attributes.get("hp_regen", 1)
        ep_regen = caller.attributes.get("ep_regen", 1)
        sp_regen = caller.attributes.get("sp_regen", 1)

        # Race modifiers
        race = caller.db.race
        if race == "troll":
            hp_regen = int(hp_regen * 3)
        elif race == "vampire":
            caller.msg("You must feed on blood to heal. Rest does little for you.")
            hp_regen = max(1, hp_regen // 4)
        elif race == "drow":
            # Check if in dark place
            caller.msg("You rest, but only dark places truly heal a drow.")

        hp_max = caller.attributes.get("hp_max", 10)
        ep_max = caller.attributes.get("ep_max", 10)
        sp_max = caller.attributes.get("sp_max", 10)

        caller.db.hp = min(hp_max, (caller.db.hp or hp_max) + hp_regen * 5)
        caller.db.ep = min(ep_max, (caller.db.ep or ep_max) + ep_regen * 5)
        caller.db.sp = min(sp_max, (caller.db.sp or sp_max) + sp_regen * 5)

        caller.msg(f"You rest and recover.")
        caller.msg(f"  HP: {caller.db.hp}/{hp_max}  EP: {caller.db.ep}/{ep_max}  SP: {caller.db.sp}/{sp_max}")


class CmdUseAbility(Command):
    """
    Use a racial or guild special ability.

    Usage:
      ability
      ability <name>
    """
    key = "ability"
    aliases = ["special", "power"]
    locks = "cmd:all()"

    def func(self):
        caller = self.caller
        args = self.args.strip().lower()

        race_special = caller.db.race_special
        guild = caller.db.guild

        if not args:
            lines = []
            lines.append("{cAvailable Abilities:{n")
            if race_special:
                lines.append(f"  [Racial] {race_special}")
            if guild:
                from typeclasses.guilds import GUILDS
                g = GUILDS.get(guild)
                if g:
                    for p in g.get("passives", []):
                        lines.append(f"  [Passive] {p['name']}: {p['effect']}")
            lines.append("Use 'ability <name>' to activate.")
            caller.msg("\n".join(lines))
            return

        # Simple racial ability implementations
        if args == race_special or (race_special and args in race_special.lower()):
            self._use_racial_ability(caller)
            return

        caller.msg("Ability not found or not available.")

    def _use_racial_ability(self, caller):
        special = caller.db.race_special
        race = caller.db.race

        if special == "berserker_rage" or race == "cromagnon":
            if caller.db.ep >= 5:
                caller.db.ep -= 5
                caller.msg("{rYou enter a primal rage! Strength surges through you!{n")
                # Effect: +2 STR for 3 rounds (simplified)
                caller.db.temp_str_bonus = 2
            else:
                caller.msg("Not enough energy!")

        elif special == "shadow_dance" or race == "drow":
            if caller.db.sp >= 10:
                caller.db.sp -= 10
                caller.msg("{gYou meld into the shadows, becoming nearly invisible.{n")
            else:
                caller.msg("Not enough spell points!")

        elif special == "stoneform" or race == "dwarf":
            if caller.db.ep >= 8:
                caller.db.ep -= 8
                caller.msg("{yYour skin hardens like granite!{n")
                caller.db.temp_dr = 0.20
            else:
                caller.msg("Not enough energy!")

        elif special == "rebirth" or race == "phoenix":
            if caller.db.sp >= 50:
                caller.db.sp = 0
                hp_max = caller.attributes.get("hp_max", 10)
                caller.db.hp = int(hp_max * 0.25)
                caller.msg("{rYou burst into flames and rise from your own ashes!{n")
            else:
                caller.msg("Not enough spell points for rebirth!")

        elif special == "regeneration" or race == "troll":
            caller.msg("{gYour wounds begin to close rapidly.{n")
            hp_max = caller.attributes.get("hp_max", 10)
            caller.db.hp = min(hp_max, caller.db.hp + int(hp_max * 0.15))

        elif special == "blood_drain" or race == "vampire":
            caller.msg("{rYour fangs extend, thirsting for blood...{n")
            # Next unarmed attack will drain
            caller.db.next_drain = True

        elif special == "mind_blast" or race == "mindflayer":
            if caller.db.sp >= 15:
                caller.db.sp -= 15
                caller.msg("{mYou unleash a wave of psionic force!{n")
            else:
                caller.msg("Not enough spell points!")

        else:
            caller.msg(f"You use your racial ability: {special}")


# ---------------------------------------------------------------------------
# Command Set
# ---------------------------------------------------------------------------
class CombatCmdSet(CmdSet):
    key = "combat_cmdset"

    def at_cmdset_creation(self):
        self.add(CmdAttack)
        self.add(CmdEquip)
        self.add(CmdRest)
        self.add(CmdUseAbility)
