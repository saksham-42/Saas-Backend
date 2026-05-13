from fastapi import WebSocket
from collections import defaultdict
import logging, asyncio, threading

logger = logging.getLogger(__name__)

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict = defaultdict(list)

    async def connect(self, websocket: WebSocket, org_id: int):
        "Accept and register a new connection for an org."
        await websocket.accept()
        self.active_connections[org_id].append(websocket)
        logger.info("WS connected: org_id=%d, total=%d", org_id, len(self.active_connections[org_id]))

    def disconnect(self, websocket: WebSocket, org_id: int):
        "Remove a connection when client disconnects."
        self.active_connections[org_id].remove(websocket)
        logger.info("WS disconnected: org_id=%d, remaining=%d", org_id, len(self.active_connections[org_id]))

    async def broadcast(self, org_id: int, message: dict):
        "Send a message to all connected clients in an org."
        connections = self.active_connections[org_id]
        for connection in connections:
            await connection.send_json(message)
        logger.debug("WS broadcast: org_id=%d, recipients=%d", org_id, len(connections))


    def broadcast_sync(self, org_id: int, message: dict):
        "Sync wrapper for broadcast — fires broadcast in a background thread."
        def run():
            import asyncio
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                loop.run_until_complete(manager.broadcast(org_id, message))
            finally:
                loop.close()
        threading.Thread(target=run, daemon=True).start()


manager = ConnectionManager()