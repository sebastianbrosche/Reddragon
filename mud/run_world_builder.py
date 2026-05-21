#!/usr/bin/env python3
"""
Run the world builder directly.
"""
import os, sys, django

# Setup Django
sys.path.insert(0, "/root/.openclaw/workspace/mud/madamsir_mud")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.conf.settings")
django.setup()

# Initialize Evennia
import evennia
evennia._init()

from typeclasses.world_builder import build_world

print("Building world...")
try:
    rooms, exits = build_world()
    print(f"✅ World build complete! {rooms} rooms, {exits} exits created.")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
