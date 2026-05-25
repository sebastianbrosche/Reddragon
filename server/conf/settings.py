"""
Darkstaff MUD - Evennia Server Configuration
Based on Islands of Myth (the original 1995 MUD)

Uses Evennia defaults, overriding only what's needed.
"""

from evennia.settings_default import *
import os

######################################################################
# Evennia Contrib Modules
######################################################################

# Traits system (rpg.traits)
# No extra settings needed - uses lazy_property on typeclass

# Buffs system (rpg.buffs)
# No extra settings needed - uses lazy_property on typeclass

# Mail system (game_systems.mail)
# Enables in-game mail between accounts/characters
# Add to command sets: commands.default_cmdsets.CharacterCmdSet
MAIL_CHARACTER_MODEL = "typeclasses.characters.Character"

# Achievements system (game_systems.achievements)
# Path to achievement module definitions
ACHIEVEMENT_CONTRIB_MODULES = ["world.achievements"]

# In-game Python scripting (base_systems.ingame_python)
# Enables builders to write Python callbacks on objects in-game
# Inherit EventCharacter, EventRoom, EventObject, EventExit
# Add CmdCallback to command sets

# LLM integration (rpg.llm)
# Requires LLM server endpoint configuration
# LLM_URL = "http://localhost:8000/v1/chat/completions"
# LLM_HEADERS = {"Authorization": "Bearer YOUR_KEY"}
# LLM_PROMPT_PREFIX = "You are an NPC in a fantasy MUD world..."

# RP System (rpg.rpsystem)
# Adds sdescs, poses, recognition, language support
# Inherit ContribRPCharacter, ContribRPRoom, ContribRPObject
# Add RPSystemCmdSet to command sets

# Extended Room (grid.extended_room)
# Adds weather, season, time-of-day descriptions
# BASE_ROOM_TYPECLASS = "evennia.contrib.grid.extended_room.ExtendedRoom"

# XYZ Grid (grid.xyzgrid)
# Build world from ASCII maps with pathfinding
# Requires: evennia xyzgrid init
# Requires: evennia xyzgrid build
# Requires: evennia xyzgrid list

######################################################################
# Game Info
######################################################################

SERVERNAME = "Red Dragon Reborn"
GAME_SLOGAN = "The original 1995 MUD, reborn."

######################################################################
# Server Access
######################################################################

# Allow all hosts
ALLOWED_HOSTS = ["*"]

######################################################################
# WebSocket client port (for browser-based MUD clients)
WEBSOCKET_CLIENT_ENABLED = True
WEBSOCKET_CLIENT_PORT = 4001
WEBSOCKET_CLIENT_INTERFACE = "0.0.0.0"

# Telnet / MUD Ports
######################################################################

# Enable telnet and set ports
TELNET_ENABLED = True
TELNET_PORTS = [3000]

# Web server
WEBSERVER_ENABLED = True
WEBSERVER_PORTS = [(8000, 8001)]

# AMP (inter-process communication)
AMP_PORT = 5000
AMP_INTERFACE = "127.0.0.1"

######################################################################
# Typeclasses
######################################################################

BASE_OBJECT_TYPECLASS = "typeclasses.objects.Object"
BASE_CHARACTER_TYPECLASS = "typeclasses.characters.Character"
BASE_ROOM_TYPECLASS = "typeclasses.rooms.Room"
BASE_EXIT_TYPECLASS = "typeclasses.exits.Exit"
BASE_ACCOUNT_TYPECLASS = "typeclasses.accounts.Account"
BASE_CHANNEL_TYPECLASS = "typeclasses.channels.Channel"
BASE_SCRIPT_TYPECLASS = "typeclasses.scripts.Script"

######################################################################
# Command Sets
######################################################################

# Character command set (includes combat, economy, etc.)
CMDSET_CHARACTER = "commands.combat.CombatCmdSet"

# Divine command set (AI Dungeon Master)
CMDSET_DIVINE = "commands.ai_dm_commands.DivineCmdSet"

# Account command set (login/register commands)
CMDSET_ACCOUNT = "commands.account.AccountCmdSet"

# Unlogged-in command set (custom IOM-style login flow)
CMDSET_UNLOGGEDIN = "commands.unloggedin.UnloggedinCmdSet"

######################################################################
# Starting Location
######################################################################

# Default home for objects/characters (Limbo #2 - standard Evennia default)
# We will update this after world construction via at_server_start
DEFAULT_HOME = "#2"

