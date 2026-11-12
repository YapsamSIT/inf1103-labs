from product import Product
from order_line import OrderLine
from discount_strategy import DiscountStrategy, NoDiscount


class Order:
    """Represents a customer order that applies discounts via Strategy pattern.
    Contains no if/elif branching on discount types (adhering to OCP).
    """

    def __init__(self, order_id: str, discount: DiscountStrategy | None = None):
        self.order_id: str = order_id
        self.order_lines: list[OrderLine] = []
        # Default to NoDiscount if none provided
        self.discount: DiscountStrategy = discount if discount is not None else NoDiscount()

    def set_discount(self, discount: DiscountStrategy) -> None:
        """Allow switching the discount algorithm at runtime."""
        self.discount = discount

    def add_order_line(self, product: Product, quantity: int) -> None:
        """Create and append an OrderLine internally (Composition)."""
        order_line = OrderLine(product, quantity)
        self.order_lines.append(order_line)

    def remove_order_line(self, product_id: str) -> bool:
        """Remove a line item matching the given product ID."""
        for i, line in enumerate(self.order_lines):
            if line.product.product_id == product_id:
                del self.order_lines[i]
                return True
        return False

    def calculate_subtotal_before_discount(self) -> float:
        """Sum of all line subtotals without discount."""
        return sum(line.calculate_subtotal() for line in self.order_lines)

    def calculate_total(self) -> float:
        """Calculate the total using the injected DiscountStrategy."""
        raw_total = self.calculate_subtotal_before_discount()
        return self.discount.apply(raw_total)

    def display_order_summary(self) -> None:
        raw_total = self.calculate_subtotal_before_discount()
        final_total = self.calculate_total()
        print(f"=== Order #{self.order_id} Summary ===")
        if not self.order_lines:
            print("  (No items in order)")
        else:
            for line in self.order_lines:
                line.display_information()
        print(f"Subtotal: ${raw_total:.2f}")
        print(f"Discount Applied: {self.discount}")
        print(f"Final Total: ${final_total:.2f}")
        print("-" * 35)

    def __repr__(self) -> str:
        return f"Order(id={self.order_id!r}, lines={len(self.order_lines)}, strategy={self.discount!r})"
