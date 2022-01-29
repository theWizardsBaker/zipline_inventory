import unittest
from inventory.product import Product, ProductDetails

class TestProduct(unittest.TestCase):

	PRODUCT_QUANTITY = 10
	PRODUCT_ID = 12
	PRODUCT_NAME = 'test'
	PRODUCT_WEIGHT = 200

	@classmethod
	def setUpClass(cls):
		cls.product = Product(cls.PRODUCT_ID, cls.PRODUCT_NAME, cls.PRODUCT_WEIGHT)
		cls.product_details = ProductDetails(cls.product, cls.PRODUCT_QUANTITY)

	def test_product_initialization(self):
		self.assertEqual(self.product.id, self.PRODUCT_ID)
		self.assertEqual(self.product.name, self.PRODUCT_NAME)
		self.assertEqual(self.product.mass, self.PRODUCT_WEIGHT)

	def test_product_details_initialization(self):
		self.assertEqual(self.product_details.quantity, self.PRODUCT_QUANTITY)
		self.assertEqual(self.product_details.product, self.product)

	def test_product_details_stock(self):
		quantity = self.product_details.quantity
		self.product_details.stock(2)
		self.assertEqual(self.product_details.quantity, quantity + 2)

	def test_product_details_ship(self):
		quantity = self.product_details.quantity
		self.product_details.ship(1)
		self.assertEqual(self.product_details.quantity, quantity - 1)
