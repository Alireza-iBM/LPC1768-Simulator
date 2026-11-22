# QEMU Cortex-M3 Proof of Concept

## Verified environment

Tested on Windows 11 using MSYS2 UCRT64.

- QEMU: 11.1.3
- Target: arm-softmmu
- Machine: mps2-an385
- CPU: cortex-m3
- ARM GNU Toolchain: 16.2.0
- GDB: gdb-multiarch 18.1

## Build QEMU

QEMU was built from source with ARM System Emulation enabled.

The resulting executable used for testing:

    ~/qemu-build-arm/qemu-system-arm.exe

## Build firmware

See `firmware/examples/minimal_startup/README.md`.

## Run QEMU

Run from the firmware example directory after building firmware.elf:

    ~/qemu-build-arm/qemu-system-arm.exe -M mps2-an385 -cpu cortex-m3 -kernel firmware.elf -nographic -monitor none -S -gdb tcp::1234

The -S option pauses the CPU at startup. The GDB server listens on TCP port 1234.

## Connect GDB

In another terminal, from the same firmware directory:

    gdb-multiarch firmware.elf

Then enter these GDB commands:

    target remote localhost:1234
    tbreak main
    continue

After reaching main, execution can be resumed with:

    continue

Press Ctrl+C to interrupt execution, then inspect:

    p counter
    info registers

Use `continue` to resume execution.

## Verified results

- QEMU built successfully.
- Cortex-M3 firmware loaded and executed.
- Reset_Handler reached main.
- The global counter increased during execution.
- GDB interrupted execution, inspected CPU registers and resumed it.
- QEMU system reset restored the initial CPU register state, verified through the QEMU monitor.
- Firmware executed again after reset.

## Limitations

- mps2-an385 is a generic QEMU machine, not an LPC1768 machine.
- The test uses 4 MiB Flash at 0x00000000 and 4 MiB RAM at 0x20000000.
- LPC1768-specific hardware and memory mapping are not implemented by this test.
- CPU register inspection was verified through GDB remote protocol, not QMP.
- This is a proof of concept, not the completed project engine interface.
