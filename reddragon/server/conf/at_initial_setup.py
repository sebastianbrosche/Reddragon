"""
Darkstaff MUD - Initial Setup

This module is called once when the server is first initialized.
World building is handled in at_server_startstop.py to avoid typeclass import issues.
"""


def at_initial_setup():
    """
    Called once when the server is first initialized.
    Minimal setup - world building happens in at_server_start.
    """
    print("Darkstaff MUD - Initial setup complete. World will be built on first server start.")
