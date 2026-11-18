from fastapi import APIRouter, HTTPException
from app.services.simulation_service import SimulationService

router = APIRouter()

simulation_service = SimulationService()


def check_session(session_id: str):
    if simulation_service.get_runtime(session_id) is None:
        raise HTTPException(
            status_code=404,
            detail="Session not found"
        )


@router.post("/simulation/sessions")
def create_simulation_session(config: dict = None):
    return simulation_service.create_session(config)


@router.post("/simulation/firmware/{session_id}")
async def load_firmware(session_id: str, firmware_path: str):
    check_session(session_id)

    result = await simulation_service.load_firmware(
        session_id,
        firmware_path
    )

    if not result.get("success"):
        raise HTTPException(
            status_code=400,
            detail=result.get("message")
        )

    return result


@router.post("/simulation/gpio/{session_id}")
async def set_gpio_input(session_id: str, pin: str, value: bool):
    check_session(session_id)

    result = await simulation_service.set_gpio_input(
        session_id,
        pin,
        value
    )

    if not result.get("success"):
        raise HTTPException(
            status_code=400,
            detail=result.get("message")
        )

    return result


@router.post("/simulation/start/{session_id}")
async def start_simulation(session_id: str):
    check_session(session_id)

    return await simulation_service.start_simulation(session_id)


@router.post("/simulation/pause/{session_id}")
async def pause_simulation(session_id: str):
    check_session(session_id)

    return await simulation_service.pause_simulation(session_id)


@router.post("/simulation/resume/{session_id}")
async def resume_simulation(session_id: str):
    check_session(session_id)

    return await simulation_service.resume_simulation(session_id)


@router.post("/simulation/reset/{session_id}")
async def reset_simulation(session_id: str):
    check_session(session_id)

    return await simulation_service.reset_simulation(session_id)


@router.post("/simulation/stop/{session_id}")
async def stop_simulation(session_id: str):
    check_session(session_id)

    return await simulation_service.stop_simulation(session_id)


@router.get("/simulation/status/{session_id}")
def get_simulation_status(session_id: str):
    check_session(session_id)

    return simulation_service.get_status(session_id)


@router.get("/simulation/events/{session_id}")
def get_simulation_events(session_id: str):
    check_session(session_id)

    events = simulation_service.get_session_events(session_id)

    return {
        "session_id": session_id,
        "events": events
    }