from fastapi import FastAPI
from database import engine, Network, Token, Holder, FungibleBalance, NFTBalance, ERC1155Balance

from repositories.networks import SQLNetworksRepository
from repositories.tokens import SQLTokensRepository
from repositories.holders import SQLHoldersRepository
from repositories.balances import SQLFungibleBalancesRepository, SQLNFTBalancesRepository, SQLERC1155BalancesRepository

app = FastAPI()

networks_repository = SQLNetworksRepository(Network, engine)
tokens_repository = SQLTokensRepository(Token, engine)
holders_repository = SQLHoldersRepository(Holder, engine)
fungible_balances_repository = SQLFungibleBalancesRepository(FungibleBalance, engine)
nft_balances_repository = SQLFungibleBalancesRepository(NFTBalance, engine)
erc1155_balances_repository = SQLFungibleBalancesRepository(ERC1155Balance, engine)

import endpoints.networks
import endpoints.tokens
import endpoints.holders
