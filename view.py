"""View

This module manages the view components.
"""

import json
import tkinter as tk
from controller import UVSimController
from tkinter import filedialog, colorchooser
import customtkinter
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("./themes/uvu.json")


class UVSimGUI(customtkinter.CTk):
    def __init__(self):
        """UVSimGUI initializer.

        :param: None
        :return: None
        """
        super().__init__()
        self.uvsim = UVSimController(self.halted)

        self.title("UVSim")
        self.geometry("780x620")

        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.sidebar_frame = customtkinter.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(5, weight=1)
        self.header = customtkinter.CTkLabel(
            self.sidebar_frame,
            text="UVSim GUI",
            font=customtkinter.CTkFont(size=20, weight="bold"),
        )
        self.header.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.accumulator_label = customtkinter.CTkTextbox(
            self.sidebar_frame,
            width=200,
            height=75,
            font=customtkinter.CTkFont(size=12, weight="normal"),
        )
        self.accumulator_label.grid(row=3, column=0, padx=20, pady=10)
        self.accumulator_label.insert(tk.INSERT, "Accumulator:\nCursor:")

        self.console_output = customtkinter.CTkTextbox(
            self.sidebar_frame,
            width=200,
            height=150,
            font=customtkinter.CTkFont(size=12, weight="normal"),
        )
        self.console_output.grid(row=4, column=0, padx=20, pady=10)
        self.console_output.insert(tk.INSERT, "Console Output:\n")

        self.color_btn = customtkinter.CTkButton(
            self.sidebar_frame,
            text="Change Color Scheme",
            command=self.change_color_scheme,
        )
        self.color_btn.grid(row=1, column=0, padx=20, pady=10)

        self.default_btn = customtkinter.CTkButton(
            self.sidebar_frame,
            text="Default Color Scheme",
            command=self.default_color_scheme,
        )
        self.default_btn.grid(row=2, column=0, padx=20, pady=10)

        self.upload_btn = customtkinter.CTkButton(
            self.sidebar_frame, text="Upload BasicML file", command=self.open_program
        )
        self.upload_btn.grid(row=6, column=0, padx=20, pady=10)

        self.program_text = customtkinter.CTkTextbox(self, width=300, height=536)
        self.program_text.grid(
            row=0, column=1, rowspan=2, padx=20, pady=(20, 0), sticky="nsew"
        )
        self.program_text.insert(tk.INSERT, "BasicML program will be displayed here.")
        self.program_text.bind("<KeyRelease>", self.limit_size, add="+")
        self.program_text.bind("<<Paste>>", self.limit_size, add="+")

        self.execute_btn = customtkinter.CTkButton(
            self, text="Run File", command=self.execute_program
        )
        self.execute_btn.grid(row=3, column=1, padx=20, pady=10, sticky="nsew")

    def limit_size(self, *args) -> None:
        """Limits size of textbox.

        :param: None
        :return: None
        """
        value = self.program_text.get("1.0", "end").split("\n")[:-1]
        if len(value) > 101:
            self.program_text.delete("1.0", "end")
            self.program_text.insert("end", "\n".join(value[:101]))

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
        self.reset_textbox(self.accumulator_label, "Accumulator:\nCursor:")
        # self.reset_textbox(self.cursor, "Cursor:\n")
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
        # self.uvsim.load_program(self.filename, True)
        with open(self.filename, "r") as f:
            lines = f.readlines()
            program_text = "BasicML Program:\n"
            instruction_set = self.uvsim.data_model.get_instructions()
            for i, val in enumerate(instruction_set):
                idx = str(i).rjust(2, "0")
                if i < len(lines):
                    program_text += str(idx) + ": " + lines[i]
                else:
                    program_text += str(idx) + ": " + "+" + str(val) + "\n"

            self.program_text.insert(tk.INSERT, program_text)
        # self.update_program()
        self.reset_textboxes()
        # self.execute_program()

    def get_input(self):
        user_input = self.program_text.get("1.0", tk.END)
        lines = user_input.split("\n")
        numbers = []
        for line in lines:
            number = line.strip()
            if ":" in line:
                parts = line.split(":")
                if len(parts) > 1:
                    number = parts[1].strip()
            if number and number.strip("+-") != "0":
                numbers.append(int(number[1:]))
        return numbers

    def execute_program(self) -> None:
        """Requests program execution.

        :param: None
        :return: None
        """
        self.uvsim.reset_accumulator()
        self.uvsim.reset_cursor()
        self.uvsim.reset_instruction()
        self.reset_textboxes()
        update_instructions = self.get_input()
        self.uvsim.load_program(update_instructions, False)
        self.uvsim.execute_program(self.read_from_user, self.write_to_console)
        self.update_program()

    def update_status(self):
        accumulator = self.uvsim.get_acc_cur()
        self.accumulator_label.delete("1.0", tk.END)
        self.accumulator_label.insert(tk.END, accumulator)

    def halted(self) -> None:
        """Displays execution completion message for user.

        :param: None
        :return: None
        """
        self.update_status()
        self.write_to_console(
            "Program completed.\n\nTo run another file, click 'Upload BasicML file'"
        )

    def default_color_scheme(self) -> None:
        self.change_color_scheme("#4C721D", "#FFFFFF")

    def change_color_scheme(self, primary_color=None, secondary_color=None) -> None:
        if primary_color is None or secondary_color is None:
            primary_color = colorchooser.askcolor(title="Choose primary color")[1]
            secondary_color = colorchooser.askcolor(title="Choose off-color color")[1]

        # if primary_color is None or secondary_color is None:
        #     return

        theme = {
            "CTk": {"fg_color": ["gray95", "gray10"]},
            "CTkToplevel": {"fg_color": ["gray95", "gray10"]},
            "CTkFrame": {
                "corner_radius": 6,
                "border_width": 0,
                "fg_color": ["gray90", "gray13"],
                "top_fg_color": ["gray85", "gray16"],
                "border_color": ["gray65", "gray28"],
            },
            "CTkButton": {
                "corner_radius": 6,
                "border_width": 0,
                "fg_color": [primary_color, primary_color],
                "hover_color": [primary_color, primary_color],
                "border_color": [primary_color, primary_color],
                "text_color": [secondary_color, secondary_color],
                "text_color_disabled": ["gray74", "gray60"],
            },
            "CTkLabel": {
                "corner_radius": 0,
                "fg_color": "transparent",
                "text_color": [primary_color, primary_color],
            },
            "CTkEntry": {
                "corner_radius": 6,
                "border_width": 2,
                "fg_color": ["#F9F9FA", "#343638"],
                "border_color": ["#979DA2", "#565B5E"],
                "text_color": ["gray14", "gray84"],
                "placeholder_text_color": ["gray52", "gray62"],
            },
            "CTkCheckBox": {
                "corner_radius": 6,
                "border_width": 3,
                "fg_color": ["#3a7ebf", "#1f538d"],
                "border_color": ["#3E454A", "#949A9F"],
                "hover_color": ["#325882", "#14375e"],
                "checkmark_color": ["#DCE4EE", "gray90"],
                "text_color": ["gray14", "gray84"],
                "text_color_disabled": ["gray60", "gray45"],
            },
            "CTkSwitch": {
                "corner_radius": 1000,
                "border_width": 3,
                "button_length": 0,
                "fg_color": ["#939BA2", "#4A4D50"],
                "progress_color": ["#3a7ebf", "#1f538d"],
                "button_color": ["gray36", "#D5D9DE"],
                "button_hover_color": ["gray20", "gray100"],
                "text_color": ["gray14", "gray84"],
                "text_color_disabled": ["gray60", "gray45"],
            },
            "CTkRadioButton": {
                "corner_radius": 1000,
                "border_width_checked": 6,
                "border_width_unchecked": 3,
                "fg_color": ["#3a7ebf", "#1f538d"],
                "border_color": ["#3E454A", "#949A9F"],
                "hover_color": ["#325882", "#14375e"],
                "text_color": ["gray14", "gray84"],
                "text_color_disabled": ["gray60", "gray45"],
            },
            "CTkProgressBar": {
                "corner_radius": 1000,
                "border_width": 0,
                "fg_color": ["#939BA2", "#4A4D50"],
                "progress_color": ["#3a7ebf", "#1f538d"],
                "border_color": ["gray", "gray"],
            },
            "CTkSlider": {
                "corner_radius": 1000,
                "button_corner_radius": 1000,
                "border_width": 6,
                "button_length": 0,
                "fg_color": ["#939BA2", "#4A4D50"],
                "progress_color": ["gray40", "#AAB0B5"],
                "button_color": ["#3a7ebf", "#1f538d"],
                "button_hover_color": ["#325882", "#14375e"],
            },
            "CTkOptionMenu": {
                "corner_radius": 6,
                "fg_color": ["#3a7ebf", "#1f538d"],
                "button_color": ["#325882", "#14375e"],
                "button_hover_color": ["#234567", "#1e2c40"],
                "text_color": ["#DCE4EE", "#DCE4EE"],
                "text_color_disabled": ["gray74", "gray60"],
            },
            "CTkComboBox": {
                "corner_radius": 6,
                "border_width": 2,
                "fg_color": ["#F9F9FA", "#343638"],
                "border_color": ["#979DA2", "#565B5E"],
                "button_color": ["#979DA2", "#565B5E"],
                "button_hover_color": ["#6E7174", "#7A848D"],
                "text_color": ["gray14", "gray84"],
                "text_color_disabled": ["gray50", "gray45"],
            },
            "CTkScrollbar": {
                "corner_radius": 1000,
                "border_spacing": 4,
                "fg_color": "transparent",
                "button_color": ["gray55", "gray41"],
                "button_hover_color": ["gray40", "gray53"],
            },
            "CTkSegmentedButton": {
                "corner_radius": 6,
                "border_width": 2,
                "fg_color": ["#979DA2", "gray29"],
                "selected_color": ["#3a7ebf", "#1f538d"],
                "selected_hover_color": ["#325882", "#14375e"],
                "unselected_color": ["#979DA2", "gray29"],
                "unselected_hover_color": ["gray70", "gray41"],
                "text_color": ["#DCE4EE", "#DCE4EE"],
                "text_color_disabled": ["gray74", "gray60"],
            },
            "CTkTextbox": {
                "corner_radius": 6,
                "border_width": 0,
                "fg_color": ["gray100", "gray20"],
                "border_color": ["#979DA2", "#565B5E"],
                "text_color": ["gray14", "gray84"],
                "scrollbar_button_color": ["gray55", "gray41"],
                "scrollbar_button_hover_color": ["gray40", "gray53"],
            },
            "CTkScrollableFrame": {"label_fg_color": ["gray80", "gray21"]},
            "DropdownMenu": {
                "fg_color": ["gray90", "gray20"],
                "hover_color": ["gray75", "gray28"],
                "text_color": ["gray14", "gray84"],
            },
            "CTkFont": {
                "macOS": {"family": "SF Display", "size": 13, "weight": "normal"},
                "Windows": {"family": "Roboto", "size": 13, "weight": "normal"},
                "Linux": {"family": "Roboto", "size": 13, "weight": "normal"},
            },
        }

        with open("./themes/uvu.json", "w") as f:
            json.dump(theme, f, indent=4)

        customtkinter.set_default_color_theme("./themes/uvu.json")

        self.execute_btn.configure(
            text_color=secondary_color,
            fg_color=primary_color,
            hover_color=primary_color,
            border_color=secondary_color,
        )
        self.upload_btn.configure(
            text_color=secondary_color,
            fg_color=primary_color,
            hover_color=primary_color,
            border_color=secondary_color,
        )
        self.header.configure(text_color=primary_color)
        self.color_btn.configure(
            text_color=secondary_color,
            fg_color=primary_color,
            hover_color=primary_color,
            border_color=secondary_color,
        )
        self.default_btn.configure(
            text_color=secondary_color,
            fg_color=primary_color,
            hover_color=primary_color,
            border_color=secondary_color,
        )
        self.update()


app = UVSimGUI()
app.mainloop()
