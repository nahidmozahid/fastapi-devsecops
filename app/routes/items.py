from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict

router = APIRouter()

class Item(BaseModel):
    id: int
    name: str
    description: str | None = None

# in-memory "db"
DB: Dict[int, Item] = {
    1: Item(id=1, name="apple", description="A juicy fruit"),
    2: Item(id=2, name="banana", description="Yellow fruit"),
}


@router.get("/", response_model=list[Item])
async def list_items():
    return list(DB.values())


@router.get("/{item_id}", response_model=Item)
async def get_item(item_id: int):
    item = DB.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.post("/", response_model=Item, status_code=201)
async def create_item(item: Item):
    if item.id in DB:
        raise HTTPException(status_code=400, detail="ID already exists")
    DB[item.id] = item
    return item
