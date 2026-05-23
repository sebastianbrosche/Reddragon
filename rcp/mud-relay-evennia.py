#!/usr/bin/env python3
"""
Myth of Islands WebSocket Relay
Bridges WebSocket clients to Evennia (localhost:3001)
"""

import asyncio
import websockets
import logging
from pathlib import Path
from datetime import datetime

# Configuration
EVENNIA_HOST = "localhost"
EVENNIA_PORT = 3001
WS_HOST = "0.0.0.0"
WS_PORT = 8766
LOG_FILE = Path("/tmp/moi-session.log")

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger('moi-relay')

class MythRelay:
    def __init__(self):
        self.clients = set()
        self.telnet_reader = None
        self.telnet_writer = None
        self.connected = False

    async def connect_telnet(self):
        try:
            logger.info(f"Connecting to Evennia {EVENNIA_HOST}:{EVENNIA_PORT}...")
            self.telnet_reader, self.telnet_writer = await asyncio.open_connection(EVENNIA_HOST, EVENNIA_PORT)
            self.connected = True
            logger.info("Connected to Evennia!")
            asyncio.create_task(self.telnet_to_clients())
        except Exception as e:
            logger.error(f"Telnet connection failed: {e}")
            self.connected = False

    async def telnet_to_clients(self):
        with open(LOG_FILE, "a", encoding="utf-8", errors="replace") as f:
            while self.connected:
                try:
                    data = await asyncio.wait_for(self.telnet_reader.read(4096), timeout=1.0)
                    if not data:
                        logger.warning("Telnet closed by server")
                        self.connected = False
                        break
                    text = data.decode("utf-8", errors="replace")
                    f.write(text)
                    f.flush()
                    # Broadcast to all WebSocket clients
                    disconnected = []
                    for client in list(self.clients):
                        try:
                            await client.send(text)
                        except Exception:
                            disconnected.append(client)
                    for client in disconnected:
                        self.clients.discard(client)
                except asyncio.TimeoutError:
                    continue
                except Exception as e:
                    logger.error(f"Telnet read error: {e}")
                    self.connected = False
                    break

    async def handle_client(self, websocket):
        logger.info(f"Client connected: {websocket.remote_address}")
        self.clients.add(websocket)
        
        if not self.connected:
            await self.connect_telnet()
        
        try:
            async for message in websocket:
                if isinstance(message, str) and self.connected and self.telnet_writer:
                    self.telnet_writer.write(message.encode("utf-8") + b"\n")
                    await self.telnet_writer.drain()
                    logger.debug(f"Sent to Evennia: {message[:50]}")
        except websockets.exceptions.ConnectionClosed:
            logger.info("Client disconnected")
        except Exception as e:
            logger.error(f"Client error: {e}")
        finally:
            self.clients.discard(websocket)

    async def run(self):
        logger.info(f"Starting WebSocket server on {WS_HOST}:{WS_PORT}")
        async with websockets.serve(self.handle_client, WS_HOST, WS_PORT, ping_interval=20, ping_timeout=10):
            await asyncio.Future()  # Run forever

if __name__ == "__main__":
    LOG_FILE.parent.mkdir(exist_ok=True)
    relay = MythRelay()
    asyncio.run(relay.run())
