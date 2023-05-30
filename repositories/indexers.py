import abc
from typing import Optional

from sqlalchemy import Row

from database import Indexer
from .sql_repository import SQLRepository
from sqlalchemy import select, update


class IndexersRepository(abc.ABC):

    @abc.abstractmethod
    def get_by_name(self, name: str) -> Optional[Indexer]:
        pass

    @abc.abstractmethod
    def set_last_block(self, name: str, last_block: int):
        pass


class SQLIndexersRepository(IndexersRepository, SQLRepository):
    def set_last_block(self, name: str, last_block: int):
        with self.engine.connect() as connection:
            expression = update(Indexer).where(Indexer.name == name).values({
                "last_block": last_block
            })
            connection.execute(expression)
            connection.commit()

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
