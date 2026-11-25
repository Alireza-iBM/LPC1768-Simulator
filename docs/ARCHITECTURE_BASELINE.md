# Architecture Baseline

## Selected architecture
~~~text
Flutter Desktop IDE
  | REST + WebSocket
Python / FastAPI Backend
  | Engine Adapter + process/IPC control
QEMU LPC1768 Machine
  | MMIO, interrupts, virtual time, pins/buses
LPC1768 peripheral models
  | modeled pin/bus connections
Virtual external components and modules
~~~

## Technology baseline

| Area | Selection |
|---|---|
| MCU | NXP LPC1768 |
| CPU | ARM Cortex-M3 |
| Emulator | QEMU custom LPC1768 machine/model |
| Desktop UI | Flutter |
| Backend | Python + FastAPI |
| UI/backend transport | REST + WebSocket |
| Firmware toolchain | ARM GNU Toolchain |
| Build system | CMake + Ninja, subject to current project config |
| Debug | GDB remote protocol / QEMU debugging facilities |
| Contract | Existing versioned protocol under protocol/ |
| Time | Coordinated virtual clock/event scheduler |
| External connectivity | Separate virtual device/network layer |

Renode is not part of the selected architecture.

## Responsibilities
- Flutter owns editor/project UI, circuit designer, board view, debugger panels, instruments and monitors. It consumes backend state/events; it must not invent hardware state.
- FastAPI owns API transport, project/session lifecycle, build/firmware orchestration, engine configuration, process lifecycle, event routing and WebSocket delivery.
- Engine abstraction defines backend-facing operations and state/events. FakeEngineAdapter remains for UI/API tests; QEMU adapter is the real implementation to integrate.
- QEMU owns machine setup, memory map, MMIO devices, interrupts, timers and machine wiring. Keep source changes reproducible against a pinned QEMU source version.
- LPC1768 model/spec owns authoritative register definitions, reset values, pin mux, peripheral behavior, interrupt routing, clocking and hardware tests. Use NXP UM10360, datasheet and errata.
- External device models own sensors, displays, motors, ESP modules, Bluetooth modules, Ethernet PHYs and other devices. They interact through modeled pins/buses and shared virtual time.
- protocol/ owns REST/WebSocket schemas, event names, units, identifiers, error codes and canonical examples.

## Cross-cutting abstractions
Define and test pin identity/direction/logic/alternate function; bus transaction semantics; interrupt source/priority/pending state; virtual clock and event scheduling; device lifecycle; event ordering/timestamps; circuit net graph; engine capability reporting; deterministic fixtures.

## No silent success
Unsupported registers, transactions, modes and device functions must be reported as unsupported or exhibit documented hardware behavior. Do not silently report success or return zero unless that is the specified hardware behavior.

## Integration sequence
1. Preserve/test current FastAPI + FakeEngine path.
2. Integrate QEMU process lifecycle and create real QEMU EngineAdapter.
3. Prove ELF load, CPU execution/control, stop/reset and debug state.
4. Prove GPIO and pin multiplexing end-to-end.
5. Prove UART TX/RX, baud, FIFO and interrupt path.
6. Add peripherals one by one with register/timing/interrupt/firmware tests.
7. Add circuit component models through stable pin/bus interfaces.
8. Add external Wi-Fi/Bluetooth/network models without bypassing MCU-side interfaces.
