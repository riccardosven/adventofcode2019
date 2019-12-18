def run(code, invalues=[1]):
    code = [int(s) for s in code.split(",")]

    idx = 0
    out = []

    while True:
        if idx < len(code):
            instruction = code[idx]
            mode, opcode = divmod(instruction, 100)
            mode, par1mode = divmod(mode, 10)
            mode, par2mode = divmod(mode, 10)
            mode, par3mode = divmod(mode, 10)

            if opcode == 1:
                # add
                op1 = code[idx+1] if par1mode else code[code[idx+1]]
                op2 = code[idx+2] if par2mode else code[code[idx+2]]
                res = op1 + op2
                if par3mode:
                    code[idx+3] = res
                else:
                    code[code[idx+3]] = res

                idx += 4
            elif opcode == 2:
                # mul
                op1 = code[idx+1] if par1mode else code[code[idx+1]]
                op2 = code[idx+2] if par2mode else code[code[idx+2]]
                res = op1 * op2
                if par3mode:
                    code[idx+3] = res
                else:
                    code[code[idx+3]] = res
                idx += 4
            elif opcode == 3:
                # input
                op1 = code[idx+1]
                val = invalues.pop(0)
                code[op1] = val
                idx += 2
            elif opcode == 4:
                # output
                op1 = code[idx+1] if par1mode else code[code[idx+1]]
                out.append(op1)
                idx += 2
            elif opcode == 5:
                # jump-if-true
                op1 = code[idx+1] if par1mode else code[code[idx+1]]
                op2 = code[idx+2] if par2mode else code[code[idx+2]]
                if not op1 == 0:
                    idx = op2
                else:
                    idx += 3
            elif opcode == 6:
                # jump if false
                op1 = code[idx+1] if par1mode else code[code[idx+1]]
                op2 = code[idx+2] if par2mode else code[code[idx+2]]
                if op1 == 0:
                    idx = op2
                else:
                    idx += 3
            elif opcode == 7:
                # less than
                op1 = code[idx+1] if par1mode else code[code[idx+1]]
                op2 = code[idx+2] if par2mode else code[code[idx+2]]
                res = int(op1 < op2)
                if par3mode:
                    code[idx+3] = res
                else:
                    code[code[idx+3]] = res
                idx += 4
            elif opcode == 8:
                # equals
                op1 = code[idx+1] if par1mode else code[code[idx+1]]
                op2 = code[idx+2] if par2mode else code[code[idx+2]]
                res = int(op1 == op2)
                if par3mode:
                    code[idx+3] = res
                else:
                    code[code[idx+3]] = res
                idx += 4
            else:
                raise Exception("Wrong code")

        if code[idx] == 99:
            return out, code


if __name__ == "__main__":
    if __debug__:
        print(run("1002,4,3,4,33"))
        print(run("1101,100,-1,4,0"))
        print(run("3,0,4,0,99", invalues=[2]))
        print(run("3,9,8,9,10,9,4,9,99,-1,8", invalues=[23]), "expect = 0")
        print(run("3,9,8,9,10,9,4,9,99,-1,8", invalues=[8]), "expect = 1")
        print(run("3,9,7,9,10,9,4,9,99,-1,8", invalues=[8]), "expect = 0")
        print(run("3,9,7,9,10,9,4,9,99,-1,8", invalues=[9]), "expect = 0")
        print(run("3,9,7,9,10,9,4,9,99,-1,8", invalues=[7]), "expect = 1")
        print(run("3,3,1108,-1,8,3,4,3,99", invalues=[8]), "expected = 1")
        print(run("3,3,1108,-1,8,3,4,3,99", invalues=[5]), "expected = 0")
        print(run("3,3,1107,-1,8,3,4,3,99", invalues=[6]), "expected = 1")
        print(run("3,3,1107,-1,8,3,4,3,99", invalues=[9]), "expected = 0")
        print(run("3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9", invalues=[0]), "expected = 0")
        print(run("3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9", invalues=[-23]), "expected = 1")
        print(run("3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99", invalues=[23]), "expected=1001")
        print(run("3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99", invalues=[8]), "expected=1000")
        print(run("3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99", invalues=[5]), "expected=999")

    else:
        with open("input", "r") as fin:
            out, code = run(fin.readline(), invalues=[5])
        
        print(out)
