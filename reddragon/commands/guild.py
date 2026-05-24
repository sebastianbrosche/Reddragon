"""
Red Dragon MUD - Guild Commands
Join guilds, check prerequisites, train skills
Uses comprehensive guild data from world/guilds/__init__.py
"""

from evennia import Command
from world.guilds import (
    GUILD_PREREQUISITES, GUILD_STARTING_SKILLS, GUILD_LOCATIONS,
    GUILD_CATEGORIES, GUILD_DESCRIPTIONS, ALPHA_GUILDS
)


def _normalize_guild_name(name):
    """Normalize guild name to key format."""
    return name.lower().replace(" ", "_").replace("-", "_")


def _check_prerequisites(caller, guild_key):
    """Check if caller meets prerequisites for a guild."""
    prereqs = GUILD_PREREQUISITES.get(guild_key)
    
    if prereqs is None:
        return True, None  # Alpha guild, no prereqs
    
    if not prereqs:
        return True, None
    
    # Get guild history
    guild_history = getattr(caller.db, 'guild_history', {})
    current_guild = getattr(caller.db, 'guild', '').lower().replace(" ", "_")
    current_level = getattr(caller.db, 'guild_level', 0)
    
    # Helper to get level in a guild
    def get_guild_level(guild_name):
        gkey = _normalize_guild_name(guild_name)
        if gkey == current_guild:
            return current_level
        return guild_history.get(gkey, 0)
    
    # Check any_of (need N levels across any of the listed guilds)
    any_count = prereqs.get('any_of', 0)
    if any_count > 0:
        bravo_guilds = prereqs.get('bravo_guilds', [])
        total = sum(get_guild_level(g) for g in bravo_guilds)
        if total < any_count * 10:  # Assuming 10 levels per guild
            return False, f"Requires {any_count} levels across: {', '.join(bravo_guilds)}"
        return True, None
    
    # Check alt_guild (OR condition)
    alt_guild = prereqs.get('alt_guild')
    alt_level = prereqs.get('alt_level', 0)
    if alt_guild:
        needed_guild = prereqs.get('guild', '')
        needed_level = prereqs.get('level', 0)
        has_a = get_guild_level(needed_guild) >= needed_level
        has_b = get_guild_level(alt_guild) >= alt_level
        if not (has_a or has_b):
            return False, f"Requires {needed_level} levels in {needed_guild} or {alt_level} in {alt_guild}"
        return True, None
    
    # Check single guild requirement
    needed_guild = prereqs.get('guild', '')
    needed_level = prereqs.get('level', 0)
    if needed_guild:
        actual = get_guild_level(needed_guild)
        if actual < needed_level:
            return False, f"Requires {needed_level} levels in {needed_guild} (you have {actual})"
    
    return True, None


