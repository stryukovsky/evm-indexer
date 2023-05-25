from typing import Optional

from pydantic import BaseModel
from pydantic import validator

from database import TokenStrategy, TokenType
from .utils import validate_eth_address, validate_string_length, validate_enum, validate_non_negative

TOKEN_STRATEGY = [element.value for element in TokenStrategy]
TOKEN_TYPE = [element.value for element in TokenType]


class CreateTokenForm(BaseModel):
    address: str
    name: str
    strategy: str
    network: str
    type: str

    @validator("address")
    def validate_address(cls, value: str) -> str:
        return validate_eth_address("address", value)

    @validator("name")
    def validate_name(cls, value: str) -> str:
        return validate_string_length("name", value)

    @validator("strategy")
    def validate_strategy(cls, value: str) -> str:
        return validate_enum("strategy", TOKEN_STRATEGY, value)

    @validator("type")
    def validate_type(cls, value: str) -> str:
        return validate_enum("type", TOKEN_TYPE, value)
