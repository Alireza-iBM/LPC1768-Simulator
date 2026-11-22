.syntax unified
.cpu cortex-m3
.thumb

.global Reset_Handler
.global vector_table

.extern main
.extern _estack
.extern _sidata
.extern _sdata
.extern _edata
.extern _sbss
.extern _ebss

.section .isr_vector, "a", %progbits
vector_table:
    .word _estack
    .word Reset_Handler

.section .text.Reset_Handler
.thumb_func
Reset_Handler:

    ldr r0, =_sidata
    ldr r1, =_sdata
    ldr r2, =_edata

copy_data:
    cmp r1, r2
    bcs zero_bss
    ldr r3, [r0], #4
    str r3, [r1], #4
    b copy_data

zero_bss:
    ldr r1, =_sbss
    ldr r2, =_ebss
    movs r3, #0

zero_bss_loop:
    cmp r1, r2
    bcs start_main
    str r3, [r1], #4
    b zero_bss_loop

start_main:
    bl main

stop:
    b stop
