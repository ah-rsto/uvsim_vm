"""Controller

This module manages the controller components.
"""

from model import DataModel
import json


class DataController:
    """Controller for data model management operations."""

    def __init__(self):
        self.data_model = DataModel()

    def load_file(self, filename: str) -> None:
        """Loads file to data model memory."""
        while True:
            try:
                with open(filename, "r") as f_in:
                    ln_idx = 0
                    for line in f_in:
                        self.data_model.memory[ln_idx] = int(line.strip())
                        ln_idx += 1
                break
            except FileNotFoundError:
                raise FileNotFoundError(f"File '{filename}' not found.")

    def save_file(self, filename: str) -> None:
        """Loads data model memory to file."""
        while True:
            try:
                with open(filename, "w") as f_out:
                    for line in self.data_model.memory:
                        f_out.write(f"{line}\n".rjust(5, "0"))
                break
            except FileNotFoundError:
                raise FileNotFoundError(f"File '{filename}' not found.")

    def save_theme(self, filename, theme) -> json:
        with open(filename, "w") as f_out:
            json.dump(theme, f_out, indent=4)

    def reset_cursor(self) -> None:
        """Resets position in instruction set runtime

        :param: None
        :return: None
        """
        self.data_model.cursor = 0

    def get_cursor(self) -> int:
        """REPLACE"""
        return self.data_model.cursor

    def set_cursor(self, value) -> None:
        """REPLACE"""
        self.data_model.cursor = value

    def reset_accumulator(self) -> None:
        """REPLACE"""
        self.data_model.accumulator = 0

    def get_accumulator(self) -> int:
        """Gets value of accumulator register.

        :param: None
        :return: self.accumulator: Value in accumulator register
        """
        return self.data_model.accumulator

    def set_accumulator(self, value: int) -> None:
        """Sets value of accumulator register.

        :param value: New value for accumulator register
        :return: None
        """
        self.data_model.accumulator = value

    def reset_memory(self) -> None:
        """REPLACE"""
        self.data_model.memory = [0] * 100

    def get_instruction(self, idx: int) -> int:
        """Gets instruction at specified memory index.

        :param idx: Index value for main memory
        :return: self.memory[idx]: Instruction from memory
        """
        return self.data_model.memory[idx]

    def set_instruction(self, idx, value: int) -> None:
        """Sets instruction at specific memory index.

        :param idx: Index value for main memory
        :param value: New value for instruction
        :return: None
        """
        self.data_model.memory[idx] = value

    def get_instructions(self) -> list:
        """Gets instruction set in memory.

        :param: None
        :return: self.memory: Instruction set from memory
        """
        return self.data_model.memory

    def set_instructions(self, value: int) -> None:
        """Sets instruction set in memory.

        :param value: New value for instruction set
        :return: None
        """
        self.data_model.memory = value

    def branch(self, instruction_idx) -> None:
        """Sets runtime cursor to new position.

        :param instruction_idx: Instruction index in memory
        :return cursor: New position in instruction set runtime
        """
        if -2 < instruction_idx and instruction_idx < 100:
            self.data_model.cursor = instruction_idx - 1
        else:
            raise IndexError(f"Memory index '{instruction_idx}' not in range.")

    def branch_zero(self, instruction_idx) -> None:
        """Sets runtime cursor to new position if accumulator is zero.

        :param cursor: Current position in instruction set runtime
        :param accumulator: Value in accumulator register
        :param instruction_idx: Instruction index in memory
        :return cursor: New position in instruction set runtime
        """
        if self.data_model.accumulator == 0:
            if -2 < instruction_idx and instruction_idx < 100:
                self.data_model.cursor = instruction_idx - 1
            else:
                raise IndexError(f"Memory index '{instruction_idx}' not in range.")

    def branch_negative(self, instruction_idx) -> int:
        """Sets runtime cursor to new position if accumulator is negative.

        :param cursor: Current position in instruction set runtime
        :param accumulator: Value in accumulator register
        :param instruction_idx: Instruction index in memory
        :return cursor: New position in instruction set runtime
        """
        if self.data_model.accumulator < 0:
            if -2 < instruction_idx and instruction_idx < 100:
                self.data_model.cursor = instruction_idx - 1
            else:
                raise IndexError(f"Memory index '{instruction_idx}' not in range.")


