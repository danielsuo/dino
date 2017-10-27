from .vertex import Vertex

class Graph:
    def __init__(self):
        self.vertices: typing.Dict[int, Vertex] = {}
        self.edges: typing.Dict[int, typing.List[int]] = {}

    def addVertex(self, vertex: Vertex) -> None:
        self.vertices[vertex.id] = vertex

        # Don't delete edges if vertex existed before
        if vertex.id not in self.edges:
            self.edges[vertex.id] = []

    def addVertices(self, *vertices: Vertex) -> None:
        for vertex in vertices:
            self.addVertex(vertex)

    def removeVertex(self, vertex: Vertex) -> None:
        self.checkVertex(vertex.id)
        for vid2 in self.edges:
            self.removeEdge(self.vertices[vid2], vertex)

        del self.vertices[vertex.id]
        del self.edges[vertex.id]

    def removeVertices(self, *vertices: Vertex) -> None:
        for vertex in vertices:
            self.removeVertex(vertex)

    def addEdge(self, v1: Vertex, v2: Vertex) -> None:
        self.checkVertex(v1.id)
        self.checkVertex(v2.id)

        if v2.id not in self.edges[v1.id]:
            self.edges[v1.id].append(v2.id)

    def removeEdge(self, v1: Vertex, v2: Vertex) -> None:
        self.checkVertex(v1.id)
        self.checkVertex(v2.id)

        # This could be a no-op
        if v1.id in self.edges:
            self.edges[v1.id] = list(filter(lambda x: x != v2.id, self.edges[v1.id]))

    def checkVertex(self, vid: int) -> None:
        assert vid in self.vertices, 'Vertex id %s not found in graph' % vid

    def __str__(self):
        return '\n'.join(['%d: %s' % (vid1, ','.join([str(vid2) for vid2 in self.edges[vid1]])) for vid1 in self.edges])
