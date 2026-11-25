
import asyncio

from app.services.simulation_service import SimulationService


def test_session_status_lifecycle():
    service = SimulationService()
    session = service.create_session()
    session_id = session["session_id"]

    assert service.get_session(session_id)["status"] == "created"

    firmware_result = asyncio.run(
        service.load_firmware(session_id, "sample_firmware.elf")
    )

    assert firmware_result["success"] is True
    assert service.get_session(session_id)["status"] == "ready"

    asyncio.run(service.start_simulation(session_id))
    assert service.get_session(session_id)["status"] == "running"

    asyncio.run(service.pause_simulation(session_id))
    assert service.get_session(session_id)["status"] == "paused"

    asyncio.run(service.resume_simulation(session_id))
    assert service.get_session(session_id)["status"] == "running"

    asyncio.run(service.reset_simulation(session_id))
    assert service.get_session(session_id)["status"] == "ready"

    asyncio.run(service.start_simulation(session_id))
    asyncio.run(service.stop_simulation(session_id))
    assert service.get_session(session_id)["status"] == "stopped"


def test_failed_start_sets_error_status():
    service = SimulationService()
    session = service.create_session({
        "simulate_startup_failure": True
    })
    session_id = session["session_id"]

    result = asyncio.run(
        service.start_simulation(session_id)
    )

    assert result["engine"]["success"] is False
    assert service.get_session(session_id)["status"] == "error"


def test_resume_simulation_updates_status():
    service = SimulationService()
    session = service.create_session()
    session_id = session["session_id"]

    asyncio.run(service.load_firmware(session_id, "sample_firmware.elf"))
    asyncio.run(service.start_simulation(session_id))
    asyncio.run(service.pause_simulation(session_id))

    result = asyncio.run(service.resume_simulation(session_id))

    assert result["success"] is True
    assert service.get_session(session_id)["status"] == "running"


def test_reset_simulation_updates_status():
    service = SimulationService()
    session = service.create_session()
    session_id = session["session_id"]

    asyncio.run(service.load_firmware(session_id, "sample_firmware.elf"))
    asyncio.run(service.start_simulation(session_id))

    result = asyncio.run(service.reset_simulation(session_id))

    assert result["success"] is True
    assert service.get_session(session_id)["status"] == "ready"


def test_stop_simulation_updates_status():
    service = SimulationService()
    session = service.create_session()
    session_id = session["session_id"]

    asyncio.run(service.load_firmware(session_id, "sample_firmware.elf"))
    asyncio.run(service.start_simulation(session_id))

    result = asyncio.run(service.stop_simulation(session_id))

    assert result["engine"]["success"] is True
    assert service.get_session(session_id)["status"] == "stopped"


def test_delete_session_stops_running_process(monkeypatch):
    service = SimulationService()
    session = service.create_session()
    session_id = session["session_id"]

    stopped_sessions = []

    service.qemu_process_manager.get_status = lambda sid: {
        "running": True
    } if sid == session_id else None

    async def fake_stop(sid):
        stopped_sessions.append(sid)
        return {"success": True}

    monkeypatch.setattr(
        service.qemu_process_manager,
        "stop",
        fake_stop,
    )

    result = asyncio.run(service.delete_session(session_id))

    assert result is True
    assert stopped_sessions == [session_id]
    assert service.get_session(session_id) is None
    assert session_id not in service.runtimes
