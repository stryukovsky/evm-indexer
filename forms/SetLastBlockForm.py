from .utils import validate_positive
from pydantic import BaseModel, validator


class SetLastBlockForm(BaseModel):
    last_block: int

    @validator("last_block")
    def validate_last_block(cls, value: int) -> int:
        return validate_positive("last_block", value)
