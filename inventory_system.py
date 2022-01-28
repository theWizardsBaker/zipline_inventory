import json
import constants
from queue import Queue
from inventory.catalog import Catalog
from inventory.product import ProductDetails
from ordering.order import Order

class InventorySystem:

    def __init__(self):
        self.catalog = Catalog()
        self.orders_queue = Queue()
        self.backorder = []

    def init_catalog(self, products_json: str):
        """
        set up items in inventory

        products_json shape:
        [
            {
                mass_g: int
                product_name: str
                product_id: int
            }
        ]
        """
        self.catalog.add_inventory(json.loads(products_json))
        print(self.catalog)

    def process_order(self, order_json: str):
        """
        push new order to the queue

        order_json shape:
        {
            order_id: int
            requested: [
                {
                    product_id: int, 
                    quantity: int
                }
            ]
        }
        """
        # create ProductDetail for every product requested
        def create_product_detail(request):
            product_details = self.catalog.get_product(request['product_id'])
            if product_details:
                return ProductDetails(product_details.product, request['quantity'])
            else:
                return None

        order = json.loads(order_json)
        request_product_details = map(create_product_detail, order['requested'])
        # create order and add it to the queue
        self.orders_queue.put(
            Order(
                order['order_id'],
                list(filter(None, request_product_details))
            )
        )

        print(self.orders_queue)

    def process_restock(self, restock_json: str):
        """
        add stock to inventory

        restock_json shape:
        [
            {
                product_id: int,
                quantity: int
            }
        ]
        """
        self.catalog.stock_inventory(json.loads(restock_json))
        print(self.catalog)

    def ship_packages(self):
        """
        send orders out for delivery
        """
        package = []
        current_order = self.orders_queue.get()

        for order in current_order.requested_products:
            print(order)
