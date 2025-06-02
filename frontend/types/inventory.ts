export interface InventoryItem {
  sku: string;         // [1] What the item is 
  lot: string;         // [2] Lot number for tracking
  uid: string;         // [3] The unique identifier for the item 
  received_by: string; // [4] Initials of the person who received the item
  date: string;        // [5] Date of receipt in julian and 2 digit year format %j%y i.e. 22125
  status: "0" | "1";   // "1" = active, "0" = exited
  price?: number;      // [6] Optional price of the item
}