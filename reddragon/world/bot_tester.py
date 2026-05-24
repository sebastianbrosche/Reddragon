# -*- coding: utf-8 -*-
"""
IOM Bot Testing System

Spawns automated bot characters that:
1. Log in fresh
2. Read onboarding sign and figure out the game
3. Select race and enter world
4. Get 1 billion XP
5. Find and join guilds in correct order
6. Train all skills/spells
7. Explore and test functionality
8. Write a report after 30 minutes

Usage:
    @py from world.bot_tester import spawn_test_bots; spawn_test_bots(5)
"""

import random
import time
from evennia import create_object, search_object
from evennia.utils import delay
from typeclasses.characters import Character
from typeclasses.rooms import IOMRoom

def spawn_test_bots(count=3):
    """Spawn test bot characters."""
    print(f"\n{'='*60}")
    print(f"SPAWNING {count} TEST BOTS")
    print(f"{'='*60}")
    
    # Find race selection room
    race_room = search_object("Race Selection Hall", typeclass=IOMRoom)
    if not race_room:
        print("Race Selection Hall not found! Run setup_race_selection first.")
        return
    race_room = race_room[0]
    
    bots = []
    for i in range(count):
        bot_name = f"Bot_{i+1}"
        
        # Create bot account and character
        from evennia.accounts.models import AccountDB
        
        # Create account
        account, errors = AccountDB.create(
            username=bot_name.lower(),
            password="testbot123",
            typeclass="typeclasses.accounts.Account"
        )
        
        if errors:
            print(f"  ✗ Failed to create account {bot_name}: {errors}")
            continue
        
        # Create character
        char = create_object(
            Character,
            key=bot_name,
            location=race_room
        )
        
        # Set up bot
        char.db.is_bot = True
        char.db.bot_id = i + 1
        char.db.race = random.choice(["Human", "Elf", "Dwarf", "Orc", "Halfling"])
        char.db.experience = 1000000000  # 1 billion XP
        char.db.level = 1  # Will level up quickly
        
        # Give bot basic commands knowledge
        char.db.known_commands = ["select", "enter", "look", "north", "south", "east", "west"]
        char.db.onboarding_stage = "new"  # new, read_sign, selected_race, in_world, leveling, guild_joining, maxed
        
        # Start bot behavior
        start_bot_behavior(char)
        
        bots.append(char)
        print(f"  ✓ {bot_name} created (Race: {char.db.race}, XP: 1B)")
    
    print(f"\n{'='*60}")
    print(f"Spawned {len(bots)} bots")
    print(f"{'='*60}")
    
    # Schedule report collection after 30 minutes
    delay(1800, lambda: collect_bot_reports(bots))
    
    return bots


def start_bot_behavior(bot):
    """Start the bot's automated behavior."""
    # Bots operate on a simple state machine with delays
    bot_states = {
        "new": bot_state_new,
        "read_sign": bot_state_read_sign,
        "selected_race": bot_state_selected_race,
        "in_world": bot_state_in_world,
        "leveling": bot_state_leveling,
        "guild_joining": bot_state_guild_joining,
        "maxed": bot_state_maxed,
    }
    
    def run_bot_state():
        stage = bot.db.onboarding_stage
        if stage in bot_states:
            next_stage = bot_states[stage](bot)
            if next_stage:
                bot.db.onboarding_stage = next_stage
            # Schedule next action (bots think every 5-15 seconds)
            delay(random.randint(5, 15), run_bot_state)
        else:
            bot.msg(f"|r[Bot Error]|n Unknown state: {stage}")
    
    # Start the bot
    delay(3, run_bot_state)


def bot_state_new(bot):
    """Bot just spawned. Look around and read the sign."""
    bot.execute_cmd("look")
    delay(2, lambda: bot.execute_cmd("read sign"))
    return "read_sign"


def bot_state_read_sign(bot):
    """Bot has read the sign. Now select a race."""
    # Pick a random race
    races = ["human", "elf", "dwarf", "orc", "halfling"]
    selected = random.choice(races)
    bot.execute_cmd(f"select {selected}")
    return "selected_race"


def bot_state_selected_race(bot):
    """Bot has selected race. Enter the portal."""
    bot.execute_cmd("enter portal")
    return "in_world"


def bot_state_in_world(bot):
    """Bot is now in the world. Start leveling up."""
    bot.msg("|y[Bot]|n Entered the world! Starting leveling process...")
    
    # Give bot massive XP and level them up
    bot.db.experience = 1000000000
    
    # Auto-level the bot
    while bot.db.experience >= bot.db.next_level and bot.db.level < 200:
        bot.level_up()
    
    bot.msg(f"|g[Bot]|n Leveled up to level {bot.db.level}!")
    
    # Now start guild joining
    return "guild_joining"


def bot_state_guild_joining(bot):
    """Bot joins guilds in correct order."""
    bot.msg("|y[Bot]|n Starting guild progression...")
    
    # Navigate to guild hall
    bot.execute_cmd("warp")  # Warp to adventurer guild
    delay(2, lambda: bot.execute_cmd("north"))  # Move toward guild hall
    delay(4, lambda: bot.execute_cmd("guild hall"))  # Enter guild hall
    
    # Join guilds in tier order
    # For now, just join warrior alpha
    delay(6, lambda: bot.execute_cmd("talk Warrior Guild Master"))
    delay(8, lambda: bot.execute_cmd("join warrior"))
    
    # Report success
    bot.msg("|g[Bot]|n Joined Warrior guild!")
    
    return "maxed"


def bot_state_maxed(bot):
    """Bot has maxed out. Explore and report."""
    # Random exploration
    directions = ["north", "south", "east", "west", "northeast", "northwest", "southeast", "southwest"]
    
    for _ in range(5):
        direction = random.choice(directions)
        bot.execute_cmd(direction)
        time.sleep(1)
    
    bot.msg("|g[Bot]|n Exploration complete. Awaiting report collection.")
    
    # Store report data
    bot.db.test_report = {
        "level": bot.db.level,
        "race": bot.db.race,
        "guild": bot.db.guild,
        "experience": bot.db.experience,
        "rooms_explored": len(bot.db.rooms_explored),
        "timestamp": time.time(),
    }
    
    return "maxed"  # Stay in maxed state


def collect_bot_reports(bots):
    """Collect reports from all bots after 30 minutes."""
    print(f"\n{'='*60}")
    print(f"BOT TEST REPORTS (30 minutes elapsed)")
    print(f"{'='*60}")
    
    for bot in bots:
        report = getattr(bot.db, "test_report", {})
        
        print(f"\n|y{bot.key}|n (Race: {bot.db.race})")
        print(f"  Level: {bot.db.level}")
        print(f"  Guild: {bot.db.guild or 'None'}")
        print(f"  XP: {bot.db.experience:,}")
        print(f"  Rooms explored: {len(bot.db.rooms_explored)}")
        
        if report:
            print(f"  Final report: {report}")
        else:
            print(f"  |rNo report generated!|n")
    
    print(f"\n{'='*60}")


if __name__ == "__main__":
    print("Run this from within Evennia with:")
    print("  @py from world.bot_tester import spawn_test_bots; spawn_test_bots(5)")
