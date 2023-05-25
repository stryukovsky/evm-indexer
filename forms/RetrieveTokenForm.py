from typing import Optional

from pydantic import BaseModel, validator
from .utils import validate_eth_address

NATIVE_TOKEN_STRING_IDENTIFIER = "native"


class RetrieveTokenForm(BaseModel):
    address: Optional[str]

    @validator("address")
    def validate_address(cls, value: Optional[str]) -> Optional[str]:
        if not value:
            raise ValueError("No address provided")
        if value == NATIVE_TOKEN_STRING_IDENTIFIER:
            return None
        return validate_eth_address("address", value)
