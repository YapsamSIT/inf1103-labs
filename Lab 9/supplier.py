class Supplier:
    """Represents a supplier in the inventory system."""

    def __init__(self, supplier_id: str, name: str, contact_email: str):
        self.supplier_id: str = supplier_id
        self.name: str = name
        self.contact_email: str = contact_email

    def display_information(self) -> None:
        print(f"Supplier ID: {self.supplier_id}")
        print(f"Supplier Name: {self.name}")
        print(f"Contact Email: {self.contact_email}")

    def __repr__(self) -> str:
        return f"Supplier({self.supplier_id!r}, {self.name!r}, {self.contact_email!r})"
