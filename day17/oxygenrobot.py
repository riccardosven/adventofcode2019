from intcodecomputer import IntcodeComputer
from copy import deepcopy
from collections import deque
from time import sleep
import pickle

NORTH = 1
SOUTH = 2
WEST = 3
EAST = 4


def peek(pos, direction):
    if direction == NORTH:
        return (pos[0], pos[1] - 1)
    elif direction == SOUTH:
        return (pos[0], pos[1] + 1)
    elif direction == EAST:
        return (pos[0] + 1, pos[1])
    elif direction == WEST:
        return (pos[0] - 1, pos[1])
    else:
        raise Exception("Bad move command")


class Robot:

    def __init__(self, program="input", map=None):
        with open(program, 'r') as fin:
            program = "".join(fin.readlines())
        self.brain = IntcodeComputer(program)
        self.pos = (0, 0)
        self.map = dict() if map is None else map
        self.map[self.pos] = "."

    def copy(self):
        other = Robot()
        other.brain = self.brain.copy()
        other.pos = deepcopy(self.pos)
        other.map = deepcopy(self.map)

        return other

    def explored(self, direction):
        if peek(self.pos, direction) in self.map:
            return True
        return False

    def move(self, direction):
        self.pos = peek(self.pos, direction)

    def step(self, direction):
        retval = self.brain.step(direction)
        oldpos = self.pos
        self.move(direction)
        if retval == 0:
            self.map[self.pos] = "#"
            self.pos = oldpos
        elif retval == 1:
            self.map[self.pos] = "."
        elif retval == 2:
            self.map[self.pos] = "O"
        else:
            raise Exception("Error in step")

    def show(self, offset=20):
        printmap = deepcopy(self.map)
        printmap[self.pos] = "X"
        render(printmap, offset=offset)


def render(mapdict, width=40, height=40, offset=20):
    plot = [[' ' for _ in range(width)] for _ in range(height)]
    for coord, val in mapdict.items():
        plot[coord[1] + offset][coord[0] + offset] = val
    print("\n".join(["".join(row) for row in plot]))


def maparea():
    outermap = dict()
    robots = deque()
    robots.append((Robot(map=outermap), []))

    while robots:
        robot, steps = robots.popleft()
        for direction in [NORTH, SOUTH, EAST, WEST]:
            if robot.explored(direction):
                continue
            newbot = robot.copy()
            newbot.map = outermap
            newbot.step(direction)
            if newbot.map[newbot.pos] == "O":
                stepsout = steps + [direction]
            robots.append((newbot, steps + [direction]))

    return outermap, stepsout

def execute(steps):
    robot = Robot()
    for step in steps:
        robot.step(step)
    print(robot.map[robot.pos])

def step1():
    area, steps = maparea()
    robot = Robot()
    for step in steps:
        robot.step(step)
    assert area[robot.pos] == "O"
    render(area)
    print("Steps taken to reach oxygen tank:", len(steps))
    with open("step1.pickle", "wb") as handle:
        pickle.dump(area, handle)
        pickle.dump(robot.pos, handle)

def step2():
    with open("step1.pickle", "rb") as handle:
        area = pickle.load(handle)
        oxygenpos = pickle.load(handle)

    queue = deque()
    queue.append((oxygenpos, 0))
    maxtime = 0
    while queue:
        pos, time = queue.popleft()
        for direction in [NORTH, SOUTH, EAST, WEST]:
            newpos = peek(pos, direction)
            if area[newpos] == ".":
                area[newpos] = "O"
                maxtime = max(maxtime, time+1)
                queue.append((newpos, time+1))

    print("Minutes before oxygen spreads:", maxtime)



if __name__ == "__main__":
    step1()
    step2()
