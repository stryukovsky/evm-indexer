import abc
import dataclasses
from typing import Type, Dict, List, Optional, Sequence

from web3.types import ChecksumAddress, HexStr, HexBytes, LogReceipt
from web3 import Web3


@dataclasses.dataclass
class TokenAction(abc.ABC):
    sender: ChecksumAddress
    recipient: ChecksumAddress
    tx_hash: HexStr

    @staticmethod
    @abc.abstractmethod
    def from_event_entry(event_entry: Dict):
        raise NotImplementedError()

    @classmethod
    @abc.abstractmethod
    def from_raw_log(cls, event: LogReceipt) -> Optional["TokenAction"]:
        raise NotImplementedError()

    @classmethod
    def _bytes32_to_address(cls, value: HexBytes) -> ChecksumAddress:
        return Web3.to_checksum_address(value.hex()[26:])

    @classmethod
    def _bytes32_to_uint256(cls, value: HexBytes) -> int:
        return int.from_bytes(value, byteorder="big")


@dataclasses.dataclass
class FungibleTokenAction(TokenAction):
    event_hash = Web3.keccak(text="Transfer(address,address,uint256)")
    amount: int

    @classmethod
    def from_raw_log(cls, event: LogReceipt) \
            -> Optional["FungibleTokenAction"]:
        if event["topics"][0] != cls.event_hash:
            return None
        return FungibleTokenAction(sender=cls._bytes32_to_address(event["topics"][1]),
                                   recipient=cls._bytes32_to_address(event["topics"][2]),
                                   tx_hash=HexStr(event["transactionHash"].hex()),
                                   amount=cls._bytes32_to_uint256(HexBytes(event["data"])))

    @staticmethod
    def from_event_entry(event_entry: Dict) -> "FungibleTokenAction":
        return FungibleTokenAction(event_entry["args"]["from"], event_entry["args"]["to"],
                                   event_entry["transactionHash"].hex(), event_entry["args"]["value"])

    def __str__(self):
        return f"Tokens {self.amount} sent {self.sender} -> {self.recipient}"


@dataclasses.dataclass
class NonFungibleTokenAction(TokenAction):
    event_hash = Web3.keccak(text="Transfer(address,address,uint256)")
    token_id: int

    @classmethod
    def from_raw_log(cls, event: LogReceipt) -> Optional["TokenAction"]:
        if event["topics"][0] != cls.event_hash:
            return None
        return NonFungibleTokenAction(sender=cls._bytes32_to_address(event["topics"][1]),
                                      recipient=cls._bytes32_to_address(event["topics"][2]),
                                      tx_hash=HexStr(event["transactionHash"].hex()),
                                      token_id=cls._bytes32_to_uint256(HexBytes(event["data"])))

    @staticmethod
    def from_event_entry(event_entry: Dict) -> "NonFungibleTokenAction":
        return NonFungibleTokenAction(event_entry["args"]["from"], event_entry["args"]["to"],
                                      event_entry["transactionHash"].hex(), event_entry["args"]["tokenId"])

    def __str__(self):
        return f"Token {self.token_id} sent {self.sender} -> {self.recipient}"


@dataclasses.dataclass
class ERC1155TokenAction(FungibleTokenAction, NonFungibleTokenAction):
    pass
