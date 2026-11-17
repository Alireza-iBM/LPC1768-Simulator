from fastapi import WebSocket


class WebSocketManager:

    def __init__(self):
        self.active_connections = {}

    async def connect(self, session_id: str, websocket: WebSocket):
        await websocket.accept()

        if session_id not in self.active_connections:
            self.active_connections[session_id] = []

        self.active_connections[session_id].append(websocket)

    def disconnect(self, session_id: str, websocket: WebSocket):
        if session_id in self.active_connections:
            if websocket in self.active_connections[session_id]:
                self.active_connections[session_id].remove(websocket)

            if not self.active_connections[session_id]:
                del self.active_connections[session_id]

    async def broadcast(self, session_id: str, event: dict):
        connections = self.active_connections.get(session_id, [])

        disconnected = []

        for websocket in connections:
            try:
                await websocket.send_json(event)
            except Exception:
                disconnected.append(websocket)

        for websocket in disconnected:
            self.disconnect(session_id, websocket)