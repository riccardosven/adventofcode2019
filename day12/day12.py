"Day 12: The N-Body Problem"

import re
from itertools import combinations
from math import gcd
import numpy as np


class Moon:
    "Single moon"

    def __init__(self, pos):
        self.pos = np.asarray(pos)  # Position
        self.vel = np.zeros(3)  # Velocity
        self.acc = np.zeros(3)

    @staticmethod
    def from_string(string):
        "Create a moon from a string specification"
        pos = list(map(int, re.findall(r'-?\d+', string)))
        return Moon(pos)

    def __str__(self):
        return f"<x={int(self.pos[0])}, y={int(self.pos[1])}, z={int(self.pos[2])}, \
            dx={int(self.vel[0])}, dy={int(self.vel[1])}, dz={int(self.vel[2])}>"

    def __repr__(self):
        return f"Moon({list(self.pos)})"

    def computegravity(self, other, axis=(0, 1, 2)):
        "Compute gravity interaction"
        if self is other:
            pass

        acceleration = np.zeros(3)
        for i in axis:
            if self.pos[i] > other.pos[i]:
                acceleration[i] = -1.0
            elif self.pos[i] < other.pos[i]:
                acceleration[i] = +1.0
            else:
                acceleration[i] = 0

        self.vel += acceleration
        other.vel -= acceleration

    def applyvelocity(self, axis=(0, 1, 2)):
        "Apply velocity to change position"
        for i in axis:
            self.pos[i] = self.pos[i] + self.vel[i]

    def energy(self):
        "Compute moon energy"
        pot = np.sum(np.abs(self.pos))
        kin = np.sum(np.abs(self.vel))

        return pot, kin, pot*kin


class System:
    "System of moons"

    def __init__(self, moons):
        self.moons = moons

    def step(self, axis=(0, 1, 2)):
        "One simulation step"
        for moon1, moon2 in combinations(self.moons, 2):
            moon1.computegravity(moon2, axis)

        for moon in self.moons:
            moon.applyvelocity(axis)

    def simulate(self, nsteps=100):
        "Simulate nsteps forward"
        for _ in range(nsteps):
            self.step()

    def energy(self):
        "Total energy of the system"
        totalenergy = 0

        for moon in self.moons:
            totalenergy += moon.energy()[2]

        return int(totalenergy)

    def __str__(self):
        return "".join(map(str, self.moons))

    def findrestart(self, guard=9999999999):
        "Find when the system restarts"

        looptimes = []

        for axs in [0, 1, 2]:  # Simulate independent axes
            seen = set()
            for i in range(guard):
                if str(self) in seen:
                    looptimes.append(i)
                    break
                seen.add(str(self))
                self.step(axis=[axs])

        lcm = looptimes[0]  # Find least common multiple of repeat times
        for i in looptimes[1:]:
            lcm = lcm*i//gcd(lcm, i)

        return lcm


def tests(instring, nsteps=100):
    "Testcases"
    moons = System([Moon.from_string(spec) for spec in instring.split("\n")])

    print(f"After {0} steps:")
    for moon in moons.moons:
        print(moon, moon.vel)
    print("")

    for i in range(1, nsteps+1):

        moons.step()

        print(f"After {i} steps:")
        for moon in moons.moons:
            print(moon, moon.vel)
        print("")

    print("Moon energies")
    for moon in moons.moons:
        pot, kin, tot = moon.energy()
        print(f"P = {pot}, K = {kin}, T = {tot}")


def star1():
    "Solution to first star"
    with open("input", "r") as fin:
        system = System([Moon.from_string(spec) for spec in fin.readlines()])

    system.simulate(1000)

    print("Star 1:", system.energy())


def star2():
    "Solution to second star"
    with open("input", "r") as fin:
        system = System([Moon.from_string(spec) for spec in fin.readlines()])

    print("Star 2:", system.findrestart())


if __name__ == "__main__":
    star1()
    star2()
