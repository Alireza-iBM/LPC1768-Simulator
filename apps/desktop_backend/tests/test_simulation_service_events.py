import asyncio
from app.services.simulation_service import SimulationService


def test_firmware_loaded_events():
    service = SimulationService()
    session = service.create_session()
    session_id = session["session_id"]

    result = asyncio.run(
        service.load_firmware(session_id, "sample_firmware.elf")
    )

    assert result["success"] is True

    events = service.get_session_events(session_id)
    event_types = [event["type"] for event in events]

    assert "SESSION_STATE_CHANGED" in event_types
    assert "FIRMWARE_LOADED" in event_types

    state_event = next(
        event for event in events
        if event["type"] == "SESSION_STATE_CHANGED"
    )
    assert state_event["payload"]["status"] == "ready"

    firmware_event = next(
        event for event in events
        if event["type"] == "FIRMWARE_LOADED"
    )

    firmware = firmware_event["payload"]["firmware"]

    assert firmware["filename"] == "sample_firmware.elf"
    assert firmware["format"] == "elf"
    assert firmware["architecture"] == "ARMv7-M"
    assert firmware["load_status"] == "loaded"


def test_failed_start_emits_error_event():
    service = SimulationService()
    session = service.create_session({
        "simulate_startup_failure": True
    })
    session_id = session["session_id"]

    asyncio.run(service.start_simulation(session_id))

    events = service.get_session_events(session_id)
    event_types = [event["type"] for event in events]

    assert "ERROR" in event_types
    assert "SESSION_STATE_CHANGED" in event_types

    error_event = next(
        event for event in events
        if event["type"] == "ERROR"
    )

    assert error_event["payload"]["code"] == "ENGINE_START_FAILED"

    session_state = service.get_session(session_id)
    assert session_state["status"] == "error"
