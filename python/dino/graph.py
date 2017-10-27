import typing
from .vertex import Vertex

from collections import deque

GRAY, BLACK = 0, 1

def topological(graph):
    order, enter, state = deque(), set(graph), {}

    def dfs(node):
        state[node] = GRAY
        for k in graph.get(node, ()):
            sk = state.get(k, None)
            if sk == GRAY: raise ValueError("cycle")
            if sk == BLACK: continue
            enter.discard(k)
            dfs(k)
        order.appendleft(node)
        state[node] = BLACK

    while enter: dfs(enter.pop())
    return order

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

    # TODO: this should probably be computed, stored, and updated appropriately
    def getSources(self) -> typing.Dict[int, Vertex]:
        sources: typing.Dict[int, Vertex] = {}
        vids = set()

        for vid in self.edges:
            vids.update(self.edges[vid])

        vids = set(self.vertices.keys()).difference(vids)

        sources = {vid: self.vertices[vid] for vid in vids}
        return sources

    # TODO: this should probably be computed, stored, and updated appropriately
    def getSinks(self) -> typing.Dict[int, Vertex]:
        sinks: typing.Dict[int, Vertex] = {}

        for vid in self.vertices:
            if vid not in self.edges or len(self.edges[vid]) == 0:
                sinks[vid] = self.vertices[vid]

        assert len(sinks) == 1, 'For now, only support one and only one sink'

        return sinks

    # TODO: this should probably be computed, stored, and updated appropriately
    def getDependencies(self, vid: int) -> typing.List[int]:
        dependencies = []
        for vid2 in self.edges:
            if vid in self.edges[vid2]:
                dependencies.append(vid2)

        return dependencies


    def run(self, data: typing.Dict[int, Vertex]) -> typing.Any:
        sources = self.getSources()

        for vid in sources:
            assert vid in data, 'Data for source vertex %d not found' % vid

        results = {}

        # TODO: for now, run in topological order
        order = topological(self.edges)

        #  for vid in order:
            # TODO: rewrite vertices function to take dictionary
            # TODO: eventually want to decouple vertex function and how it's hooked up
            #  results[vid] = self.vertices.function()

        return

    def __str__(self):
        return '\n'.join(['%d: %s' % (vid1, ','.join([str(vid2) for vid2 in self.edges[vid1]])) for vid1 in self.edges])
