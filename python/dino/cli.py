import dino
import click
import numpy as np
import glog as log
import pathos.multiprocessing as mp
import pathos.helpers as mph

@click.group(context_settings=dict(help_option_names=['-h', '--help']))
def cli():
    """Hello! Welcome to Dino!"""

@cli.command()
def graph():
    """
    Simple graph construction
    """

    def forwardMatrix(mat: np.ndarray):
        return mat

    def createMatrix(n: int) -> np.ndarray:
        return np.random.rand(n, n)

    def transposeMatrix(mat: np.ndarray) -> np.ndarray:
        return np.transpose(mat)

    def multiplyMatrix(mat1: np.ndarray, mat2: np.ndarray) -> np.ndarray:
        return np.matmul(mat1, mat2)

    g = dino.Graph()
    g.addVertex('v1', forwardMatrix)
    g.addVertex('v2', transposeMatrix)
    g.addVertex('v3', multiplyMatrix)
    g.addEdge('v1', 'v2', 'mat')
    g.addEdge('v1', 'v3', 'mat1')
    g.addEdge('v2', 'v3', 'mat2')

    print(g)
    print(g.getSources())

    print('Running...')
    mat = np.random.rand(100, 100)
    results = g.run({'v1': {'mat': mat}})

    print(np.array_equal(results['v3'], np.matmul(mat, np.transpose(mat))))

@cli.command()
@click.option('-n', '--num-workers', default=1, type=int, help='number of workers')
def worker(num_workers):
    """
    Passing functions and data to workers
    """
    click.echo('Hi worker %d!' % num_workers)

    task_queues = []
    result_queues = []
    workers = []

    for _ in range(num_workers):
        task_queue = mph.mp.Queue()
        result_queue = mph.mp.Queue()
        worker = dino.Worker(task_queue, result_queue)
        worker.start()

        def test(): print('hello from worker!')
        task_queue.put(test)
        task_queue.put(None)

