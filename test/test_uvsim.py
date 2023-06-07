import unittest
from unittest.mock import patch
from src.uvsim import UVSim


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


if __name__ == '__main__':
    unittest.main()
