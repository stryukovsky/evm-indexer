from typing import List
from urllib.parse import urlparse

from web3 import Web3
from database import STRING_LENGTH


def validate_non_negative(field: str, value: int) -> int:
    if value < 0:
        raise ValueError(f"Bad non-negative {value} at {field} field")
    return value


def validate_positive(field: str, value: int) -> int:
    if value <= 0:
        raise ValueError(f"Bad positive {value} at {field} field")
    return value


def validate_eth_address(field: str, value: str) -> str:
    try:
        return Web3.to_checksum_address(value)
    except Exception:
        raise ValueError(f"Bad Ethereum address {value} at {field} field")


def validate_url(field: str, value: str) -> str:
    try:
        urlparse(value)
        return value
    except Exception:
        raise ValueError(f"Bad url {value} at {field} field")


def validate_enum(field: str, values: List[str], value: str) -> str:
    if value not in values:
        raise ValueError(f"Bad choice for {field}. Expected one of {values}")
    return value


def validate_string_length(field: str, value: str) -> str:
    if len(value) > STRING_LENGTH:
        raise ValueError(f"Bad length of {value} at {field} field")
    return value
