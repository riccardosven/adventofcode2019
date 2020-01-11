import numpy as np

def decodeimage(string, width=25, height=6):
    "Decode image from string"
    image = np.array([int(c) for c in string if c.isnumeric()])
    image = np.reshape(image, (-1, height, width))
    return list(image)


def analyze(layers):
    "Find layer with  most zero digits"
    out = [9999, 0, 0]
    for layer in layers:
        npixels = [0, 0, 0]
        for line in layer:
            for pixel in line:
                npixels[pixel] += 1
        if npixels[0] < out[0]:
            out = npixels
    return out

def render(layers):
    "Render visible image"
    imout = [[2 for _ in range(25)] for _ in range(6)]
    for layer in layers:
        for j, row in enumerate(layer):
            for i, pixel in enumerate(row):
                if imout[j][i] == 2:
                    imout[j][i] = pixel

    for row in imout:
        print(" ".join(["#" if c else "." for c in row]))
            


def star1():
    "Solution to first star"
    with open("input", "r") as imagein:
        layers = decodeimage(imagein.readline())
        output = analyze(layers)
    print("Star 1:",output[1] * output[2])

def star2():
    with open("input", "r") as imagein:
        layers = decodeimage(imagein.readline())
    print("Star 2:")
    render(layers)



if __name__ == "__main__":
    star1()
    star2()
