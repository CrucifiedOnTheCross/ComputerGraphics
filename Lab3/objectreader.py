import numpy as np


class ObjModel:
    def __init__(self):
        self.vertex = []
        self.polygons = []
        self.texture = []
        self.normal = []
        self.polygons_texture = []
        
        textureFlag = False
        normalFlag = False

        self.minx = float('inf')
        self.miny = float('inf')
        self.maxx = float('-inf')
        self.maxy = float('-inf')
        self.maxz = float('inf')
        self.minz = float('-inf')

    def readModel(self, file: str):
        try:
            with open(file, 'r') as obj:
                for line in obj:
                    if line.startswith('v '):
                        x, y, z = map(float, line.split()[1:])
                        self.vertex.append([x, y, z])

                        self.minx = min(self.minx, x)
                        self.miny = min(self.miny, y)
                        self.maxx = max(self.maxx, x)
                        self.maxy = max(self.maxy, y)
                        self.minz = min(self.maxx, z)
                        self.maxz = max(self.maxy, z)
                    elif line.startswith('f '):
                        pol = []
                        pol_t = []
                        pol_n = []
                        for v in line.split()[1:]:
                            ar = v.split('/') 
                            pol.append(int(ar[0]))
                            pol_t.append(int(ar[1]))
                            pol_n.append(int(ar[2]))
                        for i in range(1, len(pol)-1):
                            self.polygons.append([pol[0], pol[i], pol[i+1]])
                            self.polygons_texture.append([pol_t[0], pol_t[i], pol_t[i+1]])
                            #self.polygons_normal.append([pol_n[0], pol_n[i], pol_n[i+1]])
                        
                    elif line.startswith('vt '):
                        x, y = map(float, line.split()[1:3])
                        self.texture.append([x, y])
                        
                    elif line.startswith('vn '):
                        x, y, z = map(float, line.split()[1:])
                        self.normal.append([x, y, z])

        except FileNotFoundError:
            print(f"File '{file}' not found.")

    def getVertexFromPolygon(self, polygon):
        return [self.vertex[v - 1] for v in polygon]

    def scaleObjToImgOld(self, width, height, scaleFactor=1):
        widthObj, heightObj = self.maxx - self.minx, self.maxy - self.miny

        self.minx = min([i[0] for i in self.vertex])
        self.miny = min([i[1] for i in self.vertex])
        self.maxx = max([i[0] for i in self.vertex])
        self.maxy = max([i[1] for i in self.vertex])

        scale = min(width / widthObj, height / heightObj) * scaleFactor
        move = ((width - widthObj * scale) / 2 - self.minx * scale,
                (height - heightObj * scale) / 2 - self.miny * scale, 0)
        return scale, move

    def rotateObj(self, xangle, yangle, zangle):
        xangle_rad = np.radians(xangle)
        yangle_rad = np.radians(yangle)
        zangle_rad = np.radians(zangle)

        rotation_x = np.array([[1, 0, 0],
                               [0, np.cos(xangle_rad), np.sin(xangle_rad)],
                               [0, -np.sin(xangle_rad), np.cos(xangle_rad)]])

        rotation_y = np.array([[np.cos(yangle_rad), 0, np.sin(yangle_rad)],
                               [0, 1, 0],
                               [-np.sin(yangle_rad), 0, np.cos(yangle_rad)]])

        rotation_z = np.array([[np.cos(zangle_rad), np.sin(zangle_rad), 0],
                               [-np.sin(zangle_rad), np.cos(zangle_rad), 0],
                               [0, 0, 1]])

        rotation_matrix = np.dot(rotation_x, np.dot(rotation_y, rotation_z))

        for i in range(len(self.vertex)):
            self.vertex[i] = np.dot(rotation_matrix, self.vertex[i])
            self.normal[i] = np.dot(rotation_matrix, self.normal[i])

        self.minx = min([v[0] for v in self.vertex])
        self.miny = min([v[1] for v in self.vertex])
        self.maxx = max([v[0] for v in self.vertex])
        self.maxy = max([v[1] for v in self.vertex])
        self.minz = min([v[2] for v in self.vertex])
        self.maxz = max([v[2] for v in self.vertex])

        

    def moveObj(self, moveVector):
        for i in range(len(self.vertex)):
            self.vertex[i][0] += moveVector[0]
            self.vertex[i][1] += moveVector[1]
            self.vertex[i][2] += moveVector[2]

def movePoint(point, scale, move):
    return [point[i] * scale + move[i] for i in range(len(point))]


def movePol(pol, scale, move):
    return [movePoint(pol[i], scale, move) for i in range(len(pol))]

# %%
