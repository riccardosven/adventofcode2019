"IntcodeComputer with ASCII interface"

from intcodecomputer import IntcodeComputer, InputNeeded, OutputReady, CodeReturn


class ASCIIComputer(IntcodeComputer):
    "Intcodecomputer with ASCII interface"

    def __init__(self):
        with open("input") as fhandle:
            super().__init__(fhandle.readline())

    def run(self):
        "Run ASCII computer program"
        while True:
            try:
                self.step()
            except InputNeeded:
                instring = input()
                self.inqueue.extend(map(ord, instring))
                self.inqueue.append(10)
            except OutputReady:
                print(chr(self.outqueue.popleft()), end="")
            except CodeReturn:
                return
