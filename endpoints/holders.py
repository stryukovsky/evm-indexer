from typing import Dict

from forms.CreateHolderForm import CreateHolderForm
from main import app
from database import holders_repository
from fastapi.responses import JSONResponse


@app.get("/holders")
def list_holders() -> Dict:
    data = holders_repository.list()
    return {
        "size": len(data),
        "data": data
    }


@app.post("/holders")
def create_holder(form: CreateHolderForm) -> JSONResponse:
    if holders_repository.get_by_address(form.address):
        return JSONResponse({"error": "already exists"}, status_code=400)
    holders_repository.create(**form.dict())
    return JSONResponse({"status": "success"}, status_code=200)
