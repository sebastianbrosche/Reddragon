#!/usr/bin/env python3
"""
Red Dragon MUD - Event Handler Initialization Script

This script ensures the in-game Python EventHandler is created on server start.
It runs once as a one-shot startup script.
"""

from evennia import create_script
from evennia.contrib.base_systems.ingame_python.scripts import EventHandler

def init_event_handler():
    """Create the global EventHandler script if it doesn't exist."""
    # Check if already exists
    existing = [s for s in EventHandler.objects.filter(db_key="event_handler")]
    if not existing:
        create_script(
            "evennia.contrib.base_systems.ingame_python.scripts.EventHandler",
            key="event_handler",
            persistent=True,
            desc="Global event handler for in-game Python scripting"
        )
        print("EventHandler script created.")
    else:
        print("EventHandler script already exists.")

if __name__ == "__main__":
    init_event_handler()
