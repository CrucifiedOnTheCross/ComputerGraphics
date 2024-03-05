class ObjModel:
    def __init__(self):
        self.vertex = []
        self.polygons = []

    def readModel(self, file: str):
        try:
            with open(file, 'r') as obj:
                for line in obj:
                    if line.startswith('v '):
                        x, y, z = map(float, line.split()[1:])
                        self.vertex.append((x, y, z))
                    elif line.startswith('f '):
                        vertices = [int(v.split('/')[0]) for v in line.split()[1:]]
                        self.polygons.append(vertices)
        except FileNotFoundError:
            print(f"File '{file}' not found.")

    def getVertexFromPolygon(self, polygon):
        return [self.vertex[v - 1] for v in polygon]


def movePoint(point, scale, move):
    return [point[i] * scale + move[i] for i in range(len(point))]


def movePol(pol, scale, move):
    return [movePoint(pol[i], scale, move) for i in range(len(pol))]
