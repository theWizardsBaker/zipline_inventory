import json
from queue import Queue
from inventory.catalog import Catalog
from inventory.product import ProductDetails
from ordering.order import Order
from shipping.ship import ShipPackage


class InventorySystem:
    """
    System for managing inventory

    Attributes:
        catalog (Catalog): stores inventory for the system
        orders_queue (Queue): queue for orders recieved
        backorder_orders (list): orders that cannot be filled due to product shortages

    """

    def __init__(self):
        self.catalog = Catalog()
        self.orders_queue = Queue()
        self.backorder_orders = []

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
                return ProductDetails(
                    product_details.product, request['quantity'])
            else:
                return None

        order = json.loads(order_json)
        request_product_details = map(
            create_product_detail,
            order['requested']
        )
        # create order and add it to the queue
        self.orders_queue.put(
            Order(
                order['order_id'],
                list(filter(None, request_product_details))
            )
        )

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

    def ship_package(self):
        """
        send all orders out for delivery
        """
        while not self.orders_queue.empty():

            current_order = self.orders_queue.get()

            while current_order.quantity() > 0:
                shipping_package = ShipPackage.ship(
                    current_order.requested_products,
                    self.catalog
                )
                # if we have orders that cannot be fufilled due to lack of
                # stock
                if not shipping_package.products and current_order.quantity() > 0:
                    # backorder the order
                    self.backorder_orders.append(current_order)
                    break

        # print("Backorder: ", self.backorder_orders)

    def get_backorders(self) -> list[Order]:
        """
        return all orders that have backorder items
        """
        return self.backorder_orders
