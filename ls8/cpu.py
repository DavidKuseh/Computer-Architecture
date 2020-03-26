"""CPU functionality."""

import sys

LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.sp = 7
        self.op_pc = False
        self.branchtable = {}
        self.branchtable[LDI] = self.handle_LDI
        self.branchtable[PRN] = self.handle_PRN
        self.branchtable[HLT] = self.handle_HLT
        self.branchtable[MUL] = self.handle_MUL
        self.branchtable[PUSH] = self.handle_PUSH
        self.branchtable[POP] = self.handle_POP

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
            
            if ir in self.branchtable:
                self.branchtable[ir](operand_A, operand_B)
            else:
                print(f'Invalid instruction')
                sys.exit(1)
            
    
    def handle_LDI(self, operand_A, operand_B):
        self.reg[operand_A] = operand_B
        self.op_pc = False
        if not self.op_pc:
            self.pc += 3
            
    def handle_PRN(self, operand_A, operand_B):
        print(self.reg[operand_A])
        self.op_pc = False
        if not self.op_pc:
            self.pc += 2
            
    def handle_HLT(self, operand_A, operand_B):
        sys.exit()
            
    def handle_MUL(self, operand_A, operand_B):
        self.alu('MUL', operand_A, operand_B)
        self.op_pc = False
        if not self.op_pc:
            self.pc += 3
            
    def handle_PUSH(self, operand_A, operand_B):
        self.reg[self.sp] -= 1
        self.ram[self.reg[self.sp]] = self.reg[operand_A]
        self.op_pc = False
        if not self.op_pc:
            self.pc += 2
            
    def handle_POP(self, operand_A, operand_B):
        self.reg[operand_A] = self.ram_read(self.reg[self.sp])
        self.reg[self.sp] += 1
        self.op_pc = False
        if not self.op_pc:
            self.pc += 2
            
            
        


