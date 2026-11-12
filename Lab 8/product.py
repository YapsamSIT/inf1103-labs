from abc import ABC, abstractmethod
from supplier import Supplier


class Product(ABC):
    """Abstract base class for all products.
    Maintains an Association with a Supplier.
    """

    def __init__(self, product_id: str, name: str, price: float, stock_quantity: int, supplier: Supplier):
        self._product_id: str = product_id
        self._name: str = name
        self.price: float = price                    # uses setter validation
        self.stock_quantity: int = stock_quantity    # uses setter validation
        self.supplier: Supplier = supplier          # Association: Product references a Supplier

    # ---------- Encapsulation (Getters and Setters) ----------
    @property
    def product_id(self) -> str:
        return self._product_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, value: float) -> None:
        if value < 0:
            raise ValueError("Price cannot be negative.")
        self._price = float(value)

    @property
    def stock_quantity(self) -> int:
        return self._stock_quantity

    @stock_quantity.setter
    def stock_quantity(self, value: int) -> None:
        if value < 0:
            raise ValueError("Stock quantity cannot be negative.")
        self._stock_quantity = int(value)

    # ---------- Behaviour ----------
    def update_stock(self, change: int) -> None:
        """Add (positive) or remove (negative) stock."""
        self.stock_quantity = self._stock_quantity + change

    def display_information(self) -> None:
        """Display general product details and associated supplier information."""
        print(f"Product ID: {self._product_id}")
        print(f"Name: {self._name}")
        print(f"Price: ${self._price:.2f}")
        print(f"Stock: {self._stock_quantity}")
        print(f"Supplier: {self.supplier.name} ({self.supplier.contact_email})")

    def to_dict(self) -> dict:
        """Common data every product saves. Subclasses extend this."""
        return {
            "product_id": self._product_id,
            "name": self._name,
            "price": self._price,
            "stock_quantity": self._stock_quantity,
            "supplier_id": self.supplier.supplier_id,
            "supplier_name": self.supplier.name,
            "supplier_email": self.supplier.contact_email,
        }

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        """Every product type must explain how it is fulfilled."""
        pass
