import unittest
from unittest.mock import patch
from uvsim import UVSim

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

if __name__ == '__main__':
    unittest.main()

