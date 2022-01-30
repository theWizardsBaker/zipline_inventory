import unittest
from shipping.package import Package
from inventory.product import Product, ProductDetails


class TestPackage(unittest.TestCase):
    """
    test Product class
    """

    PRODUCT_QUANTITY = 10
    PRODUCT_ID = 12
    PRODUCT_NAME = 'test'
    PRODUCT_WEIGHT = 200

    def test_creation(self):
        # generate products and product details
        product_details = []
        for pr_id in range(1, self.PRODUCT_ID):
            product = Product(pr_id, self.PRODUCT_NAME, self.PRODUCT_WEIGHT)
            product_details.append(ProductDetails(product, self.PRODUCT_QUANTITY))

        package = Package(product_details)

        self.assertEqual(package.products, product_details)

    def test_add_product(self):
        # generate products and product details
        product = Product(self.PRODUCT_ID, self.PRODUCT_NAME, self.PRODUCT_WEIGHT)
        product_details = ProductDetails(product, self.PRODUCT_QUANTITY)
        # empty package
        package = Package()
        
        self.assertTrue(len(package.products) == 0)

        package.add_product(product_details)

        self.assertTrue(len(package.products) == 1)