class ArithmeticController:
    """Controller for arithmetic operations."""

    @staticmethod
    def addition(val_a, val_b) -> int:
        """Adds designated memory value to accumulator.

        :param accumulator: Value in accumulator register
        :param instruction_set: Instruction set from memory
        :param instruction_idx: Instruction index in memory
        :return solution: Sum of accumulator and memory value
        """
        return val_a + val_b

    @staticmethod
    def subtraction(val_a, val_b) -> int:
        """Subtracts designated memory value from accumulator.

        :param accumulator: Value in accumulator register
        :param instruction_set: Instruction set from memory
        :param instruction_idx: Instruction index in memory
        :return solution: Difference of accumulator and memory value
        """
        return val_a - val_b

    @staticmethod
    def multiplication(val_a, val_b) -> int:
        """Multiplies designated memory value with accumulator.

        :param accumulator: Value in accumulator register
        :param instruction_set: Instruction set from memory
        :param instruction_idx: Instruction index in memory
        :return solution: Product of accumulator and memory value
        """
        return val_a * val_b

    @staticmethod
    def division(val_a, val_b) -> int:
        """Divides accumulator by designated memory value.

        :param accumulator: Value in accumulator register
        :param instruction_set: Instruction set from memory
        :param instruction_idx: Instruction index in memory
        :return solution: Quotient of accumulator dividend and memory value
        """
        if val_b == 0:
            raise ValueError("Invalid instruction_idx: Cannot divide by 0")
        return val_a // val_b


class ProgramController:
    """Controller for user program runtime."""

    def __init__(self, data_controller):
        """ProgramController initializer.

        :param halted: Halted callback function for ui
        :return: None
        """
        self.data_controller = data_controller
        self.halted = None
        self.read_from_user = None
        self.write_to_console = None

    def set_halted_callback(self, halted):
        self.halted = halted

    def set_read_from_user_callback(self, read_from_user):
        self.read_from_user = read_from_user

    def set_write_to_console_callback(self, write_to_console):
        self.write_to_console = write_to_console

    def get_program_text(self) -> str:
        """Requests and formats instruction set from data model.

        :param: None
        :return program_text: Formatted instruction and index for ui
        """
        program_text = ""
        instruction_set = self.data_controller.get_instructions()

        for idx, val in enumerate(instruction_set):
            idx, val = str(idx).rjust(2, "0"), (
                str(val).rjust(4, "0")
                if "-" in str(val)
                else f"+{str(val).rjust(4, '0')}"
            )

            program_text += f"{idx}: {val}\n"
        return program_text

    def get_acc_cur(self):
        """Requests and formats accumulator and cursor values.

        :param: None
        :return program_text: Formatted accumulator and cursor for ui
        """
        return (
            f"Accumulator: {self.data_controller.get_accumulator()}\n"
            f"Cursor: {self.data_controller.get_cursor()}\n"
        )

    def halt(self, halted) -> int:
        """Prints statement after program runtime completion.

        :param halted: Callback function for ui
        :param instruction_idx: Instruction index in memory
        :param instruction_idx: Instruction index in memory
        :return cursor: Final position in instruction set runtime
        """
        if halted:
            halted()
        else:
            print("Program Completed")

    def execute_program(self) -> None:
        """Executes main runtime loop and instruction validation.

        :param read_from_user: Input callback function for ui
        :param write_to_console: Output  callback function for ui
        :return: None
        """

        while True:
            instruction = self.data_controller.get_instruction(
                self.data_controller.get_cursor()
            )
            operation_code = abs(instruction) // 100
            instruction_idx = abs(instruction) % 100

            match operation_code:
                case 10:
                    self.data_controller.set_instruction(
                        instruction_idx, self.read_from_user()
                    )
                case 11:
                    self.write_to_console(
                        self.data_controller.get_instruction(instruction_idx)
                    )
                case 20:
                    self.data_controller.set_accumulator(
                        self.data_controller.get_instruction(instruction_idx)
                    )
                case 21:
                    self.data_controller.set_instruction(
                        instruction_idx, self.data_controller.get_accumulator()
                    )
                case 30:
                    self.data_controller.set_accumulator(
                        ArithmeticController.addition(
                            self.data_controller.get_accumulator(),
                            self.data_controller.get_instruction(instruction_idx),
                        )
                    )
                case 31:
                    self.data_controller.set_accumulator(
                        ArithmeticController.subtraction(
                            self.data_controller.get_accumulator(),
                            self.data_controller.get_instruction(instruction_idx),
                        )
                    )
                case 32:
                    self.data_controller.set_accumulator(
                        ArithmeticController.division(
                            self.data_controller.get_accumulator(),
                            self.data_controller.get_instruction(instruction_idx),
                        )
                    )
                case 33:
                    self.data_controller.set_accumulator(
                        ArithmeticController.multiplication(
                            self.data_controller.get_accumulator(),
                            self.data_controller.get_instruction(instruction_idx),
                        )
                    )
                case 40:
                    self.cursor = self.data_controller.branch(instruction_idx)
                case 41:
                    self.cursor = self.data_controller.branch_negative(instruction_idx)
                case 42:
                    self.cursor = self.data_controller.branch_zero(instruction_idx)
                case 43:
                    self.halt(self.halted)
                    break
                case _:
                    print(
                        f"Invalid operation code '{operation_code}'. \n"
                        "Program terminated"
                    )
                    break

            self.data_controller.set_cursor(self.data_controller.get_cursor() + 1)
