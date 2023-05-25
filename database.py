import enum
import math
import os

from sqlalchemy import create_engine, ForeignKey, Numeric, BigInteger, String, Enum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

DATABASE_URL = os.environ["DATABASE_URL"]
engine = create_engine(DATABASE_URL, echo=True)

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


class Network(Base):
    __tablename__ = "network"

    chain_id: Mapped[int] = mapped_column(BigInteger(), unique=True, primary_key=True)
    name: Mapped[str] = mapped_column(String())
    rpc_url: Mapped[str] = mapped_column(String())
    max_step: Mapped[int] = mapped_column(BigInteger(), default=DEFAULT_STEP)
    type: Mapped[str] = mapped_column(Enum(NetworkType))


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


Base.metadata.create_all(engine)
