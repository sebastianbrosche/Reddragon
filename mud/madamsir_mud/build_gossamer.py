#!/usr/bin/env python3
"""
Build Gossamer area in Red Dragon MUD
Based on IOM Gossamer map exploration data.

Run via: evennia shell < build_gossamer.py
"""
import os, sys

# Setup Django/Evennia
sys.path.insert(0, '/root/.openclaw/workspace/mud/madamsir_mud')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.conf.settings')
import django
django.setup()

from evennia import create_object, search_object
from evennia.objects.objects import DefaultRoom
from evennia.objects.objects import DefaultExit

print("Building Gossamer area...")

# =============================================================================
# GOSSAMER ROOMS
# =============================================================================

# Sandy Beach (entry point from Illium docks)
beach = search_object('Sandy Beach', typeclass=DefaultRoom)
if beach:
    beach = beach[0]
    print(f'Found Sandy Beach: #{beach.id}')
else:
    beach = create_object(DefaultRoom, key='Sandy Beach')
    beach.db.desc = "You are on a long sandy beach. Waves gently lap at the sand, covering the footprints that you are making. The beach stretches along the shore of the Gossamer River. To the northeast, a ghastly swamp rises from the water's edge."
    print(f'Created Sandy Beach: #{beach.id}')

# Ghastly Swamp (north of beach)
swamp = search_object('Ghastly Swamp', typeclass=DefaultRoom)
if swamp:
    swamp = swamp[0]
    print(f'Found Ghastly Swamp: #{swamp.id}')
else:
    swamp = create_object(DefaultRoom, key='Ghastly Swamp')
    swamp.db.desc = "Your footsteps squish as you struggle through this ghastly swamp. The odor is hideous. Dark water pools between gnarled roots, and strange insects buzz around your head. Mist hangs low over the stagnant surface."
    print(f'Created Ghastly Swamp: #{swamp.id}')

# Badlands (beyond swamp)
badlands = search_object('Badlands', typeclass=DefaultRoom)
if badlands:
    badlands = badlands[0]
    print(f'Found Badlands: #{badlands.id}')
else:
    badlands = create_object(DefaultRoom, key='Badlands')
    badlands.db.desc = "The terrain here is harsh and unforgiving. Cracked earth and jagged rocks stretch in every direction. Sparse vegetation clings to life between the stones. The heat radiates from the ground in shimmering waves."
    print(f'Created Badlands: #{badlands.id}')

# Forest (dense woodland)
forest = search_object('Dark Forest', typeclass=DefaultRoom)
if forest:
    forest = forest[0]
    print(f'Found Dark Forest: #{forest.id}')
else:
    forest = create_object(DefaultRoom, key='Dark Forest')
    forest.db.desc = "Tall trees rise on all sides, their canopy blocking out most of the sunlight. The air is cool and damp. Strange sounds echo from the depths of the woods. Vines hang from ancient branches, and the forest floor is covered in fallen leaves."
    print(f'Created Dark Forest: #{forest.id}')

# Plains (open grassland)
plains = search_object('Open Plains', typeclass=DefaultRoom)
if plains:
    plains = plains[0]
    print(f'Found Open Plains: #{plains.id}')
else:
    plains = create_object(DefaultRoom, key='Open Plains')
    plains.db.desc = "Endless grassland stretches to the horizon in every direction. The wind ripples through the tall grass like waves on a sea. Wildflowers dot the landscape in patches of color. In the distance, you can see a faint outline of mountains."
    print(f'Created Open Plains: #{plains.id}')

# Path to Docks (leads back toward Illium)
docks_path = search_object('Path to Docks', typeclass=DefaultRoom)
if docks_path:
    docks_path = docks_path[0]
    print(f'Found Path to Docks: #{docks_path.id}')
else:
    docks_path = create_object(DefaultRoom, key='Path to Docks')
    docks_path.db.desc = "A worn dirt path leads through the wilderness toward the river docks. Travelers have packed the earth here for generations. To the south, you can smell the sea air. To the north, the path continues deeper into Gossamer."
    print(f'Created Path to Docks: #{docks_path.id}')

# Adventurer's Guild (starting location)
guild = search_object("Adventurer's Guild", typeclass=DefaultRoom)
if guild:
    guild = guild[0]
    print(f"Found Adventurer's Guild: #{guild.id}")
else:
    guild = create_object(DefaultRoom, key="Adventurer's Guild")
    guild.db.desc = "The Adventurer's Guild of Gossamer. A large stone hall with banners of past heroes hanging from the rafters. Wooden tables are scattered about, and a crackling fireplace warms the room. A notice board near the entrance is covered in quests and bounties. The guild master stands behind a desk, ready to help new adventurers."
    print(f"Created Adventurer's Guild: #{guild.id}")

# =============================================================================
# EXITS
# =============================================================================

def create_exit(name, origin, destination, aliases=None):
    """Create a two-way exit between rooms."""
    aliases = aliases or []
    # Check if exit already exists
    existing = [ex for ex in origin.exits if ex.key == name]
    if existing:
        print(f'  Exit {name} already exists from {origin.key}')
        return
    
    exit_obj = create_object(DefaultExit, key=name, location=origin, destination=destination)
    for alias in aliases:
        exit_obj.aliases.add(alias)
    print(f'  Created exit: {origin.key} --{name}--> {destination.key}')

# From Sandy Beach
print("\nCreating exits from Sandy Beach...")
create_exit('northeast', beach, swamp, ['ne'])
create_exit('north', beach, docks_path, ['n'])

# From Ghastly Swamp
print("\nCreating exits from Ghastly Swamp...")
create_exit('southwest', swamp, beach, ['sw'])
create_exit('north', swamp, badlands, ['n'])
create_exit('east', swamp, forest, ['e'])

# From Badlands
print("\nCreating exits from Badlands...")
create_exit('south', badlands, swamp, ['s'])
create_exit('east', badlands, plains, ['e'])

# From Dark Forest
print("\nCreating exits from Dark Forest...")
create_exit('west', forest, swamp, ['w'])
create_exit('north', forest, plains, ['n'])
create_exit('south', forest, guild, ['s'])

# From Open Plains
print("\nCreating exits from Open Plains...")
create_exit('west', plains, badlands, ['w'])
create_exit('south', plains, forest, ['s'])

# From Path to Docks
print("\nCreating exits from Path to Docks...")
create_exit('south', docks_path, beach, ['s'])
create_exit('north', docks_path, guild, ['n'])

# From Adventurer's Guild
print("\nCreating exits from Adventurer's Guild...")
create_exit('north', guild, forest, ['n'])
create_exit('south', guild, docks_path, ['s'])

# =============================================================================
# SET STARTING LOCATION
# =============================================================================

# Set the guild as the default home for new characters
from evennia.server.models import ServerConfig
try:
    ServerConfig.objects.conf("default_home", str(guild.id))
    print(f"\nSet default home (spawn) to: {guild.key} (#{guild.id})")
except Exception as e:
    print(f"\nCould not set default home: {e}")
    print(f"Guild ID is {guild.id} — set it manually in settings if needed")

print("\nGossamer area built successfully!")
