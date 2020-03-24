"""CPU functionality."""

import sys

LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0

    # `ram_read()` should accept the address to read and return the value stored there  
    def ram_read(self, read_address):
        return self.ram[read_address]

    # `ram_write()` should accept a value to write, and the address to write it to
    def ram_write(self, write_address, write_value):
        self.ram[write_address] = write_value

    def load(self, filename):
        """Load a program into memory."""
        address = 0
        program = []
        
        try:
            with open(filename) as f:
                for line in f:
                    # split line before and after comment symbol
                    comment_split = line.split('#')
                    
                    # extract our number
                    num = comment_split[0].strip()
                    
                    if len(num) == 0:
                        continue 
                    
                    # convert our binary string to a number
                    value = int(num, 2)
                    program.append(f"{value:08b}")
                    
        except FileNotFoundError:
            print(f'{sys.argv[0]}: {sys.argv[1]} not found')
            sys.exit(2)
        
        for instruction in program:
            instruction = '0b' + instruction
            self.ram[address] = instruction
            self.ram[address] = int(instruction, 2)
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        
        else:
            raise Exception("Unsupported ALU operation")
        

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        while True:
            ir = self.ram[self.pc]
            operand_A = self.ram_read(self.pc + 1)
            operand_B = self.ram_read(self.pc + 2)
            
            if ir == LDI:
                # store the data
                self.reg[operand_A] = operand_B
                # increment the PC by 3 to skip the arguments
                self.pc += 3
                
            elif ir == PRN:
                # print
                print(self.reg[operand_A])
                # increment the PC by 2 to skip the argument
                self.pc += 2
            
            elif ir == HLT:
                sys.exit(1)
                
            elif ir == MUL:
                self.alu("MUL", operand_A, operand_B)
                self.pc += 3
                
            else:
                # print an Invalid Instruction message
                print("Invalid Instruction")
            
        


