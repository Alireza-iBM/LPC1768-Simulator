# Shared Protocol — v1.0.0

This directory is the single source of truth for communication contracts shared by
the Flutter client, Python backend, QEMU adapter, hardware model, mocks, and tests.

## Rules for all seven members

1. Read this directory before implementing an API, event, command, or mock.
2. Do not silently rename fields, change types, or add required fields.
3. Propose contract changes through a PR that updates schemas, catalogs, examples,
   mock data, and affected tests together.
4. Keep `schema_version` at `1.0.0` for compatible clarifications/additive optional
   fields. Use a version bump for breaking changes and document migration.
5. Never invent CPU/register values when the engine cannot provide them. Use
   `available: false`, `source: "unavailable"`, and `null` register values.
6. Mock data is for UI/contract development only; it is not evidence that QEMU
   hardware behavior is correct.

## Directory map

- `schemas/`: JSON Schema Draft 2020-12 definitions.
- `commands/commands.json`: HTTP/API operations and support status.
- `events/events.json`: WebSocket event names and payload expectations.
- `examples/`: canonical minimal examples.
- `mock_data/`: deterministic fixtures for frontend/backend tests.

## Event envelope

Every WebSocket message uses `examples/gpio_event.json` as the envelope pattern:
`schema_version`, `type`, `event_id`, `session_id`, `timestamp`, `payload`.

## MVP API root

`/api/v1`. The command catalog is authoritative for the initial operation names.
The exact response wrapper and HTTP status mapping must be implemented consistently
by M3 and documented in `docs/api/README.md` before frontend integration.

## Important implementation boundary

QMP capabilities vary by QEMU build and machine. This protocol describes the
application boundary, not a promise that QMP exposes every field. M3/M1 must mark
unavailable data explicitly and agree on the actual engine adapter interface.
