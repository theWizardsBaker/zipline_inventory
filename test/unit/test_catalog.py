import unittest
import json
import os
from inventory.catalog import Catalog
CATALOG_JSON_FILE = os.path.join(os.path.dirname(__file__), '../fixtures/test_catalog.json')
INVENTORY_JSON_FILE = os.path.join(os.path.dirname(__file__), '../fixtures/test_restock.json')


class TestCatalog(unittest.TestCase):
    """
    test Catalog class
    """
    PRODUCT_ID = 5

    def setUp(self):
        self.catalog = Catalog()
        with open(CATALOG_JSON_FILE, 'r') as f:
            catalog_json = json.load(f)
        self.catalog.add_inventory(catalog_json)

    def stock_inventory(self):
        with open(INVENTORY_JSON_FILE, 'r') as f:
            inventory_json = json.load(f)

        self.catalog.stock_inventory(inventory_json)

    def test_product_is_not_in_stock(self):
        # will be false to start because no products are loaded
        self.assertFalse(self.catalog.in_stock_product(self.PRODUCT_ID))

    def test_product_is_not_in_catalog(self):
        # will be false because id 100 does not exist
        self.assertFalse(self.catalog.get_product(100))

    def test_product_is_in_stock(self):
        self.stock_inventory()
        self.assertTrue(self.catalog.in_stock_product(self.PRODUCT_ID))

    def test_product_is_in_catalog(self):
        self.stock_inventory()
        product_details = self.catalog.get_product(self.PRODUCT_ID)
        self.assertTrue(product_details.product.id, self.PRODUCT_ID)

    def test_ship_product(self):
        self.stock_inventory()
        product_details = self.catalog.get_product(self.PRODUCT_ID)
        quantity = product_details.quantity
        self.catalog.ship_product(product_details.product.id, 1)
        self.assertEqual(product_details.quantity, quantity - 1)

    def test_get_empty_inventory(self):
        self.assertEqual(0, len(self.catalog.get_inventory()))

    def test_full_inventory(self):
        self.stock_inventory()
        with open(CATALOG_JSON_FILE, 'r') as f:
            catalog_json = json.load(f)

        self.assertEqual(len(catalog_json), len(self.catalog.get_inventory()))


