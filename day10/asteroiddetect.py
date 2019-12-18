"Find best place in asteroid map"
import numpy as np
from testmaps import MAP0, MAP1, MAP2, MAP3, MAP4
from bisect import insort
#from collections import OrderedDict


def cart2pol(x, y):
    "Cartesian to polar transformation"
    rho = np.sqrt(x**2 + y**2)
    phi = np.pi - np.arctan2(x, y)
    return rho, phi


class AsteroidMap:
    "Asteroid map"

    def __init__(self, inputmap):
        "Turn an input map into a set of coordinates"
        asteroidset = set()
        for i, row in enumerate(inputmap.split("\n")):
            for j, asteroid in enumerate(row):
                if asteroid == "#":
                    asteroidset.add((j, i))
        self.asteroidset = asteroidset

    def visiblefrom(self, position):
        "Finds all asteroids that are visible from a given position"
        visibleangle = dict()
        xp, yp = position
        for asteroid in self.asteroidset:
            if position == asteroid:
                continue

            x, y = asteroid

            distance, angle = cart2pol(x - xp, y - yp)

            if angle in visibleangle:
                insort(visibleangle[angle], (distance, asteroid))
            else:
                visibleangle[angle] = [(distance, asteroid)]

        return visibleangle

    def destroyasteroids(self, pos):
        "Give asteroids in order from map"
        visible = self.visiblefrom(pos)
        while True:
            printed = False
            for angle, asteroids in sorted(visible.items()):
                if not asteroids:
                    continue
                printed = True
                yield angle, asteroids.pop(0)
            if not printed:
                break
    
    def render(self, pos=None):

        print(self.asteroidset)

        # if not pos is None:
        #     x, y = pos
        #     thismap[y][x] = "o"

        # for row in thismap:
        #     print("".join(row))




def runtest(inputmap, pos=None):
    "Test one map"
    astmap = AsteroidMap(inputmap)
    if not pos is None:
        return len(astmap.visiblefrom(pos))
    else:
        best = 0
        bestpos = ()
        for asteroid in astmap.asteroidset:
            visible = astmap.visiblefrom(asteroid)
            if len(visible) > best:
                best = len(visible)
                bestpos = asteroid
    if pos is None:
        return bestpos

    return best


def testmaps():
    print(runtest(MAP0, pos=(1, 1)), " expected=2")
    print(runtest(MAP0, pos=(1, 1)), " expected=2")
    print(runtest(MAP1, pos=(5, 8)), " expected=33")
    print(runtest(MAP2, pos=(1, 2)), " expected=35")
    print(runtest(MAP3, pos=(6, 3)), " expected=41")
    print(runtest(MAP4, pos=(11, 13)), " expected=210")

    print(runtest(MAP0), " expected=(1, 1)")
    print(runtest(MAP1), " expected=(5, 8)")
    print(runtest(MAP2), " expected=(1, 2)")
    print(runtest(MAP3), " expected=(6, 3)")
    print(runtest(MAP4), " expected=(11, 13)")


def firststep(pos=None):
    with open("input", "r") as fin:
        inmap = fin.readlines()
    return runtest("".join(inmap), pos=pos)


def testdestroy(inmap, pos, compute=False):
    astmap = AsteroidMap(inmap)
    N = 199
    for i, ast in enumerate(astmap.destroyasteroids(pos)):
        if i == N:
            if compute:
                _, (_, out) = ast
                return 100*out[0] + out[1]
            else:
                return ast


def secondstep(pos):
    with open("input", "r") as fin:
        inmap = fin.readlines()

    return testdestroy("".join(inmap), pos=pos, compute=True)



if __name__ == "__main__":
    testmaps()
    bestpos = firststep()
    nbest = firststep(pos=bestpos)
    print(bestpos)
    print(nbest)
    print(secondstep(bestpos))

    #testdestroy(MAP4, (11, 13))
    #secondstep()

    # firststep()
    # secondstep()
    #testdestroy(MAP4, (11,13), compute=True)
    #testdestroy(MAP4, (11,13), compute=True)
