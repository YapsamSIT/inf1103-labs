from product import Product


class OrderLine:
    """Represents an item within an Order.
    Enforces validation: quantity must be greater than zero.
    """

    def __init__(self, product: Product, quantity: int):
        val = int(quantity)
        # Validation Rule: Quantity must be greater than zero
        if val <= 0:
            raise ValueError("Quantity must be greater than zero.")
        self.product: Product = product
        self.quantity: int = val

    def calculate_subtotal(self) -> float:
        """Return unit price multiplied by quantity."""
        return self.product.price * self.quantity

    def display_information(self) -> None:
        subtotal = self.calculate_subtotal()
        print(f"  - {self.product.name} (x{self.quantity}) @ ${self.product.price:.2f} = ${subtotal:.2f}")

    def __repr__(self) -> str:
        return f"OrderLine({self.product.name!r}, quantity={self.quantity})"
