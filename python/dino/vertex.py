import typing

class Vertex:
    def __init__(self) -> None:
        # TODO: Lol, this doesn't do anything except say we have a function
        # TODO: I suppose if we were serious, we'd use TypeVar and Generic to
        # do some type parameterization
        self.function: typing.Callable[[typing.Any], typing.Any]

    def run(self, data: typing.Any) -> typing.Any:
        return self.function(data)
