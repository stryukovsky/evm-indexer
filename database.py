import enum
import os

from sqlalchemy import create_engine, ForeignKey, Numeric, BigInteger, String, Enum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

DATABASE_URL = os.environ["DATABASE_URL"]
engine = create_engine(DATABASE_URL, echo=True)


class Base(DeclarativeBase):
    pass


class NetworkType(enum.Enum):
    filterable = "filterable"
    no_filters = "no_filters"


class Network(Base):
    __tablename__ = "network"

    chain_id: Mapped[int] = mapped_column(BigInteger(), unique=True, primary_key=True)
    name: Mapped[str] = mapped_column(String())
    rpc_url: Mapped[str] = mapped_column(String())
    max_step: Mapped[int] = mapped_column(BigInteger(), default=1000)
    type: Mapped[str] = mapped_column(Enum(NetworkType))


Base.metadata.create_all(engine)
