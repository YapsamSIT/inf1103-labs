"""INF1103: Lab 8 - Object-Oriented Relationships Part 2
Demonstration of Association, Aggregation, Composition, Type Hints,
Liskov Substitution Principle (LSP), and Polymorphism.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from supplier import Supplier
from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from inventory import Inventory
from order import Order


def show_product_details(product: Product) -> None:
    """Liskov Substitution Principle (LSP) demonstration.
    This function accepts any Product and relies only on the Product abstraction.
    Both PhysicalProduct and DigitalProduct work without modifying this function.
    """
    print(f"\n[LSP Check] Showing details for product '{product.name}':")
    product.display_information()
    print(f"Fulfilment method: {product.get_fulfilment_info()}")


def demonstrate_association() -> None:
    print("=" * 60)
    print("1. DEMONSTRATE ASSOCIATION: Supplier <--> Product")
    print("=" * 60)
    # Supplier is created independently
    supplier = Supplier("SUP-101", "Global Logistics Corp", "contact@globallogistics.com")
    supplier.display_information()

    # Product accepts Supplier reference
    desk_lamp = PhysicalProduct("P001", "Desk Lamp", 25.00, 10, supplier, weight=1.5)
    photo_editor = DigitalProduct("D001", "Photo Editor Pro", 49.90, 100, supplier, download_size=250.0)

    print("\nProducts display their associated supplier:")
    desk_lamp.display_information()
    print()
    photo_editor.display_information()

    # Predict First check: deleting the local variable 'supplier'
    print("\n--- Predict First Test (del supplier) ---")
    del supplier
    print("Local variable 'supplier' deleted.")
    print("Can desk_lamp still access supplier? ->", desk_lamp.supplier.name)
    print("Explanation: The Product still holds a reference to the Supplier object in memory.")


def demonstrate_aggregation() -> None:
    print("\n" + "=" * 60)
    print("2. DEMONSTRATE AGGREGATION: Inventory <>-- Product")
    print("=" * 60)
    supplier = Supplier("SUP-202", "Nordic Supplies", "sales@nordic.com")
    chair = PhysicalProduct("P002", "Office Chair", 120.00, 15, supplier, weight=8.5)

    inv_a = Inventory("Warehouse North")
    inv_b = Inventory("Warehouse South")

    print("Created chair before adding to any inventory.")
    inv_a.add_product(chair)
    print(f"Added chair '{chair.name}' to {inv_a.name}.")
    print(f"{inv_a.name} contains {len(inv_a.products)} product(s).")

    # Predict First check: Remove from A and transfer to B
    print("\n--- Predict First Test (Remove from Inventory A) ---")
    removed = inv_a.remove_product("P002")
    print(f"Removed '{removed.name}' from {inv_a.name}.")
    print(f"{inv_a.name} now contains: {len(inv_a.products)} product(s).")
    print("Does removed product still exist and function? ->", removed.name, f"${removed.price:.2f}")

    inv_b.add_product(removed)
    print(f"Transferred '{removed.name}' to {inv_b.name}.")
    print(f"{inv_b.name} now contains: {len(inv_b.products)} product(s).")


def demonstrate_composition() -> None:
    print("\n" + "=" * 60)
    print("3. DEMONSTRATE COMPOSITION: Order *-- OrderLine")
    print("=" * 60)
    supplier = Supplier("SUP-303", "Apex Wholesale", "orders@apex.com")
    item1 = PhysicalProduct("P003", "Monitor Stand", 39.50, 20, supplier, weight=2.1)
    item2 = DigitalProduct("D002", "Cloud Backup 1TB", 19.99, 50, supplier, download_size=10.0)

    # Order creates its own OrderLine objects internally
    order1 = Order("ORD-1001")
    order1.add_order_line(item1, 2)
    order1.add_order_line(item2, 1)
    order1.display_order_summary()

    # Predict First check: Add same product to a second Order
    print("--- Predict First Test (Same Product in Two Orders) ---")
    order2 = Order("ORD-1002")
    order2.add_order_line(item1, 5)

    print(f"Total OrderLine objects across orders: {len(order1.order_lines) + len(order2.order_lines)} (2 in order1, 1 in order2)")
    print(f"Order1 line 0 product is Order2 line 0 product? -> {order1.order_lines[0].product is order2.order_lines[0].product}")
    print(f"Order1 line 0 is Order2 line 0? -> {order1.order_lines[0] is order2.order_lines[0]}")
    print("Explanation: Each order owns distinct OrderLine instances, but both OrderLines refer to the same Product.")


def demonstrate_lsp_and_polymorphism() -> None:
    print("\n" + "=" * 60)
    print("4. DEMONSTRATE LSP & POLYMORPHISM")
    print("=" * 60)
    supplier = Supplier("SUP-404", "TechHub", "support@techhub.com")
    p_prod = PhysicalProduct("P004", "Mechanical Keyboard", 89.00, 12, supplier, weight=1.1)
    d_prod = DigitalProduct("D003", "Audio Editor Pro", 59.00, 200, supplier, download_size=120.0)

    # LSP: Passing both subtypes to a function expecting base Product
    show_product_details(p_prod)
    show_product_details(d_prod)

    # Polymorphism: Iterating through an Inventory's list[Product]
    print("\n--- Polymorphism through Inventory Collection ---")
    inventory = Inventory("Flagship Store")
    inventory.add_product(p_prod)
    inventory.add_product(d_prod)
    inventory.display_all_products()


def main() -> None:
    demonstrate_association()
    demonstrate_aggregation()
    demonstrate_composition()
    demonstrate_lsp_and_polymorphism()


if __name__ == "__main__":
    main()
