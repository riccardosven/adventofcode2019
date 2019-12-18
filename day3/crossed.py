
def trace(wire):
    wire = wire.split(",")
    visited = set()
    xpos = 0
    ypos = 0
    steps = 0 
    travelled = dict()
    for mov in wire:
        direction, amount = mov[0], int(mov[1:])
        if direction == "R":
            for _ in range(0, amount):
                steps += 1
                xpos += 1
                visited.add((xpos, ypos))
                travelled[(xpos, ypos)] = steps
        if direction == "D":
            for _ in range(0, amount):
                steps += 1
                ypos -= 1
                visited.add((xpos, ypos))
                travelled[(xpos, ypos)] = steps
        if direction == "U":
            for _ in range(0, amount):
                steps += 1
                ypos += 1
                visited.add((xpos, ypos))
                travelled[(xpos, ypos)] = steps
        if direction == "L":
            for _ in range(0, amount):
                steps += 1
                xpos -= 1
                visited.add((xpos, ypos))
                travelled[(xpos, ypos)] = steps
    return visited, travelled

def closest(trace1, trace2):
    closest = 99999999
    for crossing in trace1.intersection(trace2):
        closest = min(closest, abs(crossing[0]) + abs(crossing[1]))
    return closest

def shortest(trace1, steps1, trace2, steps2):
    shortest = 99999999

    for crossing in trace1.intersection(trace2):
        shortest = min(shortest, steps1[crossing] + steps2[crossing])
    return shortest


if __name__ == "__main__":
    if not __debug__:
        with open("input", "r") as fin:
            wire1 = fin.readline()
            wire2 = fin.readline()

        trace1, steps1 = trace(wire1)
        trace2, steps2 = trace(wire2)

        print(shortest(trace1, steps1, trace2, steps2))

    else:
        trace1 = trace("U1,R1")[0]
        trace2 = trace("R1,U1")[0]
        print(closest(trace1,trace2))

        trace1, steps1 = trace("R8,U5,L5,D3")
        trace2, steps2 = trace("U7,R6,D4,L4")
        print(shortest(trace1, steps1, trace2, steps2))
        
        trace1, steps1 = trace("R75,D30,R83,U83,L12,D49,R71,U7,L72")
        trace2, steps2 = trace("U62,R66,U55,R34,D71,R55,D58,R83")
        print(shortest(trace1,steps1, trace2, steps2))
        trace1, steps1 = trace("R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51")
        trace2, steps2 = trace("U98,R91,D20,R16,D67,R40,U7,R15,U6,R7")
        print(shortest(trace1, steps1, osesttrace2, steps2))

