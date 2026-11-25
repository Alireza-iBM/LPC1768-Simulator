# AI Agent Continuation Guide

Mandatory for every AI coding agent, IDE assistant, autonomous agent and human contributor.

## Mission
Continue the existing LPC1768 IDE and software-simulator project from its current repository state. Do not recreate it from scratch.

## Non-negotiable decisions
- Initial MCU target: LPC1768.
- Simulation engine: QEMU with the project's custom LPC1768 machine/model.
- Do not migrate to Renode or introduce a second emulator unless the project owner explicitly reverses this decision.
- Desktop frontend: Flutter. Backend: Python + FastAPI.
- Current product direction is software simulation; physical-board flashing/debugging is not a current requirement.
- Wi-Fi and Bluetooth are external modules/devices connected through modeled MCU interfaces, not native LPC1768 peripherals.
- Preserve the existing shared protocol as the single cross-module contract.
- Preserve existing implementation, tests, commits, branches and team work.

## Mandatory start-of-task procedure
1. Confirm repository root; run git status --short --branch.
2. Run git remote -v, git branch -avv and git log --oneline --decorate --graph -20 --all.
3. Run git fetch origin --prune. Never discard local changes.
4. Identify current branch and compare it with origin/main and origin/develop.
5. Read README.md, this guide, docs/PROJECT_STATUS.md, docs/ARCHITECTURE_BASELINE.md, the relevant module README and relevant protocol schemas/examples.
6. Inspect actual source and tests. A progress percentage or document is not proof that code works.
7. Identify existing code that already implements the task. Extend it; do not create duplicates.
8. Prepare a short plan listing files to reuse/change, tests and risks.
9. If branch state, contract or implementation is ambiguous, inspect history/PRs and ask the owner before destructive changes.

## Prohibited without explicit approval
- git reset --hard, git clean -fd, force-push, deleting branches or rewriting shared history.
- Replacing whole directories or regenerating scaffolding over existing files.
- Renaming/moving directories just to match an architecture diagram.
- Overwriting another member's unmerged branch.
- Merging an unreviewed/conflicting PR.
- Silently changing API routes, event names, fields, units or schema versions.
- Adding a competing event envelope or duplicate canonical fixtures.
- Claiming completion because code compiles or a UI mock looks correct.
- Switching away from QEMU.
- Inventing MCU capabilities; verify LPC1768 behavior against NXP documentation.

## Contract-first integration
Before backend/frontend/device/hardware interface changes, read:
- protocol/README.md
- protocol/commands/commands.json
- protocol/events/events.json
- relevant schemas and canonical examples under protocol/schemas/ and protocol/examples/
- docs/integration/DELIVERY_PLAYBOOK.md

The existing shared protocol is authoritative. Keep its envelope and event names. Missing capabilities require a versioned contract proposal, schema/examples updates, validation and review by affected owners. Mock data is for parallel development, not proof of hardware behavior.

## Architectural boundaries
- apps/flutter_app/: UI, editor, circuit designer, instruments and presentation. No MCU register semantics.
- apps/desktop_backend/: REST/WebSocket, project/session lifecycle, orchestration, process management and engine adapters.
- engine/qemu/: pinned QEMU version/source, patch series, apply/build/run scripts and QEMU-specific code.
- engine/lpc1768/: project-owned register/peripheral specifications, memory map, pin maps and hardware tests.
- engine/common/: engine-independent event, time, debug and register abstractions where appropriate.
- protocol/: versioned cross-module schemas, commands, events and canonical examples.
- external device models: sensors, displays, motors, ESP modules, Bluetooth modules and PHYs. Inspect existing layout before adding paths.
- tests/: unit, contract, integration and end-to-end proof.

These are ownership boundaries, not an instruction to create every directory immediately. Preserve the existing layout.

## Backend continuation
The FastAPI backend, EngineInterface and FakeEngineAdapter already exist. The fake adapter supports UI/API development but does not execute LPC1768 instructions.

QemuProcessManager exists on feature/m3-qemu-process-manager and was not safely integrated into main at the last review. Inspect docs/BRANCH_STATUS.md and the live PR before touching it.

Keep REST routes and WebSocket contracts independent of QEMU internals. A QEMU adapter must implement the engine abstraction. Process lifecycle must cover multiple sessions, duplicate starts, stdout/stderr, termination, timeout/kill and app shutdown. Do not execute shell strings; use argument arrays and validate paths.

## QEMU rules
- QEMU is the selected engine.
- Pin exact QEMU version and source commit.
- Do not commit a full QEMU checkout/build directory unless approved.
- Keep project-owned patches ordered, reproducible and checksummed.
- Generic Cortex-M3 execution is not proof of LPC1768 compatibility.
- Verify each peripheral's registers, side effects, interrupts, timing and firmware-level behavior to the stated scope.

## Definition of done
- Existing behavior preserved or migration documented.
- Interfaces/contracts/docs updated.
- Tests actually run and results recorded.
- Unsupported behavior and limitations explicit.
- No unrelated files, generated binaries, local absolute paths or secrets.
- Focused PR targets the correct branch and includes owner, scope, paths, tests, handoff and downstream impact.

## Required agent handoff
Report branch/commit, existing files reused, changed files, exact commands, actual test results, contract changes, known gaps and PR URL/base.
