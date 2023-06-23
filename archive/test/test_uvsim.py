import unittest
import sys
from unittest.mock import patch, MagicMock
from archive.uvsim import UVSim, ArithmeticUnit, Memory
from controller import UVSimController
from model import DataModel

# Added this for testing load program.
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))


class TestReadWriteStoreMemory(unittest.TestCase):
    def setUp(self):
        self.uvsim = UVSim()
        self.uvsim.operand = 0
        self.uvsim.memory = [0] * 100

    @patch("builtins.input", return_value="5000")
    def test_read_memory_success(self, mock_input):
        self.uvsim.read_memory()
        self.assertEqual(self.uvsim.memory[self.uvsim.operand], 5000)
        mock_input.assert_called_once_with("Enter an integer from -9999 to +9999: ")

    @patch("builtins.input", side_effect=["not a number", "4000"])
    def test_read_memory_failure(self, mock_input):
        self.uvsim.read_memory()
        self.assertEqual(self.uvsim.memory[self.uvsim.operand], 4000)
        mock_input.assert_called_with("Enter an integer from -9999 to +9999: ")
        self.assertEqual(mock_input.call_count, 2)

    @patch("builtins.print")
    def test_write_memory_success(self, mock_print):
        self.uvsim.memory[self.uvsim.operand] = 5000
        self.uvsim.write_memory()
        mock_print.assert_called_once_with(5000)

    def test_write_memory_failure(self):
        self.uvsim.operand = 100
        with self.assertRaises(IndexError):
            self.uvsim.write_memory()

    def test_store_memory_success(self):
        self.uvsim.accumulator = 5000
        self.uvsim.store_memory()
        self.assertEqual(self.uvsim.memory[self.uvsim.operand], 5000)

    def test_store_memory_failure(self):
        self.uvsim.operand = 100
        with self.assertRaises(IndexError):
            self.uvsim.store_memory()

    def test_addition_success(self):
        self.uvsim.accumulator = 1000
        self.uvsim.memory[self.uvsim.operand] = 500
        self.uvsim.addition()
        self.assertEqual(self.uvsim.accumulator, 1500)

    def test_addition_negative(self):
        self.uvsim.accumulator = -500
        self.uvsim.memory[self.uvsim.operand] = -300
        self.uvsim.addition()
        self.assertEqual(self.uvsim.accumulator, -800)

    def test_subtraction_success(self):
        self.uvsim.accumulator = 1000
        self.uvsim.memory[self.uvsim.operand] = 500
        self.uvsim.subtraction()
        self.assertEqual(self.uvsim.accumulator, 500)

    def test_subtraction_negative(self):
        self.uvsim.accumulator = -500
        self.uvsim.memory[self.uvsim.operand] = -300
        self.uvsim.subtraction()
        self.assertEqual(self.uvsim.accumulator, -200)

    def test_load_memory_success(self):
        self.uvsim.memory[self.uvsim.operand] = 500
        self.uvsim.load_memory()
        self.assertEqual(self.uvsim.accumulator, 500)

    def test_load_memory_negative(self):
        self.uvsim.memory[self.uvsim.operand] = -1000
        self.uvsim.load_memory()
        self.assertEqual(self.uvsim.accumulator, -1000)


