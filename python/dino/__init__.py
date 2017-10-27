import glog as log
import typing
import json

from .vertex import Vertex
from .graph import Graph

class SubTask:
    def __init__(self, id_: str) -> None:
        self.id = id_
        self.src = typing.List[str]
        self.dst = typing.List[str]

    #  @classmethod
    #  def fromDefn(cls, defn: typing.Dict) -> 'SubTask':
        #  Assert that we have an id
        #  assert 'id' in defn, 'Missing id for subtask'

        #  subtask = cls(defn['id'])


class Task:
    def __init__(self, defn_file: str = None) -> None:
        self.subtasks: typing.List[str] = []
        self.graph: typing.Dict[str, typing.List[str]] = {}

        if defn_file is not None:
            self.load(defn_file)

    def load(self, defn_file: str) -> None:
        defn = json.load(open(defn_file, 'r'))

        # Assert that we have main information we need
        assert 'subtasks' in defn, 'Missing subtasks in definition file'
        assert 'graph' in defn, 'Missing graph in definition file'

        # Assert that subtasks is an array
        assert type(defn['subtasks']) is list, 'Subtasks must be an array'

        for subtask in defn['subtasks']:
            assert 'id' in subtask, 'Missing id for subtask %s' % subtask
            assert subtask['id'] in defn['graph'], 'Missing id in graph for subtask %s' % subtask['id']
            self.add(subtask['id'], defn['graph'][subtask['id']])

    def add(self, id_: str, dst: typing.List[str]) -> None:
        self.subtasks.append(id_)
        self.graph[id_] = dst


log.info("Hello! Welcome to Dino!")
a = Task('tasks/test.json')
print(a.graph['A'])
