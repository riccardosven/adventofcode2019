"Day 6: Universal Orbit Map"


from functools import lru_cache


class Orbitmap:
    "Map of orbits"

    def __init__(self, stringmap):
        self.orbits = dict()
        for orbit in stringmap.split():
            centrum, planet = orbit.split(")")
            self.orbits[planet.strip()] = centrum.strip()

    @staticmethod
    def from_file(filename):
        with open(filename, "r") as fhandle:
            return Orbitmap(fhandle.read())

    @lru_cache(None)
    def countorbits(self, planet):
        "Return number of orbits of a planet"
        if planet == "COM":
            retval = 0
        else:
            retval = 1 + self.countorbits(self.orbits[planet])
        return retval

    def planet(self, satellite):
        "Get the center of an orbit"
        return self.orbits[satellite]

    def totalorbits(self):
        "Return total number of orbits"
        total = 0
        for planet in self.orbits:
            total += self.countorbits(planet)

        return total

    def path(self, planet):
        "Get the path of planets to COM"
        path = []
        while not planet == "COM":
            path.append(planet)
            planet = self.orbits[planet]
        return path

    def jumpsbetween(self, planet1, planet2):
        "Get jumps between two planets"
        path1 = self.path(planet1)
        path2 = self.path(planet2)
        while path1[-1] == path2[-1]:
            last = path1[-1]
            del path1[-1]
            del path2[-1]

        path2.reverse()
        return path1[1:] + [last] + path2


def tests():
    "Testcases"
    orbit_map = Orbitmap("COM)B B)C C)D D)E E)F B)G G)H D)I E)J J)K K)L ")
    assert orbit_map.totalorbits() == 42
    assert "".join(orbit_map.jumpsbetween("K", "I")) == "JEDI"


def star1():
    "Solution to first star"
    orbit_map = Orbitmap.from_file("input")
    print("Star 1:", orbit_map.totalorbits())


def star2():
    "Solution to second star"
    orbit_map = Orbitmap.from_file("input")
    start = orbit_map.planet("YOU")
    end = orbit_map.planet("SAN")
    print("Star 2:", len(orbit_map.jumpsbetween(start, end)))


if __name__ == "__main__":

    if __debug__:
        tests()

    star1()
    star2()
