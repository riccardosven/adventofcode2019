
class Wire:
    "Class representing a wire diagram"

    def __init__(self, wires):
        xpos = 0
        ypos = 0
        steps = 0
        self.distance = dict()
        for movement in wires.split(","):
            direction, amount = movement[0], int(movement[1:])

            if direction == "R":
                for _ in range(0, amount):
                    steps += 1
                    xpos += 1
                    self.distance[(xpos, ypos)] = steps
            if direction == "D":
                for _ in range(0, amount):
                    steps += 1
                    ypos -= 1
                    self.distance[(xpos, ypos)] = steps
            if direction == "U":
                for _ in range(0, amount):
                    steps += 1
                    ypos += 1
                    self.distance[(xpos, ypos)] = steps
            if direction == "L":
                for _ in range(0, amount):
                    steps += 1
                    xpos -= 1
                    self.distance[(xpos, ypos)] = steps

    def intersections(self, other):
        "Returns intersections between wires"
        for position in self.distance:
            if position in other.distance:
                yield position

    def closest(self, other):
        "Returns closest intersection between wires"
        distance = 9999999
        for intersection in self.intersections(other):
            dist = abs(intersection[0]) + abs(intersection[1])
            distance = min(dist, distance)

        return distance

    def leastdelay(self, other):
        "Returns the intersection with least delay"
        delay = 99999999
        for intersection in self.intersections(other):
            delay = min(
                delay, self.distance[intersection] + other.distance[intersection])

        return delay


def tests():
    "Testcases"
    testwire1 = Wire("R8,U5,L5,D3")
    testwire2 = Wire("U7,R6,D4,L4")
    assert testwire1.closest(testwire2) == testwire2.closest(testwire1) == 6
    assert testwire1.leastdelay(
        testwire2) == testwire2.leastdelay(testwire1) == 30

    testwire1 = Wire("R75,D30,R83,U83,L12,D49,R71,U7,L72")
    testwire2 = Wire("U62,R66,U55,R34,D71,R55,D58,R83")
    assert testwire1.closest(testwire2) == testwire2.closest(testwire1) == 159
    assert testwire1.leastdelay(
        testwire2) == testwire2.leastdelay(testwire1) == 610

    testwire1 = Wire("R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51")
    testwire2 = Wire("U98,R91,D20,R16,D67,R40,U7,R15,U6,R7")
    assert testwire1.closest(testwire2) == testwire2.closest(testwire1) == 135
    assert testwire1.leastdelay(
        testwire2) == testwire2.leastdelay(testwire1) == 410


def star1():
    "Answer to first star"
    with open("input") as fhandle:
        wire1 = Wire(fhandle.readline())
        wire2 = Wire(fhandle.readline())

    print("Star 1:", wire1.closest(wire2))


def star2():
    "Answer to second star"
    with open("input") as fhandle:
        wire1 = Wire(fhandle.readline())
        wire2 = Wire(fhandle.readline())

    print("Star 2:", wire1.leastdelay(wire2))


if __name__ == "__main__":
    if __debug__:
        tests()

    star1()
    star2()
