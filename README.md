# uvsim_vm
---------------------------------------
UVSIM - A Simple Machine Language Simulator
---------------------------------------

Prerequisites:
----------------
Before you begin, ensure you have met the following requirements:
- You have installed Python 3.10 or later.
- Install customtkinter and tkinter if not already installed.
- You have a basic understanding of tkinter and running a desktop GUI (Graphical User Interface).

Usage:
------
1. Open your command-line interface (CLI).

2. Navigate to the directory where the uvsim program is located.

3. Type the following command to start the UVSim program:
   - python view.py - it is case sensitive.
   - If you are running the code from VSCode, you can also press the 'Run' button to run the program (This looks like a play button).

4. After launching the program, a GUI will appear. This will have a button saying upload BasicML file. When you press on the button you will be directed to your folder directory and can pick a file to upload. Make sure this file is a .txt file that contains your BasicML program. Once you have found the file you want to upload, press open.
   - If you want to upload another file, press the upload file button again and repeat the process.
   - If you want to add, delete, or update the uploaded BasicML program, simply type any changes in the text box where the program contents appear. Once you are done, press the "Run File" button and the program will run the updated BasicML program.

5. To run the BasicML program, press the "Run File" button. The program will load and execute the BasicML program.

   - If the program includes READ instructions, you will be prompted to enter a number through a text input box that will appear to the screen.
   - If the program includes WRITE instructions, it will print a number to the GUI.

6. The program will continue executing the BasicML instructions until it encounters a HALT instruction or until it runs out of instructions.

7. When the program execution is completed, the following message will be printed to the GUI along side any other WRITE instructions:
   "Program Completed"

8. If you want to end the program, simply press the exit button at the top of the GUI (The X in the top right corner). If you want to continue uploading BasicML files, press the upload file button and steps 4-7 will be repeated.

---------------------------------------

Color Scheme:
------
- The default color scheme will appear on the first load. This will be the UVU color scheme.
- If you want to customize the color scheme, press the customize color scheme button. This will open a new window that will allow you to customize the color scheme.
- The new color scheme will appear right when the changes are made and will be saved for the next time you open the program.
- To go back to the default color scheme, simply press the default color scheme button.

