"Day 1: The Tyranny of the Rocket Equation"


def fuel(mass):
    "Compute fuel required for launch mass"
    return mass//3 - 2


def fuel2(mass):
    "Compute fuel required to launch mass and fuel"
    f_mass = fuel(int(mass))
    f_add = fuel(f_mass)
    while f_add > 0:
        f_mass += f_add
        f_add = fuel(f_add)

    return f_mass


def tests():
    # For first star
    assert fuel(12) == 2
    assert fuel(14) == 2
    assert fuel(1969) == 654.
    assert fuel(100756) == 33583.

    # For second star
    assert fuel2(14) == 2
    assert fuel2(1969) == 966
    assert fuel2(100756) == 50346


def star1():
    "Answer to first star"
    totalfuel = 0
    with open("input") as fhandle:
        for line in fhandle:
            totalfuel += fuel(int(line))

    print("Star 1:", totalfuel)


def star2():
    "Answer to first star"
    totalfuel = 0
    with open("input") as fhandle:
        for line in fhandle:
            totalfuel += fuel2(int(line))
    print("Star 2:", totalfuel)


if __name__ == "__main__":
    if __debug__:
        tests()
    star1()
    star2()
