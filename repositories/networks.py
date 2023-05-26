import abc
from abc import ABC
from typing import List, Optional

from sqlalchemy import Row, select, insert

from database import Network
from .sql_repository import SQLRepository


class NetworksRepository(ABC):
    @abc.abstractmethod
    def get_by_chain_id(self, chain_id: int) -> Optional[Network]:
        pass


class SQLNetworksRepository(NetworksRepository, SQLRepository):
    def list(self) -> List[Network]:
        with self.engine.connect() as connection:
            expression = select(Network)
            rows = connection.execute(expression).fetchall()
            return list(map(self.row_to_instance, rows))

    def create(self, **kwargs):
        with self.engine.connect() as connection:
            expression = insert(Network).values(**kwargs)
            connection.execute(expression)
            connection.commit()

    def get_by_chain_id(self, chain_id: int) -> Optional[Network]:
        with self.engine.connect() as connection:
            expression = select(Network).where(Network.chain_id == chain_id)
            if not (row := connection.execute(expression).first()):
                return None
            return self.row_to_instance(row)

    @staticmethod
    def row_to_instance(row: Row) -> Network:
        return Network(chain_id=row[0], name=row[1], rpc_url=row[2], max_step=row[3], type=row[4], need_poa=row[5])
