# Mock Server (development only)

Standalone FastAPI service for Flutter, board-view, and backend integration before QEMU is connected. It follows the existing `protocol/` contracts on `develop`; all values are synthetic.

## Run on Fedora/Linux

From repository root:

```bash
python3 -m venv .venv-mock
source .venv-mock/bin/activate
python -m pip install -r tools/mock_server/requirements.txt
uvicorn server:app --app-dir tools/mock_server --host 127.0.0.1 --port 8765 --reload
```

## Endpoints

- `GET /api/v1/health` (mock diagnostic)
- `GET /api/v1/status` (mock diagnostic)
- `GET /api/v1/sessions`
- `POST /api/v1/sessions`
- `GET /api/v1/sessions/{session_id}/state`
- `POST /api/v1/sessions/{session_id}/firmware` (mock metadata only; does not parse ELF)
- `POST /api/v1/sessions/{session_id}/start`
- `POST /api/v1/sessions/{session_id}/pause`
- `POST /api/v1/sessions/{session_id}/reset`
- `PUT /api/v1/sessions/{session_id}/gpio/{port}/{pin}`
- `DELETE /api/v1/sessions/{session_id}`
- `WS /api/v1/sessions/{session_id}/events`

OpenAPI docs: http://127.0.0.1:8765/docs

## Quick checks

```bash
curl http://127.0.0.1:8765/api/v1/health
curl http://127.0.0.1:8765/api/v1/status
curl -X POST http://127.0.0.1:8765/api/v1/sessions
```

WebSocket example with websocat:

```bash
websocat ws://127.0.0.1:8765/api/v1/sessions/demo-session-001/events
```

## Important

- This is not the production backend.
- It does not execute ELF files or emulate registers/interrupts.
- Firmware upload returns synthetic metadata only.
- GPIO input endpoint validates shape but does not drive QEMU.
- Never use it to claim CPU, peripheral, or interrupt behavior is verified.
- Keep it aligned with `protocol/commands/commands.json`, `protocol/events/events.json`, schemas, and examples.
- Production Flutter code should switch base URL/configuration; UI code should not branch on "mock" mode.