class TestBranchZeroNegative(unittest.TestCase):
    def setUp(self):
        self.uvsim = UVSim()
        self.uvsim.memory = [0] * 100

    def test_branch(self):
        for i in range(0, 80):
            self.uvsim.instruction_counter = i
            self.uvsim.operand = i + 5

            self.uvsim.branch()
            # Result -1 to handle auto increment after operations
            self.assertEqual(self.uvsim.instruction_counter, self.uvsim.operand - 1)

    def test_branch_index_range_success(self):
        for i in range(0, len(self.uvsim.memory) - 1):
            self.uvsim.instruction_counter = i
            self.uvsim.operand = i + 1

            self.uvsim.branch()
            self.assertEqual(self.uvsim.instruction_counter, i)

    def test_branch_index_range_failure(self):
        for i in range(0, len(self.uvsim.memory) - 1):
            self.uvsim.instruction_counter = i
            self.uvsim.accumulator = i
            self.uvsim.operand = i + 100

            self.assertRaises(IndexError, self.uvsim.branch)

    def test_branch_negative_success(self):
        for i in range(1, 80):
            self.uvsim.instruction_counter = i
            self.uvsim.accumulator = i * -1
            self.uvsim.operand = i + 5

            self.uvsim.branch_negative()
            # Result -1 to handle auto increment after operations
            self.assertEqual(self.uvsim.instruction_counter, self.uvsim.operand - 1)

    def test_branch_negative_failure(self):
        for i in range(0, 80):
            self.uvsim.instruction_counter = i
            self.uvsim.accumulator = i
            self.uvsim.operand = i + 5

            self.uvsim.branch_negative()
            # Result -1 to handle auto increment after operations
            self.assertNotEqual(self.uvsim.instruction_counter, self.uvsim.operand - 1)
            self.assertEqual(self.uvsim.instruction_counter, i)

    def test_branch_negative_index_range_success(self):
        for i in range(0, len(self.uvsim.memory) - 1):
            self.uvsim.instruction_counter = i
            self.uvsim.accumulator = i * -1
            self.uvsim.operand = i + 1

            self.uvsim.branch()
            self.assertEqual(self.uvsim.instruction_counter, i)

    def test_branch_negative_index_range_failure(self):
        for i in range(0, len(self.uvsim.memory) - 1):
            self.uvsim.instruction_counter = i
            self.uvsim.accumulator = i * -1
            self.uvsim.operand = i + 100

            self.assertRaises(IndexError, self.uvsim.branch)

    def test_branch_zero_success(self):
        for i in range(0, 80):
            self.uvsim.instruction_counter = i
            self.uvsim.accumulator = 0
            self.uvsim.operand = i + 5

            self.uvsim.branch_zero()
            # Result -1 to handle auto increment after operations
            self.assertEqual(self.uvsim.instruction_counter, self.uvsim.operand - 1)

    def test_branch_zero_failure(self):
        for i in range(1, 80):
            self.uvsim.instruction_counter = i
            self.uvsim.accumulator = i
            self.uvsim.operand = i + 5

            self.uvsim.branch_zero()
            # Result -1 to handle auto increment after operations
            self.assertNotEqual(self.uvsim.instruction_counter, self.uvsim.operand - 1)
            self.assertEqual(self.uvsim.instruction_counter, i)

    def test_branch_zero_index_range_success(self):
        for i in range(0, len(self.uvsim.memory) - 1):
            self.uvsim.instruction_counter = i
            self.uvsim.accumulator = 0
            self.uvsim.operand = i + 1

            self.uvsim.branch()
            self.assertEqual(self.uvsim.instruction_counter, i)

    def test_branch_zero_index_range_failure(self):
        for i in range(0, len(self.uvsim.memory) - 1):
            self.uvsim.instruction_counter = i
            self.uvsim.accumulator = 0
            self.uvsim.operand = i + 100

            self.assertRaises(IndexError, self.uvsim.branch)


class TestMulDivHaltUnitTests(unittest.TestCase):
    def setUp(self):
        self.S = UVSim()
        self.S.operand = 0
        self.S.memory = [0] * 100
        self.S.accumulator

    def test_multiply_success(self):
        # 5 * 5 = 25
        self.S.accumulator = 5
        self.S.memory[10] = 5
        self.S.operand = 10
        self.S.multiplication()
        self.assertEqual(self.S.accumulator, 25)

    def test_multiply_overflow(self):
        # 9876 * 5432 = 53655552 (truncated to 6432)
        self.S.accumulator = 9876
        self.S.memory[30] = 5432
        self.S.operand = 30
        self.S.multiplication()
        print(f"Accumulator multiply: {self.S.accumulator}")
        self.assertEqual(self.S.accumulator, 6432)

    def test_multiply_fail(self):
        # Invalid operand
        self.S.accumulator = 5
        self.S.memory[10] = "invalid"
        self.S.operand = 10
        try:
            self.S.multiplication()
            # should not be reached if given value error
            self.assertEqual(False, "Expected ValueError")
        except ValueError as error:
            # should come here
            self.assertEqual(str(error), "Invalid operand: must be a number")

    def test_divide_sucess(self):
        # 25 / 5 = 5
        self.S.accumulator = 25
        self.S.memory[10] = 5
        self.S.operand = 10
        self.S.division()
        self.assertEqual(self.S.accumulator, 5)

    def test_divide_zero(self):
        # 15 / 0 (division by zero)
        self.S.accumulator = 15
        self.S.memory[30] = 0
        self.S.operand = 30
        try:
            self.S.division()
            # should not be reached if given value error
            self.assertEqual(False, True, "Expected ValueError for division by zero")
        except ValueError as error:
            # should come here
            self.assertEqual(str(error), "Invalid operand: Cannot divide by 0")

    def test_divide_float(self):
        # 10.5 / 2.5 = 4.2
        self.S.accumulator = 10.5
        self.S.memory[50] = 2.5
        self.S.operand = 50
        self.S.division()
        self.assertEqual(self.S.accumulator, 4.0)

        # 10.5 / 2.5 = 4.5
        self.S.accumulator = 10.9
        self.S.memory[50] = 2.4
        self.S.operand = 50
        self.S.division()
        self.assertEqual(self.S.accumulator, 4.0)

        # 10.5 / 2.5 = 4.7
        self.S.accumulator = 23.5
        self.S.memory[50] = 5
        self.S.operand = 50
        self.S.division()
        self.assertEqual(self.S.accumulator, 4.0)

    def test_divide_fail(self):
        # invalid operand
        self.S.accumulator = 10
        self.S.memory[40] = "invalid"
        self.S.operand = 40
        try:
            self.S.division()
            # should not be reached if given value error
            self.assertEqual(False, "Expected ValueError for invalid operand")
        except ValueError as error:
            # should come here
            self.assertEqual(str(error), "Invalid operand: must be a number")

    def test_halt_sucess(self):
        with patch.object(sys, "exit") as mock_exit:
            self.S.halt()
            mock_exit.assert_called_once_with("Program Halted")