# Character creation room - set by character typeclass after login
# We use a script to teleport new players to the Adventurer Guild Entrance
CHARACTER_CREATION_ROOM = "#2"

# Start location for new players - will be set after world build
START_LOCATION = "#2"

######################################################################
# Connection Screen
######################################################################

# Our custom unloggedin module provides the connection screen
CONNECTION_SCREEN_MODULE = "commands.unloggedin"

######################################################################
# Permissions
######################################################################

PERMISSION_HIERARCHY = [
    "Guest",
    "Player",
    "Helper",
    "Builder",
    "Admin",
    "Developer",
    "Immortal",
    "Implementor",
]

######################################################################
# Game Settings
######################################################################

# Combat tick rate (seconds between combat rounds)
COMBAT_TICK_RATE = 3

# Default wimpy percentage
DEFAULT_WIMPY = 0

# Base XP for level 1
BASE_XP = 500

# XP multiplier per level
XP_MULTIPLIER = 1.5

# Idle timeout (seconds)
IDLE_TIMEOUT = 3600

# Max simultaneous sessions per account
MAX_NR_SIMULTANEOUS_LOGIN = 3

# Auto-puppet settings - auto-enter the game world on login
AUTO_PUPPET = True
AUTO_CREATE_CHARACTER_WITH_ACCOUNT = True

# Disable Django password validation (this is a MUD, not a bank)
AUTH_PASSWORD_VALIDATORS = []

######################################################################
# Database (SQLite for dev)
######################################################################

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(GAME_DIR, "server", "evennia.db3"),
        "USER": "",
        "PASSWORD": "",
        "HOST": "",
        "PORT": "",
    }
}

######################################################################
# Paths
######################################################################

ROOT_URLCONF = "web.urls"
STATIC_URL = "/static/"
# Don't set STATIC_ROOT to a directory that's in STATICFILES_DIRS
STATIC_ROOT = os.path.join(GAME_DIR, "server", ".static")
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(GAME_DIR, "web", "media")

# Remove the conflicting static directory from STATICFILES_DIRS
STATICFILES_DIRS = [
    # os.path.join(GAME_DIR, "web", "static")
]

# Template directories
TEMPLATES[0]["DIRS"] = [
    os.path.join(GAME_DIR, "web", "templates", "overrides"),
    os.path.join(GAME_DIR, "web", "templates"),
]

######################################################################
# Logging
######################################################################

LOG_DIR = os.path.join(GAME_DIR, "server", "logs")
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

######################################################################
# Secret Key (CHANGE IN PRODUCTION)
######################################################################

SECRET_KEY = "darkstaff-mud-secret-key-1995-reborn"

######################################################################
# Debug
######################################################################

DEBUG = True

######################################################################
# Timezone
######################################################################

TIME_ZONE = "UTC"
USE_TZ = True

######################################################################
# In-Game Python (LPC-style softcode)
######################################################################

EVENTFUNCS_LOCATIONS = ["world.eventfuncs"]

######################################################################
# Crafting Recipes
######################################################################

CRAFT_RECIPE_MODULES = ["world.recipes"]

######################################################################
# Custom Gametime (IOM Calendar)
######################################################################

# Real seconds = game seconds / TIME_FACTOR
# TIME_FACTOR = 2 means 1 real second = 2 game seconds
TIME_FACTOR = 2

# IOM custom calendar
TIME_UNITS = {
    "sec": 1,
    "min": 60,
    "hr": 60 * 60,
    "hour": 60 * 60,
    "day": 60 * 60 * 24,
    "week": 60 * 60 * 24 * 7,
    "month": 60 * 60 * 24 * 30,
    "yr": 60 * 60 * 24 * 30 * 12,
    "year": 60 * 60 * 24 * 30 * 12,
}

# Character Creator menu
CHARGEN_MENU = "world.chargen_menu"

# In-Game Map Display
BASIC_MAP_SIZE = 5

# LLM NPC settings (optional - configure endpoint for AI NPCs)
# LLM_SERVER_API_URL = "https://api.openai.com/v1/chat/completions"
# LLM_SERVER_API_KEY = "your-api-key"
# LLM_PROMPT_PREFIX = "You are roleplaying as {name}, a {desc} in {location}. Answer with short sentences."

# Auditing - log all input/output for QA/debugging
# To enable, uncomment: AUDIT_CALLBACK = "evennia.contrib.utils.auditing.outputs.to_file"

######################################################################
# Secret Settings Override
######################################################################

try:
    from server.conf.secret_settings import *
except ImportError:
    pass
