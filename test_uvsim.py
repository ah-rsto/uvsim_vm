
import unittest
from unittest.mock import MagicMock
from controller import DataController, ProgramController, ArithmeticController


import unittest

# Added this for testing load program.
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

class TestArithmeticUnit(unittest.TestCase):
    # Aubrey is testing the arithmetic unit
    def setUp(self):
        self.arithmetic_unit = ArithmeticController()

class TestDataController(unittest.TestCase):
    def setUp(self):
        self.data_controller = DataController()

    def test_load_file(self):
        filename = "Test1.txt"
        self.data_controller.load_file(filename)
        self.assertEqual(self.data_controller.get_instruction(0), 1007)

    def test_save_file(self):
        filename = "Test1.txt"
        self.data_controller.load_file(filename)
        self.data_controller.save_file(filename)
        with open(filename, "r") as f:
            self.assertEqual(f.readline(), "1007\n")
        
    def test_reset_accumulator(self):
        self.data_controller.set_accumulator(5000)
        self.data_controller.reset_accumulator()
        self.assertEqual(self.data_controller.get_accumulator(), 0)

    def test_get_accumulator(self):
        self.data_controller.set_accumulator(100)
        self.assertEqual(self.data_controller.get_accumulator(), 100)

    def test_get_instructions(self):
        test_instructions = [i for i in range(100)]
        self.data_controller.set_instructions(test_instructions)
        self.assertEqual(self.data_controller.get_instructions(), test_instructions)

    def test_get_cursor(self):
        self.data_controller.set_cursor(50)
        self.assertEqual(self.data_controller.get_cursor(), 50)

    def test_set_get_instruction(self):
        self.data_controller.set_instruction(0, 1007)
        self.assertEqual(self.data_controller.get_instruction(0), 1007)


class MockDataModel:
    def __init__(self):
        self.accumulator = MagicMock()
        self.memory = MagicMock()
        self.cursor = MagicMock()

class TestProgramController(unittest.TestCase):
    def setUp(self):
        self.halted_mock = MagicMock()

        self.read_from_user_mock = MagicMock()
        self.write_to_console_mock = MagicMock()

        self.data_model = MockDataModel()
        self.controller = DataController()
        self.controller.data_model = self.data_model

        self.program_controller = ProgramController(self.controller)
        self.program_controller.set_halted_callback(self.halted_mock)
        self.program_controller.set_read_from_user_callback(self.read_from_user_mock)
        self.program_controller.set_write_to_console_callback(self.write_to_console_mock)

    def test_reset_accumulator(self):
        self.controller.reset_accumulator()
        self.assertEqual(self.controller.data_model.accumulator, 0)

    def test_reset_cursor(self):
        self.controller.reset_cursor()
        self.assertEqual(self.controller.data_model.cursor, 0)

    def test_load_file(self):
        self.controller.load_file = MagicMock()
        self.controller.load_file("Test1.txt")
        self.controller.load_file.assert_called_once_with("Test1.txt")

    def test_get_program_text(self):
        self.controller.data_model.memory = [100, -200, 300]
        expected_output = "00: +0100\n01: -200\n02: +0300\n"  # Changed -0200 to -200
        self.assertEqual(self.program_controller.get_program_text(), expected_output)


    def test_get_acc_cur(self):
        self.controller.data_model.accumulator = 500
        self.controller.data_model.cursor = 3
        expected_output = (f'Accumulator: 500\nCursor: 3\n')
        self.assertEqual(self.program_controller.get_acc_cur(), expected_output)

    def test_execute_program_invalid(self):
        self.controller.get_instruction = MagicMock(return_value=-999)
        self.program_controller.execute_program()
        self.halted_mock.assert_not_called()


class TestBranchController(unittest.TestCase):

    def setUp(self):
        self.uvsim = DataController()

    def test_branch(self):
        for i in range(0, 80):
            instruction_idx = i + 5
            self.uvsim.branch(instruction_idx)
            self.assertEqual(self.uvsim.get_cursor(), instruction_idx - 1)

    def test_branch_index_range_failure(self):
        for i in range(0, len(self.uvsim.data_model.memory) - 1):
            instruction_idx = i + 100
            with self.assertRaises(IndexError):
                self.uvsim.branch(instruction_idx)

    def test_branch_negative_success(self):
        for i in range(1, 80):
            instruction_idx = i + 5
            self.uvsim.set_accumulator(i * -1)
            self.uvsim.branch_negative(instruction_idx)
            self.assertEqual(self.uvsim.get_cursor(), instruction_idx - 1)

    def test_branch_negative_failure(self):
        for i in range(1, 80):
            instruction_idx = i + 5
            self.uvsim.set_accumulator(i)
            self.uvsim.branch_negative(instruction_idx)
            self.assertNotEqual(self.uvsim.get_cursor(), instruction_idx - 1)

    def test_branch_negative_index_range_failure(self):
        for i in range(1, len(self.uvsim.data_model.memory) - 1):
            instruction_idx = i + 100
            self.uvsim.set_accumulator(i * -1)
            with self.assertRaises(IndexError):
                self.uvsim.branch_negative(instruction_idx)

    def test_branch_zero_success(self):
        for i in range(0, 80):
            instruction_idx = i + 5
            self.uvsim.set_accumulator(0)
            self.uvsim.branch_zero(instruction_idx)
            self.assertEqual(self.uvsim.get_cursor(), instruction_idx - 1)

    def test_branch_zero_failure(self):
        for i in range(1, 80):
            instruction_idx = i + 5
            self.uvsim.set_accumulator(i)
            self.uvsim.branch_zero(instruction_idx)
            self.assertNotEqual(self.uvsim.get_cursor(), instruction_idx - 1)

    def test_branch_zero_index_range_failure(self):
        for i in range(0, len(self.uvsim.data_model.memory) - 1):
            instruction_idx = i + 100
            self.uvsim.set_accumulator(0)
            with self.assertRaises(IndexError):
                self.uvsim.branch_zero(instruction_idx)


if __name__ == "__main__":
    unittest.main()
