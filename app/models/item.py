from pydantic import BaseModel
from datetime import datetime

class InventoryItem(BaseModel):
    sku: str
    lot: str
    received_by: str
    rfid_tag: str
    received_at: datetime

    def to_dict(self):
        return {
            "sku": self.sku,
            "lot": self.lot,
            "received_by": self.received_by,
            "rfid_tag": self.rfid_tag,
            "received_at": self.received_at.isoformat()
        }
