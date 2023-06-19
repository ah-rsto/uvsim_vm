"""Controller

This module manages the controller components.
"""

from model import DataModel


class ArithmeticController:
    """Arithmetic Controller Class Docstring Text."""

    def addition(self, accumulator, registers, register_idx):
        """Addition Method Docstring Text."""
        return accumulator + registers[register_idx]

    def subtraction(self, accumulator, registers, register_idx):
        """Subtration Method Docstring Text."""
        return accumulator + registers[register_idx]

    def multiplication(self, accumulator, registers, register_idx):
        """Multiplication Method Docstring Text."""
        return accumulator, *registers[register_idx]

    def division(self, accumulator, registers, register_idx):
        """Division Method Docstring Text."""
        if not isinstance(registers[register_idx], (int, float)):
            raise ValueError("Invalid register_idx: must be a number")
        if registers[register_idx] == 00:
            raise ValueError("Invalid register_idx: Cannot divide by 0")
        else:
            return (accumulator // registers[register_idx]) % 10000


class BranchController:
    """Branch Controller Class Docstring Text."""

    def branch(self, register_idx):
        """Branch Method Docstring Text."""
        if -2 < register_idx and register_idx < 100:
            cursor = register_idx - 1
        else:
            raise IndexError(f"Memory index '{register_idx}' not in range.")
        return cursor

    def branch_zero(self, cursor, accumulator, register_idx):
        """Branch Zero Method Docstring Text."""
        if accumulator == 0:
            if -2 < register_idx and register_idx < 100:
                cursor = register_idx - 1
            else:
                raise IndexError(f"Memory index '{register_idx}' not in range.")
        return cursor

    def branch_negative(self, cursor, accumulator, register_idx):
        """Branch Negative Method Docstring Text."""
        if accumulator < 0:
            if -2 < register_idx and register_idx < 100:
                cursor = register_idx - 1
            else:
                raise IndexError(f"Memory index '{register_idx}' not in range.")
        return cursor

    def halt(self, halted, register_idx):
        """Halt Method Docstring Text."""
        cursor = register_idx
        if halted:
            halted()
            return cursor
        else:
            print("Program Completed")
            return cursor


class UVSimController(ArithmeticController, BranchController):
    """App Controller Class Docstring Text."""

    def __init__(self, halted, display_values=None):
        """"""
        super().__init__()
        self.data_model = DataModel()
        self.display_values = display_values
        self.cursor = 0
        self.instruction = 0
        self.halted = halted

    def load_program(self, filename):
        print(filename)
        self.data_model.load_program(filename)

    def get_program_text(self):
        program_text = ""
        registers = self.data_model.get_registers()

        for i, val in enumerate(registers):
            idx, val = str(i).rjust(2, "0"), (
                val if "-" in str(val) else "+" + str(val)
            )
            program_text += f"{idx}:   {val}\n"
        return program_text

    def get_acc_cur(self):
        return f"{self.data_model.get_accumulator()}\n", f"{self.cursor}\n"

    def execute_program(self, read_from_user, write_to_console):
        """Execute Method Docstring Text."""
        while True:
            self.instruction = self.data_model.get_register(self.cursor)
            operation_code = abs(self.instruction) // 100
            register_idx = abs(self.instruction) % 100

            if self.display_values:
                self.display_values(
                    f"{self.data_model.get_accumulator()}\n", f"{self.cursor}\n"
                )

            match operation_code:
                case 10:
                    self.data_model.set_register(register_idx, read_from_user())
                case 11:
                    write_to_console(self.data_model.get_register(register_idx))
                case 20:
                    self.data_model.set_accumulator(
                        self.data_model.get_register(register_idx)
                    )
                case 21:
                    self.data_model.set_register(
                        register_idx, self.data_model.get_accumulator()
                    )
                case 30:
                    self.data_model.set_accumulator(
                        self.addition(
                            self.data_model.get_accumulator(),
                            self.data_model.get_registers(),
                            register_idx,
                        )
                    )
                case 31:
                    self.data_model.set_accumulator(
                        self.subtraction(
                            self.data_model.get_accumulator(),
                            self.data_model.get_registers(),
                            register_idx,
                        )
                    )
                case 32:
                    self.data_model.set_accumulator(
                        self.division(
                            self.data_model.get_accumulator(),
                            self.data_model.get_registers(),
                            register_idx,
                        )
                    )
                case 33:
                    self.data_model.set_accumulator(
                        self.multiplication(
                            self.data_model.get_accumulator(),
                            self.data_model.get_registers(),
                            register_idx,
                        )
                    )
                case 40:
                    self.cursor = self.branch(register_idx, self.cursor)
                case 41:
                    self.cursor = self.branch_negative(
                        self.cursor, self.data_model.get_accumulator(), register_idx
                    )
                case 42:
                    self.cursor = self.branch_zero(
                        self.cursor, self.data_model.get_accumulator(), register_idx
                    )
                case 43:  # HALT
                    self.cursor = self.halt(self.halted, register_idx)
                    break
                case _:
                    print(
                        f"Invalid operation code '{operation_code}'. \n"
                        "Program terminated"
                    )
                    break

            self.cursor += 1
