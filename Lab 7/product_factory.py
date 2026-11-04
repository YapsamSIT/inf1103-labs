from physical_product import PhysicalProduct
from digital_product import DigitalProduct

# Maps the saved "type" identifier to the class that can rebuild it.
PRODUCT_TYPES = {
    "physical": PhysicalProduct,
    "digital": DigitalProduct,
}


def create_product_from_dict(data):
    """Create the right Product subclass from saved data."""
    product_type = data.get("type")
    if product_type not in PRODUCT_TYPES:
        raise ValueError(f"Unknown product type: {product_type!r}")
    return PRODUCT_TYPES[product_type].from_dict(data)
