default:
	arm-none-eabi-as GPIO.s -o GPIO.o
	arm-none-eabi-ld GPIO.o -o kernel.elf
	arm-none-eabi-objcopy kernel.elf -O binary kernel7l.img
