from product import Product, ProductDetails

class Catalog:
    """
    Catalog of shippable products

    Attributes:
        inventory (dict{ product_id: ProductDetails }): 

    """

	def __init__(self):
		self.inventory = {}

    def __repr__(self):
        return "Catalog<{}>".format(
            [ "{} quantity: {}".format(inv.product, inv.quantity_available) for inv in self.inventory ].join(', ')
        )

	def in_stock_products(self, product_id: int) -> bool:
		# check if an product is in stock
		return all([product_id in self.inventory, self.inventory[product_id].quantity_available > 0])

	def stock_inventory(self, products: list):
		"""
		add inventory stock

		[
			{
				product_id: int,
				quantity: int
			}
		]
		"""
		for product in products:
			if product in self.inventory:
				self.inventory[product['product_id']].stock(product['quantity'])

	def get_inventory(self) -> list[ProductDetails]:
		# return all inventory products that have quantity available
		return [inv for inv in self.inventory if self.in_stock(inv.product.id)]

	def add_inventory(self, inventory: list[dict]):
		"""
		add all inventory items to the catalog inventory

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
				quantity,
				Product(
					product['product_id'],
					product['product_name'],
					product['mass_g']
				)
			)

	def remove_inventory(self, product_id: int) -> bool:
		# reduce the quantity available for a product
		if self.in_stock(product_id):
			self.inventory[product_id].quantity_available = self.inventory[product_id].quantity_available - 1
			return True
		else:
			return False