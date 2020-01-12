"Day 23: Category Six"

from intcodecomputer import IntcodeComputer, InputNeeded, OutputReady


class QueuedComputer(IntcodeComputer):
    "Intcodecomputer with Network interface"

    def __init__(self, idx=0):
        with open("input") as fhandle:
            super().__init__(fhandle.readline())

        self.idx = 0
        self.inqueue.append(idx)

    def send(self, xdata, ydata):
        "Send data to this computer"
        self.inqueue.append(xdata)
        self.inqueue.append(ydata)


class Network():
    "Network of computers with NAT controller"

    def __init__(self, ncpus=50):
        self.cpus = []
        self.natbuffer = None
        self.seenpackets = set()
        self.delay = ncpus*100  # Delay before checking death of network

        for idx in range(ncpus):
            self.cpus.append(QueuedComputer(idx=idx))

    def run(self, restart=False):
        "Run network"
        seen = set()
        while True:
            self.delay -= 1

            if self.delay == 0:
                self.delay = len(self.cpus)*100
                xdata, ydata = self.natbuffer
                if (xdata, ydata) in seen:
                    return
                self.natbuffer = None
                seen.add((xdata, ydata))
                self.cpus[0].inqueue.append(xdata)
                self.cpus[0].inqueue.append(ydata)

            for cpu in self.cpus:
                try:
                    cpu.step()
                except InputNeeded:
                    cpu.inqueue.append(-1)  # No input available
                except OutputReady:
                    if len(cpu.outqueue) >= 3:
                        addr = cpu.outqueue.popleft()
                        xdata = cpu.outqueue.popleft()
                        ydata = cpu.outqueue.popleft()
                        if addr == 255:
                            self.natbuffer = (xdata, ydata)
                            if not restart:
                                return
                        else:
                            self.cpus[addr].send(xdata, ydata)


def star1():
    "Solution to first star"
    net = Network()
    net.run()
    print("Star 1:", net.natbuffer[1])


def star2():
    "Solution to second star"
    net = Network()
    net.run(restart=True)
    print("Star 2:", net.natbuffer[1])


if __name__ == "__main__":
    star1()
    star2()
