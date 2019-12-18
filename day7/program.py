from itertools import permutations 
from intcodecomputer import intcodecomputer
from old import intcodecomputer as oldcomputer

def runamplifiers(settings=[], program=None):
    if not program:
        with open("input", "r") as fin:
            program = fin.readline()


    computers = [intcodecomputer(program) for _ in range(len(settings))]
    for computer in computers:
        next(computer)

    out = 0
    for setting, computer in zip(settings, computers):
        computer.send(setting)
        out = computer.send(out)

    return out

def testsettings(program):
    bestout = 0
    bestsettings = []
    for settings in permutations(range(5)):
        out = runamplifiers(program=program,settings=settings)
        if out > bestout:
            bestout = out
            bestsettings = settings
    print(bestout)

def testfeedbacksettings(program):
    bestout = 0
    bestsettings = []
    for settings in permutations(range(5,10)):
        out = runfeedbackloop(program=program,settings=settings)
        if out > bestout:
            bestout = out
            bestsettings = settings
    print(bestout)

def runfeedbackloop(settings=[], program=None):
    if not program:
        with open("input", "r") as fin:
            program = fin.readline()

    computers = [intcodecomputer(program) for _ in range(len(settings))]
    for computer in computers:
        next(computer)

    out = 0
    i = 0
    
    allhalt = True
    while True:
        if i == 0:
            allhalt = True
        try:
            computers[i].send(settings[i])
            out = computers[i].send(out)
            allhalt = False
        except StopIteration:
            pass
        if allhalt:
            return out

        i = (i + 1) % len(computers)



if __name__ == "__main__":
    if __debug__:

        #computer = intcodecomputer("00101,4,7,0,4,0,99,9")

        #runamplifiers(program="3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0", settings=[4,3,2,1,0])
        testsettings("3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0")
        testsettings("3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0")
        testsettings("3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0")

        print(runfeedbackloop(settings=[ 9,8,7,6,5], program
        ="3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5"), 139629729)
        print(runfeedbackloop(settings=[9,7,8,5,6], program =
            "3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10"), 18216)


    else:
        with open("input", "r") as fin:
            testfeedbacksettings(fin.readline())
