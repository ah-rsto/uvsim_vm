"""UVSim.

DOCUMENT
"""

class UVSim:
    def __init__(self):
        self.memory = [0]*100
        self.accumulator = 0
        self.instruction_counter = 0
        self.instruction_register = 0
        self.operation_code = 0
        self.operand = 0

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
        
    def execute_program(self):
        while True:
            self.instruction_register = self.memory[self.instruction_counter]
            self.operation_code = abs(self.instruction_register) // 100
            self.operand = abs(self.instruction_register) % 100

            if self.operation_code == 10:  # w/ READ
                self.memory[self.operand] = int(input("Enter an integer from -9999 to +9999: "))
            elif self.operation_code == 11:  # WRITE
                print(self.memory[self.operand])
            elif self.operation_code == 20:  # LOAD
                self.accumulator = self.memory[self.operand]
            elif self.operation_code == 21:  # STORE
                self.memory[self.operand] = self.accumulator
            elif self.operation_code == 30:  # ADD
                self.accumulator += self.memory[self.operand]
            elif self.operation_code == 31:  # SUBTRACT
                self.accumulator -= self.memory[self.operand]
            elif self.operation_code == 32:  # DIVIDE
                self.accumulator //= self.memory[self.operand]
            elif self.operation_code == 33:  # MULTIPLY
                self.accumulator *= self.memory[self.operand]
            elif self.operation_code == 40:  # BRANCH
                self.instruction_counter = self.operand
                continue
            elif self.operation_code == 41:  # BRANCHNEG
                if self.accumulator < 0:
                    self.instruction_counter = self.operand
                    continue
            elif self.operation_code == 42:  # BRANCHZERO
                if self.accumulator == 0:
                    self.instruction_counter = self.operand
                    continue
            elif self.operation_code == 43:  # HALT
                print("Program execution completed.")
                break

            self.instruction_counter += 1


def main():
    """Main script driver."""
    #TODO: Validate request

    #TODO: Determine operation

    #TODO: Return result
    uv_sim = UVSim()
    uv_sim.load_program()
    uv_sim.execute_program()

    pass

if __name__ == "__main__":
    #TODO: Handle terminal calls

    main()