class CmdJoinGuild(Command):
    """
    Join a guild at a guild master.
    
    Usage:
        join <guild_name>
        join warrior
        join shapeshifter
        join dragon lord
    """
    key = "join"
    locks = "cmd:all()"
    
    def func(self):
        caller = self.caller
        
        if not self.args:
            caller.msg("Join which guild? Type 'guilds' to see available guilds.")
            return
        
        guild_name = self.args.strip().lower()
        guild_key = _normalize_guild_name(guild_name)
        
        # Validate guild exists
        if guild_key not in GUILD_DESCRIPTIONS:
            # Try partial match
            matches = [k for k in GUILD_DESCRIPTIONS if guild_key in k or k.replace("_", " ").startswith(guild_name)]
            if len(matches) == 1:
                guild_key = matches[0]
            elif len(matches) > 1:
                caller.msg(f"Multiple matches: {', '.join(m.replace('_', ' ').title() for m in matches)}")
                return
            else:
                caller.msg(f"Unknown guild: {guild_name}. Type 'guilds' to see available guilds.")
                return
        
        # Check if already in this guild
        current_guild = getattr(caller.db, 'guild', '').lower().replace(" ", "_")
        if current_guild == guild_key:
            caller.msg(f"You are already a member of the {guild_key.replace('_', ' ').title()} guild!")
            return
        
        # Check prerequisites
        ok, err = _check_prerequisites(caller, guild_key)
        if not ok:
            caller.msg(f"|rCannot join: {err}|n")
            return
        
        # Record previous guild in history
        if current_guild and current_guild != guild_key:
            history = getattr(caller.db, 'guild_history', {})
            current_level = getattr(caller.db, 'guild_level', 0)
            if current_guild not in history or history[current_guild] < current_level:
                history[current_guild] = current_level
            caller.db.guild_history = history
        
        # Join the guild
        caller.db.guild = guild_key.replace("_", " ").title()
        caller.db.guild_level = 1
        caller.db.guild_xp = 0
        
        # Give starting skills
        skills = GUILD_STARTING_SKILLS.get(guild_key, {})
        if skills:
            current_skills = getattr(caller.db, 'skills', {})
            if not isinstance(current_skills, dict):
                current_skills = {}
            current_skills.update(skills)
            caller.db.skills = current_skills
        
        # Guild-specific items
        if 'shapeshifter' in guild_key or guild_key in ['animal_tamer', 'bestial_seccedaneum', 'savager']:
            from evennia import create_object
            collar = create_object("typeclasses.objects.Object", key="a collar")
            collar.db.desc = "A magical collar that allows you to shapeshift. Look at it to see your form abilities. Touch it for guild info."
            collar.db.is_collar = True
            collar.move_to(caller, quiet=True)
            caller.msg("You have been given a magical collar.")
        
        # Announce
        guild_display = guild_key.replace("_", " ").title()
        caller.msg(f"|gYou have joined the {guild_display} guild!|n")
        caller.msg(f"Your guild level is now 1.")
        
        if guild_key in GUILD_DESCRIPTIONS:
            caller.msg(f"|x{GUILD_DESCRIPTIONS[guild_key]}|n")
        
        # Location hint
        loc = GUILD_LOCATIONS.get(guild_key)
        if loc:
            caller.msg(f"|yGuild headquarters: {loc['area']} on {loc['island']} Island.|n")


