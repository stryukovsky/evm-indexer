from typing import Dict

from fastapi.responses import JSONResponse

from endpoints.utils import get_repository_by_token_type
from forms.CreateTokenForm import CreateTokenForm
from forms.RetrieveTokenForm import RetrieveTokenForm
from forms.TokenBalanceForm import TokenBalanceForm
from main import (app, tokens_repository)


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


@app.get("/tokens/{address}/balance_of/{holder}")
async def token_balance_of(address: str, holder: str) -> JSONResponse:
    try:
        validated_input = TokenBalanceForm(address=address, holder=holder)
    except Exception as e:
        return JSONResponse({"error": f"bad addresses {e}"}, status_code=400)
    if not (token := tokens_repository.get_by_address(validated_input.address)):
        return JSONResponse({"error": "token not found"}, status_code=404)
    repository = get_repository_by_token_type(token.type)
    return JSONResponse(repository.get_balance(validated_input.address, validated_input.holder).to_dict(),
                        status_code=200)
