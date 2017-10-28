import typing
from .vertex import Vertex
from .types import vname, argname

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
        self.vertices: typing.Dict[vname, Vertex] = {}
        self.edges: typing.Dict[vname, typing.Dict[vname, argname]] = {}

    def addVertex(self, name: vname, function: typing.Callable) -> None:
        assert name not in self.vertices, 'Vertex named %s already in graph' % name

        self.vertices[name] = Vertex(name, function)

        # Don't delete edges if vertex existed before
        if name not in self.edges:
            self.edges[name] = {}

    def removeVertex(self, name: vname) -> None:
        self.checkVertex(name)
        for src in self.edges:
            self.removeEdge(src, name)

        del self.vertices[name]
        del self.edges[name]

    def removeVertices(self, *names: vname) -> None:
        for name in names:
            self.removeVertex(name)

    def addEdge(self, src: vname, dst: vname, arg: argname) -> None:
        self.checkVertex(src)
        self.checkVertex(dst)

        assert arg in self.vertices[dst].args, 'Vertex %s output to vertex %s with arg %s does not exist' % (src, dst, arg)
        assert arg not in self.getFulfilledArgs(dst), 'Arg %s already fulfilled for vertex %s' % (arg, dst)

        if dst not in self.edges[src]:
            self.edges[src][dst] = arg

    def removeEdge(self, src: vname, dst: vname) -> None:
        self.checkVertex(src)
        self.checkVertex(dst)

        # This could be a no-op
        if src in self.edges and dst in self.edges[src]:
            del self.edges[src][dst]

    def checkVertex(self, name: vname) -> None:
        assert name in self.vertices, 'Vertex id %s not found in graph' % name

    # TODO: this should probably be computed, stored, and updated appropriately
    def getSources(self) -> typing.Dict[vname, Vertex]:
        sources: typing.Dict[vname, Vertex] = {}
        names: typing.Set[vname] = set()

        for name in self.edges:
            names.update(self.edges[name].keys())

        names = set(self.vertices.keys()).difference(names)

        sources = {name: self.vertices[name] for name in names}
        return sources

    # TODO: this should probably be computed, stored, and updated appropriately
    def getSinks(self) -> typing.Dict[vname, Vertex]:
        sinks: typing.Dict[vname, Vertex] = {}

        for vname in self.vertices:
            if vname not in self.edges or len(self.edges[vname]) == 0:
                sinks[vname] = self.vertices[vname]

        assert len(sinks) == 1, 'For now, only support one and only one sink'

        return sinks

    # TODO: this should probably be computed, stored, and updated appropriately
    def getDependencies(self, dst: vname) -> typing.List[vname]:
        dependencies: typing.List[vname] = []

        for src in self.edges:
            if dst in self.edges[src]:
                dependencies.append(src)

        return dependencies

    def getFulfilledArgs(self, dst: vname) -> typing.List[vname]:
        fulfilled: typing.List[vname] = []

        for src in self.edges:
            if dst in self.edges[src]:
                fulfilled.append(self.edges[src][dst])

        return fulfilled

    def run(self, data: typing.Dict[vname, typing.Any]) -> typing.Any:
        # TODO: check all vertices fulfilled
        sources = self.getSources()

        for name in sources:
            assert name in data, 'Data for source vertex %s not found' % name

        results: typing.Dict[vname, typing.Any] = {}

        # TODO: for now, run in topological order
        order = topological(self.edges)

        for dst in order:
            args: typing.Dict[vname, typing.Any] = {}
            if dst in sources:
                args = data[dst]
            else:
                srcs = self.getDependencies(dst)
                for src in srcs:
                    args[self.edges[src][dst]] = results[src]
            results[dst] = self.vertices[dst].run(**args)

        return results

    def __str__(self):
        return '\n'.join(['%s: %s' % (src, ','.join([str(dst) for dst in self.edges[src]])) for src in self.edges])
