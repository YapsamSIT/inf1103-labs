from product import Product


class OrderLine:
    """Represents a single line item within an Order.
    Demonstrates Composition: An OrderLine belongs to exactly one Order and
    is created and managed by that Order. It references a Product, but does
    not own the Product.
    """

    def __init__(self, product: Product, quantity: int):
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")
        self.product: Product = product
        self.quantity: int = quantity

    def calculate_subtotal(self) -> float:
        """Calculate subtotal by multiplying unit price by quantity."""
        return self.product.price * self.quantity

    def display_information(self) -> None:
        """Display summary of this line item."""
        subtotal = self.calculate_subtotal()
        print(f"  - {self.product.name} (ID: {self.product.product_id}) x {self.quantity} "
              f"@ ${self.product.price:.2f} = ${subtotal:.2f}")

    def __repr__(self) -> str:
        return f"OrderLine(product={self.product.name!r}, quantity={self.quantity})"
