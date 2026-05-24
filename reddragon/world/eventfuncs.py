#!/usr/bin/env python3
"""
Red Dragon MUD - Custom Event Functions for In-Game Python

These functions are available inside the in-game Python scripting environment.
Builders can use them to script room behavior, NPC AI, quests, etc.
"""

from evennia import search_object, create_object
from evennia.utils import delay

def heal_target(target, amount=10):
    """Heal a character by a given amount."""
    if hasattr(target, 'traits') and hasattr(target.traits, 'hp'):
        target.traits.hp.current = min(target.traits.hp.base, target.traits.hp.value + amount)
        target.db.hp = target.traits.hp.value
    else:
        target.db.hp = min(target.db.hp_max, target.db.hp + amount)
    target.msg(f"You are healed for {amount} HP.")

def damage_target(target, amount=10):
    """Damage a character by a given amount."""
    if hasattr(target, 'traits') and hasattr(target.traits, 'hp'):
        target.traits.hp.current -= amount
        target.db.hp = target.traits.hp.value
    else:
        target.db.hp = max(0, target.db.hp - amount)
    target.msg(f"You take {amount} damage!")

def spawn_mob(room, mob_key="a rat"):
    """Spawn a mob in a room."""
    from evennia import create_object
    mob_types = {
        "a rat": "typeclasses.npcs.NPC",
        "an earwig": "typeclasses.npcs.Earwig",
        "a bat": "typeclasses.npcs.Bat",
        "a snake": "typeclasses.npcs.Snake",
    }
    typeclass = mob_types.get(mob_key, "typeclasses.npcs.NPC")
    mob = create_object(typeclass, key=mob_key, location=room)
    if hasattr(mob, 'at_init'):
        mob.at_init()
    return mob

def announce(room, message):
    """Announce a message to everyone in a room."""
    room.msg_contents(message)

def give_gold(character, amount):
    """Give gold to a character."""
    character.db.gold = character.db.gold + amount
    character.msg(f"You receive {amount} gold.")

def teleport(character, room_key):
    """Teleport a character to a room by key."""
    from evennia import search_object
    results = search_object(room_key, typeclass="typeclasses.rooms.Room")
    if results:
        character.move_to(results[0])
        character.msg(f"You are teleported to {results[0].key}.")
    else:
        character.msg("Teleport failed.")

def add_buff(character, buff_key, stacks=1):
    """Apply an IOM buff to a character."""
    from world.buffs import apply_buff
    apply_buff(character, buff_key, stacks)

def remove_buff_from(character, buff_key):
    """Remove an IOM buff from a character."""
    from world.buffs import remove_buff
    remove_buff(character, buff_key)

def check_level(character):
    """Return character level info."""
    return {
        "level": getattr(character.db, 'level', 1),
        "xp": getattr(character.db, 'experience', 0),
        "next": getattr(character.db, 'next_level', 1000),
    }

def is_night():
    """Check if it's night time in game."""
    from evennia import gametime
    hour = gametime.game_time()[3]
    return hour < 6 or hour > 20

def is_day():
    """Check if it's day time in game."""
    return not is_night()
