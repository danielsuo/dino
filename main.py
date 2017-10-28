import dino
import numpy as np

import pyarrow.plasma as plasma
import pyarrow as pa
import timeit

def createMatrix(n: int = 0) -> np.ndarray:
    return np.random.rand(n, n)

def transposeMatrix(mat: np.ndarray = np.random.rand(0, 0)) -> np.ndarray:
    return np.transpose(mat)

def multiplyMatrix(mat1: np.ndarray, mat2: np.ndarray) -> np.ndarray:
    return np.matmul(mat1, mat2)

g = dino.Graph()
g.addVertex('v1', createMatrix)
g.addVertex('v2', transposeMatrix)
g.addVertex('v3', multiplyMatrix)
g.addEdge('v1', 'v2', 'mat')
g.addEdge('v1', 'v3', 'mat1')
g.addEdge('v2', 'v3', 'mat2')

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
g.run({'v1': 10})
