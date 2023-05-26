import abc
from typing import Optional

from sqlalchemy import Row

from database import Indexer
from .sql_repository import SQLRepository
from sqlalchemy import select


class IndexersRepository(abc.ABC):

    @abc.abstractmethod
    def get_by_name(self, name: str) -> Optional[Indexer]:
        pass


class SQLIndexersRepository(IndexersRepository, SQLRepository):
    def get_by_name(self, name: str) -> Optional[Indexer]:
        with self.engine.connect() as connection:
            expression = select(Indexer).where(Indexer.name == name)
            row = connection.execute(expression).first()
            if not row:
                return None
            return self.row_to_instance(row)

    @staticmethod
    def row_to_instance(row: Row) -> Indexer:
        return Indexer(name=row[0], last_block=row[1], network=row[2])
