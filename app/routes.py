from fastapi import APIRouter, HTTPException
from .schemas import Item
from .models import fake_items_db

router = APIRouter()

@router.post("/items/", response_model=Item)
def create_item(item: Item):
    print("Item.....", item)
    fake_items_db.append(item)
    return item

@router.get("/items/", response_model=list[Item])
def read_items():
    return fake_items_db

@router.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int):
    for item in fake_items_db:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

@router.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, updated_item: Item):
    for index, item in enumerate(fake_items_db):
        if item.id == item_id:
            fake_items_db[index] = updated_item
            return updated_item
    raise HTTPException(status_code=404, detail="Item not found")

@router.delete("/items/{item_id}")
def delete_item(item_id: int):
    for index, item in enumerate(fake_items_db):
        if item.id == item_id:
            del fake_items_db[index]
            return {"message": "Item deleted"}
    raise HTTPException(status_code=404, detail="Item not found")
