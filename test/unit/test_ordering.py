import unittest
import json
import os
from ordering.order import Order
from inventory.product import Product, ProductDetails
from util.exceptions import InadequateProduct
ORDER_JSON_FILE = os.path.join(os.path.dirname(__file__), '../fixtures/test_order.json')


class TestOrder(unittest.TestCase):
    """
    test Ordering class
    """
    PRODUCT_NAME = "TEST"
    PRODUCT_ID = 4
    PRODUCT_WEIGHT = 200

    @classmethod
    def setUp(cls):
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

    def test_quantity_in_order(self):
        with open(ORDER_JSON_FILE, 'r') as f:
            order_json = json.load(f)

        self.assertEqual(
            len(order_json['requested']),
            len(self.order.requested_products)
        )

    def test_product_sort(self):
        weights = [500, 400, 300, 200, 100]
        order_request = []
        for i in weights:
            # create product details with descending weight
            # 500 - 100
            order_request.append(self._create_product_detail(i, i))
        # when order is created, request products should be sorted
        order = Order(123, order_request)
        # weights should now be sorted in reverse order (high -> low)
        weights.reverse()
        self.assertEqual(
            weights,
            list(map(lambda p: p.product.mass, order.requested_products))
        )

    def test_ship_product(self):
        # find the quantity for PRODUCT_ID
        quantity = 0
        product = None
        for prod in self.order.requested_products:
            if prod.product.id == self.PRODUCT_ID:
                product = prod
                quantity = prod.quantity
                break

        self.order.ship_product(self.PRODUCT_ID, 1)
        self.assertEqual(
            quantity - 1,
            product.quantity
        )

    def test_ship_more_product_than_on_hand(self):
        # find the quantity for PRODUCT_ID
        quantity = 0
        product = None
        for prod in self.order.requested_products:
            if prod.product.id == self.PRODUCT_ID:
                product = prod
                quantity = prod.quantity
                break
        with self.assertRaises(InadequateProduct):
            self.order.ship_product(self.PRODUCT_ID, 3)



