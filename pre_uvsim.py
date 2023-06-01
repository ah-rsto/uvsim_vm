"""DOCUMENT."""


import sys
#TODO: Add validation/exception handling
#TODO: Add documentation

class UVSim:
    def __init__(self):
        self.memory = [0]*100
        self.accumulator = 0
        self.instruction_counter = 0
        self.instruction_register = 0
        self.operation_code = 0
        self.operand = 0


    def load_program(self: object) -> None:
        """DOCUMENT."""
        while True:
            file_name = input("Enter the name of the file to load: ")
            try:
                with open(file_name, 'r', encoding="UTF-8") as fin:
                    for location, line in enumerate(fin):
                        self.memory[location] = int(line.strip())
                break
            except FileNotFoundError:
                #TODO: Error message too specific
                print("File not found. Try again.")

    '''
    def read_memory(self: object) -> None:
        """DOCUMENT."""
        self.accumulator = self.memory[self.operand]


    def write_memory(self: object) -> None:
        """DOCUMENT."""
        self.memory[self.operand] = self.accumulator


    def read_terminal(self: object) -> None:
        """DOCUMENT."""
        self.memory[self.operand] = int(input("Enter an integer from -9999 to +9999: "))


    def write_terminal(self: object) -> None:
        """DOCUMENT."""
        print(self.memory[self.operand])


    def check_result(self: object) -> None:
        """Validates the operation result value."""
        pass


    def addition(self: object) -> None:
        """DOCUMENT."""
        self.accumulator += self.memory[self.operand]


    def subtraction(self: object) -> None:
        """DOCUMENT."""
        self.accumulator -= self.memory[self.operand]
    '''

    def multiplication(self: object) -> None:
        """
        DOCUMENT. !!!!Cassidy
        MULTIPLY = 33 multiply a word from a specific location in memory to the word in the accumulator (leave the result in the accumulator).
        """
        # Check operand is a number
        if not isinstance(self.memory[self.operand], (int, float)):
            raise ValueError("Invalid operand: must be a number")

        #Calculate
        result = self.accumulator * self.memory[self.operand]
        #Truncate and store
        self.accumulator = result % 10000
        #self.accumulator *= self.memory[self.operand]

    def division(self: object) -> None:
        """
        DOCUMENT. !!!!Cassidy
        DIVIDE = 32 Divide the word in the accumulator by a word from a specific location in memory (leave the result in the accumulator).
        """
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

    '''
    def branch(self: object) -> None:
        """DOCUMENT."""
        self.instruction_counter = self.operand


    def branch_negative(self: object) -> None:
        """DOCUMENT."""
        self.instruction_counter = self.operand


    def branch_zero(self: object) -> None:
        """DOCUMENT."""
        self.instruction_counter = self.operand
    '''
    def halt(self: object) -> None:
        """
        DOCUMENT. !!!!Cassidy
        HALT = 43 Pause the program
        """
        self.instruction_counter = self.operand
        sys.exit("Program Halted")

    def execute_program(self: object) -> None:
        """Main script driver."""
        while True:
            print("hello")
            """
            !!!!CJ Needed for when done with program?
            or does the match loop do this automatically when the program ends?
            (not sure if this would work but just trying to clarify if we need something like this)
            if self.instruction_counter >= len(self.memory):
                break
            """

            self.instruction_register = self.memory[self.instruction_counter]
            self.operation_code = abs(self.instruction_register) // 100
            self.operand = abs(self.instruction_register) % 100

            #TODO: Check op value against possible option list to prevent infinite loop
            match self.operation_code:
                case 10:
                    self.read_terminal()
                case 11:
                    self.write_terminal()
                case 20:
                    self.read_memory()
                case 21:
                    self.write_memory()
                case 30:
                    self.addition()
                case 31:
                    self.subtraction()
                case 32:
                    self.division()
                case 33:
                    self.multiplication()
                case 40:
                    self.branch()
                    continue
                case 41:
                    if self.accumulator < 0:
                        self.branch_negative()
                        continue
                case 42:
                    if self.accumulator == 0:
                        self.branch_zero()
                        continue
                case 43:
                    #!!!!CJ call halt here or is robby wanting just this?
                    print("Program execution completed.") #robby wrote
                    # break inside of halt wouldn't work unless inside of loop.
                    break
                case _:
                    print(
                        f"Invalid operation code '{self.operation_code}'. \n"
                        "Program terminated"
                    )
                    break

            self.instruction_counter += 1


if __name__ == "__main__":
    #TODO: Add terminal run functionality, accept file as arg
    uv_sim = UVSim()
    uv_sim.load_program()
    uv_sim.execute_program()


