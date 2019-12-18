from functools import lru_cache


class Orbitmap:

    def __init__(self, str_in=None, file_in=None):
        self.orbits = dict()
        if not file_in is None:
            with open(file_in, "r") as fin:
                for line in fin:
                    centrum, planet = line.split(")")
                    self.orbits[planet.strip()] = centrum.strip()
        elif not str_in is None:
            for orbit in str_in.split():
                centrum, planet = orbit.split(")")
                self.orbits[planet.strip()] = centrum.strip()
        else:
            raise ValueError("Missing orbit map")

    def countorbits(self, planet):
        self.orbitcounts = dict()
        if planet in self.orbitcounts:
            return self.orbitcounts[planet]
        if planet == "COM":
            retval = 0
        else:
            retval = 1 + self.countorbits(self.orbits[planet])
        self.orbitcounts[planet] = retval
        return retval
    
    def planet(self, satellite):
        return self.orbits[satellite]

    def totalorbits(self):
        total = 0
        for planet in self.orbits:
            total += self.countorbits(planet)
        return total

    def path(self, planet):
        path = []
        while not planet == "COM":
            path.append(planet)
            planet = self.orbits[planet]
        return path

    def jumpsbetween(self, planet1, planet2):
        path1 = self.path(planet1)
        path2 = self.path(planet2)
        while path1[-1] == path2[-1]:
            last = path1[-1]
            del(path1[-1])
            del(path2[-1])

        path2.reverse()
        return path1[1:] + [last] + path2

if __name__ == "__main__":

    if __debug__:
        orbit_map = Orbitmap("COM)B B)C C)D D)E E)F B)G G)H D)I E)J J)K K)L ")
        print(orbit_map.totalorbits())
        print(orbit_map.jumpsbetween("K", "I"))

    else:

        orbit_map = Orbitmap(file_in = "input")

        print(orbit_map.totalorbits())
        you = orbit_map.planet("YOU")
        san = orbit_map.planet("SAN")
        print(len(orbit_map.jumpsbetween(you, san)))





