From: https://bob.cs.sonoma.edu/IntroCompOrg-RPi/sec-gpio-mem.html

Your assembly program is written on a Linux O/S and is trying to access I/O memory mapped addresses.  We must use/work with the O/S to get around the Virtual addressing and MMU address remapping that we discussed in class.  Here is a dexcription of the BL OPEN and BL MMAP instructions that you see in the assembly code.

The peripheral address space on the Raspberry Pi 4, cannot be accessed directly from an application program. The Linux kernel includes a driver to a special character file, /dev/mem, which is a mirror of main memory. Similar to any file, we can open it, read bytes from or write bytes to it, and close it. The “position” of each byte in /dev/mem is the byte address in physical memory. In principle, we could program the GPIO device by opening /dev/mem, moving a pointer to the desired location of a GPIO port, and writing the appropriate value in that byte location.
Linux (and most other modern operating systems) use a memory management scheme that is based on virtual memory addresses. When you create a program, the loader assigns virtual addresses to all the memory locations. All memory references in the program are based on the virtual memory address space. Program code is divided into Pages of equal size. As an application executes, the pages containing the currently needed code and data are loaded into physical memory. The Linux kernel automatically translates the virtual memory addresses into the corresponding physical memory addresses, which depend on where the page was loaded.
We need to do the inverse when referencing I/O addresses. I/O devices are assigned physical memory addresses, which the Linux kernel prevents user programs from accessing. We need to map this physical memory into the program's virtual addressing scheme so that the program can access it.
The open function requires two arguments:
1.	A pointer to the name of the device/file to be opened.
2.	A mode specifying how the opened device/file can be used by the program.

The name of the special file we are opening is “/dev/gpiomem”. The flags specifying the open mode, O_FLAGS, were chosen such that our program can read values from this I/O memory and write to it. The synchronization flags ensure that any values written to this memory will be completed before the program continues execution. It returns a file descriptor number.


The mmap function takes six arguments:
1.	The address where the device should be mapped into, which needs to be in our programming virtual memory space. Specifying 0 to mmap allows the operating system to pick an address for us.
2.	The amount of memory for the mapping. One page is sufficient.
3.	A mode specifying the protection given to the mapped memory. This cannot conflict with the protection specified in the open operation. We want to read from and write to this memory.
4.	A mode specifying whether this mapped memory should or should not be shared with other processes. We will allow sharing. You may wish to have more than one program accessing the GPIO at the same time.
5.	The file descriptor to the device being mapped. This came from our call to open.
6.	The physical memory location of the I/O device.

