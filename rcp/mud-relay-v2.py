#!/usr/bin/env python3
"""
IOM WebSocket Relay with Autopilot Support
Bridges browser clients to Islands of Myth via telnet.
Also logs all MUD output and supports autopilot mode.

Architecture:
    Browser WS client(s) ←→ Python relay ←→ IOM telnet
    Miha (via file) → relay → IOM (autopilot commands)
    
Autopilot mode:
    - Miha writes commands to /tmp/iom-autopilot-queue.txt
    - Relay sends them when user is inactive
    - User command = autopilot pauses 120s
    - User types "resume" = autopilot resumes
"""

import asyncio
import websockets
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
import random
import time

# Configuration
IOM_HOST = "islandsofmyth.org"
IOM_PORT = 3000
WS_HOST = "0.0.0.0"
WS_PORT = 8765
LOG_FILE = Path("/tmp/iom-session.log")
QUEUE_FILE = Path("/tmp/iom-autopilot-queue.txt")
PAUSE_UNTIL_FILE = Path("/tmp/iom-autopilot-pause")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger('iom-relay')

class IOMRelay:
    def __init__(self):
        self.clients = set()
        self.telnet_reader = None
        self.telnet_writer = None
        self.connected = False
        self.user_active_until = None
        self.last_user_command = None
        self.autopilot_enabled = True
        
    async def log_output(self, text):
        """Log MUD output to file for Miha to read"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        line = f"[{timestamp}] {text}"
        with open(LOG_FILE, 'a', encoding='utf-8', errors='replace') as f:
            f.write(line + '\n')
    
    def is_user_active(self):
        """Check if user has recently sent a command (autopilot should pause)"""
        if self.user_active_until is None:
            return False
        return datetime.now() < self.user_active_until
    
    def pause_autopilot(self, seconds=120):
        """Pause autopilot for N seconds after user command"""
        self.user_active_until = datetime.now() + timedelta(seconds=seconds)
        self.autopilot_enabled = True
        logger.info(f"Autopilot paused for {seconds}s")
    
    def check_queue(self):
        """Check for autopilot commands in queue file"""
        if not QUEUE_FILE.exists():
            return None
        
        try:
            with open(QUEUE_FILE, 'r') as f:
                lines = f.readlines()
            
            if not lines:
                return None
            
            # Get first non-empty line
            for i, line in enumerate(lines):
                cmd = line.strip()
                if cmd:
                    # Remove this line from queue
                    remaining = lines[i+1:]
                    with open(QUEUE_FILE, 'w') as f:
                        f.writelines(remaining)
                    return cmd
            
            return None
            
        except Exception as e:
            logger.error(f"Error reading queue: {e}")
            return None
    
    async def send_to_iom(self, text, source="unknown"):
        """Send a command to IOM"""
        if self.telnet_writer:
            self.telnet_writer.write(text.encode('utf-8') + b'\n')
            await self.telnet_writer.drain()
            logger.info(f"Sent to IOM [{source}]: {text}")
            return True
        return False
    
    async def autopilot_loop(self):
        """Background loop that reads queue and sends autopilot commands"""
        while True:
            await asyncio.sleep(random.uniform(1.5, 3.5))  # Random delay, human-like
            
            if not self.connected or not self.autopilot_enabled:
                continue
            
            # Check if user is active
            if self.is_user_active():
                continue
            
            # Check for queue commands
            cmd = self.check_queue()
            if cmd:
                # Add small random delay before sending
                await asyncio.sleep(random.uniform(0.2, 1.0))
                await self.send_to_iom(cmd, source="autopilot")
                
                # Echo to all clients
                await self.broadcast({
                    "type": "echo",
                    "data": f">>> [bot] {cmd}\n"
                })
    
    async def broadcast(self, message, exclude=None):
        """Send message to all connected browser clients"""
        dead = set()
        for ws in self.clients:
            if ws is exclude:
                continue
            try:
                await ws.send(json.dumps(message))
            except Exception:
                dead.add(ws)
        
        for ws in dead:
            self.clients.discard(ws)
    
    async def handle_telnet(self):
        """Connect to IOM and forward output to clients"""
        while True:
            try:
                logger.info(f"Connecting to {IOM_HOST}:{IOM_PORT}...")
                self.telnet_reader, self.telnet_writer = await asyncio.open_connection(
                    IOM_HOST, IOM_PORT
                )
                self.connected = True
                logger.info("Connected to IOM")
                
                await self.broadcast({"type": "status", "msg": "Connected to Islands of Myth"})
                
                while True:
                    try:
                        data = await asyncio.wait_for(
                            self.telnet_reader.read(4096),
                            timeout=300
                        )
                        if not data:
                            break
                        
                        text = data.decode('utf-8', errors='replace')
                        
                        # Log for Miha
                        await self.log_output(text)
                        
                        # Send to browser clients
                        await self.broadcast({
                            "type": "output",
                            "data": text
                        })
                        
                    except asyncio.TimeoutError:
                        self.telnet_writer.write(b'\n')
                        await self.telnet_writer.drain()
                        
            except Exception as e:
                logger.error(f"Telnet error: {e}")
                self.connected = False
                await self.broadcast({
                    "type": "status",
                    "msg": f"Disconnected: {str(e)}. Reconnecting in 5s..."
                })
                await asyncio.sleep(5)
    
    async def handle_client(self, websocket):
        """Handle a browser client connection"""
        client_id = f"{websocket.remote_address[0]}:{websocket.remote_address[1]}"
        logger.info(f"Client connected: {client_id}")
        self.clients.add(websocket)
        
        try:
            await websocket.send(json.dumps({
                "type": "status",
                "msg": "Connected to relay" + (" (IOM connected)" if self.connected else " (IOM connecting...)")
            }))
            
            async for message in websocket:
                try:
                    data = json.loads(message)
                    cmd = data.get('cmd', '')
                    
                    if cmd == 'input' and self.telnet_writer:
                        text = data.get('text', '').strip()
                        
                        # Handle special commands
                        if text.lower() == 'resume':
                            self.user_active_until = None
                            self.autopilot_enabled = True
                            await websocket.send(json.dumps({
                                "type": "status",
                                "msg": "Autopilot resumed"
                            }))
                            logger.info("Autopilot resumed by user")
                            continue
                        
                        if text.lower() == 'bot stop':
                            self.autopilot_enabled = False
                            self.user_active_until = None
                            await websocket.send(json.dumps({
                                "type": "status",
                                "msg": "Autopilot stopped. Type 'resume' to restart"
                            }))
                            logger.info("Autopilot stopped by user")
                            continue
                        
                        # Normal user command - send to IOM and pause autopilot
                        await self.send_to_iom(text, source="user")
                        self.pause_autopilot(120)  # Pause 2 minutes
                        
                        # Echo locally
                        await self.broadcast({
                            "type": "echo",
                            "data": f">>> {text}\n"
                        }, exclude=websocket)
                        
                    elif cmd == 'naws':
                        width = data.get('width', 80)
                        height = data.get('height', 24)
                        naws = bytes([
                            255, 251, 31,
                            255, 250, 31,
                            0, width,
                            0, height,
                            255, 240
                        ])
                        self.telnet_writer.write(naws)
                        await self.telnet_writer.drain()
                        
                except json.JSONDecodeError:
                    logger.warning(f"Invalid message from {client_id}: {message[:100]}")
                    
        except websockets.exceptions.ConnectionClosed:
            logger.info(f"Client {client_id} disconnected")
        finally:
            self.clients.discard(websocket)
    
    async def start(self):
        """Start the WebSocket server and autopilot loop"""
        # Clear old logs
        if LOG_FILE.exists():
            LOG_FILE.unlink()
        if QUEUE_FILE.exists():
            QUEUE_FILE.unlink()
        
        # Start background tasks
        asyncio.create_task(self.handle_telnet())
        asyncio.create_task(self.autopilot_loop())
        
        # Start WebSocket server
        logger.info(f"WebSocket server starting on {WS_HOST}:{WS_PORT}")
        async with websockets.serve(self.handle_client, WS_HOST, WS_PORT):
            await asyncio.Future()  # run forever

if __name__ == '__main__':
    relay = IOMRelay()
    asyncio.run(relay.start())
