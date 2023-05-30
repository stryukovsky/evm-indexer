from fastapi import FastAPI

app = FastAPI()

import endpoints.networks
import endpoints.tokens
import endpoints.holders
import endpoints.indexers
