import numpy as np
from itertools import combinations
import re
from math import gcd


class Moon:
    def __init__(self, pos):
        self.pos = np.asarray(pos)  # Position
        self.vel = np.zeros(3)  # Velocity
        self.acc = np.zeros(3)

    @staticmethod
    def fromstring(string):
        pos = list(map(int, re.findall(r'-?\d+', string)))
        return Moon(pos)

    def __str__(self):
        return f"<x={int(self.pos[0])}, y={int(self.pos[1])}, z={int(self.pos[2])}, dx={int(self.vel[0])}, dy={int(self.vel[1])}, dz={int(self.vel[2])}>"

    def __repr__(self):
        return f"Moon({list(self.pos)})"

    def computegravity(self, other, axis=[0,1,2]):
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

    def applyvelocity(self, axis=[0,1,2]):
        for i in axis:
            self.pos[i] = self.pos[i] + self.vel[i]

    def energy(self):
        pot = np.sum(np.abs(self.pos))
        kin = np.sum(np.abs(self.vel))

        return pot, kin, pot*kin
    

class System:

    def __init__(self, moons):
        self.moons = moons
    
    def step(self, axis=[0,1,2]):
        for moon1, moon2 in combinations(self.moons, 2):
            moon1.computegravity(moon2, axis)

        for moon in self.moons:
            moon.applyvelocity(axis)
    
    def simulate(self, nsteps=100):
        for _ in range(1, nsteps+1):
            self.step()
    
    def __str__(self):
        return "".join(map(str, self.moons))

    def findrestart(self, guard = 999999999999999):

        looptimes = []

        for ax in [0,1,2]:
            seen = set()

            print(self)
            for i in range(guard):
                if str(self) in seen:
                    looptimes.append(i)
                    break
                seen.add(str(self))
                self.step(axis=[ax])
        
        lcm = looptimes[0]

        for i in looptimes[1:]:
            lcm = lcm*i//gcd(lcm, i)
        return lcm




def test1(instring, nsteps=100):
    moons = System([Moon.fromstring(spec) for spec in instring.split("\n")])

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


def stage1():
    with open("input", "r") as fin:
        system = System([Moon.fromstring(spec) for spec in fin.readlines()])

    system.simulate(1000)

    totalenergy = 0

    print("Moon energies")
    for moon in system.moons:
        pot, kin, tot = moon.energy()
        totalenergy += tot
        print(f"P = {pot}, K = {kin}, T = {tot}")

    print("TOTAL = ", totalenergy)
    print(system)

        

def stage2():
    with open("input", "r") as fin:
        system = System([Moon.fromstring(spec) for spec in fin.readlines()])

    instring = """<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>"""
#
#    instring2 = """<x=-8, y=-10, z=0>
##<x=5, y=5, z=10>
##<x=2, y=-7, z=3>
##<x=9, y=-8, z=-3>"""
    #system = System([Moon.fromstring(spec) for spec in instring.split("\n")])

    print(system.findrestart())

    

if __name__ == "__main__":
#    test1("""<x=-1, y=0, z=2>
#<x=2, y=-10, z=-7>
#<x=4, y=-8, z=8>
#<x=3, y=5, z=-1>""")
#
#test1("""<x=-8, y=-10, z=0>
#<x=5, y=5, z=10>
#<x=2, y=-7, z=3>
#<x=9, y=-8, z=-3>""", nsteps=100)

    stage1()
    stage2()