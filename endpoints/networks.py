from typing import Dict

from main import app
from forms.CreateNetworkForm import CreateNetworkForm

from database import networks_repository


@app.get("/networks/")
async def list_networks() -> Dict:
    data = networks_repository.list()
    return {
        "size": len(data),
        "data": data
    }


@app.get("/networks/{chain_id}")
async def retrieve_network(chain_id: int) -> Dict:
    if not (network := networks_repository.get_by_chain_id(chain_id)):
        return {"error": "no network with this chain_id exists"}
    return network.to_dict()


@app.post("/networks")
async def add_network(form: CreateNetworkForm):
    if networks_repository.get_by_chain_id(form.chain_id):
        return {"error": "chain id already used"}
    networks_repository.create(**form.dict())
    return {"status": "success"}
