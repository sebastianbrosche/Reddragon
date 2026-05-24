"""
Darkstaff MUD - Server Start/Stop Hooks
"""

from evennia.utils import search

def at_server_start():
    """Called when the server starts."""
    # Check if world has already been built
    results = search.search_object("Adventurer Guild Entrance", typeclass="typeclasses.rooms.Room")
    if results:
        print("Darkstaff MUD - World already exists, skipping build.")
    else:
        print("Darkstaff MUD - Building world for the first time...")
        from world.builder import build_world
        build_world()
        print("Darkstaff MUD - World building complete!")
    
    # Start hunger tick script
    from typeclasses.scripts.hunger_tick import start_hunger_tick
    start_hunger_tick()
    print("Darkstaff MUD - Hunger tick started.")

def at_server_stop():
    """Called when the server stops."""
    pass

def at_server_reload_start():
    """Called when the server begins a reload."""
    pass

def at_server_reload_stop():
    """Called when the server finishes a reload."""
    pass
