from unittest.mock import MagicMock, patch
from controller import UVSimController

import unittest

from model import DataModel

# Added this for testing load program.
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class TestDataModel(unittest.TestCase):
    def setUp(self):
        self.data_model = DataModel()

    def test_accumulator(self):
        self.data_model.set_accumulator(5000)
        self.assertEqual(self.data_model.get_accumulator(), 5000)

    def test_memory(self):
        self.data_model.set_instruction(0, 100)
        self.assertEqual(self.data_model.get_instruction(0), 100)

    def test_instructions(self):
        test_instructions = [i for i in range(100)]
        self.data_model.set_instructions(test_instructions)
        self.assertEqual(self.data_model.get_instructions(), test_instructions)

    def test_load_program(self):
        self.data_model.load_program('Test1.txt')
        self.assertEqual(self.data_model.get_instruction(0), 1007)

    def test_load_program_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            self.data_model.load_program('non_existent_file.txt')

    def test_whole_class(self):
        # Load a program and check that the first register is updated correctly
        self.data_model.load_program('Test2.txt')
        self.assertEqual(self.data_model.get_instruction(0), 1009)

        # Test the modification of the accumulator and register
        self.data_model.set_accumulator(10)
        self.assertEqual(self.data_model.get_accumulator(), 10)
        self.data_model.set_instruction(0, 5000)
        self.assertEqual(self.data_model.get_instruction(0), 5000)

        # Test setting the entire instruction set
        self.data_model.set_instructions([1, 2, 3, 4, 5] + [0]*95)
        self.assertEqual(self.data_model.get_instructions(), [1, 2, 3, 4, 5] + [0]*95)



class MockDataModel(DataModel):
    def __init__(self):
        self.accumulator = MagicMock()


class TestUVSimController(unittest.TestCase):
    def setUp(self):
        self.halted_mock = MagicMock()
        self.display_values_mock = MagicMock()

        self.read_from_user_mock = MagicMock()
        self.write_to_console_mock = MagicMock()

        self.controller = UVSimController(self.halted_mock, self.display_values_mock)
        self.controller.data_model = MockDataModel()
        self.controller.data_model.get_instruction = MagicMock()

    def test_init(self):
        self.assertEqual(self.controller.halted, self.halted_mock)
        self.assertEqual(self.controller.display_values, self.display_values_mock)
        self.assertEqual(self.controller.cursor, 0)
        self.assertEqual(self.controller.instruction, 0)
        self.assertIsInstance(self.controller.data_model, MockDataModel)

    def test_reset_accumulator(self):
        self.controller.data_model.reset_accumulator = MagicMock()
        self.controller.reset_accumulator()
        self.controller.data_model.reset_accumulator.assert_called_once()

    def test_reset_cursor(self):
        self.controller.reset_cursor()
        self.assertEqual(self.controller.cursor, 0)

    def test_reset_instruction(self):
        self.controller.reset_instruction()
        self.assertEqual(self.controller.instruction, 0)

    def test_load_program(self):
        self.controller.data_model.load_program = MagicMock()
        self.controller.load_program("Test1.txt")
        self.controller.data_model.load_program.assert_called_once_with("Test1.txt")

    def test_get_program_text(self):
        self.controller.data_model.get_instructions = MagicMock(return_value=[100, -200, 300])
        expected_output = "00:   +100\n01:   -200\n02:   +300\n"
        self.assertEqual(self.controller.get_program_text(), expected_output)

    def test_get_acc_cur(self):
        self.controller.data_model.get_accumulator = MagicMock(return_value=500)
        self.controller.cursor = 3
        expected_output = ("500\n", "3\n")
        self.assertEqual(self.controller.get_acc_cur(), expected_output)


    def test_execute_program_invalid(self):
        self.controller.data_model.get_instruction.return_value = -999
        self.controller.execute_program(self.read_from_user_mock, self.write_to_console_mock)
        self.halted_mock.assert_not_called()
            
if __name__ == '__main__':
    unittest.main()
