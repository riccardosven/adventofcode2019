"Day 7: Amplification Circuit"

from itertools import permutations
from intcodecomputer import IntcodeComputer, OutputReady, CodeReturn


class Amplifiers:
    "Class for a cascade of amplifiers"

    def __init__(self, *, program, settings):
        self.computers = [IntcodeComputer(program)
                          for _ in range(len(settings))]
        for computer, setting in zip(self.computers, settings):
            computer.inqueue.append(setting)

    def run(self):
        "Run cascade"
        out = 0
        for computer in self.computers:
            computer.inqueue.append(out)
            try:
                while True:
                    computer.step()
            except OutputReady:
                out = computer.outqueue.pop()

        return out

    def runfeedback(self):
        "Run feedback loop"
        out = 0
        while True:
            for computer in self.computers:
                computer.stopped = False
                computer.inqueue.append(out)
                try:
                    while True:
                        computer.step()
                except OutputReady:
                    out = computer.outqueue.pop()
                except CodeReturn:
                    computer.stopped = True
            if self.computers[-1].stopped:
                break
        return out

    @staticmethod
    def optimize(program):
        "Return maximum amplifier output"
        best = 0
        for settings in permutations(range(5)):
            amplifier = Amplifiers(program=program, settings=settings)
            out = amplifier.run()
            if out > best:
                best = out
        return best

    @staticmethod
    def optimizefeedback(program):
        "Return maximum feedback output"
        best = 0
        for settings in permutations(range(5, 10)):
            amplifier = Amplifiers(program=program, settings=settings)
            out = amplifier.runfeedback()
            if out > best:
                best = out
        return best


def tests():
    "Basic testcases"
    programs = ["3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0",
                "3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0",
                "3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0"]
    settings = [[4, 3, 2, 1, 0],
                [0, 1, 2, 3, 4],
                [1, 0, 4, 3, 2]]
    outputs = [43210, 54321, 65210]

    for prog, sett, out in zip(programs, settings, outputs):
        amp = Amplifiers(program=prog, settings=sett)
        assert out == amp.run() == Amplifiers.optimize(prog)

    settings = [9, 8, 7, 6, 5]
    output = 139629729
    program = "3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5"

    ampli = Amplifiers(program=program, settings=settings)
    assert Amplifiers.optimizefeedback(
        program) == ampli.runfeedback() == output


def star1():
    "Solution to first star"
    with open("input") as fhandle:
        program = fhandle.read().strip()
    ampli = Amplifiers.optimize(program)
    print("Star 1:", ampli)


def star2():
    "Solution to second star"
    with open("input") as fhandle:
        program = fhandle.read().strip()
    ampli = Amplifiers.optimizefeedback(program)
    print("Star 2:", ampli)


if __name__ == "__main__":
    tests()
    star1()
    star2()
