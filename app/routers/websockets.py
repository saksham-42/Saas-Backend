from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.core.websocket_manager import manager

router = APIRouter(tags=["websockets"])


@router.websocket("/ws/organizations/{org_id}")
async def websocket_endpoint(websocket: WebSocket, org_id: int):
    "Accept WS connection, keep alive, handle disconnect cleanly."
    await manager.connect(websocket, org_id)
    try:
        while True:
            await websocket.receive_text()  # keeps connection open, ignores client messages for now
    except WebSocketDisconnect:
        manager.disconnect(websocket, org_id)