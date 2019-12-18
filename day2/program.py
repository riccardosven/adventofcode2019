def run(code, fix=False, in1=12, in2=2 ):
    code = [int(s) for s in code.split(",")]
    if fix:
        code[1] = in1
        code[2] = in2

    idx = 0

    while True:
        if idx < len(code) - 3:
            addr_op1 = code[idx+1]
            addr_op2 = code[idx+2]
            addr_res = code[idx+3]


            if code[idx] == 1:
                code[addr_res] = code[addr_op1] + code[addr_op2]
            elif code[idx] == 2:
                code[addr_res] = code[addr_op1] * code[addr_op2]
            else:
                raise Error("Wrong code")
            idx += 4

        if code[idx] == 99:
            return  code

def searchfor(code, value=19690720):
    for noun in range(99):
        for verb in range(99):
            out = run(code, fix=True, in1=noun, in2=verb)[0]
            if out == value:
                print(100*noun + verb)


def test(code, result):
    assert(','.join(map(str, run(code))) == result)

if __name__ == "__main__":
    if __debug__:
        test("1,0,0,0,99", "2,0,0,0,99")
        test("2,3,0,3,99","2,3,0,6,99")
        test("2,4,4,5,99,0","2,4,4,5,99,9801")
        test("1,1,1,4,99,5,6,0,99", "30,1,1,4,2,5,6,0,99")
    else:
        with open("input", "r") as fin:
            code = fin.readline()

        print(run(code, fix=True)[0])

        searchfor(code)


