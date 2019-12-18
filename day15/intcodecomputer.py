"Implementation of the elven intcode computer"
from collections import defaultdict
from copy import deepcopy


class IntcodeComputer:

    def __init__(self, program, interactive=False):
        "Elven intcode computer"
        self.code = defaultdict(int)
        for i, s in enumerate(program.split(",")):
            self.code[i] = int(s)

        self.program = program
        self.pctr = 0
        self.relbase = 0
        self.input = 0
        self.interactive = interactive
    
    def copy(self):
        "Deep copy of the intcode computer"
        other = IntcodeComputer(self.program)
        other.code = deepcopy(self.code)
        other.pctr = self.pctr
        other.relbase = self.relbase
        other.input = self.input
        other.interactive = self.interactive

        return other

    def readparameter(self, idx, mode=0):
        "Decode parmode parameter"
        #validatecode(idx, mode)
        if mode == 0:
            return self.code[self.code[idx]]
        elif mode == 1:
            return self.code[idx]
        elif mode == 2:
            return self.code[self.relbase + self.code[idx]]
        else:
            raise Exception("Wrong mode parameter")

    def writeparameter(self, idx, val, mode=0):
        "Write parmode parameter"
        #validatecode(idx, mode)
        if mode == 0:
            self.code[self.code[idx]] = val
        elif mode == 1:
            self.code[idx] = val
        elif mode == 2:
            self.code[self.relbase + self.code[idx]] = val
        else:
            raise Exception("Wrong mode parameter")

    def step(self, invalue):
        while True:
            instruction = self.code[self.pctr]
            mode, opcode = divmod(instruction, 100)
            mode, par1mode = divmod(mode, 10)
            mode, par2mode = divmod(mode, 10)
            mode, par3mode = divmod(mode, 10)

            #print(instruction, opcode, par1mode, par2mode, par3mode)

            if opcode == 1:
                # add
                op1 = self.readparameter(self.pctr+1, par1mode)
                op2 = self.readparameter(self.pctr+2, par2mode)
                res = op1 + op2
                self.writeparameter(self.pctr+3, res, par3mode)
                self.pctr += 4
            elif opcode == 2:
                # mul
                op1 = self.readparameter(self.pctr+1, par1mode)
                op2 = self.readparameter(self.pctr+2, par2mode)
                res = op1 * op2
                self.writeparameter(self.pctr+3, res, par3mode)
                self.pctr += 4
            elif opcode == 3:
                # input
                op1 = self.readparameter(self.pctr+1, par1mode)
                val = invalue
                self.writeparameter(self.pctr+1, val, par1mode)
                op1 = self.readparameter(self.pctr+1, par1mode)
                self.pctr += 2

            elif opcode == 4:
                # output
                op1 = self.readparameter(self.pctr+1, par1mode)
                self.pctr += 2
                return op1

            elif opcode == 5:
                # jump-if-true
                op1 = self.readparameter(self.pctr+1, par1mode)
                op2 = self.readparameter(self.pctr+2, par2mode)
                if not op1 == 0:
                    self.pctr = op2
                else:
                    self.pctr += 3
            elif opcode == 6:
                # jump if false
                op1 = self.readparameter(self.pctr+1, par1mode)
                op2 = self.readparameter(self.pctr+2, par2mode)
                if op1 == 0:
                    self.pctr = op2
                else:
                    self.pctr += 3
            elif opcode == 7:
                # less than
                op1 = self.readparameter(self.pctr+1, par1mode)
                op2 = self.readparameter(self.pctr+2, par2mode)
                res = int(op1 < op2)
                self.writeparameter(self.pctr+3, res, par3mode)
                self.pctr += 4
            elif opcode == 8:
                # equals
                op1 = self.readparameter(self.pctr+1, par1mode)
                op2 = self.readparameter(self.pctr+2, par2mode)
                res = int(op1 == op2)
                self.writeparameter(self.pctr+3, res, par3mode)
                self.pctr += 4
            elif opcode == 9:
                # increase relative base
                op1 = self.readparameter(self.pctr+1, par1mode)
                self.relbase += op1
                self.pctr += 2

            elif opcode == 99:
                raise StopIteration
            else:
                raise Exception("Wrong code")
