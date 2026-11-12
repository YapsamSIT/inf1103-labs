from product import Product


class Inventory:
    """Manages Product objects using Aggregation.
    Accepts any Product subclass created by the ProductFactory.
    """

    def __init__(self, name: str = "Main Warehouse"):
        self.name: str = name
        self.products: list[Product] = []

    def add_product(self, product: Product) -> None:
        """Add a Product to the inventory."""
        for existing in self.products:
            if existing.product_id == product.product_id:
                raise ValueError(f"Product with ID '{product.product_id}' is already in inventory '{self.name}'.")
        self.products.append(product)

    def remove_product(self, product_id: str) -> Product | None:
        """Remove and return the Product with the given ID, or None if not found."""
        for i, product in enumerate(self.products):
            if product.product_id == product_id:
                return self.products.pop(i)
        return None

    def find_product(self, product_id: str) -> Product | None:
        """Find and return a Product by ID, or None if not found."""
        for product in self.products:
            if product.product_id == product_id:
                return product
        return None

    def display_all_products(self) -> None:
        """Polymorphically display all products in the inventory."""
        if not self.products:
            print(f"Inventory '{self.name}' is currently empty.")
            return
        print(f"=== Inventory: {self.name} ({len(self.products)} items) ===")
        for product in self.products:
            product.display_information()
            print(f"Fulfilment: {product.get_fulfilment_info()}")
            print("-" * 30)

    def update_stock(self, product_id: str, change: int) -> None:
        product = self.find_product(product_id)
        if product is None:
            raise KeyError(f"No product with ID '{product_id}' found in inventory '{self.name}'.")
        product.update_stock(change)

    def search(self, term: str) -> list[Product]:
        term = term.strip().lower()
        return [
            p for p in self.products
            if term == p.product_id.lower() or term in p.name.lower()
        ]
