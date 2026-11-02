class Inventory:
    """Manages a collection of Product objects."""
 
    def __init__(self):
        self.__products = []
 
    def add_product(self, product):
        if self.search_product(product.get_product_id()) is not None:
            raise ValueError("A product with this ID already exists.")
        self.__products.append(product)
 
    def search_product(self, product_id):
        """Return the matching Product, or None if not found."""
        for product in self.__products:
            if product.get_product_id() == product_id:
                return product
        return None
 
    def update_stock(self, product_id, quantity):
        product = self.search_product(product_id)
        if product is None:
            raise KeyError("Product not found.")
        product.update_stock(quantity)  # the Product controls its own stock
 
    def display_all(self):
        if not self.__products:
            print("Inventory is empty.")
            return
        for product in self.__products:
            product.display_information()
 
    def get_products(self):
        """Returns a copy of the list so outside code can't alter the original."""
        return list(self.__products)