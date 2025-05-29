# UltraSteelChallenge/app/api/endpoints.py

from fastapi import APIRouter, HTTPException
from app.models.item import InventoryItem
from app.database import client as db
from app.rfid.rfid_module import RFIDModule
from datetime import datetime

router = APIRouter()
rfid_module = RFIDModule()

@router.get("/health")
def health_check():
    return {"status": "ok", "timestamp": datetime.now().isoformat()}

@router.post("/add_manually")
def add_inventory(item: InventoryItem):
    """
    Agrega un item al inventario manualmente.
    """
    try:
        result = db.add_item(item)
        if result == 0:
            raise HTTPException(status_code=400, detail="Item already exists")
        return {"message": "Item added", "data": item.to_dict()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/add_from_tag/{epc_ascii}")
def add_from_tag(epc_ascii: str):
    """
    Agrega un ítem al inventario a partir del EPC leído de una etiqueta.
    """
    try:
        item = InventoryItem.from_epc_ascii(epc_ascii)
        result = db.add_item(item)
        if result == 0:
            raise HTTPException(status_code=400, detail="Item already exists")
        return {"message": "Item added from tag", "data": item.to_dict()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/exit_item/{uid}")
def exit_inventory(uid: str):
    """
    Marca un ítem como salido del almacén (status = 0).
    """
    try:
        success = db.exit_item(uid)
        if not success:
            raise HTTPException(status_code=404, detail="Item not found")
        return {"message": f"Item with UID '{uid}' marked as exited"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get_all_items")
def list_inventory():
    """
    Devuelve todos los ítems del inventario.
    """
    try:
        items = db.get_all_items()
        return {"items": [item.to_dict() for item in items]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/find_item_by_uid/{uid}")
def get_item(uid: str):
    """
    Busca un ítem por UID.
    """
    try:
        item = db.find_item_by_uid(uid)
        print(item)
        if item is None:
            return {"item": "Item not found"}
        return {"item": item.to_dict()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/update_item/{uid}")
def modify_item(uid: str, updated_item: InventoryItem):
    """
    Actualiza un ítem por su UID.
    """

    try:
        existing = db.find_item_by_uid(uid)
        if existing is None:
            raise HTTPException(status_code=404, detail="Item not found")
        db.update_item(uid, updated_item)
        return {"message": "Item updated", "data": updated_item.to_dict()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/delete_item/{uid}")
def remove_item(uid: str):
    """
    Elimina un ítem por su UID.
    """
    try:
        existing = db.find_item_by_uid(uid)
        if existing is None:
            raise HTTPException(status_code=404, detail="Item not found")
        db.delete_item(uid)
        return {"message": "Item deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/start_reading")
def start_reading():
    """
    Inicia la lectura RFID (modo continuo).
    """
    try:
        rfid_module.start_reading()
        return {"message": "RFID reading started"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/stop_reading")
def stop_reading():
    """
    Detiene la lectura RFID.
    """
    try:
        rfid_module.stop_reading()
        return {"message": "RFID reading stopped"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/write_tag")
def write_to_tag(data: str):
    """
    Escribe datos a una etiqueta RFID.
    """
    try:
        rfid_module.write(data)
        return {"message": "Data written to RFID tag"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
