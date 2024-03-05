import numpy as np


def getBarCor(x, y, x0, y0, x1, y1, x2, y2):
    lamda0 = ((x1 - x2) * (y - y2) - (y1 - y2) * (x - x2)) / ((x1 - x2) * (y0 - y2) - (y1 - y2) * (x0 - x2))
    lambda1 = ((x2 - x0) * (y - y0) - (y2 - y0) * (x - x0)) / ((x2 - x0) * (y1 - y0) - (y2 - y0) * (x1 - x0))
    lambda2 = 1.0 - lamda0 - lambda1
    return lamda0, lambda1, lambda2


def drawTriangle(img, pol, color, zBuffer):
    xmin = max(0, min(pol[0][0], pol[1][0], pol[2][0]))
    ymin = max(0, min(pol[0][1], pol[1][1], pol[2][1]))
    xmax = min(len(img), max(pol[0][0], pol[1][0], pol[2][0]))
    ymax = min(len(img[0]), max(pol[0][1], pol[1][1], pol[2][1]))

    for x in range(int(xmin), int(xmax) + 1):
        for y in range(int(ymin), int(ymax) + 1):
            barCor = getBarCor(x, y, pol[0][0], pol[0][1], pol[1][0], pol[1][1], pol[2][0], pol[2][1])
            zBuf = barCor[0] * pol[0][2] + barCor[1] * pol[1][2] + barCor[2] * pol[2][2]
            if all(i > 0 for i in barCor):
                if zBuffer[x][y] > zBuf:
                    zBuffer[x][y] = zBuf
                    img[x][y] = color

            # %%


def getNormal(pol):
    v1 = np.array([pol[1][0] - pol[0][0], pol[1][1] - pol[0][1], pol[1][2] - pol[0][2]])
    v2 = np.array([pol[2][0] - pol[1][0], pol[2][1] - pol[1][1], pol[2][2] - pol[1][2]])

    return np.cross(v1, v2)

# %%
