"""
Centralized mock data for LPC1768 Simulator.

These fixtures are used by the Fake Engine and backend tests.
"""

SAMPLE_FIRMWARE = {
    "name": "sample_firmware.bin",
    "path": "sample_firmware.bin",
    "format": "bin",
    "valid": True
}


INVALID_FIRMWARE = {
    "name": "invalid_firmware.txt",
    "path": "invalid_firmware.txt",
    "format": "txt",
    "valid": False
}


MOCK_CPU_STATE = {
    "PC": "0x00000000",
    "SP": "0x10000000",
    "R0": "0x00000000",
    "R1": "0x00000000",
    "R2": "0x00000000",
    "R3": "0x00000000"
}


MOCK_GPIO_STATE = {
    "P2.10": False
}


MOCK_HARDWARE_STATE = {
    "connected": False,
    "gpio_pins": MOCK_GPIO_STATE.copy()
}


MOCK_SIMULATION_CONFIG = {
    "project": "LPC1768",
    "simulate_startup_failure": False
}


MOCK_STARTUP_FAILURE_CONFIG = {
    "project": "LPC1768",
    "simulate_startup_failure": True
}