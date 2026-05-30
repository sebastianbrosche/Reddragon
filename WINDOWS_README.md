# Red Dragon MUD - Windows Self-Host Guide

## Quick Start (3 Steps)

### 1. Install Python
- Download from https://www.python.org/downloads/
- **IMPORTANT**: Check "Add Python to PATH" during installation
- Needs Python 3.10 or higher

### 2. Download & Extract
1. Download `reddragon-windows.zip`
2. Extract to a folder (e.g., `C:\MUD\`)
3. Double-click `SETUP_WINDOWS.bat`

The script will:
- Install Evennia (the MUD engine)
- Create the database
- Let you create an admin account
- Start the server

### 3. Connect

**Option A: Web Client**
Open browser: http://localhost:8000

**Option B: Any MUD Client (Fado, Mudlet, etc.)**
- Host: `localhost`
- Port: `3000`

**Option C: Standalone HTML Client**
Open `reddragon-client.html` in any browser after starting the server.

---

## Manual Setup (If BAT fails)

```cmd
pip install evennia
cd reddragon
evennia migrate
evennia createsuperuser
evennia start
```

## Default Admin Account (Server-side)
If you need to reset: `evennia shell` then:
```python
from evennia.accounts.models import AccountDB
a = AccountDB.objects.get(username="yourname")
a.set_password("newpass")
a.save()
```

## Troubleshooting

**"Python not found"**
- Reinstall Python and check "Add to PATH"
- Or use `py` instead of `python`

**"Port 3000 in use"**
- Find what's using it: `netstat -ano | findstr :3000`
- Or change port in `reddragon/server/conf/settings.py`

**Database locked**
- Delete `reddragon/server/evennia.db3` and rerun `evennia migrate`

## Server Controls

```cmd
evennia start      # Start server
evennia stop       # Stop server
evennia reload     # Reload code without disconnecting players
evennia migrate    # Update database after code changes
```

## File Structure

```
reddragon/
  server/conf/settings.py      # Server config (ports, name, etc.)
  world/                        # Game world data
    ilium.py                    # Ilium City rooms
    guilds.py                   # Guild definitions
    monsters.py                 # Mob definitions
  typeclasses/                  # Core game objects
    characters.py               # Player character logic
    rooms.py                    # Room logic
    combat.py                   # Combat system
  commands/                     # Player commands
    combat.py                   # Fight commands
    economy.py                  # Gold/shop commands
```

## Need Help?

Web client: https://40ca2775.rcp-housing.pages.dev/reddragon-client.html
(Connects to local server at ws://localhost:4001)
