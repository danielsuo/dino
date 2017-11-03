import dino
import time
import click
import typing
import glog as log
import pathos.multiprocessing as mp
import pathos.helpers as mph
import numpy as np

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

        return 1

    args = [1,2,3]
    kwargs = {'blah': 1, 'c': 3}
    task1 = dino.Task(test, *args, **kwargs)
    task2 = dino.Task(lambda x: x * 10, 1)

    #  graph = dino.examples.graph_simple()

    #  results: typing.Dict[dino.types.vname, typing.any] = {}
    #  order: typing.List[dino.Vertex] = graph.getTopological()
    #  data = {'v1': {'mat': np.random.rand(100, 100)}}
    #  sources: typing.Dict[dino.types.vname, dino.Vertex] = graph.getSources()

    #  for name in sources:
        #  assert name in data, 'Data for source vertex %s not found' % name

    #  for dst in order:
        #  args: typing.Dict[dino.types.vname, typing.Any] = {}
        #  if dst.name in sources:
            #  args = data[dst.name]
        #  else:
            #  srcs = graph.getDependencies(dst.name)
            #  for src in srcs:
                #  args[graph.edges[src][dst]] = results[src]
            #  results[dst]



    scheduler.schedule(task1, task2)
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

