from pydantic import BaseModel
from pydantic import validator
from .utils import validate_positive, validate_url, validate_enum
from database import NetworkType

NETWORK_TYPES = [element.value for element in NetworkType]


class CreateNetworkForm(BaseModel):
    chain_id: int
    name: str
    rpc_url: str
    max_step: int
    type: str
    need_poa: bool

    @validator("chain_id")
    def validate_chain_id(cls, value: int) -> int:
        return validate_positive("chain_id", value)

    @validator("rpc_url")
    def validate_rpc_url(cls, value: str) -> str:
        return validate_url("rpc_url", value)

    @validator("max_step")
    def validate_max_step(cls, value: int) -> int:
        return validate_positive("max_step", value)

    @validator("type")
    def validate_type(cls, value: str) -> str:
        return validate_enum("type", NETWORK_TYPES, value)
