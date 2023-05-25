import abc
from abc import ABC
from typing import Optional, List

from sqlalchemy import select, Row, Executable

from database import FungibleBalance, NFTBalance, ERC1155Balance, Base as BaseModel
from .sql_repository import SQLRepository


class BalancesRepository(abc.ABC):
    @abc.abstractmethod
    def get_balance(self, token: str, holder: str) -> Optional[BaseModel]:
        pass

    @abc.abstractmethod
    def get_held_tokens(self, holder: str) -> List[BaseModel]:
        pass


class SQLBalancesRepository(BalancesRepository, SQLRepository, ABC):
    def get_balance(self, token: str, holder: str) -> Optional[BaseModel]:
        with self.engine.connect() as connection:
            expression = self._expression_get_balance(token, holder)
            if not (row := connection.execute(expression).first()):
                return None
            return self.row_to_instance(row)

    def get_held_tokens(self, holder: str) -> List[BaseModel]:
        with self.engine.connect() as connection:
            expression = self._expression_get_held_tokens(holder)
            rows = connection.execute(expression).fetchall()
            return list(map(self.row_to_instance, rows))

    @staticmethod
    @abc.abstractmethod
    def _expression_get_balance(token: str, holder: str) -> Executable:
        pass

    @staticmethod
    @abc.abstractmethod
    def _expression_get_held_tokens(holder: str) -> Executable:
        pass


class SQLFungibleBalancesRepository(SQLBalancesRepository):

    @staticmethod
    def _expression_get_held_tokens(holder: str) -> Executable:
        return select(FungibleBalance).where(FungibleBalance.holder == holder)

    @staticmethod
    def _expression_get_balance(token: str, holder: str) -> Executable:
        return select(FungibleBalance) \
            .where(FungibleBalance.token == token) \
            .where(FungibleBalance.holder == holder)

    @staticmethod
    def row_to_instance(row: Row) -> FungibleBalance:
        return FungibleBalance(id=row[0], holder=row[1], token=row[2], amount=row[3])


class SQLNFTBalancesRepository(SQLBalancesRepository):
    @staticmethod
    def _expression_get_held_tokens(holder: str) -> Executable:
        return select(NFTBalance).where(NFTBalance.holder == holder)

    @staticmethod
    def _expression_get_balance(token: str, holder: str) -> Executable:
        return select(NFTBalance) \
            .where(NFTBalance.token == token) \
            .where(NFTBalance.holder == holder)

    @staticmethod
    def row_to_instance(row: Row) -> NFTBalance:
        return NFTBalance(id=row[0], holder=row[1], token=row[2], token_id=row[3])


class SQLERC1155BalancesRepository(SQLBalancesRepository):

    @staticmethod
    def _expression_get_held_tokens(holder: str) -> Executable:
        return select(ERC1155Balance).where(ERC1155Balance.holder == holder)

    @staticmethod
    def _expression_get_balance(token: str, holder: str) -> Executable:
        return select(ERC1155Balance) \
            .where(ERC1155Balance.token == token) \
            .where(ERC1155Balance.holder == holder)

    @staticmethod
    def row_to_instance(row: Row) -> ERC1155Balance:
        return ERC1155Balance(id=row[0], holder=row[1], token=row[2], amount=row[3], token_id=row[4])
