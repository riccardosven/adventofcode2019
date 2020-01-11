"Day 10: Monitoring Station"
from bisect import insort
import numpy as np
from testmaps import MAP0, MAP1, MAP2, MAP3, MAP4
from functools import lru_cache


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

    def bestpos(self):
        "Return position with most visible asteroids"
        best = 0
        bestpos = ()
        for asteroid in self.asteroidset:
            visible = self.visiblefrom(asteroid)
            if len(visible) > best:
                best = len(visible)
                bestpos = asteroid
        return bestpos


def runtest(inputmap, pos=None, expected=None):
    "Test one map"
    astmap = AsteroidMap(inputmap)
    if not pos is None:
        assert expected == len(astmap.visiblefrom(pos))
    else:

        assert astmap.bestpos() == expected


def tests():
    "Testcases"
    runtest(MAP0, pos=(1, 1), expected=2)
    runtest(MAP0, pos=(1, 1), expected=2)
    runtest(MAP1, pos=(5, 8), expected=33)
    runtest(MAP2, pos=(1, 2), expected=35)
    runtest(MAP3, pos=(6, 3), expected=41)
    runtest(MAP4, pos=(11, 13), expected=210)

    runtest(MAP0, expected=(1, 1))
    runtest(MAP1, expected=(5, 8))
    runtest(MAP2, expected=(1, 2))
    runtest(MAP3, expected=(6, 3))
    runtest(MAP4, expected=(11, 13))


def star1(astmap):
    "Solution to first star"
    print("Star 1:", len(astmap.visiblefrom(astmap.bestpos())))


def star2(astmap):
    "Solution to second star"
    N = 199
    for i, ast in enumerate(astmap.destroyasteroids(astmap.bestpos())):
        if i == N:
            _, (_, out) = ast
            print("Star 2:", 100*out[0] + out[1])
            return


if __name__ == "__main__":
    tests()
    with open("input", "r") as fin:
        inputmap = AsteroidMap(fin.read())
    star1(inputmap)
    star2(inputmap)
