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
            
            
if __name__ == '__main__':
    unittest.main()
