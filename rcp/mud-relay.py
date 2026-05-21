#!/usr/bin/env python3
"""
IOM WebSocket Relay
Bridges browser clients to Islands of Myth via telnet.
Also logs all MUD output so Miha can observe.
"""

import asyncio
import websockets
import json
import logging
from datetime import datetime
from pathlib import Path

# Configuration
IOM_HOST = "islandsofmyth.org"
IOM_PORT = 3000
WS_HOST = "0.0.0.0"
WS_PORT = 8765
LOG_FILE = Path("/tmp/iom-session.log")

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
        self.buffer = ""
        
    async def log_output(self, text):
        """Log MUD output to file for Miha to read"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        line = f"[{timestamp}] {text}"
        with open(LOG_FILE, 'a', encoding='utf-8', errors='replace') as f:
            f.write(line + '\n')
    
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
                        
                        # Decode with error handling
                        text = data.decode('utf-8', errors='replace')
                        
                        # Log for Miha
                        await self.log_output(text)
                        
                        # Send to browser clients
                        await self.broadcast({
                            "type": "output",
                            "data": text
                        })
                        
                    except asyncio.TimeoutError:
                        # Send keepalive
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
        logger.info(f"Client connected: {websocket.remote_address}")
        self.clients.add(websocket)
        
        try:
            # Send initial status
            await websocket.send(json.dumps({
                "type": "status",
                "msg": "Connected to relay" + (" (IOM connected)" if self.connected else " (IOM connecting...)")
            }))
            
            async for message in websocket:
                try:
                    data = json.loads(message)
                    cmd = data.get('cmd', '')
                    
                    if cmd == 'input' and self.telnet_writer:
                        text = data.get('text', '')
                        self.telnet_writer.write(text.encode('utf-8') + b'\n')
                        await self.telnet_writer.drain()
                        
                        # Echo command locally
                        await self.broadcast({
                            "type": "echo",
                            "data": f">>> {text}\n"
                        }, exclude=websocket)
                        
                    elif cmd == 'naws':
                        # Negotiate About Window Size - tell MUD our terminal size
                        width = data.get('width', 80)
                        height = data.get('height', 24)
                        # Send telnet NAWS: IAC WILL NAWS, then IAC SB NAWS width height IAC SE
                        naws = bytes([
                            255, 251, 31,  # IAC WILL NAWS
                            255, 250, 31,  # IAC SB NAWS
                            0, width,      # width high, low
                            0, height,     # height high, low
                            255, 240       # IAC SE
                        ])
                        self.telnet_writer.write(naws)
                        await self.telnet_writer.drain()
                        
                except json.JSONDecodeError:
                    logger.warning(f"Invalid message: {message[:100]}")
                    
        except websockets.exceptions.ConnectionClosed:
            logger.info("Client disconnected")
        finally:
            self.clients.discard(websocket)
    
    async def start(self):
        """Start the WebSocket server"""
        # Clear old log
        if LOG_FILE.exists():
            LOG_FILE.unlink()
        
        # Start telnet handler in background
        asyncio.create_task(self.handle_telnet())
        
        # Start WebSocket server
        logger.info(f"WebSocket server starting on {WS_HOST}:{WS_PORT}")
        async with websockets.serve(self.handle_client, WS_HOST, WS_PORT):
            await asyncio.Future()  # run forever

if __name__ == '__main__':
    relay = IOMRelay()
    asyncio.run(relay.start())
