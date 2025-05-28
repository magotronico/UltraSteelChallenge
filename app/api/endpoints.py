from fastapi import APIRouter, HTTPException
from datetime import datetime
from app.models.item import InventoryItem
from app.database.client import csv_insert_item
from app.rfid.rfid_module import RFIDModule

router = APIRouter()
rfid_module = RFIDModule()

@router.post("/add_manually")
def add_inventory(item: InventoryItem):
    """
    Endpoint to add an inventory item manually.
    Args:
        item (InventoryItem): The inventory item to add.
    Returns:
        dict: Confirmation message and item data.
    """

    item_dict = item.to_dict()
    try:
        response = csv_insert_item(item_dict)
        return {"message": "Item added", "data": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
def health_check():
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}

@router.get("/start_reading")
def start_reading():
    """
    Endpoint to start reading RFID tags.
    This is a placeholder for the actual RFID reading logic.
    """
    # Here you would call the function that starts reading RFID tags
    rfid_module.read()
    return {"message": "RFID reading started"}

@router.post("/stop_reading")
def stop_reading():
    """
    Endpoint to stop reading RFID tags.
    This is a placeholder for the actual logic to stop reading.
    """
    # Here you would implement the logic to stop reading RFID tags
    rfid_module.stop_reading()
    return {"message": "RFID reading stopped"}

@router.post("/write_tag")
def write_tag(data: str):
    """
    Endpoint to write data to an RFID tag.
    
    Args:
        data (str): The data to write to the RFID tag.
    
    Returns:
        dict: Confirmation message.
    """
    try:
        rfid_module.write(data)
        return {"message": "Data written to RFID tag successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
