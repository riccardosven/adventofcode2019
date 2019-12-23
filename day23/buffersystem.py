# Buffered system of intcodecomputers
from collections import deque
from intcodecomputer import IntcodeComputer, InputNeeded, OutputReady

class QueuedComputer(IntcodeComputer):
    def __init__(self, idx=0):
        with open("input") as fhandle:
            super().__init__(fhandle.readline())

        self.idx = 0
        self.inqueue.append(idx)
    
    def send(self, xdata, ydata):
        self.inqueue.append(xdata)
        self.inqueue.append(ydata)
    
class Network():
    def __init__(self, ncpus=50):
        self.cpus = []
        self.natbuffer = None
        self.seenpackets = set()
        self.delay = ncpus*100
        
        for idx in range(ncpus):
            self.cpus.append(QueuedComputer(idx=idx))
    
    def run(self):
        seen = set()
        while True:
            self.delay -= 1

            if self.delay == 0:
                self.delay = len(self.cpus)*100
                xdata, ydata = self.natbuffer
                self.natbuffer = None
                if (xdata, ydata) in seen:
                    print("END:", xdata, ydata)
                    return
                seen.add((xdata, ydata))
                print(f"255 -> 0: ({xdata}, {ydata})")
                self.cpus[0].inqueue.append(xdata)
                self.cpus[0].inqueue.append(ydata)
            
            for cpu in self.cpus:
                try:
                    cpu.step()
                except InputNeeded:
                    cpu.inqueue.append(-1) # No input available
                except OutputReady:
                    if len(cpu.outqueue) >= 3:
                        addr = cpu.outqueue.popleft()
                        xdata = cpu.outqueue.popleft()
                        ydata = cpu.outqueue.popleft()
                        # print(f"{idx} -> {addr}: ({xdata}, {ydata})")
                        if addr == 255:
                            self.natbuffer = (xdata, ydata)
                        else:
                            self.cpus[addr].send(xdata, ydata)
                


if __name__ == "__main__":
    net = Network()
    net.run()