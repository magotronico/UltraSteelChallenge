import csv
from pathlib import Path
from typing import List, Optional
from app.models.item import InventoryItem

CSV_FILE = Path("app/database/inventory.csv")
FIELDS = ["sku", "lot", "uid", "received_by", "date", "status", "price"]


def init_db(file_path: Path = CSV_FILE):
    if not file_path.exists():
        with open(file_path, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=FIELDS)
            writer.writeheader()

def add_item(item: InventoryItem, file_path: Path = CSV_FILE) -> int:
    if find_item_by_uid(item.uid, file_path) is not None:
        return 0
    with open(file_path, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writerow(item.to_dict())
    return 1

def get_all_items(file_path: Path = CSV_FILE) -> List[InventoryItem]:
    if not file_path.exists():
        return []
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        return [InventoryItem(**row) for row in reader]

def find_item_by_uid(uid: str, file_path: Path = CSV_FILE) -> Optional[InventoryItem]:
    items = get_all_items(file_path)
    return next((item for item in items if item.uid == uid), None)

def update_item(uid: str, updated_item: InventoryItem, file_path: Path = CSV_FILE):
    items = get_all_items(file_path)
    with open(file_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader()
        for item in items:
            if item.uid == uid:
                writer.writerow(updated_item.to_dict())
            else:
                writer.writerow(item.to_dict())

def delete_item(uid: str, file_path: Path = CSV_FILE):
    items = get_all_items(file_path)
    with open(file_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader()
        for item in items:
            if item.uid != uid:
                writer.writerow(item.to_dict())

def count_items_by_lot(lot: str, file_path: Path = CSV_FILE) -> int:
    return sum(1 for item in get_all_items(file_path) if item.lot == lot)

def count_items_by_sku(sku: str, file_path: Path = CSV_FILE) -> int:
    return sum(1 for item in get_all_items(file_path) if item.sku == sku)

def exit_item(uid: str, file_path: Path = CSV_FILE) -> bool:
    item = find_item_by_uid(uid, file_path)
    if item is None:
        return False
    item.set_status("0")
    update_item(uid, item, file_path)
    return True


if __name__ == "__main__":
    init_db()
    # Example usage
    item = InventoryItem(sku="123", lot="A1", uid="UID123", received_by="AB", date="22125")
    add_item(item)
    print(find_item_by_uid("UID123").status)
    print(f"Amount of items in lot A1: {count_items_by_lot('A1')}")
    print(f"Amount of items in lot A2: {count_items_by_lot('A2')}")
    print(get_all_items())
    print(find_item_by_uid("UID123"))
    item_to_update = InventoryItem(sku="123", lot="A1", uid="UID123", received_by="CD", date="22126")
    # El item sale del almacén
    exit_success = exit_item("UID123")
    print(f"Salida registrada: {exit_success}")
    update_item("UID123", item_to_update)
    print(get_all_items())
    print(find_item_by_uid("UID123").status)
    exit_item("UID123")
    print(get_all_items())
    delete_item("UID123")
