"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    global instructions
    instructions = {
        1 : "HLT",
        17: "RET",
        69 : "PUSH",
        70 : "POP",
        71 : "PRN",
        80 : "CALL",
        84 : "JMP",
        85 : "JEQ",
        86 : "JNE",
        130 : "LDI",
        160 : "ADD",
        162 : "MUL",
        167 : "CMP"
    }

    global branch_table
    branch_table = {}

    # global IR
    # IR = 0

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0]*256
        self.register = [0]*8
        self.IR = 0
        self.SP = 255
        self.FL = '00000000'
        # self.E = 0
        # self.L = 0
        # self.G = 0

        

    
    def handle_hlt(self):
        sys.exit()
    
    branch_table[instructions[1]] =  handle_hlt

    
    def handle_ldi(self, op1, op2):
        self.register[op1] = op2
        self.IR+=3
        
    branch_table[instructions[130]] = handle_ldi

    
    def handle_prn(self, op1):
        val = self.register[op1]
        print(val)
        self.IR += 2
        
    branch_table[instructions[71]] = handle_prn

    
    def handle_mul(self, op1, op2):
        val1 = self.register[op1]
        val2 = self.register[op2]
        val3 = val1 * val2
        self.register[op1] = val3
        self.IR +=3

    branch_table[instructions[162]] = handle_mul

    def handle_push(self, op1):
        self.SP -= 1
        val = self.register[op1]
        self.ram[self.SP] = val
        self.IR +=2

    branch_table[instructions[69]] = handle_push

    def handle_pop(self, op1):
        val = self.ram[self.SP]
        self.register[op1] = val
        self.SP += 1
        self.IR += 2

    branch_table[instructions[70]] = handle_pop

    def handle_call(self, op1):
        next_instruct = self.IR + 2
        self.SP -= 1
        self.ram[self.SP] = next_instruct
        self.IR = self.register[op1]

    branch_table[instructions[80]] = handle_call

    def handle_ret(self):
        next_instruct = self.ram[self.SP]
        self.SP += 1
        self.IR = next_instruct

    branch_table[instructions[17]] = handle_ret

    def handle_add(self, op1, op2):
        val1 = self.register[op1]
        val2 = self.register[op2]
        val3 = val1 + val2
        self.register[op1] = val3
        self.IR +=3

    branch_table[instructions[160]] = handle_add

    def handle_jmp(self, op1):
        address = self.register[op1]
        self.IR = address

    branch_table[instructions[84]] = handle_jmp

    def handle_jne(self, op1):
        fl = self.FL
        e_flag = fl[-1]
        fle_int = int(e_flag)
        if not fle_int:
            self.IR = self.register[op1]
        else:
            self.IR += 2

    branch_table[instructions[86]] = handle_jne

    def handle_jeq(self, op1):
        fl = self.FL
        e_flag = fl[-1]
        fle_int = int(e_flag)
        if fle_int:
            self.IR = self.register[op1]
        else:
            self.IR += 2

    branch_table[instructions[85]] = handle_jeq

    def handle_cmp(self, op1, op2):
        val1 = self.register[op1]
        val2 = self.register[op2]
        fl = self.FL
        
        if val1 == val2:
            leading = fl[:7]
            E = '1'
            self.FL = leading + E
        
        elif val1 < val2:
            leading = fl[:5]
            end = fl[6:]
            L = '1'
            self.FL = leading + L + end
        
        elif val1 > val2:
            leading = fl[:6]
            end = fl[7]
            G = '1'
            self.FL = leading + G + end

        self.IR += 3

    branch_table[instructions[167]] = handle_cmp

    def load(self):
        """Load a program into memory."""
        
        if len(sys.argv) != 2:
            print("Usage: <file.py> filename", file=sys.stderr)
            sys.exit(1)
        
        try:
            address = 0

            with open(sys.argv[1]) as f:
                for line in f:

                    #ignore comments
                    split_comments = line.split("#")
                    instruct = split_comments[0].split()
                    # print('instruct', instruct)

                    #ignore blank lines
                    if instruct == []:
                        continue

                    #print(instruct)
                    value = int(instruct[0],2)
                    # print('val', value)
                    

                    self.ram[address] = value
                    address +=1
        except FileNotFoundError:
            print(f"{sys.argv[0]}: {sys.argv[1]} not found")
            sys.exit(2)




        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
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

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value

    def run(self):
        """Run the CPU."""
        # global IR
        # IR = self.pc

        #load 8 into register 0
        # print register 0
        #halt

        running = True
        while running:
            #print(self.ram)
            command = self.ram[self.IR]
            #print('this',command)
            cmnd = instructions[command]
            if cmnd == 'HLT':
                running = False
                continue
            func = branch_table[cmnd]

            #number of instructions
            byte_string = f'{command:b}'
            if len(byte_string) < 8:
                byte_string = byte_string.rjust(8,'0')
            # print(byte_string)
            slice_of_instructs = byte_string[:2]
            # print(slice_of_instructs)
            num_of_instructs = int(slice_of_instructs,2)
            # print(cmnd, num_of_instructs)
            
            if num_of_instructs == 2:
                operand_a = self.ram_read(self.IR+1)
                operand_b = self.ram_read(self.IR+2)
                func(self, operand_a, operand_b)
                continue

            if num_of_instructs == 1:
                operand_a = self.ram_read(self.IR+1)
                func(self, operand_a)
                continue

            if num_of_instructs == 0:
                func(self)
                continue

            
            
            # if cmnd == "LDI": # load LDI
                
            #     load_reg = operand_a # register to load
            #     val = operand_b # value to insert

            #     self.register[load_reg] = val
            #     IR+=3
            #     continue
            
            # elif cmnd == "PRN": # print code
            #     reg_to_print = operand_a # register value is to be printed from
            #     val_to_print = self.register[reg_to_print] # value from register
            #     print(val_to_print) # 
            #     IR+=2
            #     continue

            # elif cmnd == "MUL":
            #     val1 = self.register[operand_a]
            #     val2 = self.register[operand_b]
            #     val3 = val1 * val2
            #     self.register[operand_a] = val3
            #     IR+=3
            #     continue


            # elif cmnd == "HLT": # halt
            #     sys.exit()
