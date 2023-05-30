import json
import time
from typing import Dict, List, Type

from database import (
    Network,
    Token,
    TokenType,
    Indexer,
    networks_repository,
    tokens_repository,
    indexers_repository
)
from indexers.strategies import AbstractStrategy, RecipientStrategy
from indexers.fetching_methods import AbstractFetchingMethod
from web3.contract import Contract
from web3 import Web3
from .fetching_methods import EventFetchingMethod, AbstractFetchingMethod
import enum
from web3.middleware import geth_poa_middleware


class FetchingMethodType(enum.Enum):
    event = "event"
    receipt = "receipt"


class Strategy(enum.Enum):
    recipient = "recipient"
    sender = "sender"


class Worker:
    indexer: Indexer
    network: Network
    token: Token
    contract: Contract
    w3: Web3
    fetching_method: AbstractFetchingMethod
    strategy: AbstractStrategy

    def __init__(self, indexer_name: str, contract_address: str, fetching_method: str, strategy: str,
                 strategy_params: dict):
        self.indexer = indexers_repository.get_by_name(indexer_name)
        self.network = networks_repository.get_by_chain_id(self.indexer.network)
        self.w3 = Web3(Web3.HTTPProvider(self.network.rpc_url))
        self.token = tokens_repository.get_by_address(self.w3.to_checksum_address(contract_address))
        if self.network.need_poa:
            self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        self.contract = self.build_contract(self.token)
        self.fetching_method = self.build_token_action_method(fetching_method)
        self.strategy = self.build_strategy(strategy, strategy_params)

    def cycle(self):
        while True:
            self.indexer = indexers_repository.get_by_name(self.indexer.name)
            latest_block = self.w3.eth.get_block("latest")["number"]
            from_block = self.indexer.last_block
            to_block = min(from_block + self.network.max_step, latest_block)
            print(f"Fetching transfers [{from_block}; {to_block}]")
            token_actions = self.fetching_method.get_token_actions(from_block, to_block)
            self.strategy.start(token_actions)
            indexers_repository.set_last_block(self.indexer.name, to_block)
            time.sleep(1)

    def build_contract(self, token: Token) -> Contract:
        abi = self._get_abi(token.type)
        address = token.address
        return self.w3.eth.contract(address=address, abi=abi)

    @staticmethod
    def _get_abi(token_type: TokenType) -> List[Dict]:
        if token_type == TokenType.erc20:
            with open("abi/ERC20.json") as file:
                return json.load(file)
        if token_type == TokenType.erc721.value:
            with open("abi/ERC721.json") as file:
                return json.load(file)
        raise ValueError(f"Unknown token type or token's ABI not provided in `abi` folder: {token_type}")

    @staticmethod
    def _get_target_event(token_type: TokenType) -> str:
        if token_type == TokenType.erc20:
            return "Transfer"
        if token_type == TokenType.erc721:
            return "Transfer"
        raise ValueError(f"Unknown token type or type not implemented {token_type.value}")

    def build_token_action_method(self, fetching_method: str) -> AbstractFetchingMethod:
        if fetching_method == FetchingMethodType.event.value:
            return EventFetchingMethod(self.contract, self.token, self._get_target_event(self.token.type),
                                       self.network.type)
        if fetching_method == FetchingMethodType.receipt:
            assert False
        raise ValueError(f"Not implemented {fetching_method}")

    @staticmethod
    def build_strategy(strategy: str, strategy_params: Dict) -> AbstractStrategy:
        if strategy == Strategy.recipient.value:
            return RecipientStrategy(strategy_params)
        raise ValueError(f"Not implemented strategy {strategy}")
