from intcodecomputer import IntcodeComputer
from collections import defaultdict


DIRECTIONS = "<^>v"


class Robot:
    "Hull painting robot"

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
        if direction == "<":
            self.pos = (self.pos[0] - 1, self.pos[1])
        elif direction == "^":
            self.pos = (self.pos[0], self.pos[1] - 1)
        elif direction == ">":
            self.pos = (self.pos[0] + 1, self.pos[1])
        elif direction == "v":
            self.pos = (self.pos[0], self.pos[1] + 1)

    def run(self):
        "Run robot"
        try:
            while True:
                self.step()
        except StopIteration:
            pass

    def render(self, width=43, height=6, offset=0):
        "Show painted surface"
        field = [["x" for _ in range(width)] for _ in range(height)]
        for pos, col in self.hull.items():
            field[pos[1] + offset][pos[0] + offset] = '#' if col else "."
            if pos == self.pos:
                field[pos[1] + offset][pos[0] +
                                       offset] = DIRECTIONS[self.direction]

        print("\n".join(["".join(row) for row in field]))


def step1():
    "Solution to first star"
    robot = Robot()
    robot.run()
    print("Star 1:", len(robot.hull))


def step2():
    "Solution to second star"
    robot = Robot()
    robot.hull[robot.pos] = 1  # Start on white panel
    robot.run()
    print("Star 2:")
    robot.render()


if __name__ == "__main__":
    step1()
    step2()
