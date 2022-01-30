class InadequateProduct(Exception):
    """
    Custom exception for requesting more product than is on-hand

    Attributes:
        quantity -- amount requested
        stock -- amount of product on hand
        message -- explanation of the error
    """
    message = "Not enough product to ship"

    def __init__(self, quantity: int, stock: int, message: str = None):
        if message:
            self.message = "{}: {} - requested {} of {}".format(
                self.message,
                message,
                quantity,
                stock
            )
        super().__init__(self.message)

