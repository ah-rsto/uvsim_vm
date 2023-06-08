"""UVSim.

DOCUMENT
"""

import sys


# Team collaboration
class UVSim:
    def __init__(self):
        self.memory = [0]*100
        self.accumulator = 0
        self.instruction_counter = 0
        self.instruction_register = 0
        self.operation_code = 0
        self.operand = 0


    # Team collaboration
    def load_program(self):
        while True:
            file_name = input("Enter the name of the file to load: ")
            try:
                with open(file_name, 'r') as f:
                    for location, line in enumerate(f):
                        self.memory[location] = int(line.strip())
                break
            except FileNotFoundError:
                print("File not found. Try again.")


    # Taylie's code
    def read_memory(self):
        while True:
            try:
                value = int(input("Enter an integer from -9999 to +9999: "))
                if value < -9999 or value > 9999:
                    raise ValueError
                self.memory[self.operand] = value
                break
            except ValueError:
                print("Invalid input. Try again.")


    # Taylie's code
    def write_memory(self):
        print(self.memory[self.operand])


    # Taylie's code
    def store_memory(self):
        self.memory[self.operand] = self.accumulator


    # Taylie's code
    def load_memory(self):
        self.accumulator = self.memory[self.operand]


    #Aubrey's code
    def addition(self):
        self.accumulator += self.memory[self.operand]

    #Aubrey's code
    def subtraction(self):
        self.accumulator -= self.memory[self.operand]

        
    # Cassidy's code
    def multiplication(self: object) -> None:
        """DOCUMENT."""
        # Check operand is a number
        if not isinstance(self.memory[self.operand], (int, float)):
            raise ValueError("Invalid operand: must be a number")

        #Calculate
        result = self.accumulator * self.memory[self.operand]
        #Truncate and store
        self.accumulator = result % 10000
        #self.accumulator *= self.memory[self.operand]


    # Cassidy's code
    def division(self: object) -> None:
        """DOCUMENT."""
        # Check operand is a number
        if not isinstance(self.memory[self.operand], (int, float)):
            raise ValueError("Invalid operand: must be a number")
        # Check operand is not 0
        if self.memory[self.operand] == 00:
            raise ValueError("Invalid operand: Cannot divide by 0")
        else:
            #self.accumulator //= self.memory[self.operand]
            #Calculate
            result = self.accumulator // self.memory[self.operand]
            #Truncate and store
            self.accumulator = result % 10000


    # Cassidy's code
    def halt(self: object) -> None:
        """DOCUMENT."""
        self.instruction_counter = self.operand
        sys.exit("Program Halted")


    # Robby's code
    def branch(self: object) -> None:
        """DOCUMENT."""
        match (-2 < self.operand and self.operand < len(self.memory)):
            case True: self.instruction_counter = self.operand - 1
            case False: 
                raise IndexError(f"Memory index '{self.operand}' not in range.")


    # Robby's code
    def branch_negative(self: object) -> None:
        """DOCUMENT."""
        if self.accumulator < 0:
            match (-2 < self.operand and self.operand < len(self.memory)):
                case True: self.instruction_counter = self.operand - 1
                case False: 
                    raise IndexError(f"Memory index '{self.operand}' not in range.")


    # Robby's code
    def branch_zero(self: object) -> None:
        """DOCUMENT."""
        if self.accumulator == 0:
            match (-2 < self.operand and self.operand < len(self.memory)):
                case True: self.instruction_counter = self.operand - 1
                case False: 
                    raise IndexError(f"Memory index '{self.operand}' not in range.")


    # Team collaboration
    def execute_program(self):
        while True:
            self.instruction_register = self.memory[self.instruction_counter]
            self.operation_code = abs(self.instruction_register) // 100
            self.operand = abs(self.instruction_register) % 100

            match self.operation_code:
                case 10:  # w/ READ
                    self.read_memory()
                case 11: # WRITE
                    self.write_memory()
                case 20: # LOAD
                    self.load_memory()
                case 21: # STORE
                    self.store_memory()
                case 30: # ADD
                    self.addition()
                    # self.accumulator += self.memory[self.operand]
                case 31: # SUBTRACT
                    self.subtraction()
                    # self.accumulator -= self.memory[self.operand]
                case 32: # DIVIDE
                    self.division()
                    # self.accumulator //= self.memory[self.operand]
                case 33: # MULTIPLY
                    self.multiplication()
                    # self.accumulator *= self.memory[self.operand]
                case 40: # BRANCH
                    self.branch()
                    # self.instruction_counter = self.operand
                    continue
                case 41: # BRANCHNEG
                    self.branch_negative()
                    # self.instruction_counter = self.operand
                    continue
                case 42: # BRANCHZERO
                    self.branch_zero()
                    # self.instruction_counter = self.operand
                    continue
                case 43: # HALT
                    self.halt()
                    break
                case _:
                    print(
                        f"Invalid operation code '{self.operation_code}'. \n"
                        "Program terminated"
                    )
                    break

            self.instruction_counter += 1


def main():
    """Main script driver."""
    uv_sim = UVSim()
    uv_sim.load_program()
    uv_sim.execute_program()

    pass

if __name__ == "__main__":
    main()
