from inventory.product import Product, ProductDetails
from util.exceptions import InadequateProduct

class Order:
    """
    Shippable Order Class

    Attributes:
        id (int): unique order id
        requested_products (List[ Product ]): the products requested in the order
        quantity (int): number of items ordered

    """

    def __init__(self, id: int, requested_products: list[ProductDetails]):
        self.id = id
        self.requested_products = requested_products
        self.__sort_requested_products_by_mass()

    def __repr__(self):
        return "Order<id: {}, requested_products: {}>".format(
            self.id,
            self.requested_products
        )

    def quantity(self) -> int:
        # returns: number of items to fulfill
        return sum([product.quantity for product in self.requested_products])

    def ship_product(self, product_id: int, quantity: int):
        """
        find product in requested_productes

        Parameters:
            product_id (int): product to remove from an order
            quantity (int): the number of product_id to remove
        """
        for req_ind, request in enumerate(self.requested_products):
            if request.product.id == product_id:
                # can't ship more than the on-hand
                if request.quantity < quantity:
                    raise InadequateProduct(quantity, request.quantity, "Order")
                    break
                # ship the product (remove quantity from order)
                request.ship(quantity)
                # if no more quantity is needed to ship, remove from order
                if request.quantity < 1:
                    self.requested_products.pop(req_ind)

    def __sort_requested_products_by_mass(self):
        # quick sort requested_products by mass
        def sort(requests, left, right):
            if left < right:

                next_left = left - 1
                pivot_mass = requests[right].product.mass

                for x in range(left, right):
                    if requests[x].product.mass <= pivot_mass:
                        next_left = next_left + 1
                        requests[next_left], requests[x] = requests[x], requests[next_left]

                requests[next_left + 1], requests[right] = requests[right], requests[next_left + 1]

                sort(requests, left, next_left)
                sort(requests, next_left + 1, right)

        if len(self.requested_products) > 1:
            sort(self.requested_products, 0, len(self.requested_products) - 1)
