import typing
from .worker import Worker
from .task import Task

class Scheduler:
    def __init__(self, num_workers: int = 1) -> None:
        self.num_workers: int = num_workers

        self.workers: typing.List[Worker] = []
        for _ in range(num_workers):
            self.workers.append(Worker())

        self.next_queue: int = 0

    def schedule(self, task: Task) -> None:
        self.workers[self.next_queue].task_queue.put(task)
        self.next_queue = (self.next_queue + 1) % self.num_workers

    def start(self) -> None:
        for worker in self.workers:
            worker.start()

    def stop(self) -> None:
        for worker in self.workers:
            worker.stop()


