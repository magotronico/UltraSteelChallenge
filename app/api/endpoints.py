from fastapi import APIRouter, HTTPException
from datetime import datetime
from models.item import InventoryItem
from database.client import supabase_insert_item

router = APIRouter()

@router.post("/add")
def add_inventory(item: InventoryItem):
    item_dict = item.to_dict()
    try:
        response = supabase_insert_item(item_dict)
        return {"message": "Item added", "data": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
