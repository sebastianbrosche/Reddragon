@echo off
REM Red Dragon MUD - Windows Setup Script
REM Run this as Administrator for best results

echo ========================================
echo   RED DRAGON MUD - Windows Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH.
    echo.
    echo Please install Python 3.10 or higher from:
    echo https://www.python.org/downloads/
    echo.
    echo IMPORTANT: During installation, check:
    echo   [x] Add Python to PATH
    echo   [x] Install pip
    echo.
    pause
    exit /b 1
)

echo [OK] Python found.
python --version
echo.

REM Install Evennia
echo [1/4] Installing Evennia...
pip install evennia
if errorlevel 1 (
    echo [ERROR] Evennia installation failed.
    pause
    exit /b 1
)

echo [OK] Evennia installed.
echo.

REM Navigate to reddragon directory
cd /d "%~dp0"
if not exist "reddragon\server\conf\settings.py" (
    echo [ERROR] reddragon folder not found.
    echo Make sure this .bat file is in the same folder as the reddragon directory.
    pause
    exit /b 1
)

cd reddragon

echo [2/4] Initializing database...
evennia migrate
if errorlevel 1 (
    echo [ERROR] Database migration failed.
    pause
    exit /b 1
)

echo [OK] Database ready.
echo.

REM Create superuser account
echo [3/4] Creating admin account...
echo.
echo You will now create an admin account for the MUD.
echo This is your GOD account - remember the password!
echo.
evennia createsuperuser

echo.
echo [4/4] Starting server...
echo.
echo The MUD will start on:
echo   Telnet/MUD Client: localhost:3000
echo   Web Client:        http://localhost:8000
echo.
echo Press Ctrl+C twice to stop the server.
echo.
pause

evennia start -l
