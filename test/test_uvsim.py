import unittest
from uvsim import UVSim

class TestLoadProgram(unittest.TestCase):
    def test_load_program_valid_file(self):
        uvsim = UVSim()
        uvsim.load_program("Test1.txt")
        expected_memory = [+1007, +1008, +2007, +2008, +2109, +1109, +4300, +0000, +0000, +0000, -99999] # instructions in the file
        self.assertEqual(uvsim.memory, expected_memory)

    def test_load_program_invalid_file(self):
        uvsim = UVSim()
        with self.assertRaises(ValueError):
            # Create this invalid file
            uvsim.load_program("invalid_program.txt")

class TestExecuteProgram(unittest.TestCase):
    # create a test for each opcode
    def test_opcode_10(self):
        uvsim = UVSim()
        uvsim.memory[0] = 1007
        uvsim.execute_program()
        self.assertEqual(uvsim.memory[7], 7)

    def test_opcode_11(self):
        uvsim = UVSim()
        uvsim.memory[0] = 1107
        uvsim.execute_program()
        self.assertEqual(uvsim.output, [7])

    def test_opcode_20(self):
        uvsim = UVSim()
        uvsim.memory[0] = 2007
        uvsim.execute_program()
        self.assertEqual(uvsim.accumulator, 7)

    def test_opcode_21(self):
        uvsim = UVSim()
        uvsim.accumulator = 7
        uvsim.memory[0] = 2108
        uvsim.execute_program()
        self.assertEqual(uvsim.memory[8], 7)

    def test_opcode_30(self):
        uvsim = UVSim()
        uvsim.accumulator = 7
        uvsim.memory[0] = 3008
        uvsim.execute_program()
        self.assertEqual(uvsim.accumulator, 15)

    def test_opcode_31(self):
        uvsim = UVSim()
        uvsim.accumulator = 7
        uvsim.memory[0] = 3108
        uvsim.execute_program()
        self.assertEqual(uvsim.accumulator, -1)

    def test_opcode_32(self):
        uvsim = UVSim()
        uvsim.accumulator = 7
        uvsim.memory[0] = 3208
        uvsim.execute_program()
        self.assertEqual(uvsim.accumulator, 1)

    def test_opcode_33(self):
        uvsim = UVSim()
        uvsim.accumulator = 7
        uvsim.memory[0] = 3308
        uvsim.execute_program()
        self.assertEqual(uvsim.accumulator, 56)

    def test_opcode_40(self):
        uvsim = UVSim()
        uvsim.memory[0] = 4007
        uvsim.execute_program()
        self.assertEqual(uvsim.pc, 7)

    def test_opcode_41(self):
        uvsim = UVSim()
        uvsim.accumulator = -1
        uvsim.memory[0] = 4107
        uvsim.execute_program()
        self.assertEqual(uvsim.pc, 7)

    def test_opcode_42(self):
        uvsim = UVSim()
        uvsim.accumulator = 0
        uvsim.memory[0] = 4207
        uvsim.execute_program()
        self.assertEqual(uvsim.pc, 7)

    def test_opcode_43(self):
        uvsim = UVSim()
        uvsim.memory[0] = 4307
        uvsim.execute_program()
        self.assertEqual(uvsim.pc, 1)



if __name__ == '__main__':
    unittest.main()

