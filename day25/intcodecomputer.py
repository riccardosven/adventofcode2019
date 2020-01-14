"Implementation of the elven intcode computer"
from collections import defaultdict, deque
from copy import copy


class InputNeeded(Exception):
    "Reached end of input queue"


class OutputReady(Exception):
    "Output available"


class CodeReturn(Exception):
    "Reached end of code"


class IntcodeComputer:
    "Elven intcode computer"

    def __init__(self, program):
        self.code = defaultdict(int, {i: int(s)
                                      for i, s in enumerate(program.split(","))})

        self.program = program
        self.pctr = 0
        self.relbase = 0
        self.inqueue = deque([])
        self.outqueue = deque([])

    @classmethod
    def from_file(cls, fname):
        "Create from file"
        with open(fname) as fhandle:
            return cls(fhandle.read())


    def reset(self):
        "Reset intcodecomputer"
        IntcodeComputer.__init__(self, self.program)

    def copy(self):
        "Deep copy of the intcode computer"
        other = IntcodeComputer(self.program)
        other.code = copy(self.code)
        other.pctr = self.pctr
        other.relbase = self.relbase

        return other

    def index(self, idx, mode=0):
        "Resolve indexing mode"
        if mode == 0:
            return self.code[idx]
        if mode == 1:
            return idx
        if mode == 2:
            return self.relbase + self.code[idx]
        raise Exception("Wrong mode parameter")

    def step(self):
        "Execute one instruction"
        instruction = self.code[self.pctr]
        mode, opcode = divmod(instruction, 100)
        mode, par1mode = divmod(mode, 10)
        mode, par2mode = divmod(mode, 10)
        mode, par3mode = divmod(mode, 10)

        op1 = self.code[self.index(self.pctr+1, par1mode)]
        op2 = self.code[self.index(self.pctr+2, par2mode)]

        if opcode == 1:
            # add
            res = op1 + op2
            self.code[self.index(self.pctr+3, par3mode)] = res
            self.pctr += 4

        elif opcode == 2:
            # mul
            res = op1 * op2
            self.code[self.index(self.pctr+3, par3mode)] = res
            self.pctr += 4

        elif opcode == 3:
            # input
            if not self.inqueue:
                raise InputNeeded
            val = self.inqueue.popleft()
            self.code[self.index(self.pctr+1, par1mode)] = val
            self.pctr += 2

        elif opcode == 4:
            # output
            self.outqueue.append(op1)
            self.pctr += 2
            raise OutputReady

        elif opcode == 5:
            # jump-if-true
            if not op1 == 0:
                self.pctr = op2
            else:
                self.pctr += 3

        elif opcode == 6:
            # jump if false
            if op1 == 0:
                self.pctr = op2
            else:
                self.pctr += 3

        elif opcode == 7:
            # less than
            res = int(op1 < op2)
            self.code[self.index(self.pctr+3, par3mode)] = res
            self.pctr += 4

        elif opcode == 8:
            # equals
            res = int(op1 == op2)
            self.code[self.index(self.pctr+3, par3mode)] = res
            self.pctr += 4

        elif opcode == 9:
            # increase relative base
            self.relbase += op1
            self.pctr += 2

        elif opcode == 99:
            raise CodeReturn

        else:
            raise Exception("Wrong code")

