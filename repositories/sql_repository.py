import abc
from typing import List, Type

from sqlalchemy import Engine, Row, select, insert
from database import Base as BaseModel


class SQLRepository(abc.ABC):
    engine: Engine
    model: Type[BaseModel]

    def __init__(self, model: Type[BaseModel], engine: Engine):
        self.engine = engine
        self.model = model

    def list(self) -> List[Type[BaseModel]]:
        with self.engine.connect() as connection:
            expression = select(self.model)
            rows = connection.execute(expression).fetchall()
            return list(map(self.row_to_instance, rows))

    def create(self, **kwargs):
        with self.engine.connect() as connection:
            expression = insert(self.model).values(kwargs)
            connection.execute(expression)
            connection.commit()

    @staticmethod
    @abc.abstractmethod
    def row_to_instance(row: Row):
        pass
