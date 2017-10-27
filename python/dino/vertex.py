import typing

class Vertex:
    vid: int = 0

    def __init__(self) -> None:
        # TODO: Lol, this doesn't do anything except say we have a function
        # TODO: I suppose if we were serious, we'd use TypeVar and Generic to
        # do some type parameterization
        self.function: typing.Callable[[typing.Any], typing.Any]
        self.id: int = Vertex.vid
        Vertex.vid += 1

    def run(self, data: typing.Any) -> typing.Any:
        return self.function(data)

    def __str__(self):
        return str(self.id)
