"Day 21: Springdroid Adventure"

from intcodecomputer import IntcodeComputer


class SpringBot:
    "Springdroid"
    def __init__(self, interactive=False):
        with open("input") as fhandle:
            self.cpu = IntcodeComputer(
                "".join(fhandle.readlines()), interactive)

    def runprogram(self, instructions):
        "Run instructions on cpu"
        self.cpu.reset()
        try:
            for char in instructions.strip():
                self.cpu.step(ord(char))
            while True:
                self.cpu.step(10)
        except StopIteration:
            pass

        return self.cpu.outval


def star1():
    "Solution to first star"

    program = """
    NOT J T
    AND A T
    AND B T
    AND C T
    NOT T J
    AND D J
    WALK
    """

    bot = SpringBot()
    retval = bot.runprogram(program)
    print("Star 1:", retval)

def star2():
    "Solution to second star"

    program = """
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
    retval = bot.runprogram(program)
    print("Star 2:", retval)


if __name__ == "__main__":
    star1()
    star2()
