from intcodecomputer import intcodecomputer

def testboost():
    with open('input', 'r') as fin:
        computer = intcodecomputer(fin.readline())
    next(computer)
    computer.send(1) # Test mode
    for c in computer:
        print(c)

def runboost():
    with open('input', 'r') as fin:
        computer = intcodecomputer(fin.readline())
    next(computer)
    computer.send(2) # Compute mode
    for c in computer:
        print(c)


def test(code, expect = ""):
    computer = intcodecomputer(code)
    for c in computer:
        print(c)
    if expect:
        print("(" + expect +")")


def test1():
    pass
    #computer = intcodecomputer("109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99")
    #computer = intcodecomputer("1102,34915192,34915192,7,4,7,99,0")
    #= intcodecomputer("104,1125899906842624,99", expect)

if __name__ == "__main__":
    if __debug__:
        test("109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99")
        #computer = intcodecomputer("1102,34915192,34915192,7,4,7,99,0")
        test("1102,34915192,34915192,7,4,7,99,0")
        test("104,1125899906842624,99", expect="1125899906842624")
    else:
        testboost()
        runboost()



