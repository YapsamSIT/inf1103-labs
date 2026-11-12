from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from supplier import Supplier


class ProductFactory:
    """Factory Pattern: Centralises instantiation of Product subclasses.
    Client code calls ProductFactory.create(...) without directly coupling
    to concrete PhysicalProduct or DigitalProduct classes.
    """

    @staticmethod
    def create(
        product_type: str,
        product_id: str,
        name: str,
        price: float,
        stock_quantity: int,
        supplier: Supplier,
        **kwargs,
    ) -> Product:
        """Create and return a Product instance according to the product_type string.
        Raises ValueError if product_type is unknown.
        """
        normalized_type = product_type.strip().lower()
        if normalized_type == "physical":
            weight = kwargs.get("weight", 1.0)
            return PhysicalProduct(
                product_id=product_id,
                name=name,
                price=price,
                stock_quantity=stock_quantity,
                supplier=supplier,
                weight=weight,
            )
        elif normalized_type == "digital":
            download_size = kwargs.get("download_size", 0.0)
            return DigitalProduct(
                product_id=product_id,
                name=name,
                price=price,
                stock_quantity=stock_quantity,
                supplier=supplier,
                download_size=download_size,
            )
        else:
            raise ValueError(f"Unknown product type: {product_type}")
