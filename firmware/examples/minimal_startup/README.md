# Cortex-M3 Minimal Firmware Test

This example validates basic Cortex-M3 firmware execution on the generic QEMU MPS2-AN385 machine.

## Files

- `main.c`: continuously increments a global counter.
- `startup.s`: defines the vector table and Reset_Handler, initializes data and clears BSS.
- `../../linker_scripts/cortex-m3-qemu-test.ld`: linker script for the test memory map.

## Build

Run from this directory:

    arm-none-eabi-gcc -mcpu=cortex-m3 -mthumb -O0 -g -ffreestanding -nostdlib -nostartfiles -T ../../linker_scripts/cortex-m3-qemu-test.ld startup.s main.c -o firmware.elf

## Verify

    arm-none-eabi-readelf -h firmware.elf

The generated file is a test build artifact and should not be committed.
