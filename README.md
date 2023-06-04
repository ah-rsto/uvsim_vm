# uvsim_vm
---------------------------------------
UVSIM - A Simple Machine Language Simulator
---------------------------------------

Prerequisites:
----------------
Before you begin, ensure you have met the following requirements:
- You have installed Python 3.6 or later.
- You have a basic understanding of command-line interfaces.
- The files that you are testing are in the same directory as uvsim.py

Usage:
------
1. Open your command-line interface (CLI).

2. Navigate to the directory where the UVSim program is located.

3. Type the following command to start the UVSim program:
    python uvsim.py - it is case sensitive.

4. After launching the program, you will be asked to enter the name of a BasicML program file:
    "Enter the name of the BasicML program file: " (example: 'program.txt' or 'Test1.txt') and press Enter - make sure that the BasicML program file is in the same directory as uvsim.py. If not, make sure you know the location of the file and enter it correctly (example: '../Test2.txt')

5. The program will load and execute the BasicML program. 
    - If the program includes READ instructions, you will be prompted to enter a number. 
    - If the program includes WRITE instructions, it will print a number to the console.

6. The program will continue executing the BasicML instructions until it encounters a HALT instruction or until it runs out of instructions.

7. When the program execution is completed, the following message will be printed:
    "Program execution completed."

8. The program will then end.

