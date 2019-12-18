import numpy as np

def decodeimage(string, width=25, height=6):
    image = np.array([int(c) for c in string if c.isnumeric()])
    image = np.reshape(image,(-1,6,25))
    print(image)
    return list(image)



def analyze(layers):
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
    imout = [[2 for _ in range(25)] for _ in range(6)]
    for layer in layers:
        for j,row in enumerate(layer):
            for i,pixel in enumerate(row):
                if imout[j][i] == 2:
                    imout[j][i] = pixel

    for row in imout:
        print(" ".join([str(c) for c in row]))
            





if __name__ == "__main__":
    with open("input","r") as imagein:
        layers = decodeimage(imagein.readline())
        output = analyze(layers)


        render(layers)