class CmdGuilds(Command):
    """
    Show available guilds and current guild status.
    
    Usage:
        guilds
        guilds <tree_name>
        guild info <guild_name>
    """
    key = "guilds"
    aliases = ["guild"]
    locks = "cmd:all()"
    
    def func(self):
        caller = self.caller
        args = self.args.strip().lower()
        
        # Show info for specific guild
        if args.startswith("info "):
            guild_name = args[5:].strip()
            guild_key = _normalize_guild_name(guild_name)
            if guild_key in GUILD_DESCRIPTIONS:
                self._show_guild_info(caller, guild_key)
            else:
                caller.msg(f"Unknown guild: {guild_name}")
            return
        
        # Show specific tree
        if args:
            tree_key = args.replace(" ", "_")
            if tree_key in GUILD_CATEGORIES:
                self._show_tree(caller, tree_key)
                return
        
        # Show overview
        current = getattr(caller.db, 'guild', None)
        level = getattr(caller.db, 'guild_level', 0)
        
        output = []
        output.append("-=-=-| Guilds |-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
        
        if current:
            output.append(f"|cCurrent Guild:|n {current} (Level {level})")
            output.append(f"Guild XP: {getattr(caller.db, 'guild_xp', 0):,}")
            
            # Show guild history
            history = getattr(caller.db, 'guild_history', {})
            if history:
                output.append("|cPrevious Guilds:|n")
                for g, lvl in sorted(history.items(), key=lambda x: -x[1]):
                    gname = g.replace("_", " ").title()
                    output.append(f"  {gname}: Level {lvl}")
        else:
            output.append("|yYou are not in any guild.|n")
        
        output.append("")
        output.append("|cGuild Trees:|n (type 'guilds <tree>' for details)")
        output.append("  |ywarrior|n - Combat: Warrior → Berserker/Defender/Knight → ... → Champion")
        output.append("  |ymartial_artist|n - Combat: Martial Artist → Dragonfist/Mystic → ... → Dragon Master")
        output.append("  |yweaver|n - Healing: Weaver → Confessor/Healer/Martyr → ... → High Priest")
        output.append("  |yunraveller|n - Dark: Unraveller → Harmer/Torturer/Sacrificer → ... → Sword")
        output.append("  |yelemental|n - Magic: Elemental → Air/Earth/Fire/Water → Lava/Mist → Nether")
        output.append("  |yevoker|n - Magic: Evoker → Elements/Ether → 8 bravo → Sorcerer")
        output.append("  |ynecromancer|n - Dark: Necromancer → Undead/Shadow/Death → ... → Dark Lord")
        output.append("  |ypsychics|n - Mental: Psychics → Telepath/Telekinetic → ... → Grandmaster")
        output.append("  |yacrobat|n - Utility: Acrobat → Juggler/Tightrope → ... → Ringmaster")
        output.append("  |ylurker|n - Stealth: Lurker → Scout/Thief → ... → Shadow Master")
        output.append("  |ydruid|n - Nature: Druid → Shaman/Witch → Elder Druid → Archdruid")
        output.append("  |ywoodsman|n - Nature: Woodsman → Ranger/Tracker → Beast Master → Forest Lord")
        output.append("  |yshapeshifter|n - Transformation: Shapeshifter → Animal Tamer/Bestial/Savager → ... → Dragon Lord")
        output.append("")
        output.append("|xType 'guild info <name>' for details about a specific guild.|n")
        output.append("|xTo join: find a guild master and type 'join <guild_name>'|n")
        output.append("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
        
        caller.msg("\n".join(output))
    
    def _show_guild_info(self, caller, guild_key):
        """Show detailed info about a specific guild."""
        output = []
        name = guild_key.replace("_", " ").title()
        output.append(f"-=-=-| {name} |-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
        
        # Description
        desc = GUILD_DESCRIPTIONS.get(guild_key, "No description available.")
        output.append(desc)
        output.append("")
        
        # Category
        cat = GUILD_CATEGORIES.get(guild_key, "Unknown")
        output.append(f"Category: {cat}")
        
        # Prerequisites
        prereqs = GUILD_PREREQUISITES.get(guild_key)
        if prereqs is None:
            output.append("Prerequisites: |gNone (Alpha Guild)|n")
        elif prereqs:
            output.append("Prerequisites:")
            any_count = prereqs.get('any_of', 0)
            if any_count > 0:
                guilds = prereqs.get('bravo_guilds', [])
                output.append(f"  {any_count} levels across: {', '.join(g.replace('_', ' ').title() for g in guilds)}")
            elif prereqs.get('alt_guild'):
                g1 = prereqs.get('guild', '')
                l1 = prereqs.get('level', 0)
                g2 = prereqs.get('alt_guild', '')
                l2 = prereqs.get('alt_level', 0)
                output.append(f"  {l1} levels in {g1.replace('_', ' ').title()} OR {l2} in {g2.replace('_', ' ').title()}")
            else:
                g = prereqs.get('guild', '')
                l = prereqs.get('level', 0)
                output.append(f"  {l} levels in {g.replace('_', ' ').title()}")
        
        # Starting skills
        skills = GUILD_STARTING_SKILLS.get(guild_key, {})
        if skills:
            output.append("")
            output.append("Starting Skills:")
            for skill, val in skills.items():
                output.append(f"  {skill}: {val}")
        
        # Location
        loc = GUILD_LOCATIONS.get(guild_key)
        if loc:
            output.append("")
            output.append(f"Location: {loc['area']} on {loc['island']} Island")
        
        output.append("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
        caller.msg("\n".join(output))
    
    def _show_tree(self, caller, tree_key):
        """Show guilds in a specific tree."""
        # Find all guilds in this category
        guilds_in_tree = [k for k, v in GUILD_CATEGORIES.items() if v.lower() == tree_key or k == tree_key]
        
        if not guilds_in_tree:
            caller.msg(f"Unknown guild tree: {tree_key}")
            return
        
        output = []
        output.append(f"-=-=-| {tree_key.replace('_', ' ').title()} Guild Tree |-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
        
        for gkey in sorted(guilds_in_tree, key=lambda k: (GUILD_PREREQUISITES.get(k) is not None, k)):
            name = gkey.replace("_", " ").title()
            prereqs = GUILD_PREREQUISITES.get(gkey)
            if prereqs is None:
                output.append(f"  |g{name}|n (Alpha - no prereqs)")
            else:
                output.append(f"  {name}")
        
        output.append("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
        caller.msg("\n".join(output))


class CmdTrain(Command):
    """
    Train a stat at Mount Olympus or other training location.
    
    Usage:
        train
        train <stat>
        train str
        train strength
    """
    key = "train"
    locks = "cmd:all()"
    
    def func(self):
        caller = self.caller
        
        if not self.args:
            # Show training costs
            from world.training import TRAINING_COST_PER_LEVEL
            current_level = getattr(caller.db, 'training_level', 1)
            cost = TRAINING_COST_PER_LEVEL.get(current_level, {})
            
            caller.msg(f"Current training level: {current_level}")
            caller.msg(f"Next training cost: {cost.get('exp', 0):,} XP, {cost.get('gold', 0):,} gold")
            return
        
        stat = self.args.strip().lower()
        
        # Map full names to abbreviations
        stat_map = {
            'strength': 'str', 'str': 'str',
            'dexterity': 'dex', 'dex': 'dex',
            'constitution': 'con', 'con': 'con',
            'stamina': 'sta', 'sta': 'sta',
            'intelligence': 'int', 'int': 'int',
            'wisdom': 'wis', 'wis': 'wis',
            'charisma': 'cha', 'cha': 'cha',
            'hp regen': 'hpr', 'hpr': 'hpr',
            'sp regen': 'spr', 'spr': 'spr',
            'ep regen': 'epr', 'epr': 'epr',
        }
        
        stat_key = stat_map.get(stat)
        if not stat_key:
            caller.msg("Invalid stat. Choose: strength, dexterity, constitution, stamina, intelligence, wisdom, charisma, hp_regen, sp_regen, ep_regen")
            return
        
        # Check costs
        from world.training import get_exp_cost, get_gold_cost
        current_level = getattr(caller.db, 'training_level', 1)
        exp_cost = get_exp_cost(current_level)
        gold_cost = get_gold_cost(current_level)
        
        xp = getattr(caller.db, 'experience', 0)
        gold = getattr(caller.db, 'gold', 0)
        
        if xp < exp_cost:
            caller.msg(f"You need {exp_cost:,} XP. You have {xp:,}.")
            return
        if gold < gold_cost:
            caller.msg(f"You need {gold_cost:,} gold. You have {gold:,}.")
            return
        
        # Pay costs
        caller.db.experience -= exp_cost
        caller.db.gold -= gold_cost
        caller.db.training_level = current_level + 1
        
        # Apply stat gain
        from world.stats import STAT_MESSAGES
        msg_data = STAT_MESSAGES.get(stat_key, {})
        
        if stat_key in ['hpr', 'spr', 'epr']:
            # Regen stats
            if stat_key == 'hpr':
                caller.db.hp_regen = getattr(caller.db, 'hp_regen', 10) + 1
            elif stat_key == 'spr':
                caller.db.sp_regen = getattr(caller.db, 'sp_regen', 5) + 1
            elif stat_key == 'epr':
                caller.db.ep_regen = getattr(caller.db, 'ep_regen', 5) + 1
        else:
            # Regular stat - use modify_stat
            caller.modify_stat(stat_key, 1)
        
        # Recalculate derived stats
        if hasattr(caller, 'recalculate_stats'):
            caller.recalculate_stats()
        
        increase_msg = msg_data.get('increase', f"You feel your {stat} increase!")
        caller.msg(increase_msg)
        caller.msg(f"Training level increased to {caller.db.training_level}.")
