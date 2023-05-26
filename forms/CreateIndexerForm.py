from .utils import validate_string_length, validate_positive
from pydantic import BaseModel, validator


class CreateIndexerForm(BaseModel):
    name: str
    last_block: int
    network: int

    @validator("name")
    def validate_name(cls, value: str) -> str:
        return validate_string_length("name", value)

    @validator("last_block")
    def validate_last_block(cls, value: int) -> int:
        return validate_positive("last_block", value)

    @validator("network")
    def validate_chain_id(cls, value: int) -> int:
        return validate_positive("network", value)
