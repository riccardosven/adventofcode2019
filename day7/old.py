"Implemtation of the elven intcode computer"

def intcodecomputer(program):

    code = [int(s) for s in program.split(",")]
    pctr = 0

    while True:
        instruction = code[pctr]
        mode, opcode = divmod(instruction, 100)
        mode, par1mode = divmod(mode, 10)
        mode, par2mode = divmod(mode, 10)
        mode, par3mode = divmod(mode, 10)

        if opcode == 1:
            # add
            op1 = code[pctr+1] if par1mode else code[code[pctr+1]]
            op2 = code[pctr+2] if par2mode else code[code[pctr+2]]
            res = op1 + op2
            if par3mode:
                code[pctr+3] = res
            else:
                code[code[pctr+3]] = res
            pctr += 4
        elif opcode == 2:
            # mul
            op1 = code[pctr+1] if par1mode else code[code[pctr+1]]
            op2 = code[pctr+2] if par2mode else code[code[pctr+2]]
            res = op1 * op2
            if par3mode:
                code[pctr+3] = res
            else:
                code[code[pctr+3]] = res
            pctr += 4

        elif opcode == 3:
            # input
            op1 = code[pctr+1]
            val = yield
            code[op1] = val
            pctr += 2

        elif opcode == 4:
            # output
            op1 = code[pctr+1] if par1mode else code[code[pctr+1]]
            yield op1
            pctr += 2

        elif opcode == 5:
            # jump-if-true
            op1 = code[pctr+1] if par1mode else code[code[pctr+1]]
            op2 = code[pctr+2] if par2mode else code[code[pctr+2]]
            if not op1 == 0:
                pctr = op2
            else:
                pctr += 3
        elif opcode == 6:
            # jump if false
            op1 = code[pctr+1] if par1mode else code[code[pctr+1]]
            op2 = code[pctr+2] if par2mode else code[code[pctr+2]]
            if op1 == 0:
                pctr = op2
            else:
                pctr += 3
        elif opcode == 7:
            # less than
            op1 = code[pctr+1] if par1mode else code[code[pctr+1]]
            op2 = code[pctr+2] if par2mode else code[code[pctr+2]]
            res = int(op1 < op2)
            if par3mode:
                code[pctr+3] = res
            else:
                code[code[pctr+3]] = res
            pctr += 4
        elif opcode == 8:
            # equals
            op1 = code[pctr+1] if par1mode else code[code[pctr+1]]
            op2 = code[pctr+2] if par2mode else code[code[pctr+2]]
            res = int(op1 == op2)
            if par3mode:
                code[pctr+3] = res
            else:
                code[code[pctr+3]] = res
            pctr += 4
        elif code[pctr] == 99:
            return 
        else:
            raise Exception("Wrong code")
