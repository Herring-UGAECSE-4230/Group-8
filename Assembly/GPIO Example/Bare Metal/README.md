# Arithmetic Operations in assembly
## Objective


## Instructions
1. Copy the files GPIO.s and makefile from this repository to your personal computer.
2. Install the arm compiler arm-none-eabi using the steps from the power point Lecture 3 Running assembly slide 11.
3. Use make to compile
4.  ***VERY IMPORTANT*** Back up your current sd card to your computer if you do not copy the files from your sd card you will lose all of your work up until this point. 
5. Take the kernel.img file and place it in the boot file of your sd card and delete the previous kernel*.imgs; Make sure you have backed up everything this will overwrite your current os and saves. Since we are only overwriting the kernal image, we only need to back up the bootfs partition.
6. FOR EMPHASIS:  You only have to copy over the kernal7l.img to your SD card to run baremetal.  You can leave everything else as is.
7. Wire the output of GPIO 21 -> led -> 1k ohm resistor -> ground
8. After all this is done eject the sd card and insert it into the raspberry pi and turn it on and observe the output.

## Deliverables

THIS IS A GROUP PROJECT
You may keep the GPIO as is on the Example.

After verifying that the program works as written, add a delay loop for on an off that you can control.  
Name the two variables: On_time and Off_time. They cannot be in seconds. They must be in nanoseconds.  So, a 1 second delay would be 1,000,000,000 as an entry.
You will not have to show a square wave with a value needing more time than this.
You may use your delay loops from the Linux assembly program or modify those in the program.

NOTE:  This is baremetal assembly.  You are not running on Linux; therefore, you are not using GCC or GDB.  There is no debugger tool.  You should think about getting the main body of the program (the delay loops) working on Linux assembly where you can debug.  

NOTE: Be careful with your SD card file management!

1) Run your program showing 1 Hz: 1 second (50/50), 1 second (25 on / 75 off).
2) Run your program with 1Khz at (50/50 duty cycle).  You cannot see this on an LED.  You will need to look at Oscilloscope. What are your two delay values for this?
3) What is the fastest that you can run a square wave with your code?  Provide the delay values and the Oscilloscope output.
4) Take data for your bare metal square wave generator.  What is the frequency range?  What is the dutycycle range?  Show this in data and graphs. You programmed xxx and measured yyy.
5) How does this compare to your best results from the Python square wave project and the linux assembly square wave?  Include data, graphs, explanation...This includes thinking about why the baremetal results are better than or worse than the Linux assembly results.
6) Include all written responses on ELC and treat it like a Phython project for requirements in your writeup.
7) Make sure your final code in on Github and is named BareMetal_asm_squarewave_final.
