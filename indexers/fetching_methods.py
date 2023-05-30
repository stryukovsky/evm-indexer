import abc
from typing import List, Callable, Type

from web3 import Web3
from web3.contract import Contract
from web3.contract.base_contract import BaseContractEvent
from web3.types import HexBytes

from database import Token, NetworkType, FUNGIBLE_TOKENS, NON_FUNGIBLE_TOKENS, ERC1155_TOKENS
from indexers.token_actions import TokenAction, FungibleTokenAction, NonFungibleTokenAction, ERC1155TokenAction


class AbstractFetchingMethod(abc.ABC):
    contract: Contract
    token: Token

    def __init__(self, contract: Contract, token: Token):
        self.contract = contract
        self.token = token

    @abc.abstractmethod
    def get_token_actions(self, from_block: int, to_block: int) -> List[TokenAction]:
        pass


class EventFetchingMethod(AbstractFetchingMethod):
    event: Type[BaseContractEvent]
    get_events_function: Callable[[int, int], List[TokenAction]]
    token_action_type: Type[TokenAction]
    network_type: str

    def __init__(self, contract: Contract, token: Token, target_event: str, network_type: str):
        self.event = contract.events[target_event]
        self.network_type = network_type

        self.token_action_type = self._get_token_action(token.type)
        super().__init__(contract, token)

    @staticmethod
    def _get_token_action(token_type: str) -> Type[TokenAction]:
        if token_type in FUNGIBLE_TOKENS:
            return FungibleTokenAction
        if token_type in NON_FUNGIBLE_TOKENS:
            return NonFungibleTokenAction
        if token_type in ERC1155_TOKENS:
            return ERC1155TokenAction

    @staticmethod
    def _get_token_event_hash(token_type: str) -> HexBytes:
        if token_type in FUNGIBLE_TOKENS:
            return Web3.keccak(text="Transfer(address,address,uint256)")
        if token_type in NON_FUNGIBLE_TOKENS:
            return Web3.keccak(text="Transfer(address,address,uint256)")
        if token_type in ERC1155_TOKENS:
            raise NotImplementedError()

    def get_token_actions(self, from_block: int, to_block: int) -> List[TokenAction]:
        if self.network_type == NetworkType.filterable:
            return self.__get_events_with_eth_filter(from_block, to_block)
        else:
            return self.__get_events_with_raw_filtering(from_block, to_block)

    def __get_events_with_eth_filter(self, from_block: int, to_block: int) -> List[TokenAction]:
        entries = self.event.create_filter(fromBlock=from_block, toBlock=to_block).get_all_entries()
        result = []
        for entry in entries:
            token_action = self.token_action_type.from_event_entry(entry)
            result.append(token_action)
        return result

    def __get_events_with_raw_filtering(self, from_block: int, to_block: int) -> List[TokenAction]:
        events = self.contract.w3.eth.get_logs(
            {'fromBlock': from_block, 'toBlock': to_block, 'address': self.contract.address})
        result = []
        for event in events:
            if token_action := self.token_action_type.from_raw_log(event):
                result.append(token_action)
        return result
