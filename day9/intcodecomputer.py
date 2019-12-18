"Implementation of the elven intcode computer"
from collections import defaultdict


def intcodecomputer(program):
    "Elven intcode computer"

    code = defaultdict(int)
    for i, s in enumerate(program.split(",")):
        code[i] = int(s)

    pctr = 0
    relbase = 0

    def readparameter(idx, mode=0):
        "Decode parmode parameter"
        #validatecode(idx, mode)
        if mode == 0:
            return code[code[idx]]
        elif mode == 1:
            return code[idx]
        elif mode == 2:
            return code[relbase + code[idx]]
        else:
            raise Exception("Wrong mode parameter")

    def writeparameter(idx, val, mode=0):
        "Write parmode parameter"
        #validatecode(idx, mode)
        if mode == 0:
            code[code[idx]] = val
        elif mode == 1:
            code[idx] = val
        elif mode == 2:
            code[relbase + code[idx]] = val
        else:
            raise Exception("Wrong mode parameter")

    while True:
        instruction = code[pctr]
        mode, opcode = divmod(instruction, 100)
        mode, par1mode = divmod(mode, 10)
        mode, par2mode = divmod(mode, 10)
        mode, par3mode = divmod(mode, 10)

        #print(instruction, opcode, par1mode, par2mode, par3mode)

        if opcode == 1:
            # add
            op1 = readparameter(pctr+1, par1mode)
            op2 = readparameter(pctr+2, par2mode)
            res = op1 + op2
            writeparameter(pctr+3, res, par3mode)
            pctr += 4
        elif opcode == 2:
            # mul
            op1 = readparameter(pctr+1, par1mode)
            op2 = readparameter(pctr+2, par2mode)
            res = op1 * op2
            writeparameter(pctr+3, res, par3mode)
            pctr += 4
        elif opcode == 3:
            # input
            op1 = readparameter(pctr+1, 0)  # Index is always parameter
            val = yield
            print("input " + str(val))
            writeparameter(op1, val, par1mode)
            pctr += 2

        elif opcode == 4:
            # output
            op1 = readparameter(pctr+1, par1mode)
            print("output " + str(op1))
            yield op1
            pctr += 2

        elif opcode == 5:
            # jump-if-true
            op1 = readparameter(pctr+1, par1mode)
            op2 = readparameter(pctr+2, par2mode)
            if not op1 == 0:
                pctr = op2
            else:
                pctr += 3
        elif opcode == 6:
            # jump if false
            op1 = readparameter(pctr+1, par1mode)
            op2 = readparameter(pctr+2, par2mode)
            if op1 == 0:
                pctr = op2
            else:
                pctr += 3
        elif opcode == 7:
            # less than
            op1 = readparameter(pctr+1, par1mode)
            op2 = readparameter(pctr+2, par2mode)
            res = int(op1 < op2)
            writeparameter(pctr+3, res, par3mode)
            pctr += 4
        elif opcode == 8:
            # equals
            op1 = readparameter(pctr+1, par1mode)
            op2 = readparameter(pctr+2, par2mode)
            res = int(op1 == op2)
            writeparameter(pctr+3, res, par3mode)
            pctr += 4
        elif opcode == 9:
            # increase relative base
            op1 = readparameter(pctr+1, par1mode)
            relbase += op1
            pctr += 2

        elif opcode == 99:
            return
        else:
            raise Exception("Wrong code")
