from .utils import validate_eth_address, validate_string_length, validate_enum
from pydantic import BaseModel, validator
from database import HolderType

HOLDER_TYPE = [element.value for element in HolderType]


class CreateHolderForm(BaseModel):
    address: str
    type: str
    name: str

    @validator("address")
    def validate_address(cls, value: str) -> str:
        return validate_eth_address("address", value)

    @validator("type")
    def validate_type(cls, value: str) -> str:
        return validate_enum("type", HOLDER_TYPE, value)

    @validator("name")
    def validate_name(cls, value: str) -> str:
        return validate_string_length("name", value)
