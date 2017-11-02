import dino
import click
import glog as log
import pathos.multiprocessing as mp
import pathos.helpers as mph

import dino.examples

@click.group(context_settings=dict(help_option_names=['-h', '--help']))
def cli():
    """Hello! Welcome to Dino!"""

@cli.command()
def graph():
    """
    Simple graph construction
    """

    dino.examples.graph_simple()


@cli.command()
@click.option('-n', '--num-workers', default=1, type=int, help='number of workers')
def worker(num_workers):
    """
    Passing functions and data to workers
    """
    click.echo('Hi worker %d!' % num_workers)

    scheduler = dino.Scheduler(num_workers)
    scheduler.start()

    def test(*args, **kwargs):
        for arg in args:
            print(arg)
        for kwarg in kwargs:
            print('%s: %s' % (str(kwarg), str(kwargs[kwarg])))

    args = [1,2,3]
    kwargs = {'blah': 1, 'c': 3}
    task = dino.Task(test, *args, **kwargs)

    scheduler.schedule(task)
    scheduler.stop()

    #  task_queues = []
    #  result_queues = []
    #  workers = []

    #  for i in range(num_workers):
        #  worker = dino.Worker()
        #  worker.start()

        #  def test(): print('hello from worker %d!' % i)
        #  worker.task_queue.put(test)
        #  worker.task_queue.put(None)

