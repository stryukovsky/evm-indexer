from pydantic import validator
from pydantic import BaseModel
from .utils import validate_eth_address


class TokenBalanceForm(BaseModel):
    address: str
    holder: str

    @validator("address")
    def validate_address(cls, value: str) -> str:
        return validate_eth_address("address", value)

    @validator("holder")
    def validate_holder(cls, value: str) -> str:
        return validate_eth_address("holder", value)
