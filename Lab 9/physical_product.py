from product import Product
from can_be_shipped import CanBeShipped
from supplier import Supplier


class PhysicalProduct(Product, CanBeShipped):
    """A physical product that is stored in inventory and shipped."""

    BASE_SHIPPING: float = 5.00
    COST_PER_KG: float = 2.50

    def __init__(
        self,
        product_id: str,
        name: str,
        price: float,
        stock_quantity: int,
        supplier: Supplier,
        weight: float = 1.0,
    ):
        super().__init__(product_id, name, price, stock_quantity, supplier)
        w = float(weight)
        if w < 0:
            raise ValueError("Weight cannot be negative.")
        self._weight: float = w

    @property
    def weight(self) -> float:
        return self._weight

    def display_information(self) -> None:
        super().display_information()
        print("Type: Physical")
        print(f"Weight: {self._weight} kg")

    def get_fulfilment_info(self) -> str:
        return "This product requires physical shipping."

    def calculate_shipping_cost(self) -> float:
        return self.BASE_SHIPPING + (self.COST_PER_KG * self._weight)

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["type"] = "physical"
        data["weight"] = self._weight
        return data

    @classmethod
    def from_dict(cls, data: dict, supplier: Supplier) -> "PhysicalProduct":
        return cls(
            data["product_id"],
            data["name"],
            float(data["price"]),
            int(data["stock_quantity"]),
            supplier,
            float(data.get("weight", 1.0)),
        )
