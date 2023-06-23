"""Model

This module manages the data model components.
"""


class DataModel:
    """Manager for main memory and register objects."""

    def __init__(self):
        """DataModel initializer.

        :param: None
        :return: None
        """
        self.accumulator = 0
        self.memory = [0] * 100

    def reset_accumulator(self) -> None:
        """Resets accumulator register.

        :param: None
        :return: None
        """
        self.accumulator = 0

    def load_program(self, filename: str) -> None:
        """Loads program instructions from file.

        :param filename: String containing file path
        :return: None
        """
        while True:
            try:
                # filename = input("Enter the name of the file to load: ")
                with open(filename, "r") as f_in:
                    for idx, line in enumerate(f_in):
                        self.memory[idx] = int(line.strip())
                break
            except FileNotFoundError:
                # print("File not found. Try again.") - had to change this because it caused an infinite loop (Taylie)
                raise FileNotFoundError('File not found. Try again.')
            # except IndexError:
            #     print("Too many lines in program. Try again.")
            # except Exception:
            #     print("An exception occurred. Try again.")

    def save_program(self, filename: str) -> None:
        """Saves modified program to file. INCOMPLETE

        :param filename: String containing file path
        :return: None
        """
        pass

    def get_accumulator(self) -> int:
        """Gets value of accumulator register.

        :param: None
        :return: self.accumulator: Value in accumulator register
        """
        return self.accumulator

    def get_instruction(self, idx: int) -> int:
        """Gets instruction at specified memory index.

        :param idx: Index value for main memory
        :return: self.memory[idx]: Instruction from memory
        """
        return self.memory[idx]

    def get_instructions(self) -> list:
        """Gets instruction set in memory.

        :param: None
        :return: self.memory: Instruction set from memory
        """
        return self.memory

    def set_accumulator(self, value: int) -> None:
        """Sets value of accumulator register.

        :param value: New value for accumulator register
        :return: None
        """
        self.accumulator = value

    def set_instruction(self, idx, value: int) -> None:
        """Sets instruction at specific memory index.

        :param idx: Index value for main memory
        :param value: New value for instruction
        :return: None
        """
        self.memory[idx] = value

    def set_instructions(self, value: int) -> None:
        """Sets instruction set in memory.

        :param value: New value for instruction set
        :return: None
        """
        self.memory = value
