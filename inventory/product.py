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

    def __repr__(self):
        return "Product<id: {}, name: {}, mass: {}>".format(
            self.id,
            self.name,
            self.mass
        )


class ProductDetails:
    """
    Shippable Order Class

    Attributes:
        quantity (bool): number of each product
        product (Product): the product

    """

    def __init__(self, product: type[Product], available: int = 0):
        self.quantity = available
        self.product = product

    def __repr__(self):
        return "ProductDetails<quantity: {}, product: {}>".format(
            self.quantity,
            self.product
        )

    def stock(self, quantity):
        """
        stock product

        Parameters:
            quantity (int): quantity to add to product stock
        """
        if quantity > 0:
            self.quantity = self.quantity + quantity

    def ship(self, quantity):
        """
        ship product

        Parameters:
            quantity (int): quantity of product stock to remove
        """
        if quantity > 0:
            self.quantity = self.quantity - quantity
