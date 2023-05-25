from typing import Dict
from web3 import Web3

from forms.CreateTokenForm import CreateTokenForm
from forms.RetrieveTokenForm import RetrieveTokenForm
from main import app, tokens_repository
from fastapi.responses import JSONResponse


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
async def retrieve_token(address: str) -> JSONResponse:
    try:
        validated_input = RetrieveTokenForm(address=address)
    except Exception as e:
        return JSONResponse({"error": f"bad address {e}"}, status_code=400)
    if not (token := tokens_repository.get_by_address(validated_input.address)):
        return JSONResponse({"error": "not found"}, status_code=404)
    return JSONResponse(token.to_dict(), status_code=200)


@app.get("/tokens/on_network/{chain_id}")
async def list_tokens_on_network(chain_id: int) -> Dict:
    data = tokens_repository.get_tokens_at_network(chain_id)
    return {
        "size": len(data),
        "data": data
    }
