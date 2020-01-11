from intcodecomputer import intcodecomputer

def testboost():
    with open('input', 'r') as fin:
        computer = intcodecomputer(fin.readline())
    next(computer)
    for c in computer:
        print(c)

def runboost(test=True):
    with open('input', 'r') as fin:
        computer = intcodecomputer(fin.readline())
    next(computer)
    if test:
        output = computer.send(1) # Test mode
    else:
        output = computer.send(2) # Compute mode

    return str(output)



def tests():
    program1 = "109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99"
    for c,val in zip(intcodecomputer(program1), program1.split(',')):
        assert str(c) == val

    assert len(str(next(intcodecomputer("1102,34915192,34915192,7,4,7,99,0")))) == 16
    assert next(intcodecomputer("104,1125899906842624,99")) == 1125899906842624

if __name__ == "__main__":
    tests()
    print("Start 1:", runboost())
    print("Start 2:", runboost(False))



