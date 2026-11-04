from product import Product


class DigitalProduct(Product):
    """A product delivered through download. Not shippable."""

    def __init__(self, product_id, name, price, stock_quantity, download_size):
        super().__init__(product_id, name, price, stock_quantity)
        if download_size < 0:
            raise ValueError("Download size cannot be negative.")
        self._download_size = download_size

    @property
    def download_size(self):
        return self._download_size

    def display_information(self):
        super().display_information()
        print(f"Type: Digital")
        print(f"Download size: {self._download_size} MB")

    def get_fulfilment_info(self):
        return "This product is delivered digitally via download."

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "digital"
        data["download_size"] = self._download_size
        return data

    @classmethod
    def from_dict(cls, data):
        return cls(data["product_id"], data["name"], data["price"],
                   data["stock_quantity"], data["download_size"])
