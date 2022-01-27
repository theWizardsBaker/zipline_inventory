from zipline.inventory.product import Product

class Order:
    """
    Shippable Order Class

    Attributes:
        id (int): unique order id
        products (List[ Product ]): the products requested in the order
        quantity (int): number of items ordered

    """
    def __init__(self, id: int, products: list[Product]):
        self.id = id
        self.products = products
        self.fulfilled = False
        self.__sort_products_by_mass()

    def __repr__(self):
        return "Order<id: {}, fulfilled: {}, products: {}>".format(
            self.id,
            self.fulfilled,
            [ str(product) for product in self.products ].join(', ')
        )

    def quantity(self) -> int:
        # returns: number of items to fulfill
        return len(self.products)

    def __sort_products_by_mass(self):
        # quick sort products by mass
        def sort(products, left, right):
            if left < right:

                next_left = left - 1
                pivot_mass = products[right].mass
             
                for x in range(left, right):
                    if products[x].mass <= pivot:
                        next_left = next_left + 1
                        products[next_left], products[x] = products[x], products[next_left]
             
                products[next_left + 1], products[right] = products[right], products[next_left + 1]

            sort(products, left, next_left)
            sort(products, next_left + 1, right)

        if len(self.products) > 1:
            self.products = sort(self.products, 0, len(self.products))