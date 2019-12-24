#from collections import defaultdict


class Solution:
    "Solution for planet of discord"

    def __init__(self, spec=None, width=5, height=5):
        self.grid = dict()
        self.width = width
        self.height = height
        self.smallest = -1
        self.largest = 1

        if not spec is None:
            for row_idx, row in enumerate(spec.split("\n")):
                for col_idx, elem in enumerate(row.strip()):
                    if elem == "#":
                        self.grid[(row_idx, col_idx, 0)] = 1

    def evolve(self):
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
        for row_idx in range(self.width):
            for col_idx in range(self.height):
                if (row_idx, col_idx, self.largest) in self.grid:
                    return True
        return False
        
    
    def shoulddecrease(self):
        for (row_idx, col_idx) in [(1,2), (2,1), (2, 3), (3,2)]:
            if (row_idx, col_idx, self.smallest) in self.grid:
                return True
        return False

    def bugcount(self):
        return len(self.grid)

    def getneighbors(self, pos):
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

    def biodiversity(self):
        biodiv = 0
        idx = 0
        for row_idx in range(self.height):
            for col_idx in range(self.width):
                if (row_idx, col_idx, 0) in self.grid:
                    biodiv += 2**idx
                idx += 1
        return biodiv

    def showneighbors(self):
        out = []
        for row_idx in range(self.height):
            out.append("")
            for col_idx in range(self.width):
                out[-1] += str(self.getneighbors((row_idx, col_idx, 0)))

        print("\n".join(out))

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

def test():
    state = """ ....#
        #..#.
        #..##
        ..#..
        #...."""
    grid = Solution(spec=state)
    print("Initial state")
    print(grid)
    print()
    for _ in range(10):
        grid.evolve()
    print(grid)
    print(grid.bugcount())

def star():
    with open("input") as fhandle:
        grid = Solution(spec=fhandle.read())
    for _ in range(200):
        grid.evolve()
    print(f"There are {grid.bugcount()} bugs!")



if __name__ == "__main__":
    star()