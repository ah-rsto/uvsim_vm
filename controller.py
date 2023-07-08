"""Controller

This module manages the controller components.
"""

from model import DataModel


class Loader:
    def __init__(self):
        pass

    def load_from_file(self, filename: str) -> list:
        instructions = []
        while True:
            try:
                with open(filename, "r") as f:
                    for line in f:
                        instructions.append(int(line.strip()))
                break
            except FileNotFoundError:
                raise FileNotFoundError(f"File '{filename}' not found.")
        return instructions

    def load_from_input(self, user_input: list) -> list:
        instructions = []
        for line in user_input:
            instructions.append(int(line))
        return instructions


class ArithmeticController:
    """Manager for arithmetic operations."""

    def addition(self, accumulator, instruction_set, instruction_idx) -> int:
        """Adds designated memory value to accumulator.

        :param accumulator: Value in accumulator register
        :param instruction_set: Instruction set from memory
        :param instruction_idx: Instruction index in memory
        :return solution: Sum of accumulator and memory value
        """
        return accumulator + instruction_set[instruction_idx]

    def subtraction(self, accumulator, instruction_set, instruction_idx) -> int:
        """Subtracts designated memory value from accumulator.

        :param accumulator: Value in accumulator register
        :param instruction_set: Instruction set from memory
        :param instruction_idx: Instruction index in memory
        :return solution: Difference of accumulator and memory value
        """
        return accumulator - instruction_set[instruction_idx]

    def multiplication(self, accumulator, instruction_set, instruction_idx) -> int:
        """Multiplies designated memory value with accumulator.

        :param accumulator: Value in accumulator register
        :param instruction_set: Instruction set from memory
        :param instruction_idx: Instruction index in memory
        :return solution: Product of accumulator and memory value
        """
        if not isinstance(instruction_set[instruction_idx], (int, float)):
            raise ValueError("Invalid instruction_idx: must be a number")
        result = accumulator * instruction_set[instruction_idx]
        return result % 10000

    def division(self, accumulator, instruction_set, instruction_idx) -> int:
        """Divides accumulator by designated memory value.

        :param accumulator: Value in accumulator register
        :param instruction_set: Instruction set from memory
        :param instruction_idx: Instruction index in memory
        :return solution: Quotient of accumulator dividend and memory value
        """
        if not isinstance(instruction_set[instruction_idx], (int, float)):
            raise ValueError("Invalid instruction_idx: must be a number")
        if instruction_set[instruction_idx] == 00:
            raise ValueError("Invalid instruction_idx: Cannot divide by 0")
        else:
            return (accumulator // instruction_set[instruction_idx]) % 10000


class BranchController:
    """Manager for branch operations."""

    def branch(self, instruction_idx) -> int:
        """Sets runtime cursor to new position.

        :param instruction_idx: Instruction index in memory
        :return cursor: New position in instruction set runtime
        """
        if -2 < instruction_idx and instruction_idx < 100:
            cursor = instruction_idx - 1
        else:
            raise IndexError(f"Memory index '{instruction_idx}' not in range.")
        return cursor

    def branch_zero(self, cursor, accumulator, instruction_idx) -> int:
        """Sets runtime cursor to new position if accumulator is zero.

        :param cursor: Current position in instruction set runtime
        :param accumulator: Value in accumulator register
        :param instruction_idx: Instruction index in memory
        :return cursor: New position in instruction set runtime
        """
        if accumulator == 0:
            if -2 < instruction_idx and instruction_idx < 100:
                cursor = instruction_idx - 1
            else:
                raise IndexError(f"Memory index '{instruction_idx}' not in range.")
        return cursor

    def branch_negative(self, cursor, accumulator, instruction_idx) -> int:
        """Sets runtime cursor to new position if accumulator is negative.

        :param cursor: Current position in instruction set runtime
        :param accumulator: Value in accumulator register
        :param instruction_idx: Instruction index in memory
        :return cursor: New position in instruction set runtime
        """
        if accumulator < 0:
            if -2 < instruction_idx and instruction_idx < 100:
                cursor = instruction_idx - 1
            else:
                raise IndexError(f"Memory index '{instruction_idx}' not in range.")
        return cursor

    def halt(self, halted, instruction_idx) -> int:
        """Prints statement after program runtime completion.

        :param halted: Callback function for ui
        :param instruction_idx: Instruction index in memory
        :param instruction_idx: Instruction index in memory
        :return cursor: Final position in instruction set runtime
        """
        cursor = instruction_idx
        if halted:
            halted()
            return cursor
        else:
            print("Program Completed")
            return cursor


class UVSimController(ArithmeticController, BranchController):
    """Manager for application runtime."""

    def __init__(self, halted=None):
        """UVSimController initializer.

        :param halted: Halted callback function for ui
        :param display_values: Display value callback function for ui
        :return: None
        """
        super().__init__()
        self.data_model = DataModel(Loader())
        self.cursor = 0
        self.instruction = 0
        self.halted = halted

    def reset_accumulator(self) -> None:
        """Requests data model accumulator reset.

        :param: None
        :return: None
        """
        self.data_model.reset_accumulator()

    def reset_cursor(self) -> None:
        """Resets position in instruction set runtime

        :param: None
        :return: None
        """
        self.cursor = 0

    def reset_instruction(self) -> None:
        """Resets initial instruction assignment

        :param: None
        :return: None
        """
        self.instruction = 0

    def load_program(self, source, is_file) -> None:
        """Requests data model program load from file

        :param filename: String containing file path
        :return: None
        """
        # self.data_model.load_program(filename)
        self.data_model.load_program(source, is_file)

    def get_program_text(self) -> str:
        """Requests and formats instruction set from data model.

        :param: None
        :return program_text: Formatted instruction and index for ui
        """
        program_text = ""
        instruction_set = self.data_model.get_instructions()

        for i, val in enumerate(instruction_set):
            idx, val = str(i).rjust(2, "0"), (
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
            f"Accumulator: {self.data_model.get_accumulator()}\nCursor: {self.cursor}\n"
        )

    def execute_program(self, read_from_user, write_to_console) -> None:
        """Executes main runtime loop and instruction validation.

        :param read_from_user: Input callback function for ui
        :param write_to_console: Output  callback function for ui
        :return: None
        """

        while True:
            self.instruction = self.data_model.get_instruction(self.cursor)
            operation_code = abs(self.instruction) // 100
            instruction_idx = abs(self.instruction) % 100

            match operation_code:
                case 10:
                    self.data_model.set_instruction(instruction_idx, read_from_user())
                case 11:
                    write_to_console(self.data_model.get_instruction(instruction_idx))
                case 20:
                    self.data_model.set_accumulator(
                        self.data_model.get_instruction(instruction_idx)
                    )
                case 21:
                    self.data_model.set_instruction(
                        instruction_idx, self.data_model.get_accumulator()
                    )
                case 30:
                    self.data_model.set_accumulator(
                        self.addition(
                            self.data_model.get_accumulator(),
                            self.data_model.get_instructions(),
                            instruction_idx,
                        )
                    )
                case 31:
                    self.data_model.set_accumulator(
                        self.subtraction(
                            self.data_model.get_accumulator(),
                            self.data_model.get_instructions(),
                            instruction_idx,
                        )
                    )
                case 32:
                    self.data_model.set_accumulator(
                        self.division(
                            self.data_model.get_accumulator(),
                            self.data_model.get_instructions(),
                            instruction_idx,
                        )
                    )
                case 33:
                    self.data_model.set_accumulator(
                        self.multiplication(
                            self.data_model.get_accumulator(),
                            self.data_model.get_instructions(),
                            instruction_idx,
                        )
                    )
                case 40:
                    self.cursor = self.branch(instruction_idx)
                case 41:
                    self.cursor = self.branch_negative(
                        self.cursor, self.data_model.get_accumulator(), instruction_idx
                    )
                case 42:
                    self.cursor = self.branch_zero(
                        self.cursor, self.data_model.get_accumulator(), instruction_idx
                    )
                case 43:  # HALT
                    self.cursor = self.halt(self.halted, instruction_idx)
                    break
                case _:
                    print(
                        f"Invalid operation code '{operation_code}'. \n"
                        "Program terminated"
                    )
                    break

            self.cursor += 1
