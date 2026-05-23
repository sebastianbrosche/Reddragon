r"""
Evennia settings file.

The available options are found in the default settings file found
here:

https://www.evennia.com/docs/latest/Setup/Settings-Default.html

Remember:

Don't copy more from the default file than you actually intend to
change; this will make sure that you don't overload upstream updates
unnecessarily.

When changing a setting requiring a file system path (like
path/to/actual/file.py), use GAME_DIR and EVENNIA_DIR to reference
your game folder and the Evennia library folders respectively. Python
paths (path.to.module) should be given relative to the game's root
folder (typeclasses.foo) whereas paths within the Evennia library
needs to be given explicitly (evennia.foo).

If you want to share your game dir, including its settings, you can
put secret game- or server-specific settings in secret_settings.py.

"""

# Use the defaults from Evennia unless explicitly overridden
from evennia.settings_default import *

######################################################################
# Evennia base server config
######################################################################

# This is the name of your game. Make it catchy!
SERVERNAME = "Myth of Islands"

# Port overrides — running on 3000 range
TELNET_PORTS = [3001]
WEBSERVER_PORTS = [(3000, 4005)]
WEBSOCKET_CLIENT_PORT = 3002

# Web client websocket URL for external access through tunnel
WEBSOCKET_CLIENT_URL = "wss://enabling-male-involve-impressive.trycloudflare.com/ws"

# CSRF trusted origins for the tunnel domain
CSRF_TRUSTED_ORIGINS = ['https://enabling-male-involve-impressive.trycloudflare.com']

# No password restrictions — allow any password
AUTH_PASSWORD_VALIDATORS = []

# Idle timeout: 1 hour (3600 seconds)
IDLE_TIMEOUT = 3600

# Default home for new characters — Adventurer's Guild of Illium
DEFAULT_HOME = "#1937"

######################################################################
# Settings given in secret_settings.py override those in this file.
######################################################################
try:
    from server.conf.secret_settings import *
except ImportError:
    print("secret_settings.py file not found or failed to import.")