class TestArithmeticUnit(unittest.TestCase):
    def setUp(self):
        self.arithmetic_unit = ArithmeticUnit()
        self.memory = Memory()
        self.memory.memory = [0] * 100

    def test_addition_success(self):
        operand = 0
        self.memory.memory[operand] = 500
        accumulator = 1000
        self.arithmetic_unit.addition(operand, accumulator, self.memory.memory)
        self.assertEqual(accumulator, 1500)

    def test_addition_negative(self):
        operand = 1
        self.memory.memory[operand] = -300
        accumulator = -500
        self.arithmetic_unit.addition(operand, accumulator, self.memory.memory)
        self.assertEqual(accumulator, -800)

    def test_subtraction_success(self):
        operand = 2
        self.memory.memory[operand] = 500
        accumulator = 1000
        self.arithmetic_unit.subtraction(operand, accumulator, self.memory.memory)
        self.assertEqual(accumulator, 500)

    def test_subtraction_negative(self):
        operand = 3
        self.memory.memory[operand] = -300
        accumulator = -500
        self.arithmetic_unit.subtraction(operand, accumulator, self.memory.memory)
        self.assertEqual(accumulator, -200)

    def test_multiplication_success(self):
        operand = 4
        self.memory.memory[operand] = 5
        accumulator = 10
        self.arithmetic_unit.multiplication(operand, accumulator, self.memory.memory)
        self.assertEqual(accumulator, 50)

    def test_multiplication_invalid_operand(self):
        operand = 5
        self.memory.memory[operand] = "not a number"
        accumulator = 10
        with self.assertRaises(ValueError):
            self.arithmetic_unit.multiplication(
                operand, accumulator, self.memory.memory
            )

    def test_division_success(self):
        operand = 6
        self.memory.memory[operand] = 10
        accumulator = 100
        self.arithmetic_unit.division(operand, accumulator, self.memory.memory)
        self.assertEqual(accumulator, 10)

    def test_division_invalid_operand(self):
        operand = 7
        self.memory.memory[operand] = "not a number"
        accumulator = 100
        with self.assertRaises(ValueError):
            self.arithmetic_unit.division(operand, accumulator, self.memory.memory)

    def test_division_divide_by_zero(self):
        operand = 8
        self.memory.memory[operand] = 0
        accumulator = 100
        with self.assertRaises(ValueError):
            self.arithmetic_unit.division(operand, accumulator, self.memory.memory)


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
        self.data_model.load_program("Test1.txt")
        self.assertEqual(self.data_model.get_instruction(0), 1007)

    def test_load_program_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            self.data_model.load_program("non_existent_file.txt")

    def test_whole_class(self):
        # Load a program and check that the first register is updated correctly
        self.data_model.load_program("Test2.txt")
        self.assertEqual(self.data_model.get_instruction(0), 1009)

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
        self.controller.data_model.get_instructions = MagicMock(
            return_value=[100, -200, 300]
        )
        expected_output = "00:   +100\n01:   -200\n02:   +300\n"
        self.assertEqual(self.controller.get_program_text(), expected_output)

    def test_get_acc_cur(self):
        self.controller.data_model.get_accumulator = MagicMock(return_value=500)
        self.controller.cursor = 3
        expected_output = ("500\n", "3\n")
        self.assertEqual(self.controller.get_acc_cur(), expected_output)

    def test_execute_program_invalid(self):
        self.controller.data_model.get_instruction.return_value = -999
        self.controller.execute_program(
            self.read_from_user_mock, self.write_to_console_mock
        )
        self.halted_mock.assert_not_called()


if __name__ == "__main__":
    unittest.main()
