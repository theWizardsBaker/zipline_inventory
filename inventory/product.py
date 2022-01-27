class Product:
    """
    Product Class

    Attributes:
        id (int): product id
        name (str): display name for product
        mass (int): product mass in grams
    """
    def __init__(self, id: int, name: str, mass: int):
        self.id = id
        self.name = name
        self.mass = mass

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "Product<id: {}, name: {}, mass: {}>".format(self.id, self.name, self.mass)



class ProductDetails:
    """
    Shippable Order Class

    Attributes:
        quantity_available (bool): number of each product
        products (Product): the product

    """

    def __init__(self, product: type[Product], available: int = 0):
        self.quantity_available = available
        self.product = product

    def stock(self, quantity):
        if quantity > 0:
            self.quantity_available = self.quantity_available + quantity

    def ship(self, quantity):
        if quantity > 0:
            self.quantity_available = self.quantity_available - quantity

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "ProductDetails<quantity: {}, product: {}>".format(self.quantity_available, self.product)
