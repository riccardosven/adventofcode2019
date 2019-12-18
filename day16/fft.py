
from itertools import cycle
from copy import copy


def repeatingpattern(n):
    basepattern = [0, 1, 0, -1]
    start = 1
    for val in cycle(basepattern):
        for _ in range(start, n+1):
            yield val
        start = 0

def sparsepattern(n):
    i = n
    mul = 1
    while True:
        for _ in range(n+1):
            yield i, mul
            i += 1
        mul = -mul
        i += n + 1


def oldphasesum(inputlist, i):
    value = 0

    for ival, pval in zip(inputlist, cycle(repeatingpattern(i))):
        value += ival * pval

    return value

def phasesum(inputlist, i):
    value = 0

    for idx, mul in sparsepattern(i):
        if idx >= len(inputlist):
            return value
        value += mul*inputlist[idx] 
    


def decodesignal(signalstring):
    #out = []
    #while signal:
    #    signal, rem = divmod(signal, 10)
    #    out = [rem] + out
    return list(map(int, signalstring))


def applyfft(signalvector):
    outputvector = copy(signalvector)
    for i in range(len(outputvector)):
        val = abs(phasesum(signalvector, i)) % 10
        outputvector[i] = val
    return outputvector


def encodesignal(signalvector, length=8, skip=0):
    return "".join(map(str, signalvector[skip:skip+length]))


def handle(num, phase=100):
    num = decodesignal(num)
    for _ in range(0, phase):
        num = applyfft(num)

    return encodesignal(num)

def handlewithoffset(input_string):
    offset = int(input_string[:7], 10)
    input_list = list(map(int, input_string)) * 10000
    input_length = len(input_list)

    for i in range(100):
        partial_sum = sum(input_list[j] for j in range(offset, input_length))
        for j in range(offset, input_length):
            t = partial_sum
            partial_sum -= input_list[j]
            if t >= 0:
                input_list[j] = t % 10
            else:
                input_list[j] = (-t) % 10

                
    #print(input_list[offset: offset+8])
    return "".join(map(str, input_list[offset: offset+8]))



def test1():

    print(handle("12345678", phase=1), "48226158")
    print(handle("12345678", phase=2), "34040438")
    print(handle("12345678", phase=3), "03415518")
    print(handle("12345678", phase=4), "01029498")

    print(handle("80871224585914546619083218645595"), 24176176)
    print(handle("19617804207202209144916044189917"), 73745418)
    print(handle("69317163492948606335995924319873"), 52432133)

def test2():
    print(handlewithoffset('03036732577212944063491565474664'), 84462026)
    print(handlewithoffset('02935109699940807407585447034323'), 78725270)
    print(handlewithoffset('03081770884921959731165446850517'), 53553731)

def star1():
    print(handle("59762574510031092870627555978901048140761858379740610694074091049186715780458779281173757827279664853239780029412670100985236587608814782710381775353184676765362101185238452198186925468994552552398595814359309282056989047272499461615390684945613327635342384979527937787179298170470398889777345335944061895986118963644324482739546009761011573063020753536341827987918039441655270976866933694280743472164322345885084587955296513566305016045735446107160972309130456411097870723829697443958231034895802811058095753929607703384342912790841710546106752652278155618050157828313372657706962936077252259769356590996872429312866133190813912508915591107648889331"))

def star2():
    
    print(handlewithoffset("59762574510031092870627555978901048140761858379740610694074091049186715780458779281173757827279664853239780029412670100985236587608814782710381775353184676765362101185238452198186925468994552552398595814359309282056989047272499461615390684945613327635342384979527937787179298170470398889777345335944061895986118963644324482739546009761011573063020753536341827987918039441655270976866933694280743472164322345885084587955296513566305016045735446107160972309130456411097870723829697443958231034895802811058095753929607703384342912790841710546106752652278155618050157828313372657706962936077252259769356590996872429312866133190813912508915591107648889331"))

def testsparse():
    n = 0
    length = 10
    out1 = []
    for i, n1 in enumerate(repeatingpattern(n)):
        out1.append(n1)
        if i > length:
            break

    out2 = [0 for _ in range(len(out1))]
    for i, (idx, val) in enumerate(sparsepattern(n)):
        print(idx, val)
        if idx >= len(out2):
            break
        out2[idx] = val
    print(out1)
    print(out2)
    


if __name__ == "__main__":
    #test1()
    #star1()
    test2()
    star2()
    #testsparse()
