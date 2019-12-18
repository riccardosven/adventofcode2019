from intcodecomputer import IntcodeComputer

# 0 is an empty tile. No game object appears in this tile.
# 1 is a wall tile. Walls are indestructible barriers.
# 2 is a block tile. Blocks can be broken by the ball.
# 3 is a horizontal paddle tile. The paddle is indestructible.
# 4 is a ball  b in self.screen.items():

class ArtificialIntelligence:
    def __init__(self):
        self.player_x = 0
        self.ball_x = 0
        self.command = 0

    def update(self, xpos, ypos, what):
        if what == 3:
            self.player_x = xpos
        if what == 4:
            self.ball_x = xpos
        if self.ball_x < self.player_x:
            self.command = -1
        elif self.ball_x > self.player_x:
            self.command = +1
        else:
            self.command = 0
    

    

class ArcadeGame:

    def __init__(self):
        with open("input", "r") as fin:
            program = "".join(fin.readlines())

        self.tiles = " Xv-o"
        self.cpu = IntcodeComputer(program)
        self.ai = ArtificialIntelligence()
        self.screen = dict()

    def run(self):
        try:
            while True:
                xpos = self.cpu.step(self.ai.command)
                ypos = self.cpu.step(self.ai.command)
                what = self.cpu.step(self.ai.command)
                self.ai.update(xpos, ypos, what)

                self.screen[(xpos, ypos)] = what
                self.render()
        except StopIteration:
            pass

    def render(self, width=40, height=40):
        screen = [[' ' for _ in range(width)] for _ in range(height)]
        score = 0
        for (x, y), tile in self.screen.items():
            if x == -1 and y == 0:
                score = tile
            else:
                screen[y][x] = self.tiles[tile]
        print("\n".join(["".join(row) for row in screen]))
        print("Score: " + str(score))


def stage1():
    game = ArcadeGame()

    game.run()
    game.render()

    print(sum([1 for x in game.screen.values() if x == 2]))


if __name__ == "__main__":
    stage1()
