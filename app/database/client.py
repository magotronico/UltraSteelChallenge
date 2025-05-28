import csv
from typing import List, Dict, Any

def csv_insert_item(item: dict):
    """
    Inserts an item into the CSV file.
    
    Args:
        item (dict): The item to insert, with keys matching the CSV header.
    
    Returns:
        dict: The inserted item.
    """
    file_path = 'app/database/inventory.csv'
    
    # Read existing data
    with open(file_path, mode='a+', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=item.keys())
        file.seek(0, 2)  # Move to the end of the file
        if file.tell() == 0:  # If the file is empty, write the header
            writer.writeheader()
        writer.writerow(item)
    
    return item

