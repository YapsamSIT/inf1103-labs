from abc import ABC, abstractmethod


class Product(ABC):
    """Abstract base class for all products."""

    def __init__(self, product_id, name, price, stock_quantity):
        self._product_id = product_id
        self._name = name
        self.price = price                    # uses setter (validation)
        self.stock_quantity = stock_quantity  # uses setter (validation)

    # ---------- encapsulation ----------
    @property
    def product_id(self):
        return self._product_id

    @property
    def name(self):
        return self._name

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value < 0:
            raise ValueError("Price cannot be negative.")
        self._price = value

    @property
    def stock_quantity(self):
        return self._stock_quantity

    @stock_quantity.setter
    def stock_quantity(self, value):
        if value < 0:
            raise ValueError("Stock quantity cannot be negative.")
        self._stock_quantity = value

    # ---------- behaviour ----------
    def update_stock(self, change):
        """Add (positive) or remove (negative) stock."""
        self.stock_quantity = self._stock_quantity + change

    def display_information(self):
        print(f"ID: {self._product_id}")
        print(f"Name: {self._name}")
        print(f"Price: ${self._price:.2f}")
        print(f"Stock: {self._stock_quantity}")

    def to_dict(self):
        """Common data every product saves. Subclasses extend this."""
        return {
            "product_id": self._product_id,
            "name": self._name,
            "price": self._price,
            "stock_quantity": self._stock_quantity,
        }

    @abstractmethod
    def get_fulfilment_info(self):
        """Every product type must explain how it is fulfilled."""
        pass
