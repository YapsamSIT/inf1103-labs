"""INF1103: Lab 9 - Design Patterns and Error Handling
Demonstrates:
- Strategy Pattern (Order Discounts)
- Factory Pattern (ProductFactory)
- Domain Validation (Price, Stock, Quantity)
- Exception Handling (try/except/else/finally with graceful error recovery)
"""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from supplier import Supplier
from inventory import Inventory
from order import Order
from product_factory import ProductFactory
from discount_strategy import (
    NoDiscount,
    PercentageDiscount,
    BulkDiscount,
    StudentDiscount,
)
from file_loader import load_products, get_positive_float


def demonstrate_strategy_pattern() -> None:
    print("=" * 65)
    print("1. STRATEGY PATTERN: Order Discounts")
    print("=" * 65)
    supplier = Supplier("SUP-1", "Central Distributor", "sales@central.com")

    # Build products via Factory
    desk = ProductFactory.create("physical", "P100", "Standing Desk", 200.0, 5, supplier, weight=25.0)
    mat = ProductFactory.create("physical", "P101", "Floor Mat", 50.0, 10, supplier, weight=2.0)

    # Order starts with BulkDiscount(200, 20)
    order = Order("ORD-901", BulkDiscount(200, 20))
    order.add_order_line(desk, 1)  # 200
    order.add_order_line(mat, 1)   # 50  => total = 250

    print("Initial Order with BulkDiscount(200, 20):")
    order.display_order_summary()
    print(f"-> Predict First check: Bulk discount on 250 should be $230.00: ${order.calculate_total():.2f}")

    # Switch strategy dynamically on the same order to PercentageDiscount(10)
    print("\nSwitching strategy dynamically to PercentageDiscount(10%):")
    order.set_discount(PercentageDiscount(10))
    order.display_order_summary()
    print(f"-> Predict First check: 10% discount on 250 should be $225.00: ${order.calculate_total():.2f}")

    # Switch to 4th strategy: StudentDiscount(5%)
    print("\nSwitching to StudentDiscount(5%):")
    order.set_discount(StudentDiscount(5))
    order.display_order_summary()


def demonstrate_factory_pattern() -> None:
    print("\n" + "=" * 65)
    print("2. FACTORY PATTERN: Centralised Product Creation")
    print("=" * 65)
    supplier = Supplier("SUP-2", "Global Tech", "info@globaltech.com")

    # Creating products without referencing PhysicalProduct or DigitalProduct classes
    p1 = ProductFactory.create("physical", "P201", "Ergonomic Mouse", 45.0, 30, supplier, weight=0.2)
    p2 = ProductFactory.create("digital", "D201", "Cloud Storage Plan", 9.99, 500, supplier, download_size=0.0)

    print(f"Created via Factory: {p1.name} (Type: {type(p1).__name__})")
    print(f"Created via Factory: {p2.name} (Type: {type(p2).__name__})")

    # Predict First check: unknown product type
    print("\n--- Predict First Test (ProductFactory with unknown type 'service') ---")
    try:
        ProductFactory.create("service", "S201", "Onsite Assembly", 80.0, 10, supplier)
    except ValueError as e:
        print(f"Caught expected ValueError: {e}")


def demonstrate_validation() -> None:
    print("\n" + "=" * 65)
    print("3. DOMAIN VALIDATION: Price, Stock, and Quantity Invariants")
    print("=" * 65)
    supplier = Supplier("SUP-3", "SafeGoods", "safety@safegoods.com")

    # Test 1: Price <= 0
    try:
        ProductFactory.create("physical", "P301", "Faulty Item", -10.0, 5, supplier)
    except ValueError as e:
        print(f"Price validation caught: {e}")

    # Test 2: Stock < 0
    try:
        ProductFactory.create("digital", "D301", "Ghost Software", 29.99, -5, supplier)
    except ValueError as e:
        print(f"Stock validation caught: {e}")

    # Test 3: OrderLine quantity <= 0
    valid_prod = ProductFactory.create("physical", "P302", "Paper Clips", 3.50, 100, supplier)
    test_order = Order("ORD-902")
    try:
        test_order.add_order_line(valid_prod, 0)
    except ValueError as e:
        print(f"OrderLine quantity validation caught: {e}")


def demonstrate_file_loading_and_exceptions() -> None:
    print("\n" + "=" * 65)
    print("4. EXCEPTION HANDLING: CSV Product Loading (try/except/else/finally)")
    print("=" * 65)
    supplier = Supplier("SUP-4", "Universal Supply", "orders@universal.com")
    inventory = Inventory("CSV Inventory")

    csv_path = os.path.join(os.path.dirname(__file__), "products.csv")

    print(f"--- Loading from '{csv_path}' ---")
    load_products(csv_path, inventory, supplier)

    print("\nInventory after loading:")
    inventory.display_all_products()

    print("\n--- Testing Missing File Graceful Recovery ---")
    missing_path = os.path.join(os.path.dirname(__file__), "non_existent_file.csv")
    load_products(missing_path, inventory, supplier)


def main() -> None:
    demonstrate_strategy_pattern()
    demonstrate_factory_pattern()
    demonstrate_validation()
    demonstrate_file_loading_and_exceptions()


if __name__ == "__main__":
    main()
