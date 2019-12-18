def fuel(mass):
    return mass//3 - 2

def process(mass):
    f_mass = fuel(int(mass))
    f_add = fuel(f_mass)
    while f_add > 0:
        f_mass += f_add
        f_add = fuel(f_add)
    
    return f_mass
if __name__ == "__main__":
    total = 0 
    if __debug__:
        print(process(1969))
        print(process(100756))
    else:
        with open("input", "r") as fin:
            for line in fin:
                f_mass = process(line)
                total += f_mass

        print(total)


