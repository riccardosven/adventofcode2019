import re
import math
from collections import defaultdict


class ReactionTable:
    def __init__(self, infile):
        regex = re.compile(r"(\d+) (\w+)")
        reactiontable = dict()

        with open(infile, "r") as fin:
            for line in fin.readlines():
                reagents, products = line.split("=>")
                reagents = regex.findall(reagents)
                product_amount, product = regex.findall(products)[0]

                reactiontable[product] = (int(product_amount), [
                                          (int(amt), reag) for amt, reag in reagents])

        self.reactiontable = reactiontable
        self.storage = defaultdict(int)

    def produce(self, product):

        amount, name = product
        ore = 0

        produced, reagents = self.reactiontable[name]
        multiplier = math.ceil(amount/produced)

        for reagent in reagents:
            input_amount, input_name = reagent
            if input_name == "ORE":
                ore += multiplier*input_amount
                continue
            if not input_name in self.storage:
                self.storage[input_name] = 0

            if self.storage[input_name] < multiplier*input_amount:
                ore += self.produce((multiplier*input_amount -
                                     self.storage[input_name], input_name))
            self.storage[input_name] -= multiplier*input_amount

        if not name in self.storage:
            self.storage[name] = 0

        self.storage[name] += multiplier*produced

        return ore

    def oretoproduce(self, amount):
        left = 0
        right = amount

        while left < right:
            mid = (left + right)//2
            orerequired = self.produce((mid, "FUEL"))
            if orerequired > amount:
                right = mid
            else:
                left = mid + 1
        return left - 1


def stage1(infile, expect=None):
    table = ReactionTable(infile)
    print("Needed ", table.produce((1, "FUEL")), end="")
    if not expect is None:
        print("expected ", expect)
    else:
        print()


def stage2(infile, expect=None):
    table = ReactionTable(infile)
    print("Produced", table.oretoproduce(1000000000000), "fuel", end="")
    if not expect is None:
        print("expected ", expect)
    else:
        print


if __name__ == "__main__":
    if __debug__:
        stage1("test1", expect=165)
        stage1("test2", expect=13312)
        stage1("test3", expect=180697)
        stage1("test4", expect=2210736)

        stage2("test2", expect=82892753)
        stage2("test3", expect=5586022)
        stage2("test4", expect=460664)
    else:
        stage1("input")
        stage2("input")
