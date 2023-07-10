from unittest.mock import MagicMock, Mock
from controller import UVSimController, ArithmeticController

import unittest

from model import DataModel

# Added this for testing load program.
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))


class TestArithmeticUnit(unittest.TestCase):
    def setUp(self):
        self.arithmetic_unit = ArithmeticController()
        self.memory = DataModel(MockLoader())

    def test_addition_success(self):
        operand = 0
        self.memory.memory[operand] = 500
        accumulator = 1000
        new_accumulator = self.arithmetic_unit.addition(
            accumulator, self.memory.memory, operand
        )
        self.assertEqual(new_accumulator, 1500)

    def test_addition_negative(self):
        operand = 1
        self.memory.memory[operand] = -300
        accumulator = -500
        new_accumulator = self.arithmetic_unit.addition(
            accumulator, self.memory.memory, operand
        )
        self.assertEqual(new_accumulator, -800)

    def test_subtraction_success(self):
        operand = 2
        self.memory.memory[operand] = 500
        accumulator = 1000
        new_accumulator = self.arithmetic_unit.subtraction(
            accumulator, self.memory.memory, operand
        )
        self.assertEqual(new_accumulator, 500)

    def test_subtraction_negative(self):
        operand = 3
        self.memory.memory[operand] = -300
        accumulator = -500
        new_accumulator = self.arithmetic_unit.subtraction(
            accumulator, self.memory.memory, operand
        )
        self.assertEqual(new_accumulator, -200)

    def test_multiplication_success(self):
        operand = 4
        self.memory.memory[operand] = 5
        accumulator = 10
        new_accumulator = self.arithmetic_unit.multiplication(
            accumulator, self.memory.memory, operand
        )
        self.assertEqual(new_accumulator, 50)

    def test_multiplication_invalid_operand(self):
        operand = 5
        self.memory.memory[operand] = "not a number"
        accumulator = 10
        with self.assertRaises(ValueError):
            self.arithmetic_unit.multiplication(
                accumulator, self.memory.memory, operand
            )

    def test_division_success(self):
        operand = 6
        self.memory.memory[operand] = 10
        accumulator = 100
        new_accumulator = self.arithmetic_unit.division(
            accumulator, self.memory.memory, operand
        )
        self.assertEqual(new_accumulator, 10)

    def test_division_invalid_operand(self):
        operand = 7
        self.memory.memory[operand] = "not a number"
        accumulator = 100
        with self.assertRaises(ValueError):
            self.arithmetic_unit.division(accumulator, self.memory.memory, operand)

    def test_division_divide_by_zero(self):
        operand = 8
        self.memory.memory[operand] = 0
        accumulator = 100
        with self.assertRaises(ValueError):
            self.arithmetic_unit.division(accumulator, self.memory.memory, operand)


class MockLoader:
    def load_from_file(self, filename: str) -> list:
        if filename == "Test1.txt":
            return [1007, 1008, 2007, 2008, 2109, 1109, 4300]
        else:
            raise FileNotFoundError(f'File "{filename}" not found')

    def load_from_input(self, user_input: list) -> list:
        return [int(num) for num in user_input]


class TestDataModel(unittest.TestCase):
    def setUp(self):
        self.loader = MockLoader()
        self.data_model = DataModel(self.loader)

    def test_reset_accumulator(self):
        self.data_model.set_accumulator(5000)
        self.data_model.reset_accumulator()
        self.assertEqual(self.data_model.get_accumulator(), 0)

    def test_load_program_from_file(self):
        self.data_model.load_program("Test1.txt", True)
        self.assertEqual(self.data_model.get_instruction(0), 1007)

    def test_load_program_from_input(self):
        self.data_model.load_program(
            [1007, 1008, 1009, 1010, 1011, 1012, 1013, 1014], False
        )
        self.assertEqual(self.data_model.get_instruction(0), 1007)

    def test_get_accumulator(self):
        self.data_model.set_accumulator(100)
        self.assertEqual(self.data_model.get_accumulator(), 100)

    def test_get_instructions(self):
        test_instructions = [i for i in range(100)]
        self.data_model.set_instructions(test_instructions)
        self.assertEqual(self.data_model.get_instructions(), test_instructions)

    def test_whole_class(self):
        # Load a program and check that the first register is updated correctly
        self.data_model.load_program("Test1.txt", True)
        self.assertEqual(self.data_model.get_instruction(0), 1007)

        # Test the modification of the accumulator and register
        self.data_model.set_accumulator(10)
        self.assertEqual(self.data_model.get_accumulator(), 10)
        self.data_model.set_instruction(0, 5000)
        self.assertEqual(self.data_model.get_instruction(0), 5000)

        # Test setting the entire instruction set
        self.data_model.set_instructions([1, 2, 3, 4, 5] + [0] * 95)
        self.assertEqual(self.data_model.get_instructions(), [1, 2, 3, 4, 5] + [0] * 95)


class MockDataModel(DataModel):
    def __init__(self):
        self.accumulator = MagicMock()
        self.memory = MagicMock()
        self.loader = MagicMock()


