from typing import Dict

from forms.CreateTokenForm import CreateTokenForm
from main import app, tokens_repository


@app.get("/tokens")
async def list_tokens() -> Dict:
    data = tokens_repository.list()
    return {
        "size": len(data),
        "data": data
    }


@app.post("/tokens")
async def create_token(form: CreateTokenForm) -> Dict:
    if tokens_repository.get_by_address(form.address):
        return {"error": "already exists"}
    tokens_repository.create(**form.dict())
    return {"status": "success"}


@app.get("/tokens/{address}")
async def retrieve_token(address: str) -> Dict:
    if not (token := tokens_repository.get_by_address(address)):
        return {"error": "not found"}
    return token.__dict__


@app.get("/tokens/on_network/{chain_id}")
async def list_tokens_on_network(chain_id: int) -> Dict:
    data = tokens_repository.get_tokens_at_network(chain_id)
    return {
        "size": len(data),
        "data": data
    }
