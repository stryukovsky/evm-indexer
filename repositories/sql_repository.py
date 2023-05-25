import abc
from sqlalchemy import Engine, Row


class SQLRepository(abc.ABC):
    engine: Engine

    def __init__(self, engine: Engine):
        self.engine = engine

    @abc.abstractmethod
    def list(self):
        pass

    @abc.abstractmethod
    def create(self, **kwargs):
        pass

    @staticmethod
    @abc.abstractmethod
    def row_to_instance(row: Row):
        pass
