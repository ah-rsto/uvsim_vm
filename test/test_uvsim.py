import unittest
from unittest.mock import patch
from src.uvsim import UVSim
import sys

class TestReadWriteStoreMemory(unittest.TestCase):
    def setUp(self):
        self.uvsim = UVSim()
        self.uvsim.operand = 0
        self.uvsim.memory = [0]*100


    @patch('builtins.input', return_value='5000')
    def test_read_memory_success(self, mock_input):
        self.uvsim.read_memory()
        self.assertEqual(self.uvsim.memory[self.uvsim.operand], 5000)
        mock_input.assert_called_once_with("Enter an integer from -9999 to +9999: ")


    @patch('builtins.input', side_effect=['not a number', '4000'])
    def test_read_memory_failure(self, mock_input):
        self.uvsim.read_memory()
        self.assertEqual(self.uvsim.memory[self.uvsim.operand], 4000)
        mock_input.assert_called_with("Enter an integer from -9999 to +9999: ")
        self.assertEqual(mock_input.call_count, 2)


    @patch('builtins.print')
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


class TestBranchZeroNegative(unittest.TestCase):
    def setUp(self):
        self.uvsim = UVSim()
        self.uvsim.memory = [0]*100


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
        self.S.memory = [0]*100
        self.S.accumulator

    """Multiply Tests"""
    #test correct answer in accumulator
    def test_multiply_success(self):
        # 5 * 5 = 25
        self.S.accumulator = 5
        self.S.memory[10] = 5
        self.S.operand = 10
        self.S.multiplication()
        self.assertEqual(self.S.accumulator, 25)

        #test when given over 4 it cuts off
    def test_multiply_overflow(self): 
        # 9876 * 5432 = 53655552 (truncated to 6432)
        self.S.accumulator = 9876
        self.S.memory[30] = 5432
        self.S.operand = 30
        self.S.multiplication()
        print(f'Accumulator multiply: {self.S.accumulator}')
        self.assertEqual(self.S.accumulator, 6432)

        #test error when given invalid input
        
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


        """Divide tests"""
        #test divide sucess in accumulator
    def test_divide_sucess(self): 
        #25 / 5 = 5
        self.S.accumulator = 25
        self.S.memory[10] = 5
        self.S.operand = 10
        self.S.division()
        self.assertEqual(self.S.accumulator, 5)


        #test divide by 0
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


        #test divide by float
        #want to be rounded/whole number
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

        #test error when given invalid input
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


        """Halt Tests"""
        #test halt
    def test_halt_sucess(self): 
        # check program was halted
        with patch.object(sys, "exit") as mock_exit:
            self.S.halt()
            mock_exit.assert_called_once_with("Program Halted")



if __name__ == '__main__':
    unittest.main()
