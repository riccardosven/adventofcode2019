"Day 14: Space Stoichiometry"

import re
import math
from collections import defaultdict


class ReactionTable:
    "Table of reactions"

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
        "Return amount of ore needed to produce product"

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

    def oretoproduce(self, fuelamount):
        "Find the ore required to produce a certain amount of fuel"

        left = 0
        right = fuelamount

        while left < right:  # Uses bisection search
            mid = (left + right)//2
            orerequired = self.produce((mid, "FUEL"))
            if orerequired > fuelamount:
                right = mid
            else:
                left = mid + 1
        return left - 1


def tests():
    testcases1 = [("test1", 165), ("test2",
                                   13312),  ("test3", 180697), ("test4", 2210736)]
    for test, exp in testcases1:
        assert exp == ReactionTable(test).produce((1, "FUEL"))

    testcases2 = [("test2", 82892753), ("test3", 5586022), ("test4", 460664)]

    for test, exp in testcases2:
        assert exp == ReactionTable(test).oretoproduce(1000000000000)


def star1():
    "Solution to first star"
    print("Star 1:", ReactionTable("input").produce((1, "FUEL")))


def star2():
    "Solution to second star"
    print("Star 2:", ReactionTable("input").oretoproduce(1000000000000))


if __name__ == "__main__":
    tests()
    star1()
    star2()