"""Model

This module manages the data model components.
"""


class DataModel:
    """Manager for main memory and register objects."""

    def __init__(self, loader):
        """DataModel initializer.

        :param: None
        :return: None
        """
        self.accumulator = 0
        self.memory = [0] * 100
        self.loader = loader

    def reset_accumulator(self) -> None:
        """Resets accumulator register.

        :param: None
        :return: None
        """
        self.accumulator = 0

    def load_program(self, source, is_file: bool) -> None:
        """Loads program instructions from file.

        :param filename: String containing file path
        :return: None
        """
        if is_file:
            instructions = self.loader.load_from_file(source)
        else:
            instructions = self.loader.load_from_input(source)

        for idx, instruction in enumerate(instructions):
            self.memory[idx] = instruction

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
