from typing import Dict

from database import indexers_repository, networks_repository
from forms.CreateIndexerForm import CreateIndexerForm
from forms.SetLastBlockForm import SetLastBlockForm
from main import app
from fastapi.responses import JSONResponse


@app.get("/indexers")
async def list_indexers() -> Dict:
    data = indexers_repository.list()
    return {
        "size": len(data),
        "data": data
    }


@app.post("/indexers")
async def create_indexer(form: CreateIndexerForm) -> JSONResponse:
    if indexers_repository.get_by_name(form.name):
        return JSONResponse({"error": "already exists"}, status_code=400)
    if not networks_repository.get_by_chain_id(form.network):
        return JSONResponse({"error": "network not found"}, status_code=404)
    indexers_repository.create(**form.dict())
    return JSONResponse({"status": "success"}, status_code=200)


@app.get("/indexers/{name}")
async def retrieve_indexer(name: str):
    if not (indexer := indexers_repository.get_by_name(name)):
        return JSONResponse({"error": "not found"}, status_code=404)
    return indexer.to_dict()


@app.patch("/indexers/{name}/set_last_block")
async def set_last_block(name: str, form: SetLastBlockForm):
    if not indexers_repository.get_by_name(name):
        return JSONResponse({"error": "not found"}, status_code=404)
    indexers_repository.set_last_block(name, **form.dict())
    return JSONResponse({"status": "success"}, status_code=200)
