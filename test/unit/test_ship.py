import unittest
import json
import os
from shipping.ship import ShipPackage
from ordering.order import Order
from inventory.catalog import Catalog
from inventory.product import Product, ProductDetails
from util.exceptions import InadequateProduct
ORDER_JSON_FILE = os.path.join(os.path.dirname(__file__), '../fixtures/test_order.json')
CATALOG_JSON_FILE = os.path.join(os.path.dirname(__file__), '../fixtures/test_catalog.json')
INVENTORY_JSON_FILE = os.path.join(os.path.dirname(__file__), '../fixtures/test_restock.json')


class TestShipPackage(unittest.TestCase):
    """
    test ShipPackage class
    """
    PRODUCT_NAME = "TEST"
    PRODUCT_ID = 4
    PRODUCT_WEIGHT = 200
    PACKAGE_MAX_WEIGHT = 1800

    @classmethod
    def setUp(cls):
        """
        Build a full catalog and orders

        Need to build to test the Ship class ship method
        """
        # setup catalog
        cls.catalog = Catalog()

        with open(CATALOG_JSON_FILE, 'r') as f:
            catalog_json = json.load(f)

        cls.catalog.add_inventory(catalog_json)

        # add inventory
        with open(INVENTORY_JSON_FILE, 'r') as f:
            inventory_json = json.load(f)

        cls.catalog.stock_inventory(inventory_json)

        # get json from order file
        with open(ORDER_JSON_FILE, 'r') as f:
            order_json = json.load(f)

        order_request = []

        for request in order_json['requested']:
            order_request.append(
                cls._create_product_detail(
                    cls,
                    request['quantity'],
                    cls.PRODUCT_WEIGHT
                )
            )

        cls.order = Order(order_json['order_id'], order_request)

    def _create_product_detail(self, quantity, weight):

        return ProductDetails(
            Product(
                self.PRODUCT_ID,
                self.PRODUCT_NAME,
                weight
            ),
            quantity
        )

    def test_ship(self):
        package = ShipPackage.ship(
            self.order.requested_products,
            self.catalog
        )
        self.assertTrue(package.weight == self.PACKAGE_MAX_WEIGHT)

