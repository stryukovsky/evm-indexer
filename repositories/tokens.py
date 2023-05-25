import abc
from typing import List, Optional

from sqlalchemy import Row, select, insert, func

from database import Token
from .sql_repository import SQLRepository


class TokensRepository(abc.ABC):

    @abc.abstractmethod
    def get_tokens_at_network(self, chain_id: int) -> List[Token]:
        pass

    @abc.abstractmethod
    def get_by_address(self, address: str) -> Optional[Token]:
        pass


class SQLTokensRepository(TokensRepository, SQLRepository):
    def get_tokens_at_network(self, chain_id: int) -> List[Token]:
        with self.engine.connect() as connection:
            expression = select(Token).where(Token.network == chain_id)
            rows = connection.execute(expression).fetchall()
            return list(map(self.row_to_instance, rows))

    def get_by_address(self, address: str) -> Optional[Token]:
        with self.engine.connect() as connection:
            expression = select(Token).where(func.lower(Token.address) == address.lower())
            if not (row := connection.execute(expression).first()):
                return None
            return self.row_to_instance(row)

    def list(self) -> List[Token]:
        with self.engine.connect() as connection:
            expression = select(Token)
            rows = connection.execute(expression).fetchall()
            return list(map(self.row_to_instance, rows))

    def create(self, **kwargs):
        with self.engine.connect() as connection:
            expression = insert(Token).values(kwargs)
            connection.execute(expression)
            connection.commit()

    @staticmethod
    def row_to_instance(row: Row) -> Token:
        return Token(address=row[0], name=row[1], strategy=row[2], network=row[3], type=row[4], total_supply=row[5],
                     volume=row[6])
