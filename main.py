from fastapi import FastAPI
from database import engine

from repositories.networks import SQLNetworksRepository
from repositories.tokens import SQLTokensRepository

app = FastAPI()

networks_repository = SQLNetworksRepository(engine)
tokens_repository = SQLTokensRepository(engine)

import endpoints.networks
import endpoints.tokens
