import time
import typing
import inspect
import glog as log

from .types import vname, argname

# TODO: eventually want to decouple vertex function and how it's hooked up
class Vertex:
    vid: int = 0

    def __init__(self, name: vname, function: typing.Callable) -> None:
        self.name = name
        self.function = function
        self.args = inspect.getfullargspec(self.function).args
        self.id: int = Vertex.vid
        Vertex.vid += 1

    def run(self, *args, **kwargs) -> typing.Any:
        beg = time.time()
        result = self.function(*args, **kwargs)
        end = time.time()
        log.info('Vertex %d took %sms' %
                 (self.id, '{:,.2f}'.format((end - beg) * 1000)))
        return result

    def __str__(self):
        return str(self.id)
