import unittest
from unittest.mock import patch
from src.uvsim import UVSim
from src.model import DataModel
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# unit tests from milestone 3
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
        self.data_model.load_program('Test1.txt')
        self.assertEqual(self.data_model.get_instruction(0), 1007)

        # Test the modification of the accumulator and register
        self.data_model.set_accumulator(10)
        self.assertEqual(self.data_model.get_accumulator(), 10)
        self.data_model.set_instruction(0, 5000)
        self.assertEqual(self.data_model.get_instruction(0), 5000)

        # Test setting the entire instruction set
        self.data_model.set_instructions([1, 2, 3, 4, 5] + [0]*95)
        self.assertEqual(self.data_model.get_instructions(), [1, 2, 3, 4, 5] + [0]*95)


# unit tests from milestone 2
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



if __name__ == '__main__':
    unittest.main()

