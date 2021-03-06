from intcodecomputer import IntcodeComputer

class VacuumRobot:
    "ASCIIRobot"
    def __init__(self):
        with open("input", 'r') as fhandle:
            program = fhandle.read().strip()
            self.map = None
            self.brain = IntcodeComputer(program)
    
    def getmap(self):
        "Explore area to find alignment parameters"
        view = []
        try:
            while True:
                char = chr(self.brain.step(None))
                view.append(char)
        except StopIteration:
            pass
        
        view = list("".join(view).strip().split("\n"))
        width = len(view[0])
        height = sum(1 for row in view if len(row) == len(view[0]))
        assert height == len(view)
        alignpar = 0
        
        for i in range(len(view)):
            for j in range(len(view[0])):
                if view[i][j] == "#":
                    neigbors = 0
                    neigbors += 1 if i > 0 and view[i-1][j] == "#" else 0
                    neigbors += 1 if i < height-1 and view[i+1][j] == "#" else 0
                    neigbors += 1 if j > 0 and view[i][j-1] == "#" else 0
                    neigbors += 1 if j < width-1 and view[i][j+1] == "#" else 0
                    if neigbors == 4:
                        alignpar += i*j
        
        self.map = view
        return alignpar

    def showmap(self):
        "print map from viewport"
        view = self.getmap()
        print("\n".join(["".join(row) for row in view]))

    def execute(self, instructions):
        for instruction in instructions:
            self.brain.step(ord(instruction))

    
    def override(self, program, funcA, funcB, funcC, video="y"):
        self.brain.code[0] = 2

        # Main Program
        self.execute(program)

        # Function A
        self.execute(funcA)

        # Function B
        self.execute(funcB)

        # Function C
        self.execute(funcC)

        # Video
        self.execute(video+"\n")

        while True:
            self.brain.step(0)




def star1():
    bot = VacuumRobot()
    print("Star 1:", bot.getmap())

def star2():
    bot = VacuumRobot()
    try:
        bot.override("A,B,A,C,B,C,A,C,B,C\n", "L,8,R,10,L,10\n", "R,10,L,8,L,8,L,10\n", "L,4,L,6,L,8,L,8\n")
    except StopIteration:
        pass
    print(bot.brain.outval)

if __name__ == "__main__":
    star1()
