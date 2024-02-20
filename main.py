class ObjModel:
    def __init__(self):
        self.vertex = []

    def readModel(self, file: str):
        with open(file, 'r') as obj:
            data = obj.read()

        lines = data.splitlines()
        self.vertex = []

        for line in lines:
            elem = line.split()
            if elem and elem[0] == 'v':
                self.vertex.append((float(elem[1]), float(elem[2]), float(elem[3])))


obj = ObjModel()
obj.readModel('model_1.obj')
print(obj.vertex)
# %%
