
from pathlib import Path
from uuid import uuid4
from typing import Literal

from fastapi import APIRouter, File, HTTPException, UploadFile
from pydantic import BaseModel

from app.services.simulation_service import SimulationService


router = APIRouter()
simulation_service = SimulationService()

UPLOAD_ROOT = Path(__file__).resolve().parents[2] / "uploads"


class GPIOInput(BaseModel):
    level: Literal[0, 1]


def raise_api_error(status_code, code, message, recoverable=True):
    raise HTTPException(
        status_code=status_code,
        detail={
            "code": code,
            "message": message,
            "recoverable": recoverable,
            "details": {}
        }
    )


def check_session(session_id: str):
    if simulation_service.get_runtime(session_id) is None:
        raise_api_error(
            404,
            "SESSION_NOT_FOUND",
            "Simulation session was not found.",
            False
        )


@router.post("/sessions/{session_id}/firmware")
async def load_firmware(
    session_id: str,
    firmware: UploadFile = File(...)
):
    check_session(session_id)

    original_filename = (firmware.filename or "").replace("\\", "/")
    original_filename = original_filename.rsplit("/", 1)[-1]

    if not original_filename or Path(original_filename).suffix.lower() != ".elf":
        raise_api_error(
            400,
            "INVALID_FIRMWARE",
            "Only ELF firmware files are supported.",
            False
        )

    content = await firmware.read()

    if not content:
        raise_api_error(
            400,
            "EMPTY_FIRMWARE",
            "The uploaded firmware file is empty.",
            False
        )

    session_dir = UPLOAD_ROOT / session_id
    session_dir.mkdir(parents=True, exist_ok=True)

    saved_path = session_dir / f"{uuid4().hex}.elf"
    saved_path.write_bytes(content)

    result = await simulation_service.load_firmware(
        session_id,
        str(saved_path),
        filename=original_filename
    )

    if not result.get("success"):
        saved_path.unlink(missing_ok=True)
        raise_api_error(
            400,
            "FIRMWARE_LOAD_FAILED",
            result.get("message", "Firmware could not be loaded."),
            False
        )

    session = simulation_service.get_protocol_session(session_id)

    return {
        "firmware": session["firmware"]
    }


@router.post("/sessions/{session_id}/start")
async def start_simulation(session_id: str):
    check_session(session_id)

    result = await simulation_service.start_simulation(session_id)
    engine_result = result.get("engine", {})

    if not engine_result.get("success"):
        raise_api_error(
            409,
            "ENGINE_START_FAILED",
            engine_result.get("message", "Simulation could not start.")
        )

    session = simulation_service.get_protocol_session(session_id)

    return {
        "session_id": session_id,
        "status": session["status"]
    }


@router.post("/sessions/{session_id}/pause")
async def pause_simulation(session_id: str):
    check_session(session_id)

    result = await simulation_service.pause_simulation(session_id)

    if not result.get("success"):
        raise_api_error(
            409,
            "ENGINE_PAUSE_FAILED",
            result.get("message", "Simulation could not be paused.")
        )

    session = simulation_service.get_protocol_session(session_id)

    return {
        "session_id": session_id,
        "status": session["status"]
    }


@router.post("/sessions/{session_id}/reset")
async def reset_simulation(session_id: str):
    check_session(session_id)

    result = await simulation_service.reset_simulation(session_id)

    if not result.get("success"):
        raise_api_error(
            409,
            "ENGINE_RESET_FAILED",
            result.get("message", "Simulation could not be reset.")
        )

    session = simulation_service.get_protocol_session(session_id)

    return {
        "session_id": session_id,
        "status": session["status"]
    }


@router.get("/sessions/{session_id}/state")
def get_simulation_state(session_id: str):
    check_session(session_id)

    state = simulation_service.get_status(session_id)

    if state is None:
        raise_api_error(
            404,
            "SESSION_NOT_FOUND",
            "Simulation session was not found.",
            False
        )

    return state


@router.put("/sessions/{session_id}/gpio/{port}/{pin}")
async def set_gpio_input(
    session_id: str,
    port: int,
    pin: int,
    body: GPIOInput
):
    check_session(session_id)

    if port not in range(5) or pin not in range(32):
        raise_api_error(
            400,
            "INVALID_GPIO_PIN",
            "The specified GPIO pin is invalid.",
            False
        )

    pin_name = f"P{port}.{pin}"

    result = await simulation_service.set_gpio_input(
        session_id,
        pin_name,
        bool(body.level)
    )

    if not result.get("success"):
        raise_api_error(
            400,
            "GPIO_UPDATE_FAILED",
            result.get("message", "GPIO input could not be updated."),
            False
        )

    return {
        "port": port,
        "pin": pin,
        "direction": "input",
        "level": body.level,
        "source": "user"
    }
