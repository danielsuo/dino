class Task:
    tid = 0
    def __init__(self, func, *args, **kwargs):
        self.id = Task.tid

        self.func = func
        self.args = args
        self.kwargs = kwargs

        Task.tid += 1
