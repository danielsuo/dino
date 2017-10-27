import dino
import numpy as np

import pyarrow.plasma as plasma
import pyarrow as pa
import timeit

v1 = dino.Vertex()
v2 = dino.Vertex()
v3 = dino.Vertex()

def createMatrix(n: int = 0) -> np.ndarray:
    return np.random.rand(n, n)

def transposeMatrix(mat: np.ndarray = np.random.rand(0, 0)) -> np.ndarray:
    return np.transpose(mat)

def multiplyMatrix(mat1: np.ndarray, mat2: np.ndarray) -> np.ndarray:
    return np.matmul(mat1, mat2)

v1.setFunction(createMatrix)
v2.setFunction(transposeMatrix)
v3.setFunction(multiplyMatrix)

print(v2.run(v1.run(10)))

g = dino.Graph()
g.addVertices(v1, v2, v3)
g.addEdge(v1, v2, 'mat')
g.addEdge(v1, v3, 'mat1')
g.addEdge(v2, v3, 'mat2')

# This should fail
#  g.addEdge(v2, v3, 'mat')
# This should fail
#  g.addEdge(v2, v1, 'mat')
print(g)
print(g.getSources())

#  g.removeEdge(v1, v2)
#  print(g)
#  print(g.getSources())

#  g.removeVertex(v3)
#  print(g)
#  print(g.getSources())

print('Running...')
g.run({0: 10})
