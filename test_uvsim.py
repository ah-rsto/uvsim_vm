"""
UVSim Unit Test Module.

Houses all the unittests for uvsim testing.
"""
import unittest
from pre_uvsim import UVSim
from unittest.mock import patch
import sys

class UnitTests(unittest.TestCase):

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
        """
        see https://docs.python.org/3/library/unittest.mock.html
        assert_called_once_with(*args, **kwargs)
        Assert that the mock was called exactly once and that call was with the specified arguments.
        """


        # check program was halted
        with patch.object(sys, "exit") as mock_exit:
            self.S.halt()
            mock_exit.assert_called_once_with("Program Halted")





if __name__ == '__main__':
    unittest.main()
