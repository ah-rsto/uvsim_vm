"""Controller

This module manages the controller components.
"""

from model import DataModel


class ArithmeticController:
    """Manager for arithmetic operations."""

    def addition(self, accumulator, instruction_set, instruction_idx) -> int:
        """Addition Method Docstring Text.

        :param accumulator: Value in accumulator register
        :param instruction_set: Instruction set from memory
        :param instruction_idx: Instruction index in memory
        :return solution: Sum of accumulator and memory value
        """
        return accumulator + instruction_set[instruction_idx]

    def subtraction(self, accumulator, instruction_set, instruction_idx) -> int:
        """Subtration Method Docstring Text.

        :param accumulator: Value in accumulator register
        :param instruction_set: Instruction set from memory
        :param instruction_idx: Instruction index in memory
        :return solution: Difference of accumulator and memory value
        """
        return accumulator - instruction_set[instruction_idx]

    def multiplication(self, accumulator, instruction_set, instruction_idx) -> int:
        """Multiplication Method Docstring Text.

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
        """Division Method Docstring Text.

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
        """Branch Method Docstring Text.

        :param instruction_idx: Instruction index in memory
        :return cursor: New position in instruction set runtime
        """
        if -2 < instruction_idx and instruction_idx < 100:
            cursor = instruction_idx - 1
        else:
            raise IndexError(f"Memory index '{instruction_idx}' not in range.")
        return cursor

    def branch_zero(self, cursor, accumulator, instruction_idx) -> int:
        """Branch Zero Method Docstring Text.

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
        """Branch Negative Method Docstring Text.

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
        """Halt Method Docstring Text.

        :param halted: None
        :param instruction_idx: Instruction index in memory
        :param instruction_idx: Instruction index in memory
        :return cursor: FInal position in instruction set runtime
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

    def __init__(self, halted, display_values=None):
        """"""
        super().__init__()
        self.data_model = DataModel()
        self.display_values = display_values
        self.cursor = 0
        self.instruction = 0
        self.halted = halted

    def reset_accumulator(self) -> None:
        """REPLACE

        :param: None
        :return: None
        """
        self.data_model.reset_accumulator()

    def reset_cursor(self) -> None:
        """REPLACE

        :param: None
        :return: None
        """
        self.cursor = 0

    def reset_instruction(self) -> None:
        """REPLACE

        :param: None
        :return: None
        """
        self.instruction = 0

    def load_program(self, filename) -> None:
        """REPLACE

        :param : None
        :return: None
        """
        print(filename)
        self.data_model.load_program(filename)

    def get_program_text(self) -> str:
        """REPLACE

        :param: None
        :return program_text: Formatted instruction and index for ui
        """
        program_text = ""
        instruction_set = self.data_model.get_instructions()

        for i, val in enumerate(instruction_set):
            idx, val = str(i).rjust(2, "0"), (
                val if "-" in str(val) else "+" + str(val)
            )
            program_text += f"{idx}:   {val}\n"
        return program_text

    def get_acc_cur(self) -> tuple[str, str]:
        """REPLACE

        :param: None
        :return program_text: Formatted accumulator and cursor for ui
        """
        return f"{self.data_model.get_accumulator()}\n", f"{self.cursor}\n"

    def execute_program(self, read_from_user, write_to_console) -> None:
        """Executes main runtime loop and instruction validation.

        :param : None
        :param : None
        :return: None
        """
        while True:
            self.instruction = self.data_model.get_instruction(self.cursor)
            operation_code = abs(self.instruction) // 100
            instruction_idx = abs(self.instruction) % 100

            if self.display_values:
                self.display_values(
                    f"{self.data_model.get_accumulator()}\n", f"{self.cursor}\n"
                )

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
                    self.cursor = self.branch(instruction_idx, self.cursor)
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
