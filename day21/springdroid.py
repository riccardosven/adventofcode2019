from intcodecomputer import IntcodeComputer
from itertools import product, combinations_with_replacement


instructions = """
NOT A J
NOT B T
AND T J
NOT C T
AND T J
AND D J
AND D J
AND D J
AND D J
AND D J
AND D J
AND D J
AND D J
AND D J
AND D J
WALK
"""


class SpringBot:
    def __init__(self, interactive=False):
        with open("input") as fhandle:
            self.cpu = IntcodeComputer("".join(fhandle.readlines()), interactive)
    
    def runprogram(self, instructions):
        self.cpu.reset()
        try:
            for char in instructions.strip():
                self.cpu.step(ord(char))
            while True:
                self.cpu.step(10)
        except StopIteration:
            pass
        
        return self.cpu.outval


def bfsolve():
    # nll three instructions, the second argument (Y) needs to be a writable
    # register (either T or J). The first argument (X) can be any register
    #(including A, B, C, or D)
    instructions = ["NOT",  "AND", "OR"]
    readable = "ABCDTJ"
    writable = "TJ"

    bot = SpringBot(True)
    bot.runprogram("NOT A J\nWALK\n")
    #optval = 0
    #for proglen in range(15):
    #    for program in combinations_with_replacement(product(instructions, readable, writable), proglen):
    #        optval += 1
            #program = "\n".join([" ".join(row) for row in program])
            #program = program + "\nWALK\n"
            #retval = bot.runprogram(program)
            #print(retval)
            #if not retval is None and retval > optval:
                #optval = retval
    #print(optval)

    #return optval


def main():
    # program = """
    # NOT A J
    # NOT B T
    # OR T J
    # NOT C T
    # OR T J
    # AND D J
    # WALK"""

    program1 = """
    NOT J T
    AND A T
    AND B T
    AND C T
    NOT T J
    AND D J
    WALK
    """

    program2 = """
    NOT J T
    AND A T
    AND B T
    AND C T
    NOT T J
    AND D J
    NOT J T
    OR E T
    OR H T
    AND T J
    RUN
    """

    bot = SpringBot()
    retval = bot.runprogram(program2)
    print(retval)

if __name__ == "__main__":
    main()



