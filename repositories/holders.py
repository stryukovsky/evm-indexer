import abc
from typing import Optional

from sqlalchemy import Row, select

from database import Holder, Token, TokenType
from .sql_repository import SQLRepository


class HoldersRepository(abc.ABC):
    pass


class SQLHoldersRepository(HoldersRepository, SQLRepository):

    def get_by_address(self, address: str) -> Optional[Holder]:
        with self.engine.connect() as connection:
            expression = select(Holder).where(Holder.address == address)
            if not (row := connection.execute(expression).first()):
                return None
            return self.row_to_instance(row)

    @staticmethod
    def row_to_instance(row: Row):
        return Holder(address=row[0], type=row[1], name=row[2])
