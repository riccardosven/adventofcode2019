from intcodecomputer import IntcodeComputer

with open("input") as fhandle:
    cpu = IntcodeComputer("".join(fhandle.readlines()))

memo = dict()
def tractor(x, y):
    if (x, y) in memo:
        return memo[(x, y)]
    cpu.reset()
    cpu.step(x)
    cpu.step(y)
    try:
        val = cpu.step(None)
    except StopIteration:
        pass
    memo[(x, y)] = val
    return val

#grid = [[tractor(x, y)  for x in range(50)] for y in range(20)]


class RectZone:
    def __init__(self, x, y, width, height ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    
    @property
    def northeast(self):
        return (self.x + self.width - 1, self.y)

    @property
    def southwest(self):
        return (self.x, self.y + self.height - 1)

    @property
    def northwest(self):
        return (self.x, self.y)

    @property
    def southeast(self):
        return (self.x + self.width - 1, self.y + self.height -1)
    
    def adapt(self):
        while True:
#            grid[self.y][self.x] = 2
#            grid[self.y + self.height - 1][self.x] = 2
#            grid[self.y][self.x + self.width - 1] = 2
#            grid[self.y + self.height - 1][self.x + self.width - 1] = 2
#            for row in grid:
#                for e in row:
#                    if e == 0:
#                        print('.', end ="")
#                    if e == 1:
#                        print('#', end ="")
#                    if e == 2:
#                        print('O', end ="")
#                print()
#            input()
            if not tractor(*self.northeast):
                self.y += 1
            if not tractor(*self.southwest):
                self.x += 1
            if tractor(*self.northeast) and tractor(*self.northwest) and tractor(*self.southeast) and tractor(*self.southwest):
                return True



    
##grid = [['#' if tractor(x, y) else "." for x in range(100)] for y in range(100)]
#grid = [[tractor(x, y)  for x in range(50)] for y in range(20)]

#rect = RectZone(17, 8, 5, 5)
#rect.adapt()

#grid[rect.y][rect.x] = "O"
#grid[rect.y + rect.height - 1][rect.x] = "O"
#grid[rect.y][rect.x + rect.width - 1] = "O"
#grid[rect.y + rect.height - 1][rect.x + rect.width - 1] = "O"
#print("\n".join(["".join(['#' if e else '.' for e in row]) for row in grid]))




#for row in grid:
#    print(sum(row))

    
rect = RectZone(17, 8, 100, 100)
rect.adapt()
print(rect.x, rect.y)


#
# def inside(x, y, width, height):
#    if (x, y) in memo:
#        return memo[(x, y)
#    for dx in range(width):
#        for dy in range(height):
#                cpu.reset()
#                cpu.step(x+dx)
#                cpu.step(y+dy)
#                try:
#                    val = cpu.step(None)
#                except StopIteration:
#                    val = 0
#                memo[(x+dx, y+dy)] = val
#                if not val:
#                    return 0
#    return 1
#
#print(inside(0, 0, 1, 1))
#print(inside(5, 3, 1, 1))
#print(inside(3, 5, 1, 1))
#print(inside(14, 6, 2, 2))
#print(inside(6, 14, 2, 2))

#grid = [[0 for _ in range(100)] for _ in range(100)]
# for i in range(100):
#    for j in range(100):
#        cpu.reset()
#        cpu.step(i)
#        cpu.step(j)
#        try:
#            val = cpu.step(None)
#            grid[i][j] = val
#            if inside(i, j, 2, 2):
#                grid[i][j] = 2
#            npulled += val
#        except StopIteration:
#            pass
#
#
#
#
#
# for row in grid:
#    for e in row:
#        if e == 0:
#            print(".", end="")
#        if e == 1:
#            print("#", end="")
#        if e == 2:
#            print("O", end="")
#    print()
#
# print("\n".join(["".join("#" if e else "." for e in row) for row in grid]))
#
# print("\n".join(["".join("#" if e else "." for e in row) for row in grid]))
# print(npulled)
