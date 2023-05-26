import abc
import dataclasses
from typing import Type, Dict

from web3.types import ChecksumAddress, HexStr


@dataclasses.dataclass
class TokenAction(abc.ABC):
    sender: ChecksumAddress
    recipient: ChecksumAddress
    tx_hash: HexStr

    @staticmethod
    @abc.abstractmethod
    def from_event_entry(event_entry: Dict):
        raise NotImplementedError()


@dataclasses.dataclass
class FungibleTokenAction(TokenAction):
    amount: int

    @staticmethod
    def from_event_entry(event_entry: Dict) -> "FungibleTokenAction":
        return FungibleTokenAction(event_entry["args"]["from"], event_entry["args"]["to"],
                                   event_entry["transactionHash"].hex(), event_entry["args"]["value"])

    def __str__(self):
        return f"Tokens {self.amount} sent {self.sender} -> {self.recipient}"


@dataclasses.dataclass
class NonFungibleTokenAction(TokenAction):
    @staticmethod
    def from_event_entry(event_entry: Dict) -> "NonFungibleTokenAction":
        return NonFungibleTokenAction(event_entry["args"]["from"], event_entry["args"]["to"],
                                      event_entry["transactionHash"].hex(), event_entry["args"]["tokenId"])

    token_id: int

    def __str__(self):
        return f"Token {self.token_id} sent {self.sender} -> {self.recipient}"


@dataclasses.dataclass
class ERC1155TokenAction(FungibleTokenAction, NonFungibleTokenAction):
    pass
