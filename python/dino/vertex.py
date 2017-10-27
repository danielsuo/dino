import time
import typing
import glog as log

class Vertex:
    vid: int = 0

    def __init__(self) -> None:
        self.function = lambda args: 1 / 0
        self.id: int = Vertex.vid
        Vertex.vid += 1

    def run(self, *data: typing.Any) -> typing.Any:
        beg = time.time()
        result = self.function(*data)
        end = time.time()
        log.info('Vertex %d took %sms' % (self.id, '{:,.2f}'.format((end - beg) * 1000)))
        return result

    def __str__(self):
        return str(self.id)
