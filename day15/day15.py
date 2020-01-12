"Day 15: Oxygen System"

import pickle
from copy import deepcopy
from collections import deque
from intcodecomputer import IntcodeComputer

NORTH = 1
SOUTH = 2
WEST = 3
EAST = 4

def peek(pos, direction):
    "return position in direction"
    if direction == NORTH:
        return (pos[0], pos[1] - 1)
    if direction == SOUTH:
        return (pos[0], pos[1] + 1)
    if direction == EAST:
        return (pos[0] + 1, pos[1])
    if direction == WEST:
        return (pos[0] - 1, pos[1])
    raise Exception("Bad move command")


class Robot:
    "Repair droid"
    def __init__(self, program="input", areamap=None):
        with open(program, 'r') as fin:
            program = "".join(fin.readlines())
        self.brain = IntcodeComputer(program)
        self.pos = (0, 0)
        self.areamap = dict() if areamap is None else areamap
        self.areamap[self.pos] = "."

    def clone(self):
        "Create a new robot clone"
        other = Robot()
        other.brain = self.brain.copy()
        other.pos = deepcopy(self.pos)
        other.areamap = deepcopy(self.areamap)

        return other

    def isexplored(self, direction):
        "Check if a position has been explored"
        if peek(self.pos, direction) in self.areamap:
            return True
        return False

    def move(self, direction):
        "Move to a new position"
        self.pos = peek(self.pos, direction)

    def step(self, direction):
        "Take one step in a direction"
        retval = self.brain.step(direction)
        oldpos = self.pos
        self.move(direction)
        if retval == 0:
            self.areamap[self.pos] = "#"
            self.pos = oldpos
        elif retval == 1:
            self.areamap[self.pos] = "."
        elif retval == 2:
            self.areamap[self.pos] = "O"
        else:
            raise Exception("Error in step")

    def show(self, offset=20):
        "Print situation"
        printmap = deepcopy(self.areamap)
        printmap[self.pos] = "X"
        render(printmap, offset=offset)


def render(mapdict, width=40, height=40, offset=20):
    "Render map"
    plot = [[' ' for _ in range(width)] for _ in range(height)]
    for coord, val in mapdict.items():
        plot[coord[1] + offset][coord[0] + offset] = val
    print("\n".join(["".join(row) for row in plot]))


def maparea():
    "Map the whole area around the robot"
    outermap = dict()
    robots = deque()
    robots.append((Robot(areamap=outermap), []))

    while robots:
        robot, steps = robots.popleft()
        for direction in [NORTH, SOUTH, EAST, WEST]:
            if robot.isexplored(direction):
                continue
            newbot = robot.clone()
            newbot.areamap = outermap
            newbot.step(direction)
            if newbot.areamap[newbot.pos] == "O":
                stepsout = steps + [direction]
            robots.append((newbot, steps + [direction]))

    return outermap, stepsout


def star1():
    "Solution to first star"
    area, steps = maparea()
    robot = Robot()
    for step in steps:
        robot.step(step)
    assert area[robot.pos] == "O"
    print("Star 1:", len(steps))

    # Use pickle to skip recomputing the map in step 2
    with open("step1.pickle", "wb") as handle:
        pickle.dump(area, handle)
        pickle.dump(robot.pos, handle)


def step2():
    "Solution to second star"

    # Use map computed in step 1
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

    print("Star 2:", maxtime)

if __name__ == "__main__":
    star1()
    step2()
