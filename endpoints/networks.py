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


@app.post("/networks")
def add_network(form: CreateNetworkForm):
    if networks_repository.get_by_chain_id(form.chain_id):
        return {"error": "chain id already used"}
    networks_repository.create(**form.__dict__)
    return {"status": "success"}
