import asyncio

from app.main import app
from app.api.simulation import simulation_service


def test_qemu_processes_are_stopped_on_shutdown(monkeypatch):
    called = False

    async def fake_stop_all():
        nonlocal called
        called = True

    monkeypatch.setattr(
        simulation_service.qemu_process_manager,
        "stop_all",
        fake_stop_all
    )

    async def run_lifecycle():
        async with app.router.lifespan_context(app):
            pass

    asyncio.run(run_lifecycle())

    assert called is True
