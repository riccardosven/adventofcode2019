import sys
from collections import defaultdict, deque
from copy import deepcopy


def parseinput(inputfile):

    grid = [list(row) for row in inputfile.readlines()]

    width = len(grid[0])
    height = len(grid)

    outerportal = defaultdict(tuple)
    innerportal = defaultdict(tuple)
    neighbors = defaultdict(set)
    for i in range(2, height-2):
        for j in range(2, width-2):

            if grid[i][j] == ".":
                if grid[i+1][j] == ".":
                    neighbors[(i, j)].add((i+1, j))
                    neighbors[(i+1, j)].add((i, j))
                if grid[i][j+1] == ".":
                    neighbors[(i, j)].add((i, j+1))
                    neighbors[(i, j+1)].add((i, j))
                if grid[i-1][j] == ".":
                    neighbors[(i, j)].add((i-1, j))
                    neighbors[(i-1, j)].add((i, j))
                if grid[i][j-1] == ".":
                    neighbors[(i, j)].add((1, j-1))
                    neighbors[(i, j-1)].add((i, j))
                if grid[i-1][j] == grid[i-2][j] == "A" or \
                    grid[i+1][j] == grid[i+2][j] == "A" or \
                    grid[i][j+1] == grid[i][j+2] == "A" or \
                    grid[i][j-1] == grid[i][j-2] == "A":
                    startingpoint = (i, j)
                elif grid[i-1][j] == grid[i-2][j] == "Z" or \
                    grid[i+1][j] == grid[i+2][j] == "Z" or \
                    grid[i][j+1] == grid[i][j+2] == "Z" or \
                    grid[i][j-1] == grid[i][j-2] == "Z":
                    endingpoint = (i, j)
                elif grid[i-1][j].isupper() and grid[i-2][j].isupper():
                    if i < height//2:
                        outerportal[grid[i-2][j] + grid[i-1][j]] = (i, j)
                    else:
                        innerportal[grid[i-2][j] + grid[i-1][j]]= (i, j)
                elif grid[i+1][j].isupper() and grid[i+2][j].isupper():
                    if i < height//2:
                        innerportal[grid[i+1][j] + grid[i+2][j]] = (i, j)
                    else:
                        outerportal[grid[i+1][j] + grid[i+2][j]] = (i, j)
                elif grid[i][j-1].isupper() and grid[i][j-2].isupper():
                    if j < width//2:
                        outerportal[grid[i][j-2] + grid[i][j-1]] = (i, j)
                    else:
                        innerportal[grid[i][j-2] + grid[i][j-1]] = (i, j)
                elif grid[i][j+1].isupper() and grid[i][j+2].isupper():
                    if j < width//2:
                        innerportal[grid[i][j+1] + grid[i][j+2]] = (i, j)
                    else:
                        outerportal[grid[i][j+1] + grid[i][j+2]] = (i, j)
    
    #for name, location in innerportal.items():
    #    neighbors[location].add(outerportal[name])
    #    neighbors[outerportal[name]].add(location)

    return neighbors, startingpoint, endingpoint, innerportal, outerportal

def navigate(neighbors, startingpoint, endingpoint, innerportal, outerportal):

    neighbors = deepcopy(neighbors)
    for name, location in innerportal.items():
        neighbors[location].add(outerportal[name])
        neighbors[outerportal[name]].add(location)
    bfs = deque([(startingpoint, 0, set())])
    beststeps = None
    while bfs:
        pos, steps, visited = bfs.popleft()
        if pos == endingpoint:
            if beststeps is None or steps < beststeps:
                beststeps = steps
        for nextpos in neighbors[pos]:
            if nextpos in visited:
                continue
            bfs.append((nextpos, steps+1, visited.union([nextpos])))
    return beststeps
                
def navigaterecursive(neighbors, startingpoint, endingpoint, innerportal, outerportal, maxdepth=10):
    bfs = deque([((startingpoint, 0), 0, set() )])
    beststeps = None
    oldlvl = None
    while bfs:
        (pos, lvl), steps, visited = bfs.popleft()
        if not lvl == oldlvl:
            oldlvl = lvl
            print(lvl)
        if lvl > maxdepth:
            continue
        if pos == endingpoint and lvl == 0:
            if beststeps is None or steps < beststeps:
                beststeps = steps
        for nextpos in neighbors[pos]:
            if (nextpos, lvl) in visited:
                continue
            bfs.append(((nextpos, lvl), steps+1, visited.union([(nextpos, lvl)])))
        if lvl > 0:
            for name, loc in outerportal.items():
                if loc == pos:
                    nextpos = innerportal[name]
                    if (nextpos, lvl-1) not in visited:
                        bfs.append(((nextpos, lvl-1), steps+1, visited.union([(nextpos, lvl-1)])))
        for name, loc in innerportal.items():
            if loc == pos:
                nextpos = outerportal[name]
                if (nextpos, lvl+1) not in visited:
                    bfs.append(((nextpos, lvl+1), steps+1, visited.union([(nextpos, lvl+1)])))

    return beststeps
                

if __name__ == "__main__":
    with open(sys.argv[1]) as fhandle:
        #print(navigate(*parseinput(fhandle)))
        print(navigaterecursive(*parseinput(fhandle), maxdepth=int(sys.argv[2])))
