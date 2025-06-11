from fastapi import APIRouter, Depends, HTTPException
from database.crud import PostgresCRUD

router = APIRouter(prefix="/items")
crud = PostgresCRUD("наш DSN")

@router.post("/")
async def create_item(data: dict):
    item_id = crud.create("items", data)
    return {"id":item_id, **data}

@router.get("/")
async def read_item(data: dict):
    item_id = crud.read("items", data)
    return {"id":item_id, **data}

@router.put("/")
async def update_item(data: dict):
    item_id = crud.update("items", data)
    return {"id":item_id, **data}

@router.delete("/")
async def delete_item(data: dict):
    item_id = crud.delete("items", data)
    return {"id":item_id, **data}
