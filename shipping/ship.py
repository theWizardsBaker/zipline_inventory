import constants
from inventory.product import ProductDetails
from inventory.catalog import Catalog
from .package import Package

class ShipPackage(object):
    """
    Methods for sending packages
    """
    def __init__(self, ):
        pass

    @classmethod
    def ship(self, current_order: list[ProductDetails], catalog: type[Catalog]) -> type[Package]:
        """
        find products in the order that can be shipped together

        Parameters:
            current_order (list[ProductDetails]): a list of all the products in the current order
            catalog (Catalog): the catalog of inventory available to be shipped
        Returns:
            Package for shipping
        """
        package = Package()
        smallest_package_weight = current_order[0].product.mass
        # move from heaviest to lightest mass product
        for order in current_order[::-1]:
            for i in range(1, order.quantity + 1):
                if all([
                    package.weight != constants.MAX_SHIPPING_WEIGHT_GRAMS,
                    (package.weight + order.product.mass) <= constants.MAX_SHIPPING_WEIGHT_GRAMS,
                    catalog.in_stock_product(order.product.id)
                ]):
                    # remove quantity from products available
                    catalog.ship_product(order.product.id, 1)
                    # update shipping weight
                    package.weight = package.weight + order.product.mass
                    # remove quantity from order
                    order.ship(1)
                    # place product in package to ship
                    package.add_product(order.product)
                else:
                    break
            # do not continue if we are at, or will exceed the shipping weight
            if any([
                package.weight == constants.MAX_SHIPPING_WEIGHT_GRAMS,
                (package.weight + smallest_package_weight) > constants.MAX_SHIPPING_WEIGHT_GRAMS,
            ]):
                break

        return package