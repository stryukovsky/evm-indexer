from fastapi import FastAPI

app = FastAPI()

import endpoints.networks
import endpoints.tokens
import endpoints.holders
import endpoints.indexers

from indexers.main import Worker

Worker("polygon-mainnet-usdt-tracker", "0xc2132D05D31c914a87C6611C10748AEb04B58e8F", "event", "recipient", {
    "recipient": '0xF07C30E4CD6cFff525791B4b601bD345bded7f47'
}).cycle()
