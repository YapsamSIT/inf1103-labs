from product import Product
from order_line import OrderLine


class Order:
    """Represents a customer order.
    Demonstrates Composition with OrderLine: The Order creates and manages
    its own OrderLine objects. An OrderLine has a terminal lifecycle tied
    directly to this Order.
    """

    def __init__(self, order_id: str):
        self.order_id: str = order_id
        # Whole owns its parts: OrderLine objects exist only within this Order
        self.order_lines: list[OrderLine] = []

    def add_order_line(self, product: Product, quantity: int) -> None:
        """Create and manage an OrderLine internally.
        Clients do not pass an OrderLine instance in directly; the Order owns line creation.
        """
        order_line = OrderLine(product, quantity)
        self.order_lines.append(order_line)

    def remove_order_line(self, product_id: str) -> bool:
        """Remove an order line for a given product ID."""
        for i, line in enumerate(self.order_lines):
            if line.product.product_id == product_id:
                del self.order_lines[i]
                return True
        return False

    def calculate_total(self) -> float:
        """Calculate total by asking each OrderLine for its subtotal."""
        return sum(line.calculate_subtotal() for line in self.order_lines)

    def display_order_summary(self) -> None:
        """Display full order details including line items and total."""
        print(f"=== Order #{self.order_id} Summary ===")
        if not self.order_lines:
            print("  (Order contains no line items)")
        else:
            for line in self.order_lines:
                line.display_information()
        print(f"Total Order Value: ${self.calculate_total():.2f}")
        print("-" * 35)

    def __repr__(self) -> str:
        return f"Order(id={self.order_id!r}, lines={len(self.order_lines)}, total={self.calculate_total():.2f})"
