
def check(num):
    olddigit = 10
    olderigit = 10
    repeated = set()
    while num>0:
        num, digit = divmod(num, 10)
        if digit > olddigit:
            return False
        if digit == olddigit:
            repeated.add(digit)
        if digit == olddigit == olderdigit:
            repeated.remove(digit)
        olderdigit = olddigit
        olddigit = digit

    return repeated

def check2(num):
    letters = list(str(num))
    repeated = False
    for i, d in enumerate(letters):
        if i > 0 and letters[i-1] == letters[i]:
            repeated = True
        if i > 0 and letters[i-1] > letters[i]:
            return False
    return repeated

def findpass(a, b):
    for num in range(a, b+1):
        if check(num):
            yield num

if __name__ == "__main__":

    if __debug__:
        print(check(111111))
        print(check(223450))
        print(check(123789))
        print(check(123389))
    else:

        numpass = 0
        for num in findpass(402328, 864247):
            print(num)
            numpass += 1

        print(numpass)



