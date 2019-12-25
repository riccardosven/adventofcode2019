from intcodecomputer import IntcodeComputer

def ASCIIComputer:
    def __init__(self):
        with open("input") as fhandle:
            self.cpu = IntcodeComputer(fhandle.readline())
        
    def step(self):
        line = input()
        for letter in line: