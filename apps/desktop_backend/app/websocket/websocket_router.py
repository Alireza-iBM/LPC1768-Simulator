
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.websocket.websocket_manager import WebSocketManager


router = APIRouter()
websocket_manager = WebSocketManager()


@router.websocket("/api/v1/sessions/{session_id}/events")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await websocket_manager.connect(session_id, websocket)

    try:
        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        websocket_manager.disconnect(session_id, websocket)

    except Exception:
        websocket_manager.disconnect(session_id, websocket)
