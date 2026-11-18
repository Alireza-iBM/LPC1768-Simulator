import re
from pathlib import Path

from app.engine.engine_interface import EngineInterface
from app.services.event_manager import EventManager

from app.fixtures.mock_data import (
    MOCK_CPU_STATE,
    MOCK_GPIO_STATE,
    SAMPLE_FIRMWARE,
    INVALID_FIRMWARE
)


class FakeEngineAdapter(EngineInterface):

    def __init__(self, event_manager=None, startup_failure=False):
        self.running = False
        self.paused = False
        self.loaded_firmware = None

        self.gpio_pins = MOCK_GPIO_STATE.copy()

        self.event_manager = event_manager or EventManager()
        self.startup_failure = startup_failure

        self.valid_gpio_ports = {
            0: 30,
            1: 31,
            2: 13,
            3: 26,
            4: 29
        }

    def load_firmware(self, firmware_path):

        if not isinstance(firmware_path, str) or not firmware_path.strip():
            return {
                "success": False,
                "message": "Invalid firmware path"
            }

        path = Path(firmware_path.strip())

        if path.name == INVALID_FIRMWARE["name"]:
            return {
                "success": False,
                "message": "Invalid firmware"
            }

        if (
            path.suffix.lower() !=
            SAMPLE_FIRMWARE["format"].lower().replace(".", "")
            and path.suffix.lower() != ".bin"
        ):
            return {
                "success": False,
                "message": "Invalid firmware format"
            }

        self.loaded_firmware = str(path)

        return {
            "success": True,
            "message": "Firmware loaded successfully",
            "firmware": self.loaded_firmware
        }

    def start(self):

        if self.running:
            return {
                "success": False,
                "message": "Engine is already running"
            }

        if self.startup_failure:
            self.event_manager.emit(
                "ENGINE_START_FAILED",
                data={"message": "Simulated startup failure"}
            )

            return {
                "success": False,
                "message": "Simulated startup failure"
            }

        self.running = True
        self.paused = False

        cpu_state = self.get_cpu_state()

        self.event_manager.emit(
            "ENGINE_STARTED",
            data=cpu_state
        )

        self.event_manager.emit(
            "CPU_STATE_UPDATED",
            data=cpu_state
        )

        return {
            "success": True,
            "message": "Fake engine started"
        }

    def pause(self):

        if not self.running or self.paused:
            return {
                "success": False,
                "message": "Engine cannot be paused"
            }

        self.paused = True

        self.event_manager.emit(
            "ENGINE_PAUSED",
            data=self.get_cpu_state()
        )

        return {
            "success": True,
            "message": "Fake engine paused"
        }

    def resume(self):

        if not self.running or not self.paused:
            return {
                "success": False,
                "message": "Engine cannot be resumed"
            }

        self.paused = False

        self.event_manager.emit(
            "ENGINE_RESUMED",
            data=self.get_cpu_state()
        )

        return {
            "success": True,
            "message": "Fake engine resumed"
        }

    def reset(self):

        self.running = False
        self.paused = False
        self.gpio_pins = MOCK_GPIO_STATE.copy()

        self.event_manager.emit(
            "ENGINE_RESET",
            data=self.get_cpu_state()
        )

        return {
            "success": True,
            "message": "Fake engine reset"
        }

    def stop(self):

        if not self.running:
            return {
                "success": False,
                "message": "Engine is not running"
            }

        self.running = False
        self.paused = False

        self.event_manager.emit(
            "ENGINE_STOPPED",
            data=self.get_cpu_state()
        )

        return {
            "success": True,
            "message": "Fake engine stopped"
        }

    def get_cpu_state(self):

        return {
            "running": self.running,
            "paused": self.paused,
            "firmware": self.loaded_firmware,
            "registers": MOCK_CPU_STATE.copy()
        }

    def get_hardware_state(self):

        return {
            "gpio_pins": self.gpio_pins.copy()
        }

    def is_valid_gpio_pin(self, pin):

        if not isinstance(pin, str):
            return False

        match = re.fullmatch(
            r"P([0-4])\.(\d{1,2})",
            pin.strip().upper()
        )

        if not match:
            return False

        port = int(match.group(1))
        bit = int(match.group(2))

        return bit <= self.valid_gpio_ports[port]

    def set_gpio_input(self, pin, value):

        if not self.is_valid_gpio_pin(pin):
            return {
                "success": False,
                "message": f"Invalid GPIO pin: {pin}"
            }

        pin = pin.strip().upper()
        self.gpio_pins[pin] = bool(value)

        self.event_manager.emit(
            "GPIO_CHANGED",
            data={
                "pin": pin,
                "value": self.gpio_pins[pin]
            }
        )

        return {
            "success": True,
            "pin": pin,
            "value": self.gpio_pins[pin]
        }

    def get_status(self):

        return {
            "running": self.running,
            "paused": self.paused,
            "firmware": self.loaded_firmware
        }