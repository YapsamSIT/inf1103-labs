from product import Product


class Inventory:
    """Manages a collection of Product objects using Aggregation.
    The Inventory contains references to Product objects, but does not own
    their lifecycle. Products can exist before being added, can be removed
    without being destroyed, and can be transferred to other inventories.
    """

    def __init__(self, name: str = "Main Inventory"):
        self.name: str = name
        # Typed collection using the base class Product (Aggregation)
        self.products: list[Product] = []

    def add_product(self, product: Product) -> None:
        """Add an existing Product reference to the inventory."""
        # Optional safeguard: check if product_id is already present
        for existing in self.products:
            if existing.product_id == product.product_id:
                raise ValueError(f"Product with ID '{product.product_id}' is already in inventory '{self.name}'.")
        self.products.append(product)

    def remove_product(self, product_id: str) -> Product | None:
        """Remove and return the matching Product reference from the inventory.
        Does not destroy the Product object itself.
        """
        for i, product in enumerate(self.products):
            if product.product_id == product_id:
                return self.products.pop(i)
        return None

    def find_product(self, product_id: str) -> Product | None:
        """Locate and return a matching Product, or None if not found."""
        for product in self.products:
            if product.product_id == product_id:
                return product
        return None

    def display_all_products(self) -> None:
        """Polymorphically display details for all products in the inventory."""
        if not self.products:
            print(f"Inventory '{self.name}' is empty.")
            return
        print(f"=== Inventory: {self.name} ({len(self.products)} item(s)) ===")
        for product in self.products:
            product.display_information()
            print(f"Fulfilment: {product.get_fulfilment_info()}")
            print("-" * 30)

    def update_stock(self, product_id: str, change: int) -> None:
        """Update the stock quantity of a product in this inventory."""
        product = self.find_product(product_id)
        if product is None:
            raise KeyError(f"No product with ID '{product_id}' in inventory '{self.name}'.")
        product.update_stock(change)

    def search(self, term: str) -> list[Product]:
        """Search products by ID or partial name (case-insensitive)."""
        term = term.strip().lower()
        return [
            p for p in self.products
            if term == p.product_id.lower() or term in p.name.lower()
        ]
