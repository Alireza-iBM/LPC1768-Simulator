from app.adapters.fake_engine_adapter import FakeEngineAdapter
from app.adapters.fake_hardware_adapter import FakeHardwareAdapter
from app.services.event_manager import EventManager
from app.sessions.session_manager import SessionManager
from app.websocket.websocket_router import websocket_manager


class SimulationService:

    def __init__(self):
        self.session_manager = SessionManager()
        self.runtimes = {}

    def create_session(self, config=None):
        config = config or {}

        if isinstance(config.get("config"), dict):
            config = config["config"]

        session = self.session_manager.create_session(config)
        session_id = session["session_id"]

        event_manager = EventManager()

        startup_failure = config.get(
            "simulate_startup_failure",
            False
        )

        self.runtimes[session_id] = {
            "event_manager": event_manager,
            "engine": FakeEngineAdapter(
                event_manager,
                startup_failure=startup_failure
            ),
            "hardware": FakeHardwareAdapter()
        }

        return session

    def get_runtime(self, session_id):
        return self.runtimes.get(session_id)

    def get_session(self, session_id):
        return self.session_manager.get_session(session_id)

    def list_sessions(self):
        return self.session_manager.list_sessions()

    def delete_session(self, session_id):
        if self.session_manager.get_session(session_id) is None:
            return False

        self.runtimes.pop(session_id, None)

        return self.session_manager.delete_session(session_id)

    def _get_hardware_status(self, runtime):
        hardware_status = runtime["hardware"].get_status()

        engine_hardware = runtime["engine"].get_hardware_state()

        hardware_status["gpio_pins"] = engine_hardware.get(
            "gpio_pins",
            {}
        )

        return hardware_status

    async def _sync_events(self, session_id):
        runtime = self.get_runtime(session_id)

        if runtime is None:
            return

        event_manager = runtime["event_manager"]
        events = event_manager.get_events()

        for event in events:
            event["session_id"] = session_id

            self.session_manager.add_event(session_id, event)

            await websocket_manager.broadcast(session_id, event)

        event_manager.clear_events()

    async def load_firmware(self, session_id, firmware_path):
        runtime = self.get_runtime(session_id)

        if runtime is None:
            return {
                "success": False,
                "message": "Session not found"
            }

        result = runtime["engine"].load_firmware(firmware_path)

        if result.get("success"):
            self.session_manager.update_status(session_id, "ready")

        await self._sync_events(session_id)

        return result

    async def set_gpio_input(self, session_id, pin, value):
        runtime = self.get_runtime(session_id)

        if runtime is None:
            return {
                "success": False,
                "message": "Session not found"
            }

        result = runtime["engine"].set_gpio_input(pin, value)

        await self._sync_events(session_id)

        return result

    async def start_simulation(self, session_id):
        runtime = self.get_runtime(session_id)

        if runtime is None:
            return {
                "success": False,
                "message": "Session not found"
            }

        engine_result = runtime["engine"].start()

        new_status = (
            "running" if engine_result.get("success") else "error"
        )
        self.session_manager.update_status(session_id, new_status)

        await self._sync_events(session_id)

        return {
            "engine": engine_result,
            "hardware": self._get_hardware_status(runtime)
        }

    async def pause_simulation(self, session_id):
        runtime = self.get_runtime(session_id)

        if runtime is None:
            return {
                "success": False,
                "message": "Session not found"
            }

        result = runtime["engine"].pause()

        if result.get("success"):
            self.session_manager.update_status(session_id, "paused")

        await self._sync_events(session_id)

        return result

    async def resume_simulation(self, session_id):
        runtime = self.get_runtime(session_id)

        if runtime is None:
            return {
                "success": False,
                "message": "Session not found"
            }

        result = runtime["engine"].resume()

        if result.get("success"):
            self.session_manager.update_status(session_id, "running")

        await self._sync_events(session_id)

        return result

    async def reset_simulation(self, session_id):
        runtime = self.get_runtime(session_id)

        if runtime is None:
            return {
                "success": False,
                "message": "Session not found"
            }

        result = runtime["engine"].reset()

        if result.get("success"):
            new_status = (
                "ready"
                if runtime["engine"].loaded_firmware
                else "created"
            )
            self.session_manager.update_status(session_id, new_status)

        await self._sync_events(session_id)

        return result

    async def stop_simulation(self, session_id):
        runtime = self.get_runtime(session_id)

        if runtime is None:
            return {
                "success": False,
                "message": "Session not found"
            }

        engine_result = runtime["engine"].stop()

        if engine_result.get("success"):
            self.session_manager.update_status(session_id, "stopped")

        await self._sync_events(session_id)

        return {
            "engine": engine_result,
            "hardware": self._get_hardware_status(runtime)
        }

    def get_status(self, session_id):
        runtime = self.get_runtime(session_id)

        if runtime is None:
            return None

        return {
            "engine": runtime["engine"].get_cpu_state(),
            "hardware": self._get_hardware_status(runtime)
        }

    def get_session_events(self, session_id):
        return self.session_manager.get_session_events(session_id)
