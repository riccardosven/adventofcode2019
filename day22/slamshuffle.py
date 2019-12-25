import numpy as np
import sys

class Deck:
    def __init__(self, ncards = 10007):
        self.ncards = ncards
        self.cards = np.array(range(ncards), dtype=np.uint8)
    
    def newstack(self):
        self.cards = np.flip(self.cards)
    
    def cutn(self, n):
        self.cards = np.roll(self.cards, -n)
    
    def dealincrement(self, n):
        newcards = np.zeros(self.ncards, dtype=np.uint8)
        for i in range(self.ncards):
            newcards[(n*i)%self.ncards] = self.cards[i]
        self.cards = newcards
    
    def __str__(self):
        return ",".join(map(str, self.cards))

    def applyinstruction(self, instruction):

        if not instruction:
            return

        fields = instruction.split(" ")

        if fields[-2] == "cut":
            self.cutn(int(fields[-1]))
        elif fields[-2] == "increment":
            self.dealincrement(int(fields[-1]))
        elif fields[-2] == "new":
            self.newstack()

    @staticmethod
    def from_instructions(instructions, ncards=10007):
        deck = Deck(ncards)

        for instruction in instructions:
            deck.applyinstruction(instruction)
        
        return deck







def test():
    cards = Deck(ncards=10)
    cards.newstack()
    #cards = Deck.from_instructions("deal into new stack".split("\n"))
    assert str(cards) == "9,8,7,6,5,4,3,2,1,0"

    cards = Deck(ncards=10)
    cards.newstack()
    cards.newstack()
    assert str(cards) == "0,1,2,3,4,5,6,7,8,9"

    cards = Deck(ncards=10)
    cards.cutn(3)
    assert str(cards) == "3,4,5,6,7,8,9,0,1,2"

    cards = Deck(ncards=10)
    cards.cutn(-4)
    assert str(cards) == "6,7,8,9,0,1,2,3,4,5"

    cards = Deck(ncards=10)
    cards.dealincrement(3)
    assert str(cards) == "0,7,4,1,8,5,2,9,6,3"


def test1():
    deck = Deck.from_instructions("""deal with increment 7
deal into new stack
deal into new stack
""".split("\n"), ncards=10)
    assert str(deck) == "0,3,6,9,2,5,8,1,4,7"

    deck = Deck.from_instructions("""cut 6
deal with increment 7
deal into new stack
""".split("\n"),ncards = 10)
    assert str(deck) == "3,0,7,4,1,8,5,2,9,6"

    deck = Deck.from_instructions("""deal with increment 7
deal with increment 9
cut -2
""".split("\n"), ncards=10)
    assert str(deck) == "6,3,0,7,4,1,8,5,2,9"

    deck = Deck.from_instructions("""deal into new stack
cut -2
deal with increment 7
cut 8
cut -4
deal with increment 7
cut 3
deal with increment 9
deal with increment 3
cut -1""".split("\n"), ncards=10)
    assert str(deck) == "9,2,5,8,1,4,7,0,3,6"


def main():
    deck = Deck()
    with open(sys.argv[1]) as fhandle:
        deck = Deck.from_instructions(fhandle.readlines())
    print(np.where(deck.cards == 2019))


def main2():
    deck = Deck(ncards=119315717514047)
    for _ in range(101741582076661):
        with open(sys.argv[1]) as fhandle:
            for instruction in fhandle.readlines():
                deck.applyinstruction(instruction)

    print(np.where(deck.cards == 2020))

    for card in deck.cards:
     print(card)



#if __name__ == "__main__":
#    main2()

import collections
import math
import re
import sys

import sortedcollections

with open(sys.argv[1]) as f:
    lines = [l.rstrip('\n') for l in f]
    nlines = [[int(i) for i in re.findall(r'-?\d+', l)] for l in lines]

    ld = 10007
    deck = list(range(ld))
    for line, nline in zip(lines, nlines):
        if line.startswith('deal with increment'):
            ndeck = [0] * ld
            inc = nline[0]
            for i in range(ld):
                ndeck[i * inc % ld] = deck[i]
            assert len(set(ndeck)) == ld
        elif line.startswith('cut'):
            inc = nline[0]
            ndeck = deck[inc:] + deck[:inc]
        elif line == 'deal into new stack':
            ndeck = deck[::-1]
        else:
            assert False, line
        #print(line, deck.index(2019))
        deck = ndeck
    print(deck.index(2019))

    ld = 119315717514047
    card = 2020
    times = 101741582076661
    # ld, card, times = 10007, 7665, 1

    # q came from aq + b
    a = 1
    b = 0
    for line, nline in reversed(list(zip(lines, nlines))):
        if line.startswith('deal with increment'):
            inc = nline[0]
            #card = card * pow(inc, ld-2,ld) % ld
            p = pow(inc, ld-2,ld)
            a *= p
            b *= p
        elif line.startswith('cut'):
            inc = nline[0]
            #card = (card - inc + ld) % ld
            b += inc
        elif line == 'deal into new stack':
            #card = ld - 1 - card
            b += 1
            a *= -1
            b *= -1
        else:
            assert False, line
        a %= ld
        b %= ld
        # print(line, (a * card + b) % ld)

    # q
    # aq + b
    # a(aq+b) + b = a^2q + ab + b
    # a(a^2q + ab + b) = a^3q + a^2b + ab + b
    # ...
    # a^t q + b * (a^t - 1) / (a - 1)
    print((
        pow(a, times, ld) * card +
        b * (pow(a, times, ld) +ld- 1)
          * (pow(a-1, ld - 2, ld))
    ) % ld)
