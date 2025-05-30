import unittest
from pathlib import Path
import csv
from app.database.client import (
    init_db, add_item, get_all_items, find_item_by_uid,
    update_item, delete_item, count_items_by_lot,
    count_items_by_sku, exit_item, FIELDS
)
from app.models.item import InventoryItem


class TestInventoryDatabase(unittest.TestCase):
    TEST_FILE = Path("app/database/test_inventory.csv")

    def setUp(self):
        # Inicializa la base de datos limpia antes de cada prueba
        init_db(self.TEST_FILE)

    def tearDown(self):
        # Elimina el archivo después de cada prueba
        if self.TEST_FILE.exists():
            self.TEST_FILE.unlink()

    def test_add_and_find_item(self):
        item = InventoryItem(sku="001", lot="L001", uid="U001", received_by="XY", date="12345")
        result = add_item(item, self.TEST_FILE)
        self.assertEqual(result, 1)

        found = find_item_by_uid("U001", self.TEST_FILE)
        self.assertIsNotNone(found)
        self.assertEqual(found.uid, "U001")

    def test_prevent_duplicate_uid(self):
        item = InventoryItem(sku="002", lot="L002", uid="U002", received_by="ZZ", date="12345")
        result1 = add_item(item, self.TEST_FILE)
        result2 = add_item(item, self.TEST_FILE)

        self.assertEqual(result1, 1)
        self.assertEqual(result2, 0)

    def test_exit_item_status_change(self):
        item = InventoryItem(sku="003", lot="L003", uid="U003", received_by="AA", date="12346")
        add_item(item, self.TEST_FILE)
        success = exit_item("U003", self.TEST_FILE)
        self.assertTrue(success)

        updated = find_item_by_uid("U003", self.TEST_FILE)
        self.assertEqual(updated.status, "0")

    def test_update_item(self):
        original = InventoryItem(sku="004", lot="L004", uid="U004", received_by="CD", date="12347")
        updated = InventoryItem(sku="004", lot="L004", uid="U004", received_by="ZZ", date="54321")
        add_item(original, self.TEST_FILE)
        update_item("U004", updated, self.TEST_FILE)

        result = find_item_by_uid("U004", self.TEST_FILE)
        self.assertEqual(result.received_by, "ZZ")
        self.assertEqual(result.date, "54321")

    def test_delete_item(self):
        item = InventoryItem(sku="005", lot="L005", uid="U005", received_by="EF", date="12348")
        add_item(item, self.TEST_FILE)
        delete_item("U005", self.TEST_FILE)
        self.assertIsNone(find_item_by_uid("U005", self.TEST_FILE))

    def test_count_by_sku_and_lot(self):
        items = [
            InventoryItem(sku="AAA", lot="B1", uid="ID1", received_by="AA", date="11111"),
            InventoryItem(sku="AAA", lot="B1", uid="ID2", received_by="AA", date="11112"),
            InventoryItem(sku="BBB", lot="B2", uid="ID3", received_by="BB", date="11113")
        ]
        for item in items:
            add_item(item, self.TEST_FILE)

        self.assertEqual(count_items_by_sku("AAA", self.TEST_FILE), 2)
        self.assertEqual(count_items_by_lot("B1", self.TEST_FILE), 2)
        self.assertEqual(count_items_by_sku("BBB", self.TEST_FILE), 1)


if __name__ == "__main__":
    unittest.main()
