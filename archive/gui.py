import tkinter as tk
from uvsim import UVSim
from tkinter import filedialog
import customtkinter

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

class UVSimGUI(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.uvsim = UVSim(self.read_from_user, self.write_to_console, self.halted, self.displayValues)

        self.title("UVSim GUI")
        self.geometry("780x620")

        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.sidebar_frame = customtkinter.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.header = customtkinter.CTkLabel(self.sidebar_frame, text="UVSim GUI", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.header.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.accumulator_label = customtkinter.CTkTextbox(self.sidebar_frame, width=200, height=100, font=customtkinter.CTkFont(size=12, weight="normal"))
        self.accumulator_label.grid(row=1, column=0, padx=20, pady=10)
        self.accumulator_label.insert(tk.INSERT, "Accumulator:\n")

        self.counter = customtkinter.CTkTextbox(self.sidebar_frame, width=200, height=100, font=customtkinter.CTkFont(size=12, weight="normal"))
        self.counter.grid(row=2, column=0, padx=20, pady=10)
        self.counter.insert(tk.INSERT, "Counter:\n")

        self.console_output = customtkinter.CTkTextbox(self.sidebar_frame, width=200, height=100, font=customtkinter.CTkFont(size=12, weight="normal"))
        self.console_output.grid(row=3, column=0, padx=20, pady=10)
        self.console_output.insert(tk.INSERT, "Console output:\n")


        self.upload_btn = customtkinter.CTkButton(self.sidebar_frame, text="Upload BasicML file", command=self.open_program)
        self.upload_btn.grid(row=5, column=0, padx=20, pady=10)

        self.program_text = customtkinter.CTkTextbox(self, width=300)
        self.program_text.grid(row=0, column=1, rowspan=2, padx=20, pady=(20, 0), sticky="nsew")
        self.program_text.insert(tk.INSERT, "BasicML program will be displayed here.")


        self.execute_btn = customtkinter.CTkButton(self, text="Run File", command=self.execute_program)
        self.execute_btn.grid(row=3, column=1, padx=20, pady=10, sticky="nsew")


    def reset_textbox(self, textbox, text):
        textbox.delete("1.0", tk.END)
        textbox.insert(tk.INSERT, text)

    def read_from_user(self):
        dialog = customtkinter.CTkInputDialog(text="Enter a number from -9999 to 9999", title="READ Input")
        user_input = dialog.get_input()
        try:
            value = int(user_input)
            if value < -9999 or value > 9999:
                raise ValueError
            return value
        except ValueError:
            self.write_to_console("Invalid input. Try again.")
            return self.read_from_user()

    def write_to_console(self, value):
        self.console_output.insert(tk.END, str(value) + "\n")
        self.console_output.see(tk.END)
    
    def open_program(self):
        self.program_text.delete("1.0", tk.END)
        self.filename = filedialog.askopenfilename(initialdir="/", title="Select file", filetypes=(("txt files", "*.txt"), ("all files", "*.*")))
        if self.filename == "":
            self.program_text.insert(tk.INSERT, "No file selected. Try again.")
        self.uvsim.load_program(self.filename)
        # with open(self.filename, 'r') as f:
        #     program = f.read()
        memory = self.uvsim.memory.memory
        program_text = "Memory Registers:\n"
        for i, val in enumerate(memory):
            program_text += f"{i}: {val}\n"
        self.program_text.insert(tk.INSERT, program_text)
        self.reset_textbox(self.accumulator_label, "Accumulator:\n")
        self.reset_textbox(self.counter, "Counter:\n")
        self.reset_textbox(self.console_output, "Console output:\n")
        # self.execute_program()

    def execute_program(self):
        self.uvsim.execute_program()
    
    def displayValues(self, accumulator, counter):
        self.accumulator_label.insert(tk.END, str(accumulator))
        self.counter.insert(tk.END, str(counter))

    def halted(self):
        self.write_to_console("Program completed.\n\nTo run another file, click 'Upload BasicML file'")


app = UVSimGUI()
app.mainloop()