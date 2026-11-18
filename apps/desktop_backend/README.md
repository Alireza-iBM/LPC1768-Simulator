# LPC1768 Simulator – Desktop Backend

## 1. Overview

The Desktop Backend is the simulation controller for the LPC1768 Simulator project.

It is built with **Python** and **FastAPI** and provides REST API endpoints and WebSocket communication for managing simulation sessions, controlling the simulation engine, loading firmware, handling GPIO inputs, and streaming simulation events.

The current implementation uses a Fake Engine and mock hardware components. It is designed to support future integration with a real QEMU-based engine.

## 2. Features

* FastAPI-based REST API
* Independent simulation sessions
* Fake Engine Adapter
* Fake Hardware Adapter
* Firmware loading simulation
* Start, Pause, Resume, Reset, and Stop operations
* GPIO input handling
* CPU and hardware state reporting
* Event management
* WebSocket event broadcasting
* Backend health check
* Backend availability testing
* Simulated startup failure handling

## 3. Project Structure

```text
desktop_backend/
│
├── app/
│   ├── adapters/
│   │   ├── fake_engine_adapter.py
│   │   └── fake_hardware_adapter.py
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── sessions.py
│   │   └── simulation.py
│   │
│   ├── engine/
│   │   └── engine_interface.py
│   │
│   ├── fixtures/
│   │   └── mock_data.py
│   │
│   ├── services/
│   │   ├── event_manager.py
│   │   └── simulation_service.py
│   │
│   ├── sessions/
│   │   ├── __init__.py
│   │   └── session_manager.py
│   │
│   ├── websocket/
│   │   ├── websocket_manager.py
│   │   └── websocket_router.py
│   │
│   ├── __init__.py
│   └── main.py
│
├── tests/
├── README.md
└── requirements.txt
```

## 4. Requirements

* Python 3.12 or compatible version
* pip
* Windows or Linux

## 5. Installation

Install the project dependencies:

```bash
pip install -r requirements.txt
```

If using a virtual environment, activate it before installing dependencies.

## 6. Running the Backend

Run the following command from the `desktop_backend` directory:

```bash
python -m uvicorn app.main:app --reload
```

The backend will be available at:

```text
http://127.0.0.1:8000
```

FastAPI Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

## 7. REST API Endpoints

All REST API endpoints use the `/api/v1` prefix.

### Health Check

| Method | Endpoint         | Description                |
| ------ | ---------------- | -------------------------- |
| GET    | `/api/v1/health` | Check backend availability |

### Session Management

| Method | Endpoint                               | Description         |
| ------ | -------------------------------------- | ------------------- |
| POST   | `/api/v1/sessions`                     | Create a session    |
| GET    | `/api/v1/sessions`                     | List all sessions   |
| GET    | `/api/v1/sessions/{session_id}`        | Get session details |
| DELETE | `/api/v1/sessions/{session_id}`        | Delete a session    |
| GET    | `/api/v1/sessions/{session_id}/events` | Get session events  |

### Simulation Control

| Method | Endpoint                                   | Description                 |
| ------ | ------------------------------------------ | --------------------------- |
| POST   | `/api/v1/simulation/sessions`              | Create a simulation session |
| POST   | `/api/v1/simulation/firmware/{session_id}` | Load firmware               |
| POST   | `/api/v1/simulation/gpio/{session_id}`     | Set GPIO input              |
| POST   | `/api/v1/simulation/start/{session_id}`    | Start simulation            |
| POST   | `/api/v1/simulation/pause/{session_id}`    | Pause simulation            |
| POST   | `/api/v1/simulation/resume/{session_id}`   | Resume simulation           |
| POST   | `/api/v1/simulation/reset/{session_id}`    | Reset simulation            |
| POST   | `/api/v1/simulation/stop/{session_id}`     | Stop simulation             |
| GET    | `/api/v1/simulation/status/{session_id}`   | Get simulation status       |
| GET    | `/api/v1/simulation/events/{session_id}`   | Get simulation events       |

### Backend Availability Testing

| Method | Endpoint                            | Description                             |
| ------ | ----------------------------------- | --------------------------------------- |
| POST   | `/api/v1/test/backend-availability` | Change backend availability for testing |

This test endpoint accepts a Boolean `available` parameter.

## 8. WebSocket Communication

WebSocket connections use the following endpoint:

```text
ws://127.0.0.1:8000/ws/{session_id}
```

Each session has its own WebSocket connections.

Events are broadcast to connected clients belonging to the corresponding session.

Example event types:

* `ENGINE_STARTED`
* `ENGINE_PAUSED`
* `ENGINE_RESUMED`
* `ENGINE_RESET`
* `ENGINE_STOPPED`
* `ENGINE_START_FAILED`
* `CPU_STATE_UPDATED`
* `GPIO_CHANGED`

Example event structure:

```json
{
  "event": "GPIO_CHANGED",
  "session_id": "example-session-id",
  "timestamp": "2026-11-17T12:00:00+00:00",
  "data": {
    "pin": "P2.10",
    "value": true
  }
}
```

## 9. Fake Engine and Hardware Architecture

The current backend uses `FakeEngineAdapter` to simulate engine behavior without executing actual LPC1768 firmware instructions.

The `EngineInterface` defines the common methods required by simulation engines.

This interface is intended to allow a future QEMU adapter to implement the same operations without changing the REST API contract.

The `FakeHardwareAdapter` provides mock hardware connection and GPIO operations.

## 10. Mock Data and Error Simulation

Mock data is stored in:

```text
app/fixtures/mock_data.py
```

The current implementation supports simulated scenarios including:

* Valid and invalid firmware inputs
* Invalid GPIO pins
* Unknown sessions
* Backend unavailability
* Engine startup failure

Startup failure can be enabled through the session configuration:

```json
{
  "project": "LPC1768",
  "simulate_startup_failure": true
}
```

## 11. Current Limitations

* The current engine is a Fake Engine.
* Actual QEMU integration is not implemented yet.
* Real LPC1768 CPU instruction execution is not performed.
* Hardware behavior is simulated.
* Session data is stored in memory and is not persistent across backend restarts.
* The backend availability test endpoint is intended for development and testing.

## 12. Future Development

Planned improvements include:

* QEMU Engine Adapter integration
* Configurable QEMU executable and firmware paths
* Improved hardware simulation
* Automated backend tests
* Flutter frontend integration
* Production-ready configuration and security

---

**Project:** LPC1768 Simulator
**Component:** M3 – Desktop Backend / Simulation Controller
**Framework:** FastAPI
**Language:** Python
