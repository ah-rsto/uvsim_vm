"""View

This module manages the view components.
"""

import tkinter as tk
from controller import ProgramController, DataController
from tkinter import filedialog, colorchooser
import customtkinter
import os


DATACONTROLLER = DataController()
PROGRAMCONTROLLER = ProgramController(DATACONTROLLER)

os.chdir(os.path.dirname(os.path.abspath(__file__)))

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("./themes/uvu.json")


class GUIView(customtkinter.CTk):
    def __init__(self):
        """GUIView initializer.

        :param: None
        :return: None
        """
        super().__init__()
        PROGRAMCONTROLLER.set_halted_callback(self.halted)
        PROGRAMCONTROLLER.set_read_from_user_callback(self.read_from_user)
        PROGRAMCONTROLLER.set_write_to_console_callback(self.write_to_console)

        self.title("UVSim")

        app_width, app_height = 780, 620
        self.screen_width, self.screen_height = (
            self.winfo_screenwidth(),
            self.winfo_screenheight(),
        )
        x_offset = (self.screen_width // 2) - (app_width // 2)
        y_offset = (self.screen_height // 2) - (app_height // 2)

        self.geometry(f"{app_width}x{app_height}+{x_offset}+{y_offset}")

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
            self.sidebar_frame, text="Upload BasicML file", command=self.load_program
        )
        self.upload_btn.grid(row=6, column=0, padx=20, pady=10)

        self.program_label = customtkinter.CTkLabel(
            self,
            text="BasicML program",
            font=customtkinter.CTkFont(size=20, weight="bold"),
            justify="right",
        )
        self.program_label.grid(row=0, column=1, columnspan=2, padx=20, pady=10)

        self.program_text = customtkinter.CTkTextbox(self, width=300, height=526)
        self.program_text.grid(
            row=1,
            column=1,
            rowspan=2,
            columnspan=2,
            padx=20,
            pady=(0, 10),
            sticky="nsew",
        )
        # self.program_text.bind("<KeyRelease>", self.limit_size, add="+")
        # self.program_text.bind("<<Paste>>", self.limit_size, add="+")

        self.execute_btn = customtkinter.CTkButton(
            self, text="Run File", command=self.execute_program, state="disabled"
        )
        self.execute_btn.grid(row=3, column=1, padx=20, pady=10, sticky="nsew")

        self.save_btn = customtkinter.CTkButton(
            self, text="Save File", command=self.save_program, state="disabled"
        )
        self.save_btn.grid(row=3, column=2, padx=20, pady=10, sticky="nsew")

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
        dialog.geometry("300x150+390+320")
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

        # program_text = "BasicML Program:\n"
        program_text = ""
        program_text += PROGRAMCONTROLLER.get_program_text()
        self.program_text.insert(tk.INSERT, program_text)

    def load_program(self, filename: str = "") -> None:
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

        DATACONTROLLER.load_file(self.filename)
        self.save_btn.configure(state="normal")
        self.execute_btn.configure(state="normal")
        self.update_program()
        self.reset_textboxes()

    def save_program(self) -> None:
        """Requests program instruction set and displays for user.

        :param: None
        :return: None
        """
        self.filename = filedialog.asksaveasfilename(
            initialdir="/",
            title="Save file",
            filetypes=(("txt files", "*.txt"), ("all files", "*.*")),
            defaultextension=".txt",
        )
        if self.filename == "":
            self.program_text.insert(tk.INSERT, "No file selected. Try again.")

        DATACONTROLLER.save_file(self.filename)
        self.write_to_console("File saved!")

    def update_instructions(self):
        """Gets input from user and converts to readable format.

        :param: None
        :return: None
        """
        program_dialog_text = self.program_text.get("1.0", tk.END)
        lines = program_dialog_text.split("\n")
        for idx, val in enumerate(lines):
            if idx < len(DATACONTROLLER.get_instructions()):
                val = int(val.strip().split(": ")[1])
                DATACONTROLLER.set_instruction(idx, val)

    def update_status(self):
        """Updates accumulator and cursor status.

        :param: None
        :return: None
        """
        self.accumulator_label.delete("1.0", tk.END)
        self.accumulator_label.insert(tk.END, PROGRAMCONTROLLER.get_acc_cur())

    def execute_program(self) -> None:
        """Requests program execution.

        :param: None
        :return: None
        """
        DATACONTROLLER.reset_cursor()
        DATACONTROLLER.reset_accumulator()
        self.reset_textboxes()
        self.update_instructions()
        PROGRAMCONTROLLER.execute_program()
        self.update_program()

    def halted(self) -> None:
        """Displays execution completion message for user.

        :param: None
        :return: None
        """
        self.update_status()
        self.write_to_console(
            "Program completed.\n\nTo run another file, click\n'Upload BasicML file'"
        )

    def default_color_scheme(self) -> None:
        """Changes color scheme of GUI to default UVU colors.

        :param: None
        :return: None
        """
        self.change_color_scheme("#4C721D", "#FFFFFF")

    def change_color_scheme(self, primary_color=None, secondary_color=None) -> None:
        """Changes color scheme of GUI.

        :param primary_color: Primary color for GUI
        :param secondary_color: Secondary color for GUI
        :return: None
        """
        # if primary_color is None or secondary_color is None:
        #     primary_color = colorchooser.askcolor(title="Choose primary color")[1]
        #     secondary_color = colorchooser.askcolor(title="Choose off-color")[1]
        if primary_color is None:
            selected_color = colorchooser.askcolor(title="Choose primary color")
            if selected_color != (None, None):
                primary_color = selected_color[1]
            else:
                primary_color = "#4C721D"

        if secondary_color is None:
            selected_color = colorchooser.askcolor(title="Choose off-color")
            if selected_color != (None, None):
                secondary_color = selected_color[1]
            else:
                secondary_color = "#FFFFFF"

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

        DATACONTROLLER.save_theme("./themes/uvu.json", theme)

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
        self.save_btn.configure(
            text_color=secondary_color,
            fg_color=primary_color,
            hover_color=primary_color,
            border_color=secondary_color,
        )
        self.program_label.configure(text_color=primary_color)
        self.update()


app = GUIView()
app.mainloop()
