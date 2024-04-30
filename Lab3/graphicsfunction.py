import numpy as np


def getBarCor(x, y, x0, y0, x1, y1, x2, y2):
    det = (x1 - x2) * (y0 - y2) - (y1 - y2) * (x0 - x2)
    lamda0 = ((x1 - x2) * (y - y2) - (y1 - y2) * (x - x2)) / det
    lambda1 = ((x2 - x0) * (y - y0) - (y2 - y0) * (x - x0)) / det
    lambda2 = 1.0 - lamda0 - lambda1
    return lamda0, lambda1, lambda2


def _movPol(ax, ay, pol, width, height):
    # return [[(ax * i[0]) / i[2] + width, (ay * i[1]) / i[2] + height] for i in pol]
    return [[i[0], i[1]] for i in pol]


def drawTriangleShadow(img, pol, ax, ay, DEFAULT_COLOR, I0, I1, I2, zBuffer):
    movPol = pol
    xmin = max(0, min(movPol[0][0], movPol[1][0], movPol[2][0]))
    ymin = max(0, min(movPol[0][1], movPol[1][1], movPol[2][1]))
    xmax = min(len(img), max(movPol[0][0], movPol[1][0], movPol[2][0]) + 1)
    ymax = min(len(img[0]), max(movPol[0][1], movPol[1][1], movPol[2][1]) + 1)

    for x in range(int(xmin), min(int(xmax) + 1, len(img))):
        for y in range(int(ymin), min(int(ymax) + 1, len(img[0]))):
            barCor = getBarCor(x, y, movPol[0][0], movPol[0][1], movPol[1][0], movPol[1][1], movPol[2][0], movPol[2][1])
            zBuf = barCor[0] * (pol[0][2]) + barCor[1] * (pol[1][2]) + barCor[2] * (pol[2][2])
            if all(i >= 0 for i in barCor) and zBuffer[x][y] > zBuf:
                zBuffer[x][y] = zBuf
                img[x][y] = [max(-255*(barCor[0]*I0 + barCor[1]*I1 + barCor[2]*I2), 0),
                             max(-255*(barCor[0]*I0 + barCor[1]*I1 + barCor[2]*I2), 0),
                             max(-255*(barCor[0]*I0 + barCor[1]*I1 + barCor[2]*I2), 0)]

def drawTriangleTexture(img, pol, ax, ay, texture_array, texture, pol_texture, zBuffer):
    movPol = pol
    xmin = max(0, min(movPol[0][0], movPol[1][0], movPol[2][0]))
    ymin = max(0, min(movPol[0][1], movPol[1][1], movPol[2][1]))
    xmax = min(len(img), max(movPol[0][0], movPol[1][0], movPol[2][0]) + 1)
    ymax = min(len(img[0]), max(movPol[0][1], movPol[1][1], movPol[2][1]) + 1)

    for x in range(int(xmin), min(int(xmax) + 1, len(img))):
        for y in range(int(ymin), min(int(ymax) + 1, len(img[0]))):
            barCor = getBarCor(x, y, movPol[0][0], movPol[0][1], movPol[1][0], movPol[1][1], movPol[2][0], movPol[2][1])
            zBuf = barCor[0] * (pol[0][2]) + barCor[1] * (pol[1][2]) + barCor[2] * (pol[2][2])
            if all(i >= 0 for i in barCor) and zBuffer[x][y] > zBuf:
                zBuffer[x][y] = zBuf
                img[x][y] = texture_array[int(len(texture_array[0])*(barCor[0]*texture[pol_texture[0] - 1][1] + barCor[1]*texture[pol_texture[1] - 1][1] + barCor[2]*texture[pol_texture[2] - 1][1]))][int(len(texture_array)*(barCor[0]*texture[pol_texture[0] - 1][0] + barCor[1]*texture[pol_texture[1] - 1][0] + barCor[2]*texture[pol_texture[2] - 1][0]))]

def getNormal(pol):
    v1 = np.array([pol[1][0] - pol[0][0], pol[1][1] - pol[0][1], pol[1][2] - pol[0][2]])
    v2 = np.array([pol[2][0] - pol[1][0], pol[2][1] - pol[1][1], pol[2][2] - pol[1][2]])
    return np.cross(v1, v2)

# %%
