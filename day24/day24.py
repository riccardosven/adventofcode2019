"Day 24: Planet of Discord"

class Solution:
    "Solution for planet of discord"
    def __init__(self, width=5, height=5):
        self.grid = dict()
        self.width = width
        self.height = height

    @staticmethod
    def from_string(spec):
        "Constructor"
        grid = dict()
        for row_idx, row in enumerate(spec.split("\n")):
            for col_idx, elem in enumerate(row.strip()):
                if elem == "#":
                    grid[(row_idx, col_idx)] = 1
        sol = Solution(height=row_idx+1, width=col_idx+1)
        sol.grid = grid
        return sol

    def evolve(self):
        "One step of the rules"
        newgrid = dict()
        for row_idx in range(self.height):
            for col_idx in range(self.width):
                nneigh = self.getneighbors((row_idx, col_idx))
                if (row_idx, col_idx) in self.grid and nneigh == 1:
                    newgrid[(row_idx, col_idx)] = 1
                elif not (row_idx, col_idx) in self.grid and (nneigh == 1 or nneigh == 2):
                    newgrid[(row_idx, col_idx)] = 1

        self.grid = newgrid

    def untilrepeat(self):
        "Evolve until a repeating pattern is found"
        seen = set()
        while True:
            if self.biodiversity() in seen: # Identify the pattern using its biodiversity
                return
            seen.add(self.biodiversity())
            self.evolve()


    def bugcount(self):
        "Return the number of bugs"
        return len(self.grid)

    def getneighbors(self, pos):
        "Counts the number of neighbors of a position"
        nneigh = 0
        row_idx, col_idx = pos
        for drow, dcol in [(-1, 0), (0, 1), (0, -1), (1, 0)]:
            nneigh += self.grid.get((row_idx + drow, col_idx + dcol), 0)
        return nneigh

    def biodiversity(self):
        "Returns the biodiversity of the grid"
        biodiv = 0
        idx = 0
        for row_idx in range(self.height):
            for col_idx in range(self.width):
                if (row_idx, col_idx) in self.grid:
                    biodiv += 2**idx
                idx += 1
        return biodiv

    def __str__(self):
        out = []
        for row_idx in range(self.height):
            out.append("")
            for col_idx in range(self.width):
                if self.grid.get((row_idx, col_idx), 0):
                    out[-1] += "#"
                else:
                    out[-1] += "."

        return "\n".join(out)


class Recursive(Solution):
    "Solution for planet of discord"

    def __init__(self, width=5, height=5):
        super().__init__(width=width, height=height)
        self.smallest = -1
        self.largest = 1

    @staticmethod
    def from_string(spec):
        "Constructor"
        grid = dict()
        for row_idx, row in enumerate(spec.split("\n")):
            for col_idx, elem in enumerate(row.strip()):
                if elem == "#":
                    grid[(row_idx, col_idx, 0)] = 1
        sol = Recursive(height=row_idx+1, width=col_idx+1)
        sol.grid = grid
        return sol


    def evolve(self):
        "One step of the recursive rules"
        newgrid = dict()
        if self.shoulddecrease():
            self.smallest -= 1

        if self.shouldincrease():
            self.largest += 1

        for lvl in range(self.smallest, self.largest+1):
            for row_idx in range(self.height):
                for col_idx in range(self.width):
                    if col_idx == row_idx == 2:
                        continue
                    nneigh = self.getneighbors((row_idx, col_idx, lvl))
                    if (row_idx, col_idx, lvl) in self.grid and nneigh == 1:
                        newgrid[(row_idx, col_idx, lvl)] = 1
                    elif not (row_idx, col_idx, lvl) in self.grid and (nneigh == 1 or nneigh == 2):
                        newgrid[(row_idx, col_idx, lvl)] = 1

        self.grid = newgrid
    
    def shouldincrease(self):
        "Heuristic verifying wether we need to add levels outwards"
        for row_idx in range(self.width):
            for col_idx in range(self.height):
                if (row_idx, col_idx, self.largest) in self.grid:
                    return True
        return False
        
    
    def shoulddecrease(self):
        "Heuristic verifying wether we need to add levels inwards"
        for (row_idx, col_idx) in [(1,2), (2,1), (2, 3), (3,2)]:
            if (row_idx, col_idx, self.smallest) in self.grid:
                return True
        return False

    def getneighbors(self, pos):
        "Counts the number of neighbors of a position"
        nneigh = 0
        row_idx, col_idx, lvl = pos
        for drow, dcol in [(-1, 0), (0, 1), (0, -1), (1, 0)]:
            nneigh += self.grid.get((row_idx + drow, col_idx + dcol, lvl), 0)
        if row_idx == 0:  # First row, check outer layer
            nneigh += self.grid.get((1, 2, lvl-1), 0)
        elif row_idx == 4:  # Last row, check outer layer
            nneigh += self.grid.get((3, 2, lvl-1), 0)
        if col_idx == 0:  # First col, check outer layer
            nneigh += self.grid.get((2, 1, lvl-1), 0)
        elif col_idx == 4:  # last col, check outer layer
            nneigh += self.grid.get((2, 3, lvl-1), 0)
        if row_idx == 2 and col_idx == 1:  # Inner left
            nneigh += sum(self.grid.get((r, 0, lvl+1), 0)
                            for r in range(self.height))
        if row_idx == 2 and col_idx == 3:  # Inner right
            nneigh += sum(self.grid.get((r, 4, lvl+1), 0)
                            for r in range(self.height))
        if row_idx == 1 and col_idx == 2:  # Inner top
            nneigh += sum(self.grid.get((0, c, lvl+1), 0)for c in range(self.width))
                            
        if row_idx == 3 and col_idx == 2:  # Inner bottom
            nneigh += sum(self.grid.get((4, c, lvl+1), 0)
                            for c in range(self.width))

        return nneigh

    def __str__(self):
        out = []
        for lvl in range(self.smallest, self.largest+1):
            out.append(f"Level {lvl}")
            for row_idx in range(self.height):
                out.append("")
                for col_idx in range(self.width):
                    if self.grid.get((row_idx, col_idx, lvl), 0):
                        out[-1] += "#"
                    else:
                        out[-1] += "."

        return "\n".join(out)
    
def tests():
    state = """ ....#
        #..#.
        #..##
        ..#..
        #...."""
    grid = Solution.from_string(state)
    grid.untilrepeat()
    assert grid.biodiversity() == 2129920

    grid = Recursive.from_string(state)
    for _ in range(10):
        grid.evolve()
    assert grid.bugcount() == 99

    

def star1():
    "Solution to first star"
    with open("input") as fhandle:
        grid = Solution.from_string(fhandle.read())
    grid.untilrepeat()
    print("Star 1:", grid.biodiversity())

def star2():
    "Solution to second star"
    with open("input") as fhandle:
        grid = Recursive.from_string(fhandle.read())
    for _ in range(200):
        grid.evolve()
    print("Star 2:", grid.bugcount())



if __name__ == "__main__":
    tests()
    star1()
    star2()