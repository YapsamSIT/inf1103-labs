from product import Product
from can_be_shipped import CanBeShipped


class PhysicalProduct(Product, CanBeShipped):
    """A product that is stored and shipped.
    Single inheritance from Product + one interface (CanBeShipped)."""

    BASE_SHIPPING = 5.00
    COST_PER_KG = 2.50

    def __init__(self, product_id, name, price, stock_quantity, weight):
        super().__init__(product_id, name, price, stock_quantity)
        if weight < 0:
            raise ValueError("Weight cannot be negative.")
        self._weight = weight

    @property
    def weight(self):
        return self._weight

    def display_information(self):
        super().display_information()
        print(f"Type: Physical")
        print(f"Weight: {self._weight} kg")

    def get_fulfilment_info(self):
        return "This product requires physical shipping."

    def calculate_shipping_cost(self):
        return self.BASE_SHIPPING + self.COST_PER_KG * self._weight

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "physical"
        data["weight"] = self._weight
        return data

    @classmethod
    def from_dict(cls, data):
        return cls(data["product_id"], data["name"], data["price"],
                   data["stock_quantity"], data["weight"])
