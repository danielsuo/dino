import time
import typing
import inspect
import glog as log

# TODO: eventually want to decouple vertex function and how it's hooked up
class Vertex:
    vid: int = 0

    def __init__(self) -> None:
        self.function: typing.Callable = None
        self.args: typing.List[str] = []
        self.id: int = Vertex.vid
        Vertex.vid += 1

    def run(self, *args, **kwargs) -> typing.Any:
        beg = time.time()
        result = self.function(*args, **kwargs)
        end = time.time()
        log.info('Vertex %d took %sms' %
                 (self.id, '{:,.2f}'.format((end - beg) * 1000)))
        return result

    def setFunction(self, function):
        self.function = function
        self.args = inspect.getfullargspec(self.function).args

    def __str__(self):
        return str(self.id)
