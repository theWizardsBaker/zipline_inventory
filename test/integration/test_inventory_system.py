import unittest
import json
import os
from inventory_system import InventorySystem
CATALOG_JSON_FILE = os.path.join(os.path.dirname(__file__), '../fixtures/test_catalog.json')
INVENTORY_JSON_FILE = os.path.join(os.path.dirname(__file__), '../fixtures/test_restock.json')
ORDER_JSON_FILE = os.path.join(os.path.dirname(__file__), '../fixtures/test_order.json')


class TestInventory(unittest.TestCase):
    """
    test ShipPackage class
    """

    def test_inventory_system(self):
        """
        Run the inventory system
        """
        inventory_system = InventorySystem()

        with open(CATALOG_JSON_FILE, 'r') as f:
            catalog_json = f.read()

        inventory_system.init_catalog(catalog_json)

        with open(INVENTORY_JSON_FILE, 'r') as f:
            inventory_json = f.read()

        inventory_system.process_restock(inventory_json)

        with open(ORDER_JSON_FILE, 'r') as f:
            order_json = f.read()

        inventory_system.process_order(order_json)

        inventory_system.ship_package()

        self.assertTrue(len(inventory_system.get_backorders()) == 0)

    def test_inventory_system_backorder(self):
        """
        Run the inventory system
        """
        inventory_system = InventorySystem()

        with open(CATALOG_JSON_FILE, 'r') as f:
            catalog_json = f.read()

        inventory_system.init_catalog(catalog_json)

        with open(INVENTORY_JSON_FILE, 'r') as f:
            inventory_json = f.read()

        inventory_system.process_restock(inventory_json)

        with open(ORDER_JSON_FILE, 'r') as f:
            order_json = f.read()

        inventory_system.process_order(order_json)
        # double our orders
        inventory_system.process_order(order_json)

        inventory_system.ship_package()

        self.assertTrue(len(inventory_system.get_backorders()) > 0)

