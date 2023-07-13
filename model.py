"""Model

This module manages the data model components.
"""


class DataModel:
    """Data Model for main memory and register objects."""

    def __init__(self):
        """DataModel initializer.

        :param: None
        :return: None
        """
        self.cursor = 0
        self.accumulator = 0
        self.memory = [0] * 100
