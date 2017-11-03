import pathos.multiprocessing as mp
import pathos.helpers as mph
import glog as log
import psutil

from .task import Task
from .result import Result

class Worker(mph.mp.Process):
    wid = 0
    def __init__(self, result_queue):
        super(Worker, self).__init__()
        self.task_queue = mph.mp.Queue()
        self.result_queue = result_queue
        self.id = Worker.wid
        Worker.wid += 1

        self.running = False

    def run(self):
        while True:
            task: Task = self.task_queue.get()
            if task is None:
                # Received poison pill
                log.info('Worker %d: Exiting' % self.id)
                break
            data = task.func(*task.args, **task.kwargs)
            result = Result(task.id, data)
            self.result_queue.put(result)
        return

    def start(self):
        if not self.running:
            super(Worker, self).start()
            self.process = psutil.Process(self.pid)
            self.running = True
        else:
            log.warn('Worker %d: cannot start more than once' % self.id)

    def stop(self):
        if self.running:
            self.task_queue.put(None)
            self.running = False
        else:
            log.warn('Worker %d: cannot stop more than once' % self.id)

    def suspend(self):
        self.process.suspend()

    def resume(self):
        self.process.resume()


