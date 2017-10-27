import dino
import numpy as np

v1 = dino.Vertex()
v2 = dino.Vertex()
v3 = dino.Vertex()

def createMatrix(n: int) -> np.ndarray:
    return np.random.rand(n, n)

def transposeMatrix(mat: np.ndarray) -> np.ndarray:
    return np.transpose(mat)

v1.function = createMatrix
v2.function = transposeMatrix

print(v2.run(v1.run(10)))

g = dino.Graph()
g.addVertices(v1, v2, v3)
g.addEdge(v1, v2)
g.addEdge(v1, v3)
g.addEdge(v2, v3)
g.addEdge(v2, v1)

g.removeEdge(v1, v2)
g.removeVertex(v3)
print(g)
