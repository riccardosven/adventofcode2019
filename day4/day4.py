"Day 4: Secure Container"


def check1(password):
    "Check password according to given criteria"
    letters = list(str(password))
    repeated = False
    for i, _ in enumerate(letters):
        if i > 0 and letters[i-1] == letters[i]:  # Double
            repeated = True
        if i > 0 and letters[i-1] > letters[i]:  # Decreasing
            return False
    return repeated


def check2(password):
    "Check password according to given criteria"
    olddigit = 10
    olderdigit = 10
    repeated = set()

    while password:

        password, digit = divmod(password, 10)
        if digit > olddigit:  # Decreasing
            return False
        if digit == olddigit:  # Double digit
            repeated.add(digit)
        if digit == olddigit == olderdigit:  # Triple digit
            repeated.remove(digit)
        olderdigit, olddigit = olddigit, digit

    return bool(repeated)


def findpass(a=402328, b=864247, criterion=check1):
    "Find matching passwords in the given range"
    for num in range(a, b+1):
        if criterion(num):
            yield num


def tests():
    "Testcases"
    assert check1(111111)
    assert check1(122345)
    assert not check1(223450)
    assert not check1(123789)
    assert check1(123389)

    assert check2(112233)
    assert not check2(123444)
    assert check2(111122)


def star1():
    "Solution to first star"
    numpass = 0
    for _ in findpass():
        numpass += 1

    print("Star 1:", numpass)


def star2():
    "Solution to second star"
    numpass = 0
    for _ in findpass(criterion=check2):
        numpass += 1

    print("Star 2:", numpass)


if __name__ == "__main__":

    if __debug__:
        tests()

    star1()
    star2()
