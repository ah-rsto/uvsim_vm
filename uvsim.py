class Memory:
    def __init__(self):
        self.memory = [0]*100

    def load_program(self, filename):
        while True:
            try:
                # filename = input("Enter the name of the file to load: ")
                with open(filename, 'r') as f:
                    for location, line in enumerate(f):
                        self.memory[location] = int(line.strip())
                break
            except FileNotFoundError:
                print("File not found. Try again.")
        
    def read_memory(self, operand, read_callback):
        if read_callback:
            value = read_callback()
            if value < -9999 or value > 9999:
                raise ValueError("Invalid input. Try again.")
            self.memory[operand] = value
        else:
            print('No read callback set')

    def write_memory(self, operand, write_callback):
        if write_callback:
            write_callback(self.memory[operand])
        else:
            print(f'No write callback set - print to console: {self.memory[operand]}')

    def store_memory(self, operand, accumulator):
        self.memory[operand] = accumulator

    def load_memory(self, operand, accumulator):
        if operand < 0 or operand >= len(self.memory):
            raise IndexError(f"Memory index '{operand}' not in range.")
        accumulator = self.memory[operand]
        return accumulator

    
class ArithmeticUnit:
    def addition(self, operand, accumulator, memory):
        accumulator += memory[operand]
        return accumulator

    def subtraction(self, operand, accumulator, memory):
        accumulator -= memory[operand]
        return accumulator

    def multiplication(self, operand, accumulator, memory):
        if not isinstance(memory[operand], (int, float)):
            raise ValueError("Invalid operand: must be a number")
        result = accumulator * memory[operand]
        accumulator = result % 10000
        return accumulator

    def division(self, operand, accumulator, memory):
        if not isinstance(memory[operand], (int, float)):
            raise ValueError("Invalid operand: must be a number")
        if memory[operand] == 00:
            raise ValueError("Invalid operand: Cannot divide by 0")
        else:
            result = accumulator // memory[operand]
            accumulator = result % 10000
            return accumulator
        

class BranchUnit:
    def branch(self, operand, instruction_counter):
        if -2 < operand and operand < len(self.memory):
            instruction_counter = operand - 1
        else:
            raise IndexError(f"Memory index '{operand}' not in range.")
        return instruction_counter

    def branch_negative(self, operand, instruction_counter, accumulator):
        if accumulator < 0:
            if -2 < operand and operand < len(self.memory):
                instruction_counter = operand - 1
            else:
                raise IndexError(f"Memory index '{operand}' not in range.")
        return instruction_counter

    def branch_zero(self, operand, instruction_counter, accumulator):
        if accumulator == 0:
            if -2 < operand and operand < len(self.memory):
                instruction_counter = operand - 1
            else:
                raise IndexError(f"Memory index '{operand}' not in range.")
        return instruction_counter
    
    def halt(self, operand, instruction_counter, halted):
        instruction_counter = operand
        if halted:
            halted()
            return instruction_counter


# Team collaboration
class UVSim:
    def __init__(self, read_callback=None, write_callback=None, halted=None):
        # self.memory = [0]*100
        self.memory = Memory()
        self.arithmetic_unit = ArithmeticUnit()
        self.branch_unit = BranchUnit()
        self.accumulator = 0
        self.instruction_counter = 0
        self.instruction_register = 0
        self.operation_code = 0
        self.read_callback = read_callback
        self.write_callback = write_callback
        self.halted = halted
    
    def load_program(self, filename):
        self.memory.load_program(filename)

    # Team collaboration
    def execute_program(self):
        while True:
            self.instruction_register = self.memory.memory[self.instruction_counter]
            self.operation_code = abs(self.instruction_register) // 100
            operand = abs(self.instruction_register) % 100

            match self.operation_code:
                case 10:  # w/ READ
                    self.memory.read_memory(operand, self.read_callback)
                case 11: # WRITE
                    self.memory.write_memory(operand, self.write_callback)
                case 20: # LOAD
                    self.accumulator = self.memory.load_memory(operand, self.accumulator)
                case 21: # STORE
                    self.memory.store_memory(operand, self.accumulator)
                case 30: # ADD
                    self.accumulator = self.arithmetic_unit.addition(operand, self.accumulator, self.memory.memory)
                case 31: # SUBTRACT
                    self.accumulator = self.arithmetic_unit.subtraction(operand, self.accumulator, self.memory.memory)
                case 32: # DIVIDE
                    self.accumulator = self.arithmetic_unit.division(operand, self.accumulator, self.memory.memory)
                case 33: # MULTIPLY
                    self.accumulator = self.arithmetic_unit.multiplication(operand, self.accumulator, self.memory.memory)
                case 40: # BRANCH
                    self.instruction_counter = self.branch_unit.branch(operand, self.instruction_counter)
                case 41: # BRANCHNEG
                    self.instruction_counter = self.branch_unit.branch_negative(operand, self.instruction_counter, self.accumulator)
                case 42: # BRANCHZERO
                    self.instruction_counter = self.branch_unit.branch_zero(operand, self.instruction_counter, self.accumulator)
                case 43: # HALT
                    self.instruction_counter = self.branch_unit.halt(operand, self.instruction_counter, self.halted)
                    break
                case _:
                    print(
                        f"Invalid operation code '{self.operation_code}'. \n"
                        "Program terminated"
                    )
                    break
    
            self.instruction_counter += 1


# def main():
#     """Main script driver."""
#     uv_sim = UVSim()
#     uv_sim.load_program()
#     uv_sim.execute_program()

#     pass

# if __name__ == "__main__":
#     main()

