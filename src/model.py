"""Model

This module manages the data model components.
"""


class DataModel:
    """REPLACE"""

    def __init__(self):
        self.accumulator = 0
        self.registers = [0] * 100

    def reset_accumulator(self):
        self.accumulator = 0

    def load_program(self, filename):
        """REPLACE
        Args:
            REPLACE (TYPE): DESCRIPTION

        Returns:
            REPLACE (TYPE): DESCRIPTION
        """
        while True:
            try:
                # filename = input("Enter the name of the file to load: ")
                with open(filename, "r") as f_in:
                    for idx, line in enumerate(f_in):
                        self.registers[idx] = int(line.strip())
                break
            except FileNotFoundError:
                print("File not found. Try again.")
            # except IndexError:
            #     print("Too many lines in program. Try again.")
            # except Exception:
            #     print("An exception occurred. Try again.")

    def save_program(self, filename):
        """Saves modified program to file. INCOMPLETE
        Args:
            filename (str): Path to file

        Returns:
            None
        """
        pass

    def get_accumulator(self):
        """REPLACE
        Args:
            REPLACE (TYPE): DESCRIPTION

        Returns:
            REPLACE (TYPE): DESCRIPTION
        """
        return self.accumulator

    def get_register(self, idx):
        """REPLACE
        Args:
            REPLACE (TYPE): DESCRIPTION

        Returns:
            REPLACE (TYPE): DESCRIPTION
        """
        return self.registers[idx]

    def get_registers(self):
        """REPLACE
        Args:
            REPLACE (TYPE): DESCRIPTION

        Returns:
            REPLACE (TYPE): DESCRIPTION
        """
        return self.registers

    def set_accumulator(self, value):
        """REPLACE
        Args:
            REPLACE (TYPE): DESCRIPTION

        Returns:
            REPLACE (TYPE): DESCRIPTION
        """
        self.accumulator = value

    def set_register(self, idx, value):
        """REPLACE
        Args:
            REPLACE (TYPE): DESCRIPTION

        Returns:
            REPLACE (TYPE): DESCRIPTION
        """
        self.registers[idx] = value

    def set_registers(self, value):
        """REPLACE
        Args:
            REPLACE (TYPE): DESCRIPTION

        Returns:
            REPLACE (TYPE): DESCRIPTION
        """
        self.registers = value
