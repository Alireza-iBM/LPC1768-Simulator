# Modular Delivery Matrix

> Status: planning baseline v1.0. Update this file whenever ownership, acceptance criteria, or module boundaries change.
> Member IDs M1-M7 are role identifiers. Replace/confirm GitHub handles in the team roster; do not infer a person's identity from a role.

## Current project facts

- M1 (project lead) owns the QEMU-based engine work; current work includes LPC1768 GPIO/GPIOINT integration and ongoing QEMU machine development.
- M2 owns LPC1768 peripheral behavior and hardware validation; current progress has reached NVIC testing.
- M3 owns the Python desktop backend; an initial WebSocket connection test has passed.
- M4 owns the Flutter desktop UI; the dashboard shell is implemented.
- M5 owns the 3D board/visualization; the board model is reported as nearly complete.
- M6 owns shared protocol and integration coordination.
- M7 owns QA, reproducible tests, and release validation.

These are role assignments, not claims that every listed module is complete.

## Workstream matrix

| ID | Owner | Scope / repository paths | Inputs required | Deliverables | Acceptance gate | Can work now? |
|---|---|---|---|---|---|---|
| M1 | Alireza / project lead | QEMU source patch; `engine/qemu/`; engine integration | QEMU pinned version, machine build config, agreed hardware register/event contract | Patch series, build/apply scripts, machine launch script, reproducible test logs, known-limitations list | Clean apply to pinned QEMU; reproducible build; smoke test; no undocumented local-only edits | Yes |
| M2 | Hardware model owner | `engine/lpc1768/`; `docs/hardware/`; `tests/hardware/` | LPC1768 user manual references, memory map, M1 QEMU integration points | Peripheral register map, GPIO/PINSEL/PINMODE/NVIC behavior tests, IRQ matrix, test firmware | Register read/write and interrupt behavior verified against cited reference and test cases | Yes |
| M3 | Backend owner | `apps/desktop_backend/`; `tools/mock_server/` | Protocol schemas, command/event examples, engine adapter interface | FastAPI backend, session lifecycle, firmware upload contract, WebSocket publisher, adapter + mock adapter | API tests pass; reconnect/error handling; mock can be replaced without changing API routes | Yes, use mock |
| M4 | Flutter owner | `apps/flutter_app/` | OpenAPI/API examples, WebSocket event schema, mock server URL/config | Dashboard, session controls, firmware selection, CPU/memory/log views, connection state | UI works against mock server; loading/empty/error/disconnected states covered | Yes, use mock |
| M5 | Board visualization owner | `apps/flutter_app/lib/board_view/`; board assets; `docs/hardware/board-mapping.json` | Approved board model, physical pin map, GPIO event schema | 3D board view, pin/component mapping, LED/button interactions | A simulated GPIO event changes the correct visual pin/component; mapping is data-driven | Yes, use fixtures |
| M6 | Protocol/integration owner | `protocol/`; `docs/api/`; `docs/integration/` | Requirements from M1-M5 | Versioned JSON schemas, REST/OpenAPI agreement, event catalog, examples, compatibility notes, integration checklist | Contract examples validate; breaking changes reviewed and versioned | Yes; unblock everyone first |
| M7 | QA/release owner | `tests/`; `scripts/`; `docs/development/` | Acceptance criteria from every owner | Test matrix, smoke scripts, CI checks, regression report, release checklist | A clean checkout can run documented checks; failures are actionable and reproducible | Yes; start with contract and mock tests |

## Delivery waves (gates, not calendar promises)

### Wave 0 — Enable parallel work (immediately)
- M6 publishes protocol envelope, event catalog, command catalog, and sample payloads.
- M3 publishes a mock-compatible backend interface and runs the standalone mock server.
- M4 and M5 integrate against mock events; no dependency on QEMU completion.
- M7 adds contract validation and a smoke-test skeleton.
- M1/M2 publish current hardware facts and explicit known gaps, not unverified "done" claims.

### Wave 1 — First real vertical slice
- M1 supplies a pinned, reproducible QEMU patch/build/run procedure.
- M2 verifies the first real GPIO and interrupt paths.
- M3 connects the real EngineAdapter behind the existing backend service interface.
- M4/M5 consume the same protocol without UI/model rewrites.
- M7 runs one automated end-to-end scenario.

### Wave 2 — Expand peripheral coverage
- Add peripherals only after their register behavior, event contract, UI mapping, and tests are agreed.
- Keep unsupported peripherals explicitly marked unsupported; do not simulate success with silent no-ops.

### Wave 3 — MVP hardening
- Reset, pause/resume/stop, invalid ELF, missing firmware, disconnect/reconnect, repeated sessions, and clean-machine installation.
- Freeze MVP scope before adding optional peripherals.

## Module handoff contract

Every handoff must include:
1. Exact repository path(s) and commit SHA / PR URL.
2. Owner and receiving owner.
3. Contract/API version used.
4. Build/run commands from a clean checkout.
5. Automated test command and actual result.
6. One working example (request/event/firmware/test fixture).
7. Known limitations and unsupported behavior.
8. Follow-up issue links.

A folder upload, screenshot, or "works on my machine" is not a complete handoff.

## Definition of Ready
- Task has one directly responsible owner.
- Inputs and upstream contract versions are named.
- File paths and expected outputs are listed.
- Mock/fixture exists if the upstream implementation is unavailable.
- Acceptance tests are written before integration.

## Definition of Done
- Code is committed on a task branch and PR targets `develop`.
- Relevant unit/contract tests pass.
- No secrets, generated binaries, local absolute paths, or unrelated formatting changes.
- README/API/schema/examples are updated.
- A second member reviews the change.
- Handoff record is completed.

## Team roster to confirm

| Role | GitHub handle | Confirmed name |
|---|---|---|
| M1 | @Alireza-iBM | Alireza |
| M2 | TBD | TBD |
| M3 | TBD | TBD |
| M4 | TBD | TBD |
| M5 | TBD | TBD |
| M6 | TBD | TBD |
| M7 | TBD | TBD |
