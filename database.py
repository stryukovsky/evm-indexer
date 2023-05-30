import enum
import math
import os

from sqlalchemy import create_engine, ForeignKey, Numeric, BigInteger, String, Enum, Integer, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

DATABASE_URL = os.environ["DATABASE_URL"]
engine = create_engine(DATABASE_URL)

INT256_PRECISION_DECIMALS = int(math.ceil(math.log10(2 ** 256)))
INT256_SCALE_DECIMALS = 0  # wei values has no decimal point
ETHEREUM_ADDRESS_LENGTH = 42
STRING_LENGTH = 255
DEFAULT_STEP = 1000


class Base(DeclarativeBase):
    pass

    def to_dict(self):
        result = {}
        for column in self.__table__.columns:
            name = column.name
            value = getattr(self, column.name)
            result[name] = value
        return result


class NetworkType(enum.Enum):
    filterable = "filterable"
    no_filters = "no_filters"


class TokenStrategy(enum.Enum):
    event_based_transfer = "event_based_transfer"
    receipt_based_transfer = "receipt_based_transfer"


class TokenType(enum.Enum):
    native = "native"
    erc20 = "erc20"
    erc721 = "erc721"
    erc777 = "erc777"
    erc1155 = "erc1155"


FUNGIBLE_TOKENS = [TokenType.native, TokenType.erc20, TokenType.erc777]
NON_FUNGIBLE_TOKENS = [TokenType.erc721]
ERC1155_TOKENS = [TokenType.erc1155]


class Network(Base):
    __tablename__ = "network"

    chain_id: Mapped[int] = mapped_column(BigInteger(), unique=True, primary_key=True)
    name: Mapped[str] = mapped_column(String())
    rpc_url: Mapped[str] = mapped_column(String())
    max_step: Mapped[int] = mapped_column(BigInteger(), default=DEFAULT_STEP)
    type: Mapped[str] = mapped_column(Enum(NetworkType))
    need_poa: Mapped[bool] = mapped_column(Boolean, default=False)


class Indexer(Base):
    __tablename__ = "indexer"

    name: Mapped[str] = mapped_column(String(), unique=True, primary_key=True)
    last_block: Mapped[int] = mapped_column(BigInteger(), default=0)

    network: Mapped[int] = mapped_column(ForeignKey("network.chain_id"))

    def to_dict(self):
        return {
            "name": self.name,
            "last_block": self.last_block,
            "network": self.network
        }


class Token(Base):
    __tablename__ = "token"

    address: Mapped[str] = mapped_column(String(ETHEREUM_ADDRESS_LENGTH), unique=True, nullable=True, primary_key=True)
    name: Mapped[str] = mapped_column(String(STRING_LENGTH))
    strategy: Mapped[str] = mapped_column(Enum(TokenStrategy))
    network: Mapped[int] = mapped_column(ForeignKey("network.chain_id"))
    type: Mapped[str] = mapped_column(Enum(TokenType))

    total_supply: Mapped[int] = mapped_column(Numeric(scale=INT256_SCALE_DECIMALS, precision=INT256_PRECISION_DECIMALS),
                                              default=0)
    volume: Mapped[int] = mapped_column(Numeric(scale=INT256_SCALE_DECIMALS, precision=INT256_PRECISION_DECIMALS),
                                        default=0)

    def to_dict(self):
        return {
            "address": self.address,
            "name": self.name,
            "strategy": self.strategy.value,
            "network": self.network,
            "type": self.type.value,
            "tracking_params": {
                "total_supply": str(self.total_supply),
                "volume": str(self.volume),
            }
        }


class HolderType(enum.Enum):
    externally_owned_account = "externally_owned_account"
    contract_account = "contract_account"


class Holder(Base):
    __tablename__ = "holder"
    address: Mapped[str] = mapped_column(String(ETHEREUM_ADDRESS_LENGTH), unique=True, primary_key=True)

    type: Mapped[str] = mapped_column(Enum(HolderType))
    name: Mapped[str] = mapped_column(String(STRING_LENGTH))

    def to_dict(self):
        return {
            "address": self.address,
            "name": self.name,
            "type": self.type.value,
        }


class FungibleBalance(Base):
    __tablename__ = "fungible_balance"
    id: Mapped[int] = mapped_column(Integer(), primary_key=True)

    holder: Mapped[str] = mapped_column(ForeignKey("holder.address"))
    token: Mapped[str] = mapped_column(ForeignKey("token.address"))

    amount: Mapped[int] = mapped_column(Numeric(precision=INT256_PRECISION_DECIMALS, scale=INT256_SCALE_DECIMALS),
                                        default=0)

    def to_dict(self):
        return {
            "holder": self.holder,
            "token": self.token,
            "amount": int(self.amount),
        }


class NFTBalance(Base):
    __tablename__ = "non_fungible_balance"
    id: Mapped[int] = mapped_column(Integer(), primary_key=True)

    holder: Mapped[str] = mapped_column(ForeignKey("holder.address"))
    token: Mapped[str] = mapped_column(ForeignKey("token.address"))

    token_id: Mapped[int] = mapped_column(Numeric(precision=INT256_PRECISION_DECIMALS, scale=INT256_SCALE_DECIMALS))

    def to_dict(self):
        return {
            "holder": self.holder,
            "token": self.token,
            "token_id": int(self.token_id),
        }


class ERC1155Balance(Base):
    __tablename__ = "erc1155_balance"
    id: Mapped[int] = mapped_column(Integer(), primary_key=True)

    holder: Mapped[str] = mapped_column(ForeignKey("holder.address"))
    token: Mapped[str] = mapped_column(ForeignKey("token.address"))

    amount: Mapped[int] = mapped_column(Numeric(precision=INT256_PRECISION_DECIMALS, scale=INT256_SCALE_DECIMALS))
    token_id: Mapped[int] = mapped_column(Numeric(precision=INT256_PRECISION_DECIMALS, scale=INT256_SCALE_DECIMALS))

    def to_dict(self):
        return {
            "holder": self.holder,
            "token": self.token,
            "amount": int(self.amount),
            "token_id": int(self.token_id),
        }


Base.metadata.create_all(engine)

from repositories.balances import SQLFungibleBalancesRepository, SQLNFTBalancesRepository, SQLERC1155BalancesRepository
from repositories.holders import SQLHoldersRepository
from repositories.networks import SQLNetworksRepository
from repositories.tokens import SQLTokensRepository
from repositories.indexers import SQLIndexersRepository

networks_repository = SQLNetworksRepository(Network, engine)
tokens_repository = SQLTokensRepository(Token, engine)
holders_repository = SQLHoldersRepository(Holder, engine)
fungible_balances_repository = SQLFungibleBalancesRepository(FungibleBalance, engine)
nft_balances_repository = SQLNFTBalancesRepository(NFTBalance, engine)
erc1155_balances_repository = SQLERC1155BalancesRepository(ERC1155Balance, engine)
indexers_repository = SQLIndexersRepository(Indexer, engine)
