from pydantic import BaseModel

# [SKU]  [LOT]     [UID]  [INITIALS] [DATE] 
# [0-9] [A-Z0-9] [A-Z0-9]    [DC]    [22425]  

class InventoryItem(BaseModel):
    sku: str # [1] What the item is 
    lot: str # [2] Lot number for tracking
    uid: str # [2] The unique identifier for the item 
    received_by: str # [2] Initials of the person who received the item
    date: str # [5] Date of receipt in julian and 2 digit year format %j%y i.e. 22125

    def to_dict(self):
        return {
            "sku": self.sku,
            "lot": self.lot,
            "uid": self.uid,
            "received_by": self.received_by,
            "date": self.date
        }
