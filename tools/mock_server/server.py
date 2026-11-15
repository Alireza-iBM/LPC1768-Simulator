"""Development-only mock API/WebSocket server for the LPC1768 Simulator.

This server intentionally provides deterministic fake data. It is not the real
simulation backend and must never be used to claim that QEMU hardware behavior
has been verified.
"""
from __future__ import annotations

import asyncio
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="LPC1768 Simulator Mock Server", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Development only; production backend must restrict origins.
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

SESSIONS: dict[str, dict[str, Any]] = {
    "mock-session-001": {
        "session_id": "mock-session-001",
        "name": "GPIO demo",
        "status": "stopped",
        "firmware": None,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
}


def envelope(event_type: str, payload: dict[str, Any], session_id: str | None = None) -> dict[str, Any]:
    return {
        "protocol_version": "1.0.0",
        "type": event_type,
        "message_id": str(uuid4()),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "session_id": session_id,
        "payload": payload,
    }


@app.get("/api/v1/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "service": "lpc1768-mock-server", "mode": "mock"}


@app.get("/api/v1/status")
async def system_status() -> dict[str, Any]:
    return {
        "cpu": {"status": "ready", "architecture": "ARM Cortex-M3"},
        "simulation": {"status": "stopped"},
        "firmware": {"status": "not_loaded", "filename": None},
        "hardware": {"status": "ready", "board": "LPC1768"},
        "mode": "mock",
    }


@app.get("/api/v1/sessions")
async def list_sessions() -> dict[str, Any]:
    return {"items": list(SESSIONS.values()), "count": len(SESSIONS), "mode": "mock"}


@app.post("/api/v1/sessions")
async def create_session() -> dict[str, Any]:
    session_id = f"mock-{uuid4().hex[:12]}"
    session = {
        "session_id": session_id,
        "name": "New mock session",
        "status": "stopped",
        "firmware": None,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    SESSIONS[session_id] = session
    return session


@app.get("/api/v1/sessions/{session_id}")
async def get_session(session_id: str) -> dict[str, Any]:
    session = SESSIONS.get(session_id)
    if session is None:
        return {"error": "session_not_found", "session_id": session_id}
    return session


@app.post("/api/v1/sessions/{session_id}/{action}")
async def session_action(session_id: str, action: str) -> dict[str, Any]:
    session = SESSIONS.get(session_id)
    if session is None:
        return {"error": "session_not_found", "session_id": session_id}
    if action not in {"start", "pause", "resume", "stop", "reset"}:
        return {"error": "unsupported_action", "action": action}
    session["status"] = {
        "start": "running",
        "pause": "paused",
        "resume": "running",
        "stop": "stopped",
        "reset": "stopped",
    }[action]
    return {"session": session, "event": envelope(f"simulation.{action}", {"status": session["status"]}, session_id)}


@app.websocket("/ws/v1/sessions/{session_id}")
async def session_events(websocket: WebSocket, session_id: str) -> None:
    await websocket.accept()
    if session_id not in SESSIONS:
        await websocket.send_json(envelope("session.error", {"code": "session_not_found"}, session_id))
        await websocket.close(code=1008)
        return

    await websocket.send_json(envelope("session.snapshot", {
        "status": SESSIONS[session_id]["status"],
        "cpu": {"pc": "0x00000000", "state": "ready"},
        "firmware": SESSIONS[session_id]["firmware"],
    }, session_id))

    # Deterministic demo event so Flutter and the board view can be developed
    # before the QEMU adapter is connected.
    await asyncio.sleep(0.5)
    await websocket.send_json(envelope("gpio.pin_changed", {
        "port": 0, "pin": 0, "level": 1, "direction": "output", "function": "gpio"
    }, session_id))

    try:
        while True:
            # Keep the socket open; respond to optional client ping messages.
            message = await websocket.receive_text()
            await websocket.send_json(envelope("connection.pong", {"echo": message}, session_id))
    except WebSocketDisconnect:
        return
