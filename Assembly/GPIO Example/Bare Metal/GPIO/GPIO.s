.global _start

.equ GPIO_BASE, 0xFE200000
.equ GPFSEL2, 0x08

.equ GPIO_21_OUTPUT, 0x8 ;//# 1 << 3

.equ GPFSET0, 0x1c
.equ GPFCLR0, 0x28

.equ GPIOVAL, 0x200000 ;//# 1 << 21

_start:

	;//# base of our GPIO structure
	ldr r0, =GPIO_BASE

	;//# set the GPIO 21 function as output
	ldr r1, =GPIO_21_OUTPUT
	str r1, [r0, #GPFSEL2]

	# set counter
	ldr r2, =0x800000

loop:
	# turn on the LED
	ldr r1, =GPIOVAL ;//# value to write to set register
	str r1, [r0, #GPFSET0] ;//# store in set register

	# Wait for some time, delay
	mov r9, #3200      ;//# Adjust the number of repetitions
	mov r8, #3200   ;//# Adjust the initial value for each chunk delay

delay_outer:
	mov r10, r8    ;//# Preserve the initial value for each chunk delay

delay_inner:
	subs r10, r10, #1
	bne delay_inner

	subs r9, r9, #1
	bne delay_outer



	# turn off the LED
	ldr r1, =GPIOVAL ;//# value to write to set register
	str r1, [r0, #GPFCLR0] ;//# store in set register

	# Wait for some time, delay
	mov r9, #3200      ;//# Adjust the number of repetitions
	mov r8, #3200   ;//# Adjust the initial value for each chunk delay

delay_outer1:
	mov r10, r8    ;//# Preserve the initial value for each chunk delay

delay_inner1:
	subs r10, r10, #1
	bne delay_inner1

	subs r9, r9, #1
	bne delay_outer1


	b loop
