from product import Product
from supplier import Supplier


class DigitalProduct(Product):
    """A digital product delivered via electronic download."""

    def __init__(
        self,
        product_id: str,
        name: str,
        price: float,
        stock_quantity: int,
        supplier: Supplier,
        download_size: float = 0.0,
    ):
        super().__init__(product_id, name, price, stock_quantity, supplier)
        ds = float(download_size)
        if ds < 0:
            raise ValueError("Download size cannot be negative.")
        self._download_size: float = ds

    @property
    def download_size(self) -> float:
        return self._download_size

    def display_information(self) -> None:
        super().display_information()
        print("Type: Digital")
        print(f"Download size: {self._download_size} MB")

    def get_fulfilment_info(self) -> str:
        return "This product is delivered digitally via download."

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["type"] = "digital"
        data["download_size"] = self._download_size
        return data

    @classmethod
    def from_dict(cls, data: dict, supplier: Supplier) -> "DigitalProduct":
        return cls(
            data["product_id"],
            data["name"],
            float(data["price"]),
            int(data["stock_quantity"]),
            supplier,
            float(data.get("download_size", 0.0)),
        )
