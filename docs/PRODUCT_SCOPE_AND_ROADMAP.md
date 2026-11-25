# Product Scope and Roadmap

## Product definition
An LPC1768-focused embedded development environment combining C/C++ editing, ARM build/link, QEMU simulation, CPU/peripheral debugging, circuit design, virtual components and protocol/network analysis.

The initial MCU target is LPC1768. Other MCUs are not assumed in the first release.

## MCU hardware coverage target
Account for actual LPC1768 blocks:
- Cortex-M3, NVIC, SysTick, reset, clock and power control.
- Flash, main SRAM, AHB SRAM banks, memory map and boot-related behavior.
- GPIO, PINSEL, PINMODE and open-drain configuration.
- UART0-UART3.
- SPI and SSP controllers (model separately and accurately).
- I2C0-I2C2.
- CAN controllers.
- USB.
- Ethernet MAC and external PHY interface.
- ADC, DAC, PWM, motor-control PWM.
- Timers, capture/compare, DMA, RTC, watchdog, I2S, QEI and RIT.

This is target coverage, not a claim of current implementation. Use NXP LPC17xx User Manual UM10360, datasheet and errata to verify registers, pin mux, clocks, reset values and interrupt assignments.

## Communication target

### MCU-side interfaces
UART, SPI/SSP, I2C, CAN, USB, Ethernet MAC/PHY-side interface and GPIO timing-based signaling. For each, define pin behavior, registers, framing, timing, error states, interrupts and DMA interactions.

### Wi-Fi modules
Initial candidate: ESP8266 ESP-01 over UART with AT-command behavior. Later candidates may include ESP32 and generic module interfaces. Target behavior may include station/AP mode, association, reconnect, DHCP/IP, DNS, TCP/UDP, HTTP and MQTT. Define offline virtual networking and optional controlled host-network bridging. Do not imply arbitrary ESP firmware is emulated unless it is.

### Bluetooth
Keep Bluetooth Classic and BLE distinct:
- Classic candidates: HC-05/HC-06 with UART/AT behavior and virtual peer/serial bridge.
- BLE candidates: HM-10-like devices and later richer BLE models, with advertising, scanning, connection, GATT services/characteristics, read/write/notify and documented timing/MTU fidelity.

A UART AT-command model is not a full Bluetooth radio/controller/host-stack emulator. State fidelity explicitly.

### Other devices
Sensors, displays, storage, motors, encoders, transceivers, Ethernet PHY and analog components connect through modeled pins/buses and shared virtual time.

## Circuit designer target
Drag/drop library; MCU/package/pin representation; wires/nets/buses/power/ground; component configuration; electrical/logic validation; pin-conflict detection; save/load/export; runtime visualization. A component icon is not a simulation model: each device needs pins, behavior, state, timing/events, parameters, docs and tests.

## IDE and instruments target
C/C++ editor; project explorer; ARM GCC build profiles; linker/startup support; ELF/HEX/BIN import/export; GDB breakpoints/stepping/registers/stack/memory; peripheral register and interrupt views; UART monitor; protocol monitors; logic analyzer/trigger/decoders; oscilloscope for modeled analog signals; clock/baud/timer/PWM/ADC/DAC tools; event timeline and logs.

## Delivery waves
A. Preserve/stabilize existing work: audit branches/PRs, integrate backend process lifecycle, align protocol/docs, pin QEMU and record real status.
B. Real simulation vertical slice: QEMU LPC1768 ELF execution, backend EngineAdapter, CPU/debug state, GPIO/pin mux, LED/button, UART and Serial Monitor.
C. Core IDE/circuit workflow: editor/build/debug, circuit designer, basic devices, save/load.
D. Core peripherals: SPI/SSP, I2C, CAN, timers, PWM, ADC/DAC, DMA, interrupts and tests/instruments.
E. Connectivity: Ethernet MAC + virtual PHY/network, ESP8266/Wi-Fi, Bluetooth Classic, BLE/GATT and explicit offline/host-bridge modes.
F. Product hardening: Windows/Linux packaging, offline install, performance, deterministic replay, reliability, docs and regression suite.

## Feature maturity labels
Planned, In progress, Implemented, Verified, Integrated, Unsupported. Do not use one percentage as the only evidence of completion.
