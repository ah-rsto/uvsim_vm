"""View

This module manages the view components.
"""

import tkinter as tk
from controller import UVSimController
from tkinter import filedialog
import customtkinter

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")


class UVSimGUI(customtkinter.CTk):
    def __init__(self):
        """UVSimGUI initializer.

        :param: None
        :return: None
        """
        super().__init__()
        self.uvsim = UVSimController(self.halted, self.display_values)

        self.title("UVSim")
        self.geometry("780x620")

        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.sidebar_frame = customtkinter.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.header = customtkinter.CTkLabel(
            self.sidebar_frame,
            text="UVSim GUI",
            font=customtkinter.CTkFont(size=20, weight="bold"),
        )
        self.header.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.accumulator_label = customtkinter.CTkTextbox(
            self.sidebar_frame,
            width=200,
            height=150,
            font=customtkinter.CTkFont(size=12, weight="normal"),
        )
        self.accumulator_label.grid(row=1, column=0, padx=20, pady=10)
        self.accumulator_label.insert(tk.INSERT, "Accumulator:\n")

        self.cursor = customtkinter.CTkTextbox(
            self.sidebar_frame,
            width=200,
            height=150,
            font=customtkinter.CTkFont(size=12, weight="normal"),
        )
        self.cursor.grid(row=2, column=0, padx=20, pady=10)
        self.cursor.insert(tk.INSERT, "Cursor:\n")

        self.console_output = customtkinter.CTkTextbox(
            self.sidebar_frame,
            width=200,
            height=150,
            font=customtkinter.CTkFont(size=12, weight="normal"),
        )
        self.console_output.grid(row=3, column=0, padx=20, pady=10)
        self.console_output.insert(tk.INSERT, "Console Output:\n")

        self.upload_btn = customtkinter.CTkButton(
            self.sidebar_frame, text="Upload BasicML file", command=self.open_program
        )
        self.upload_btn.grid(row=5, column=0, padx=20, pady=10)

        self.program_text = customtkinter.CTkTextbox(self, width=300, height=536)
        self.program_text.grid(
            row=0, column=1, rowspan=2, padx=20, pady=(20, 0), sticky="nsew"
        )
        self.program_text.insert(tk.INSERT, "BasicML program will be displayed here.")

        self.execute_btn = customtkinter.CTkButton(
            self, text="Run File", command=self.execute_program
        )
        self.execute_btn.grid(row=3, column=1, padx=20, pady=10, sticky="nsew")

    def reset_textbox(self, textbox: customtkinter.CTkTextbox, text: str) -> None:
        """Resets specified textbox content with new text.

        :param textbox: Textbox to be reset with new content
        :param text: Text to replace original textbox content
        :return: None
        """
        textbox.delete("1.0", tk.END)
        textbox.insert(tk.INSERT, text)

    def reset_textboxes(self) -> None:
        """Resets default textboxes for subsequent runs.

        :param: None
        :return: None
        """
        self.reset_textbox(self.accumulator_label, "Accumulator:\n")
        self.reset_textbox(self.cursor, "Cursor:\n")
        self.reset_textbox(self.console_output, "Console Output:\n")

    def read_from_user(self) -> int:
        """Reads input from user.

        :param: None
        :return value: Input value provided by user
        """
        dialog = customtkinter.CTkInputDialog(
            text="Enter a number from -9999 to 9999", title="READ Input"
        )
        user_input = dialog.get_input()

        try:
            value = int(user_input)
            if value < -9999 or value > 9999:
                raise ValueError
            return value
        except ValueError:
            self.write_to_console("Invalid input. Try again.")
            return self.read_from_user()

    def write_to_console(self, value: str) -> None:
        """Writes value to output for user.

        :param: None
        :return value: Output value requested from memory
        """
        self.console_output.insert(tk.END, str(value) + "\n")
        self.console_output.see(tk.END)

    def update_program(self) -> None:
        """Updates program dialog text content.

        :param: None
        :return: None
        """
        self.program_text.delete("1.0", tk.END)
        program_text = "Memory Registers:\n"
        program_text += self.uvsim.get_program_text()

        self.program_text.insert(tk.INSERT, program_text)

    def open_program(self, filename: str = "") -> None:
        """Requests program instruction set and displays for user.

        :param filename: String containing file path
        :return: None
        """
        self.filename = filename
        while self.filename == "":
            self.program_text.delete("1.0", tk.END)
            self.filename = filedialog.askopenfilename(
                initialdir="/",
                title="Select file",
                filetypes=(("txt files", "*.txt"), ("all files", "*.*")),
            )
            if self.filename == "":
                self.program_text.insert(tk.INSERT, "No file selected. Try again.")
        self.uvsim.load_program(self.filename)
        self.update_program()
        self.reset_textboxes()
        # self.execute_program()

    def execute_program(self) -> None:
        """Requests program execution.

        :param: None
        :return: None
        """
        self.uvsim.reset_accumulator()
        self.uvsim.reset_cursor()
        self.uvsim.reset_instruction()
        self.open_program(filename=self.filename)
        self.reset_textboxes()
        self.uvsim.execute_program(self.read_from_user, self.write_to_console)

    def display_values(self, accumulator: str, cursor: str) -> None:
        """Requests accumulator and cursor value to display for user.

        :param accumulator: Value in accumulator register
        :param cursor: Current position in instruction set runtime
        :return: None
        """
        accumulator, cursor = self.uvsim.get_acc_cur()

        self.accumulator_label.insert(tk.END, str(accumulator))
        self.cursor.insert(tk.END, str(cursor))

    def halted(self) -> None:
        """Displays execution completion message for user.

        :param: None
        :return: None
        """
        self.write_to_console(
            "Program completed.\n\nTo run another file, click 'Upload BasicML file'"
        )


app = UVSimGUI()
app.mainloop()
