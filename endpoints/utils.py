from database import FUNGIBLE_TOKENS, NON_FUNGIBLE_TOKENS, ERC1155_TOKENS
from database import fungible_balances_repository, nft_balances_repository, erc1155_balances_repository
from repositories.balances import SQLBalancesRepository


def get_repository_by_token_type(token_type: str) -> SQLBalancesRepository:
    if token_type in FUNGIBLE_TOKENS:
        return fungible_balances_repository
    elif token_type in NON_FUNGIBLE_TOKENS:
        return nft_balances_repository
    elif token_type in ERC1155_TOKENS:
        return erc1155_balances_repository
    raise ValueError(f"Bad type {token_type}. You should register it in database module")