class TestUVSimController(unittest.TestCase):
    def setUp(self):
        self.halted_mock = MagicMock()

        self.read_from_user_mock = MagicMock()
        self.write_to_console_mock = MagicMock()

        self.controller = UVSimController(self.halted_mock)
        self.controller.data_model = Mock()

    def test_init(self):
        self.assertEqual(self.controller.halted, self.halted_mock)
        self.assertEqual(self.controller.cursor, 0)
        self.assertEqual(self.controller.instruction, 0)

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
        self.controller.load_program("Test1.txt", True)
        self.controller.data_model.load_program.assert_called_once_with("Test1.txt", True)

    def test_get_program_text(self):
        self.controller.data_model.get_instructions = MagicMock(
            return_value=[100, -200, 300]
        )
        expected_output = "00: +0100\n01: -200\n02: +0300\n"
        self.assertEqual(self.controller.get_program_text(), expected_output)

    def test_get_acc_cur(self):
        self.controller.data_model.get_accumulator = MagicMock(return_value=500)
        self.controller.cursor = 3
        expected_output = (f'Accumulator: 500\nCursor: 3\n')
        self.assertEqual(self.controller.get_acc_cur(), expected_output)

    def test_execute_program_invalid(self):
        self.controller.data_model.get_instruction.return_value = -999
        self.controller.execute_program(
            self.read_from_user_mock, self.write_to_console_mock
        )
        self.halted_mock.assert_not_called()


class TestBranchController(unittest.TestCase):
    def setUp(self):
        self.uvsim = UVSimController()

    def test_branch(self):
        for i in range(0, 80):
            instruction_idx = i + 5

            new_cursor = self.uvsim.branch(instruction_idx)
            self.assertEqual(new_cursor, instruction_idx - 1)

    def test_branch_index_range_success(self):
        for i in range(0, len(self.uvsim.data_model.memory) - 1):
            instruction_idx = i + 1

            new_cursor = self.uvsim.branch(instruction_idx)
            self.assertEqual(new_cursor, i)

    def test_branch_index_range_failure(self):
        for i in range(0, len(self.uvsim.data_model.memory) - 1):
            self.uvsim.data_model.accumulator = i
            instruction_idx = i + 100

            self.assertRaises(IndexError, self.uvsim.branch, instruction_idx)

    def test_branch_negative_success(self):
        for i in range(1, 80):
            cursor = i
            accumulator = i * -1
            instruction_idx = i + 5

            new_cursor = self.uvsim.branch_negative(
                cursor, accumulator, instruction_idx
            )
            self.assertEqual(new_cursor, instruction_idx - 1)

    def test_branch_negative_failure(self):
        for i in range(0, 80):
            cursor = i
            accumulator = i
            instruction_idx = i + 5

            new_cursor = self.uvsim.branch_negative(
                cursor, accumulator, instruction_idx
            )
            self.assertNotEqual(new_cursor, instruction_idx - 1)
            self.assertEqual(new_cursor, i)

    def test_branch_negative_index_range_success(self):
        for i in range(0, len(self.uvsim.data_model.memory) - 1):
            cursor = i
            accumulator = i * -1
            instruction_idx = i + 1

            new_cursor = self.uvsim.branch_negative(
                cursor, accumulator, instruction_idx
            )
            self.assertEqual(new_cursor, i)

    def test_branch_negative_index_range_failure(self):
        for i in range(1, len(self.uvsim.data_model.memory) - 1):
            cursor = i
            accumulator = i * -1
            instruction_idx = i + 100

            self.assertRaises(
                IndexError,
                self.uvsim.branch_negative,
                cursor,
                accumulator,
                instruction_idx,
            )

    def test_branch_zero_success(self):
        for i in range(0, 80):
            cursor = i
            accumulator = 0
            instruction_idx = i + 5

            new_cursor = self.uvsim.branch_zero(cursor, accumulator, instruction_idx)
            self.assertEqual(new_cursor, instruction_idx - 1)

    def test_branch_zero_failure(self):
        for i in range(1, 80):
            cursor = i
            accumulator = i
            instruction_idx = i + 5

            self.uvsim.branch_zero(cursor, accumulator, instruction_idx)
            # Result -1 to handle auto increment after operations
            self.assertNotEqual(cursor, instruction_idx - 1)
            self.assertEqual(cursor, i)

    def test_branch_zero_index_range_success(self):
        for i in range(0, len(self.uvsim.data_model.memory) - 1):
            cursor = i
            accumulator = 0
            instruction_idx = i + 1

            new_cursor = self.uvsim.branch_zero(cursor, accumulator, instruction_idx)
            self.assertEqual(new_cursor, i)

    def test_branch_zero_index_range_failure(self):
        for i in range(0, len(self.uvsim.data_model.memory) - 1):
            cursor = i
            accumulator = 0
            instruction_idx = i + 100

            self.assertRaises(
                IndexError,
                self.uvsim.branch_zero,
                cursor,
                accumulator,
                instruction_idx,
            )

    def test_halt_sucess(self):
        halted, instruction_idx = None, 0

        # as gui app it no longer actually stops full application run
        self.assertEquals(self.uvsim.halt(halted, instruction_idx), instruction_idx)


if __name__ == "__main__":
    unittest.main()
