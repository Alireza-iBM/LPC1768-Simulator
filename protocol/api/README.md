# API Contract Notes

Base path: `/api/v1`

The initial command list is in `protocol/commands/commands.json`.
All session-specific endpoints use `{session_id}`. Firmware upload is multipart
binary input; do not put host absolute paths in client-visible JSON.

WebSocket endpoint:
`/api/v1/sessions/{session_id}/events`

Every event must conform to `protocol/schemas/event.schema.json`.
Payload shapes are described in `protocol/events/events.json` and the fixtures.

## Error response convention

Use this shape for API errors:

```json
{
  "error": {
    "code": "ENGINE_UNAVAILABLE",
    "message": "The simulation engine is unavailable.",
    "recoverable": true,
    "details": {}
  }
}
```

`details` is optional and must not contain secrets or host absolute paths.
