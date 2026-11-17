from fastapi import APIRouter, HTTPException
from app.api.simulation import simulation_service

router = APIRouter()


@router.post("/sessions")
def create_session(config: dict = None):
    return simulation_service.create_session(config)


@router.get("/sessions")
def list_sessions():
    return simulation_service.list_sessions()


@router.get("/sessions/{session_id}")
def get_session(session_id: str):
    session = simulation_service.get_session(session_id)

    if session is None:
        raise HTTPException(
            status_code=404,
            detail="Session not found"
        )

    return session


@router.delete("/sessions/{session_id}")
def delete_session(session_id: str):
    deleted = simulation_service.delete_session(session_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Session not found"
        )

    return {
        "message": "Session deleted successfully"
    }


@router.get("/sessions/{session_id}/events")
def get_session_events(session_id: str):
    events = simulation_service.get_session_events(session_id)

    if events is None:
        raise HTTPException(
            status_code=404,
            detail="Session not found"
        )

    return {
        "session_id": session_id,
        "events": events
    }