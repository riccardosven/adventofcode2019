"Day 13: Care Package"

from intcodecomputer import IntcodeComputer

# 0 is an empty tile. No game object appears in this tile.
# 1 is a wall tile. Walls are indestructible barriers.
# 2 is a block tile. Blocks can be broken by the ball.
# 3 is a horizontal paddle tile. The paddle is indestructible.
# 4 is a ball  b in self.screen.items():


class ArcadeGame:
    "Arcade cabinet"

    def __init__(self):
        with open("input", "r") as fin:
            program = "".join(fin.readlines())

        self.tiles = " Xv-o"
        self.cpu = IntcodeComputer(program)
        self.screen = dict()

    def run(self):
        "Simulate arcade cabinet"
        try:
            nsteps = 0
            while True:
                nsteps += 1
                xpos = self.cpu.step(0)
                ypos = self.cpu.step(0)
                what = self.cpu.step(0)
                self.screen[(xpos, ypos)] = what
        except StopIteration:
            pass
        return nsteps

    def score(self):
        "Return player score"
        return self.screen.get((-1, 0), None)

    def render(self, width=40, height=40):
        "Show screen"
        screen = [[' ' for _ in range(width)] for _ in range(height)]
        score = 0
        for (x, y), tile in self.screen.items():
            if x == -1 and y == 0:
                score = tile
            else:
                screen[y][x] = self.tiles[tile]
        print("\n".join(["".join(row) for row in screen]))
        print("Score: " + str(score))


class ArtificialIntelligence:
    "Solver for game"

    def __init__(self):
        self.player_x = 0
        self.ball_x = 0
        self.command = 0

    def update(self, xpos, what):
        "Update commands"
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


class ArcadeGameAI(ArcadeGame):
    "Arcade cabinet"

    def __init__(self):
        super().__init__()

        with open("input", "r") as fin:
            program = fin.read()
        program = "2" + program[1:]  # Insert coin
        self.cpu = IntcodeComputer(program)
        self.ai = ArtificialIntelligence()

    def run(self):
        "Simulate arcade cabinet"
        try:
            while True:
                xpos = self.cpu.step(self.ai.command)
                ypos = self.cpu.step(self.ai.command)
                what = self.cpu.step(self.ai.command)
                self.ai.update(xpos, what)

                self.screen[(xpos, ypos)] = what
        except StopIteration:
            pass


def star1():
    "Solution to first star"
    game = ArcadeGame()
    game.run()

    print("Star 1:", sum([1 for x in game.screen.values() if x == 2]))


def star2():
    "Solution to second star"
    game = ArcadeGameAI()
    game.run()

    print("Star 2:", game.score())


if __name__ == "__main__":
    star1()
    star2()
