# Mock Server (development only)

This standalone FastAPI service lets Flutter, board visualization, and backend integration work before QEMU is connected. All values and events are synthetic.

## Run on Fedora/Linux

From the repository root:

```bash
python3 -m venv .venv-mock
source .venv-mock/bin/activate
python -m pip install -r tools/mock_server/requirements.txt
uvicorn server:app --app-dir tools/mock_server --host 127.0.0.1 --port 8765 --reload
```

## Endpoints

- `GET /api/v1/health`
- `GET /api/v1/status`
- `GET /api/v1/sessions`
- `POST /api/v1/sessions`
- `GET /api/v1/sessions/{session_id}`
- `POST /api/v1/sessions/{session_id}/{start|pause|resume|stop|reset}`
- `WS /ws/v1/sessions/{session_id}`

OpenAPI docs: http://127.0.0.1:8765/docs

## Quick checks

```bash
curl http://127.0.0.1:8765/api/v1/health
curl http://127.0.0.1:8765/api/v1/status
curl -X POST http://127.0.0.1:8765/api/v1/sessions
```

WebSocket example with websocat:

```bash
websocat ws://127.0.0.1:8765/ws/v1/sessions/mock-session-001
```

## Important

- This is not the production backend.
- It does not execute ELF files or emulate registers/interrupts.
- Do not connect it to release builds.
- Keep its payloads aligned with `protocol/schemas/` and examples.
- When the real backend is ready, Flutter should switch the base URL/configuration; UI code should not need mock-specific logic.
