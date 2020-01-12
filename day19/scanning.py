"Day 19: Tractor Beam"

from functools import lru_cache
from intcodecomputer import IntcodeComputer


class Area:
    "Area closest to the ship"

    def __init__(self):
        with open("input") as fhandle:
            self.cpu = IntcodeComputer(fhandle.read().strip())

    @lru_cache
    def tractor(self, pos):
        "Check if a position is within the tractor beam "
        self.cpu.reset()
        self.cpu.step(pos[0])
        self.cpu.step(pos[1])
        try:
            val = self.cpu.step(None)
        except StopIteration:
            pass
        return val

    def countaffected(self, width, height):
        "Count number of points affected by the tractor beam"
        naffected = 0
        for i in range(height):
            for j in range(width):
                if self.tractor((i, j)):
                    naffected += 1

        return naffected


class RectZone(Area):
    "Rectangular zone to fit Santa's ship"

    def __init__(self, pos, width, height):
        super().__init__()
        self.x = pos[0]
        self.y = pos[1]
        self.width = width
        self.height = height

    @property
    def northeast(self):
        "upper left"
        return (self.x + self.width - 1, self.y)

    @property
    def southwest(self):
        "lower right"
        return (self.x, self.y + self.height - 1)

    @property
    def northwest(self):
        "upper right"
        return (self.x, self.y)

    @property
    def southeast(self):
        "lower left"
        return (self.x + self.width - 1, self.y + self.height - 1)

    def adapt(self):
        "Tune the beam to fit in the tractor area"
        while not (self.tractor(self.northeast) and self.tractor(self.northwest) and self.tractor(self.southeast) and self.tractor(self.southwest)):
            # It is not fully inside
            if not self.tractor(self.northeast):
                self.y += 1  # We can move it down
            if not self.tractor(self.southwest):
                self.x += 1  # We can move it right


def star1():
    "Solution to first star"
    area = Area()
    print("Star 1:", area.countaffected(50, 50))


def star2():
    "Solution to second star"
    # Start the area in a known tractor beam position
    rect = RectZone((17, 8), 100, 100)
    rect.adapt()
    print("Star 2:", 10000*rect.x + rect.y)


if __name__ == "__main__":
    star1()
    star2()
