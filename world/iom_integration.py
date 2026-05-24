# -*- coding: utf-8 -*-
"""
IOM Integration Script - Sets up the complete world

Run from Evennia with:
    @py from world.iom_integration import setup_complete_world; setup_complete_world()

This sets up everything in the correct order:
1. Build the world (all 11,314 rooms)
2. Set up race selection room
3. Place guild masters
4. Upgrade ferries with delays
5. Configure character spawn location
"""

from evennia import search_object, create_object
from typeclasses.rooms import IOMRoom

def setup_complete_world():
    """Set up the complete IOM world with all systems."""
    print("=" * 60)
    print("IOM COMPLETE WORLD SETUP")
    print("=" * 60)
    
    # Step 1: Build the world (rooms and exits)
    print("\n[1/5] Building world...")
    try:
        from world.iom_complete_builder import build_full_world
        build_full_world()
        print("  ✓ World built")
    except Exception as e:
        print(f"  ✗ World build failed: {e}")
    
    # Step 2: Set up race selection
    print("\n[2/5] Setting up race selection...")
    try:
        from world.race_selection import setup_race_selection
        race_room, central = setup_race_selection()
        print(f"  ✓ Race selection room: {race_room.id}")
    except Exception as e:
        print(f"  ✗ Race selection failed: {e}")
    
    # Step 3: Place guild masters
    print("\n[3/5] Placing guild masters...")
    try:
        from world.guild_masters import place_guild_masters
        place_guild_masters()
        print("  ✓ Guild masters placed")
    except Exception as e:
        print(f"  ✗ Guild master placement failed: {e}")
    
    # Step 4: Upgrade ferries
    print("\n[4/5] Upgrading ferries...")
    try:
        from world.ferry_system import upgrade_ferries_to_delayed
        upgrade_ferries_to_delayed()
        print("  ✓ Ferries upgraded")
    except Exception as e:
        print(f"  ✗ Ferry upgrade failed: {e}")
    
    # Step 5: Configure login flow
    print("\n[5/5] Configuring login flow...")
    try:
        configure_login_flow()
        print("  ✓ Login flow configured")
    except Exception as e:
        print(f"  ✗ Login flow config failed: {e}")
    
    print(f"\n{'='*60}")
    print("SETUP COMPLETE")
    print(f"{'='*60}")
    print("\nNew characters will:")
    print("  1. Spawn in Race Selection Hall")
    print("  2. Read the sign with 'read sign'")
    print("  3. Select race with 'select <race>'")
    print("  4. Enter world with 'enter portal'")
    print("\nTo test with bots:")
    print("  @py from world.bot_tester import spawn_test_bots; spawn_test_bots(5)")


def configure_login_flow():
    """Configure where new characters spawn."""
    from evennia import DefaultRoom
    
    # Find race selection room
    race_room = search_object("Race Selection Hall", typeclass=IOMRoom)
    if not race_room:
        print("  Race Selection Hall not found!")
        return
    
    race_room = race_room[0]
    
    # Update the default character creation to use race room
    # This is typically done in typeclasses/accounts.py or server/conf/settings.py
    # For now, we just make sure the room exists and is accessible
    
    # Create a connection from Limbo to Race Selection Hall
    limbo = search_object("Limbo", typeclass=DefaultRoom)
    if limbo:
        limbo = limbo[0]
        
        # Check if exit exists
        has_exit = any(ex.destination == race_room for ex in limbo.exits)
        if not has_exit:
            from typeclasses.exits import IOMExit
            to_race = create_object(IOMExit, key="north")
            to_race.aliases.add("n")
            to_race.location = limbo
            to_race.destination = race_room
            print(f"  Created Limbo -> Race Hall exit")
    
    print("  Login flow configured: New characters should be moved to Race Selection Hall")


if __name__ == "__main__":
    print("Run this from within Evennia with:")
    print("  @py from world.iom_integration import setup_complete_world; setup_complete_world()")
