"""Model

This module manages the data model components.
"""


class DataModel:
    """REPLACE"""

    def __init__(self):
        self.accumulator = 0
        self.memory = [0] * 100

    def reset_accumulator(self):
        """Resets accumulator registry."""
        self.accumulator = 0

    def load_program(self, filename: str) -> None:
        """Loads program instructions from file."""
        while True:
            try:
                # filename = input("Enter the name of the file to load: ")
                with open(filename, "r") as f_in:
                    for idx, line in enumerate(f_in):
                        self.memory[idx] = int(line.strip())
                break
            except FileNotFoundError:
                print("File not found. Try again.")
            # except IndexError:
            #     print("Too many lines in program. Try again.")
            # except Exception:
            #     print("An exception occurred. Try again.")

    def save_program(self, filename: str) -> None:
        """Saves modified program to file. INCOMPLETE"""
        pass

    def get_accumulator(self) -> int:
        """Gets value in accumulator registry."""
        return self.accumulator

    def get_instruction(self, idx: int) -> int:
        """Gets instruction at specified memory index."""
        return self.memory[idx]

    def get_instructions(self) -> list:
        """Gets instruction set in memory."""
        return self.memory

    def set_accumulator(self, value: int) -> None:
        """Sets value in accumulator registy."""
        self.accumulator = value

    def set_instruction(self, idx, value: int) -> None:
        """Sets instruction at specific memory index."""
        self.memory[idx] = value

    def set_instructions(self, value: int) -> None:
        """Sets instruction set in memory."""
        self.memory = value
