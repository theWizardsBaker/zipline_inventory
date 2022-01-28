from .product import Product, ProductDetails

class Catalog:
    """
    Catalog of shippable products

    Attributes:
        inventory (dict{ product_id: ProductDetails }): dict to keep track of inventory by product_id
    """

    def __init__(self):
        self.inventory = {}

    def __repr__(self):
        inv = [ str(inv) for inv in self.inventory.values()]
        return "Catalog<\n\r{}\n\r>".format('\n\r'.join(inv))

    def in_stock_product(self, product_id: int) -> bool:
        """
        check if an product is in stock

        Parameters:
            product_id (int): id to check

        Returns:
            if product is in stock
        """
        return all([product_id in self.inventory, self.inventory[product_id].quantity > 0])

    def ship_product(self, product_id: int, quantity: int):
        """
        reduce quantity from catalog when product is shipped
        
        Parameters:
            product_id (int): id to retrieve
            quantity (int): amount to decrease by
        """
        product = self.get_product(product_id)
        if product:
            product.ship(quantity)

    def get_product(self, product_id: int) -> ProductDetails:
        """
        retrieve product by id
        
        Parameters:
            product_id (int): id to retrieve

        Returns:
            ProductDetails for product_id
        """
        if product_id in self.inventory:
            return self.inventory[product_id]
        else:
            return None

    def stock_inventory(self, products: list):
        """
        add inventory stock
        
        Parameters:
            products shape:
            [
                {
                    product_id: int,
                    quantity: int
                }
            ]
        """
        for product in products:
            if product['product_id'] in self.inventory:
                self.inventory[product['product_id']].stock(product['quantity'])

    def get_inventory(self) -> list[ProductDetails]:
        # return all inventory products that have quantity available
        return [inv for inv in self.inventory if self.in_stock(inv.product.id)]

    def add_inventory(self, inventory: list[dict]):
        """
        add all inventory items to the catalog inventory

        inventory shape:
        [
            {
                mass_g: int
                product_name: str
                product_id: int
            }
        ]
        """
        for product in inventory:
            quantity = product['quantity'] if 'quantity' in product else 0
            self.inventory[product['product_id']] = ProductDetails(
                Product(
                    product['product_id'],
                    product['product_name'],
                    product['mass_g']
                ),
                quantity
            )

    def remove_inventory(self, product_id: int):
        """
        reduce the quantity available for a product

         Parameters:
            product_id (int): id to remove inventory
        """
        if self.in_stock(product_id):
            self.inventory[product_id].quantity = self.inventory[product_id].quantity - 1