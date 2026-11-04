import json
from product_factory import create_product_from_dict


class Inventory:
    """Manages Product objects. It calls their methods but does not
    implement product behaviour itself."""

    def __init__(self):
        self._products = {}

    def add_product(self, product):
        if product.product_id in self._products:
            raise ValueError(f"Product ID {product.product_id} already exists.")
        self._products[product.product_id] = product

    def get_product(self, product_id):
        return self._products.get(product_id)

    def display_all(self):
        if not self._products:
            print("Inventory is empty.")
            return
        for product in self._products.values():
            product.display_information()
            print(product.get_fulfilment_info())
            print("-" * 30)

    def update_stock(self, product_id, change):
        product = self.get_product(product_id)
        if product is None:
            raise KeyError(f"No product with ID {product_id}.")
        product.update_stock(change)

    def search(self, term):
        """Match by exact ID or part of the name (case-insensitive)."""
        term = term.lower()
        return [p for p in self._products.values()
                if term == str(p.product_id).lower() or term in p.name.lower()]

    def save(self, filename):
        with open(filename, "w") as f:
            json.dump([p.to_dict() for p in self._products.values()], f, indent=4)

    def load(self, filename):
        with open(filename, "r") as f:
            records = json.load(f)
        self._products = {}
        for record in records:
            product = create_product_from_dict(record)
            self._products[product.product_id] = product
