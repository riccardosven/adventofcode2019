from intcodecomputer import IntcodeComputer
#from oldcomputer import intcodecomputer
from collections import namedtuple, defaultdict


DIRECTIONS = "<^>v"
#Position = namedtuple("Position", ["x", "y"])


class DummyBrain:
    def __init__(self, *args, **kwargs):
        self.instructions = [1, 0,
                             0, 0,
                             1, 0,
                             1, 0,
                             0, 1,
                             1, 0,
                             1, 0]

    def step(self, *args):
        try:
            return self.instructions.pop(0)
        except Exception:
            raise StopIteration


class Robot:

    def __init__(self, code="input"):
        self.pos = (0, 0)
        self.direction = 1  # "^"
        self.hull = defaultdict(int)
        with open(code, "r") as fin:
            program = "".join(fin.readlines())
        self.brain = IntcodeComputer(program)

    def step(self):
        "Input 0 if black or 1 if white output color to paint and new direction"
        col = self.hull[self.pos]

        self.hull[self.pos] = self.brain.step(col)

        clockwise = self.brain.step(col)
        if clockwise:
            self.direction = self.direction + 1 if self.direction < 3 else 0
        else:
            self.direction = self.direction - 1 if self.direction > 0 else 3

        direction = DIRECTIONS[self.direction]
        paintcol = "#" if self.hull[self.pos] else "."
        if direction == "<":
            self.pos = (self.pos[0] - 1, self.pos[1])
        elif direction == "^":
            self.pos = (self.pos[0], self.pos[1] - 1)
        elif direction == ">":
            self.pos = (self.pos[0] + 1, self.pos[1])
        elif direction == "v":
            self.pos = (self.pos[0], self.pos[1] + 1)

    def run(self):
        try:
            while True:
                self.step()
        except StopIteration:
            pass

    def onestep(self):
        col = "#" if self.hull[self.pos] else "."
        print(self.pos, col)
        self.step()
        self.render()

    def runstep(self):
        while True:
            self.onestep()
            input()

    def render(self, width=50, height=8, offset=1):
        field = [["x" for _ in range(width)] for _ in range(height)]
        for pos, col in self.hull.items():
            field[pos[1] + offset][pos[0] + offset] = '#' if col else "."
            if pos == self.pos:
                field[pos[1] + offset][pos[0] +
                                       offset] = DIRECTIONS[self.direction]

        print("\n".join(["".join(row) for row in field]))


def step1():
    print("Solving step 1")
    robot = Robot()
    robot.run()
    print(len(robot.hull))

def step2():
    print("Solving step 2")
    robot = Robot()
    robot = Robot()
    robot.hull[robot.pos] = 1
    robot.run()
    robot.render()


if __name__ == "__main__":
    step1()
    step2()
