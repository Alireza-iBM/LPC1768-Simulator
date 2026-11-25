# Project Status and Current Reality

Last repository review: 2026-11-25. Refresh after significant merges.

## Product direction
- LPC1768-only initial target.
- Flutter desktop IDE + Python/FastAPI backend.
- QEMU is selected; Renode migration has been rejected.
- Software-only virtual hardware simulation; physical board flashing/debugging is out of current scope.
- Wi-Fi/Bluetooth are external modules, not native LPC1768 features.

## Verified repository facts
- Repository: Alireza-iBM/LPC1768-Simulator; default branch: main.
- main contains the initial desktop-backend merge, PR #4, merge commit 198feac7101fa3cd52bb802c8c7ab3597bf8d23e.
- The merged backend includes FastAPI routes, session/event services, WebSocket handling, EngineInterface, FakeEngineAdapter and FakeHardwareAdapter.
- QEMU process-manager code and tests exist on feature/m3-qemu-process-manager; that branch was not safely integrated into main at this review.
- Generic Cortex-M3 QEMU execution proof-of-concept exists. It is not proof of a complete LPC1768 QEMU machine.
- Shared protocol and modular-delivery work exist in repository history/branches. Inspect the checked-out branch before assuming a file is present.

## Backend distinction
The merged backend is an API/orchestration foundation using FakeEngineAdapter. It does not itself execute LPC1768 firmware. QemuProcessManager is process-lifecycle infrastructure, not a completed QEMU EngineAdapter. Real QEMU execution, firmware loading, QMP/GDB integration and state/event mapping require separate verification.

## Team-reported hardware progress (not independently verified)
M2 reported approximate progress:
- QEMU machine environment/build: 90%
- Memory map, Flash and SRAM: 80%
- GPIO and registers: 80%
- Hardware model connection to Cortex-M3: 85%
- Interrupts and NVIC connection: 70%
- GPIO output to Backend: 35%
- Hardware event delivery to Backend: 15%
- Comprehensive tests/docs/final handoff: 40%

These are estimates, not test results. UART was reported as near completion. Inspect actual source, commits and firmware tests before relying on these claims.

## Do not overclaim
- A production, fully validated LPC1768 QEMU machine is not established by the generic Cortex-M3 PoC.
- Complete LPC1768 peripheral coverage is not established.
- A real QEMU EngineAdapter is not established by the presence of EngineInterface and QemuProcessManager.
- Full Flutter-to-real-QEMU end-to-end integration is not established.
- Circuit simulation, Wi-Fi, Bluetooth Classic, BLE, Ethernet networking, USB and protocol decoders are roadmap goals unless tests prove otherwise.
- Test status must be checked on the actual target branch.

## Immediate continuation priorities
1. Reconcile and integrate M3 process lifecycle without duplicating backend work.
2. Align shared protocol and delivery docs on the stable baseline.
3. Pin QEMU source/version and reproducible build procedure.
4. Verify M2 GPIO/PINSEL/UART/NVIC implementation with firmware tests.
5. Connect the backend EngineAdapter to real QEMU.
6. Prove GPIO + UART end-to-end before expanding peripheral coverage.
