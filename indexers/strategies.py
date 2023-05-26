import abc
from typing import List, Dict

from .fetching_methods import AbstractFetchingMethod
from .token_actions import TokenAction


class AbstractStrategy(abc.ABC):
    strategy_params: Dict

    def __init__(self, strategy_params: Dict):
        self.strategy_params = strategy_params

    @abc.abstractmethod
    def start(self, token_actions: List[TokenAction]):
        pass


class RecipientStrategy(AbstractStrategy):

    def start(self, token_actions: List[TokenAction]):
        recipient = self.strategy_params.get("recipient")
        if not recipient:
            raise ValueError("Strategy has no `recipient` provided. Please add recipient address to the strategy dict")
        for action in token_actions:
            if action.recipient == recipient:
                print(str(action))


class SenderStrategy(AbstractStrategy):

    def start(self, token_actions: List[TokenAction]):
        raise NotImplementedError


class TokenScanStrategy(AbstractStrategy):

    def start(self, token_actions: List[TokenAction]):
        raise NotImplementedError


class TokenomicsStrategy(AbstractStrategy):

    def start(self, token_actions: List[TokenAction]):
        raise NotImplementedError
