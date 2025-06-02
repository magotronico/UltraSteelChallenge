from pydantic import BaseModel
from typing import ClassVar


class InventoryItem(BaseModel):
    sku: str          # [1] What the item is 
    lot: str          # [2] Lot number for tracking
    uid: str          # [2] The unique identifier for the item 
    received_by: str  # [2] Initials of the person who received the item
    date: str         # [5] Date of receipt in julian and 2 digit year format %j%y i.e. 22125
    status: str = "1" #     Default status is "1" (active)
    price: float = 0.0 # Optional price field, default is 0.0

    LENGTHS: ClassVar[dict] = {
        'sku': 1,          # e.g., "A"
        'lot': 2,          # e.g., "B4"
        'uid': 2,          # e.g., "C22"
        'received_by': 2,  # e.g., "DC"
        'date': 5          # e.g., "25425" (simplified here; adjust as needed)
    }

    @classmethod
    def from_epc_ascii(cls, epc_ascii: str):
        idx = 0
        parts = {}
        for field, length in cls.LENGTHS.items():
            parts[field] = epc_ascii[idx:idx + length]
            idx += length
        return cls(**parts)

    def to_dict(self):
        return {
            "sku": self.sku,
            "lot": self.lot,
            "uid": self.uid,
            "received_by": self.received_by,
            "date": self.date,
            "status": self.status,
            "price": self.price
        }

    def set_status(self, new_status: str):
        if new_status not in ["0", "1"]:
            raise ValueError("Status must be '0' or '1'.")
        self.status = new_status