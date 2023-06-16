import tkinter as tk
from uvsim import UVSim
from tkinter import filedialog, scrolledtext, simpledialog
import customtkinter


class UVSimGUI:
    def __init__(self, root):
        self.uvsim = UVSim(self.read_from_user, self.write_to_console, self.halted)
        self.root = root

        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("blue")

        root.title("UVSim GUI")
        root.geometry("600x600")
        

        self.title = customtkinter.CTkLabel(root, text="UVSim GUI", font=("Arial", 30))
        self.title.pack(pady=10)

        # self.program_text = scrolledtext.ScrolledText(root, width=50, height=10)
        self.program_text = customtkinter.CTkTextbox(root, width=350, height=150)
        self.program_text.pack(pady=10)
        self.program_text.insert(tk.INSERT, "BasicML program will be displayed here.")

        # self.console_output = scrolledtext.ScrolledText(root, width=50, height=10)
        self.console_output = customtkinter.CTkTextbox(root, width=350, height=150)
        self.console_output.pack(pady=10)
        self.console_output.insert(tk.INSERT, "Console output will be displayed here.\n")

        upload_btn = customtkinter.CTkButton(root, text="Upload BasicML file", command=self.open_program)
        upload_btn.pack()

    def read_from_user(self):
        dialog = customtkinter.CTkInputDialog(text="Enter a number from -9999 to 9999", title="READ Input")
        user_input = dialog.get_input()
        # user_input = simpledialog.askstring("Input", "Enter a number from -9999 to 9999", parent=self.root)
        try:
            value = int(user_input)
            if value < -9999 or value > 9999:
                raise ValueError
            return value
        except ValueError:
            user_input.set("Invalid input. Try again.")

    def write_to_console(self, value):
        self.console_output.insert(tk.END, str(value) + "\n")
        self.console_output.see(tk.END)
    
    def open_program(self):
        self.program_text.delete("1.0", tk.END)
        self.root.filename = filedialog.askopenfilename(initialdir="/", title="Select file", filetypes=(("txt files", "*.txt"), ("all files", "*.*")))
        if self.root.filename == "":
            return 'No file uploaded. Try again.'
        with open(self.root.filename, 'r') as f:
            program = f.read()
        self.program_text.insert(tk.INSERT, program)
        self.uvsim.load_program(self.root.filename)
        self.execute_program()

    def execute_program(self):
        self.uvsim.execute_program()

    def halted(self):
        self.write_to_console("Program completed.\nTo run another file, click 'Upload BasicML file'")



root = customtkinter.CTk()
app = UVSimGUI(root)
root.mainloop()