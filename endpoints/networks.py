from typing import Dict

from main import app
from forms.CreateNetworkForm import CreateNetworkForm

from main import networks_repository


@app.get("/networks/")
def list_networks() -> Dict:
    data = networks_repository.list()
    return {
        "size": len(data),
        "data": data
    }


@app.get("/networks/{chain_id}")
def retrieve_network(chain_id: int) -> Dict:
    if not (network := networks_repository.get_by_chain_id(chain_id)):
        return {"error": "no network with this chain_id exists"}
    return network.__dict__


@app.post("/networks")
def add_network(form: CreateNetworkForm):
    if networks_repository.get_by_chain_id(form.chain_id):
        return {"error": "chain id already used"}
    networks_repository.create(**form.__dict__)
    return {"status": "success"}
