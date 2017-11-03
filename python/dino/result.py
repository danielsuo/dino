import typing

class Result:
    rid = 0
    def __init__(self, tid: int, data: typing.Any) -> None:
        self.id = Result.rid
        self.tid = tid
        self.data = data

        Result.rid += 1
