from fastapi import FastAPI
from database import engine

from repositories.networks import SQLNetworksRepository

app = FastAPI()

networks_repository = SQLNetworksRepository(engine)

import endpoints.networks
