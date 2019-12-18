from collections import deque
import sys

class TunnelMap:
    "Parse a tunnelmap"

    def __init__(self, infile):

        with open(infile) as fhandle:
            self.grid = [row for row in fhandle.readlines()]

        self.width = len(self.grid)
        self.height = len(self.grid[0])
        self._memo = dict()

        self.entrances = []
        for i, row in enumerate(self.grid):
            for j, elem in enumerate(row):
                if elem == "@":
                    self.entrances.append((i,j))

    def findkeys(self, pos, havekeys=''):
        "Returns all possible next keys that can be collected from a given position"
        queue = deque()
        queue.append(pos)

        visited = {pos: 0} # Gives distances to visited nodes
        reachable = dict()
        while queue:
            pos = queue.popleft()

            for newpos in [
                    (pos[0] + 1, pos[1]),
                    (pos[0] - 1, pos[1]),
                    (pos[0], pos[1] + 1),
                    (pos[0], pos[1] - 1)
                ]:
                if newpos in visited:
                    continue

                if not (0 <= newpos[0] < self.width and 0 <= newpos[1] < self.height):
                    continue # Outside grid

                visited[newpos] = visited[pos] + 1
                newchar = self.grid[newpos[0]][newpos[1]]

                if newchar == "#":
                    continue # Wall

                if "A" <= newchar <= "Z" and not newchar.lower() in havekeys:
                    continue # Door that I cannot open

                if "a" <= newchar <= "z" and not newchar in havekeys:
                    reachable[newchar] = visited[newpos], newpos # Key that I do not have
                else:
                    queue.append(newpos)

        return reachable



    def collectkeys(self, pos, havekeys=''):
        "Collect all keys in the map optimally"
        hks = "".join(sorted(havekeys))
        if (pos, hks) in self._memo:
            return self._memo[(pos, hks)]

        nextkeys = self.findkeys(pos, hks)
        if len(nextkeys) == 0:
            ans = 0 # All keys collected
        else:
            ans = None
            for key, (dist, newpos) in nextkeys.items():
                newsteps = dist + self.collectkeys(newpos, hks+key)
                if ans is None or newsteps < ans:
                    ans = newsteps
        
        self._memo[(pos, hks)] = ans
        return ans


if __name__ == "__main__":
    m = TunnelMap(sys.argv[1])
    print(m.findkeys(m.entrances[0], ''))
    print(m.collectkeys(m.entrances[0], ''))
    # print(m.keys)
    # print(m.doors)
    # print(m.keytokey["b"])
    #print(m.collectallkeys())
