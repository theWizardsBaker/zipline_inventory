from inventory.product import ProductDetails


class Package:
    """
    Packaged items for shipping

    Attributes:
        products (list[ProductDetails]): All the products to ship
        weight (int): total weight of the packaged products
    """

    def __init__(self, products: list[ProductDetails] = None, weight: int = 0):
        if products is None:
            products = []
        self._products = products
        self.weight = weight

    def __repr__(self):
        return "Package<weight: {}, products: {}>".format(
            self.weight,
            self.products
        )

    @property
    def products(self):
        return self._products

    def add_product(self, product):
        self._products.append(product)
