"Day 2: 1202 Program Alarm"


def run(code, fix=False, in1=12, in2=2):
    "Run intcode program"
    code = [int(s) for s in code.strip().split(",")]
    if fix:
        code[1] = in1
        code[2] = in2

    idx = 0
    while True:
        addr_op1 = code[idx+1]
        addr_op2 = code[idx+2]
        addr_res = code[idx+3]

        if code[idx] == 1:  # Add
            code[addr_res] = code[addr_op1] + code[addr_op2]
        elif code[idx] == 2:  # Mul
            code[addr_res] = code[addr_op1] * code[addr_op2]
        else:
            raise Exception("Wrong code")
        idx += 4

        if code[idx] == 99:  # End
            return code



def searchfor(code, value=19690720):
    "Find inputs that yield the desired value"
    for noun in range(99):
        for verb in range(99):
            out = run(code, fix=True, in1=noun, in2=verb)[0]
            if out == value:
                return 100*noun + verb
    return None


def test(code, result):
    "Test program results"
    assert(','.join(map(str, run(code))) == result)


def star1():
    "Answer for first star"
    with open("input") as fhandle:
        code = fhandle.readline()
    print("Star 1:", run(code, fix=True)[0])


def star2():
    "Answer to second star"
    with open("input") as fhandle:
        code = fhandle.readline()
    print("Star 2:", searchfor(code))


if __name__ == "__main__":
    if __debug__:
        test("1,0,0,0,99", "2,0,0,0,99")
        test("2,3,0,3,99", "2,3,0,6,99")
        test("2,4,4,5,99,0", "2,4,4,5,99,9801")
        test("1,1,1,4,99,5,6,0,99", "30,1,1,4,2,5,6,0,99")

    star1()
    star2()
