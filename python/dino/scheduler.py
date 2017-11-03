import typing
import select
import threading
import pathos.helpers as mph

from .worker import Worker
from .task import Task

class Scheduler:
    def __init__(self, num_workers: int = 1) -> None:
        self.num_workers: int = num_workers

        self.result_queue = mph.mp.Queue()
        self.result_thread = threading.Thread(target=self.handle_results)

        self.workers: typing.List[Worker] = []
        for _ in range(num_workers):
            self.workers.append(Worker(self.result_queue))

        self.next_queue: int = 0

        self.tids: typing.Set[int] = set()

    def schedule(self, *tasks: Task) -> None:
        # Global round robin scheduling. Lol.
        for task in tasks:
            self.workers[self.next_queue].task_queue.put(task)
            self.next_queue = (self.next_queue + 1) % self.num_workers
            self.tids.add(task.id)

    # TODO: have some safety around start / stop
    def start(self) -> None:
        for worker in self.workers:
            worker.start()

        self.result_thread.start()

    def stop(self) -> None:
        for worker in self.workers:
            worker.stop()

        self.result_queue.put(None)

        # TODO: consider adding timeout
        self.result_thread.join()

    def handle_results(self) -> None:
        received_poison = False
        while True:
            result = self.result_queue.get()
            if result is None:
                if not self.tids:
                    break
                else:
                    received_poison = True
            else:
                self.tids.remove(result.tid)
                print(result.tid, result.data)

            if received_poison and not self.tids:
                break

