"""Development-only mock API/WebSocket server.

Payload names and event envelopes follow protocol/ on develop (schema_version
1.0.0). Values are synthetic and are not evidence of QEMU correctness.
"""
from __future__ import annotations

import asyncio
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="LPC1768 Simulator Mock Server", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Development only. Restrict this in production.
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

SESSIONS: dict[str, dict[str, Any]] = {
    "demo-session-001": {
        "session_id": "demo-session-001",
        "status": "stopped",
        "firmware": None,
        "target": {"mcu": "LPC1768"},
    }
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def event(event_type: str, session_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "1.0.0",
        "type": event_type,
        "event_id": str(uuid4()),
        "session_id": session_id,
        "timestamp": now(),
        "payload": payload,
    }


@app.get("/api/v1/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "service": "lpc1768-mock-server", "mode": "mock"}


@app.get("/api/v1/status")
async def system_status() -> dict[str, Any]:
    return {
        "cpu": {"available": True, "architecture": "ARM Cortex-M3", "state": "ready"},
        "simulation": {"status": "stopped"},
        "firmware": {"loaded": False, "filename": None},
        "hardware": {"available": True, "target": "LPC1768"},
        "mode": "mock",
    }


@app.get("/api/v1/sessions")
async def list_sessions() -> dict[str, Any]:
    return {"items": list(SESSIONS.values())}


@app.post("/api/v1/sessions")
async def create_session() -> dict[str, Any]:
    session_id = f"mock-{uuid4().hex[:12]}"
    session = {
        "session_id": session_id,
        "status": "stopped",
        "firmware": None,
        "target": {"mcu": "LPC1768"},
    }
    SESSIONS[session_id] = session
    return session


@app.get("/api/v1/sessions/{session_id}/state")
async def get_state(session_id: str) -> dict[str, Any]:
    session = SESSIONS.get(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail={"code": "SESSION_NOT_FOUND"})
    return {
        "session": session,
        "cpu_state": {"available": False, "source": "unavailable", "pc": None, "registers": None},
        "hardware_state": {"available": True, "source": "mock", "gpio": []},
    }


@app.post("/api/v1/sessions/{session_id}/firmware")
async def load_firmware(session_id: str) -> dict[str, Any]:
    session = SESSIONS.get(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail={"code": "SESSION_NOT_FOUND"})
    # No file parsing here: this endpoint only unblocks client development.
    session["firmware"] = {"filename": "mock-firmware.elf", "loaded": True, "source": "mock"}
    return session["firmware"]


@app.post("/api/v1/sessions/{session_id}/{action}")
async def session_action(session_id: str, action: str) -> dict[str, Any]:
    session = SESSIONS.get(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail={"code": "SESSION_NOT_FOUND"})
    transitions = {
        "start": "running",
        "pause": "paused",
        "reset": "stopped",
    }
    if action not in transitions:
        raise HTTPException(status_code=404, detail={"code": "UNSUPPORTED_ACTION"})
    session["status"] = transitions[action]
    return {"session": session, "mode": "mock"}


@app.put("/api/v1/sessions/{session_id}/gpio/{port}/{pin}")
async def set_gpio_input(session_id: str, port: int, pin: int, body: dict[str, Any]) -> dict[str, Any]:
    if session_id not in SESSIONS:
        raise HTTPException(status_code=404, detail={"code": "SESSION_NOT_FOUND"})
    level = body.get("level")
    if port not in range(5) or pin not in range(32) or level not in (0, 1):
        raise HTTPException(status_code=422, detail={"code": "INVALID_GPIO_INPUT"})
    return {"port": port, "pin": pin, "level": level, "source": "mock"}


@app.delete("/api/v1/sessions/{session_id}", status_code=204)
async def delete_session(session_id: str) -> None:
    if session_id not in SESSIONS:
        raise HTTPException(status_code=404, detail={"code": "SESSION_NOT_FOUND"})
    del SESSIONS[session_id]


@app.websocket("/api/v1/sessions/{session_id}/events")
async def session_events(websocket: WebSocket, session_id: str) -> None:
    await websocket.accept()
    if session_id not in SESSIONS:
        await websocket.send_json(event("ERROR", session_id, {
            "code": "SESSION_NOT_FOUND", "message": "Unknown mock session",
            "recoverable": False, "details": None
        }))
        await websocket.close(code=1008)
        return

    session = SESSIONS[session_id]
    await websocket.send_json(event("SESSION_STATE_CHANGED", session_id, {"status": session["status"]}))
    await websocket.send_json(event("GPIO_CHANGED", session_id, {
        "port": 0, "pin": 0, "direction": "output", "level": 1, "source": "mock"
    }))
    try:
        while True:
            # Receive text to detect disconnects; this mock is server-event driven.
            await websocket.receive_text()
    except WebSocketDisconnect:
        return
