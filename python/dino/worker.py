import pathos.multiprocessing as mp
import pathos.helpers as mph
import glog as log

class Worker(mph.mp.Process):
    def __init__(self, task_queue, result_queue):
        mph.mp.Process.__init__(self)
        self.task_queue = task_queue
        self.result_queue = result_queue

    def run(self):
        while True:
            next_task = self.task_queue.get()
            if next_task is None:
                # Received poison pill
                log.info('%s: Exiting' % self.name)
                break

            next_task()

        return


