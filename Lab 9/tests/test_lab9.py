"""Automated unit test suite for Lab 9:
Design Patterns and Error Handling (Strategy, Factory, Validation, Exception Handling)
Ready for continuous integration (CI) pipelines.
"""

import os
import sys
import tempfile
import unittest
from unittest.mock import patch

# Add parent directory of tests (Lab 9) to module search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from supplier import Supplier
from inventory import Inventory
from order import Order
from order_line import OrderLine
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from product_factory import ProductFactory
from discount_strategy import (
    DiscountStrategy,
    NoDiscount,
    PercentageDiscount,
    BulkDiscount,
    StudentDiscount,
)
from file_loader import get_positive_float, load_products


class TestDiscountStrategies(unittest.TestCase):
    """Tests for Strategy pattern implementations."""

    def test_no_discount(self):
        strategy = NoDiscount()
        self.assertEqual(strategy.apply(100.0), 100.0)
        self.assertEqual(strategy.apply(0.0), 0.0)

    def test_percentage_discount(self):
        strategy = PercentageDiscount(10)
        self.assertAlmostEqual(strategy.apply(200.0), 180.0)
        self.assertAlmostEqual(strategy.apply(250.0), 225.0)

        # 0% discount
        zero_disc = PercentageDiscount(0)
        self.assertEqual(zero_disc.apply(150.0), 150.0)

        # 100% discount
        full_disc = PercentageDiscount(100)
        self.assertEqual(full_disc.apply(150.0), 0.0)

        # Invalid percentages
        with self.assertRaises(ValueError):
            PercentageDiscount(-5)
        with self.assertRaises(ValueError):
            PercentageDiscount(105)

    def test_bulk_discount(self):
        strategy = BulkDiscount(threshold=200, amount=20)

        # Total meets threshold
        self.assertEqual(strategy.apply(200.0), 180.0)
        self.assertEqual(strategy.apply(250.0), 230.0)

        # Total below threshold
        self.assertEqual(strategy.apply(199.99), 199.99)
        self.assertEqual(strategy.apply(50.0), 50.0)

        # Invalid threshold or amount
        with self.assertRaises(ValueError):
            BulkDiscount(-10, 20)
        with self.assertRaises(ValueError):
            BulkDiscount(200, -5)

    def test_student_discount(self):
        strategy = StudentDiscount(percentage=5.0)
        self.assertAlmostEqual(strategy.apply(100.0), 95.0)
        self.assertAlmostEqual(strategy.apply(250.0), 237.5)


class TestOrderWithDiscountStrategy(unittest.TestCase):
    """Tests demonstrating Order using DiscountStrategy dynamically."""

    def setUp(self):
        self.supplier = Supplier("S1", "Test Sup", "test@example.com")
        self.prod1 = ProductFactory.create("physical", "P1", "Desk", 200.0, 5, self.supplier)
        self.prod2 = ProductFactory.create("physical", "P2", "Mat", 50.0, 10, self.supplier)

    def test_default_strategy_is_no_discount(self):
        order = Order("ORD-1")
        order.add_order_line(self.prod1, 1)
        self.assertIsInstance(order.discount, NoDiscount)
        self.assertEqual(order.calculate_total(), 200.0)

    def test_dynamic_strategy_switching(self):
        # Order with lines adding up to 250
        order = Order("ORD-2", BulkDiscount(200, 20))
        order.add_order_line(self.prod1, 1)  # 200
        order.add_order_line(self.prod2, 1)  # 50 => raw total = 250

        # Predict First Section 2.3 check 1: BulkDiscount(200, 20) -> 230.0
        self.assertEqual(order.calculate_total(), 230.0)

        # Predict First Section 2.3 check 2: Switch to PercentageDiscount(10) -> 225.0
        order.set_discount(PercentageDiscount(10))
        self.assertEqual(order.calculate_total(), 225.0)

        # Switch to StudentDiscount(5%) -> 237.5
        order.set_discount(StudentDiscount(5))
        self.assertAlmostEqual(order.calculate_total(), 237.5)


class TestProductFactory(unittest.TestCase):
    """Tests for ProductFactory centralised creation."""

    def setUp(self):
        self.supplier = Supplier("S2", "Factory Supply", "fs@example.com")

    def test_create_physical_product(self):
        product = ProductFactory.create(
            "physical", "P10", "Laptop Stand", 40.0, 15, self.supplier, weight=1.5
        )
        self.assertIsInstance(product, PhysicalProduct)
        self.assertEqual(product.name, "Laptop Stand")
        self.assertEqual(product.weight, 1.5)

    def test_create_digital_product(self):
        product = ProductFactory.create(
            "digital", "D10", "Code Editor", 60.0, 50, self.supplier, download_size=150.0
        )
        self.assertIsInstance(product, DigitalProduct)
        self.assertEqual(product.name, "Code Editor")
        self.assertEqual(product.download_size, 150.0)

    def test_unknown_product_type_raises_value_error(self):
        # Predict First Section 3.2: Calling with "service"
        with self.assertRaises(ValueError) as context:
            ProductFactory.create("service", "S1", "Maintenance", 50.0, 5, self.supplier)
        self.assertIn("Unknown product type", str(context.exception))


class TestValidation(unittest.TestCase):
    """Tests for price, stock quantity, and order quantity validation."""

    def setUp(self):
        self.supplier = Supplier("S3", "Val Supplies", "val@example.com")

    def test_product_price_must_be_greater_than_zero(self):
        with self.assertRaises(ValueError):
            ProductFactory.create("physical", "P1", "Free Gift", 0.0, 10, self.supplier)
        with self.assertRaises(ValueError):
            ProductFactory.create("physical", "P2", "Debt Item", -15.0, 10, self.supplier)

    def test_product_stock_cannot_be_negative(self):
        with self.assertRaises(ValueError):
            ProductFactory.create("digital", "D1", "Negative Stock", 20.0, -1, self.supplier)

    def test_order_line_quantity_must_be_greater_than_zero(self):
        prod = ProductFactory.create("physical", "P3", "Mouse", 25.0, 10, self.supplier)
        with self.assertRaises(ValueError):
            OrderLine(prod, 0)
        with self.assertRaises(ValueError):
            OrderLine(prod, -3)


class TestExceptionHandlingAndFileLoading(unittest.TestCase):
    """Tests for try/except/else/finally CSV loading and input helpers."""

    def setUp(self):
        self.supplier = Supplier("S4", "Load Supplies", "load@example.com")
        self.inventory = Inventory("Test Inventory")

    def test_get_positive_float_recovers_from_invalid_input(self):
        # Predict First Section 5.1: inputs 'abc', then '-5', then '12.50'
        inputs = iter(["abc", "-5", "12.50"])
        with patch("builtins.input", lambda prompt: next(inputs)):
            result = get_positive_float("Enter price: ")
            self.assertEqual(result, 12.50)

    def test_load_products_with_mixed_csv_rows(self):
        # Predict First Section 5.2: 5 rows with 2 bad rows
        csv_content = (
            "product_type,product_id,name,price,stock_quantity\n"
            "physical,P001,Desk Lamp,25.00,10\n"
            "digital,D001,Photo Editor,49.90,100\n"
            "service,S001,Installation,30.00,5\n"
            "physical,P002,Office Chair,abc,3\n"
            "physical,P003,Monitor Stand,39.50,7\n"
        )
        with tempfile.NamedTemporaryFile("w", delete=False, suffix=".csv") as tmp:
            tmp.write(csv_content)
            tmp_path = tmp.name

        try:
            loaded_count = load_products(tmp_path, self.inventory, self.supplier)
            self.assertEqual(loaded_count, 3)
            self.assertEqual(len(self.inventory.products), 3)
            self.assertIsNotNone(self.inventory.find_product("P001"))
            self.assertIsNotNone(self.inventory.find_product("D001"))
            self.assertIsNotNone(self.inventory.find_product("P003"))
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    def test_load_products_missing_file_does_not_crash(self):
        missing_path = os.path.join(tempfile.gettempdir(), "non_existent_inventory_file.csv")
        if os.path.exists(missing_path):
            os.remove(missing_path)

        # Should catch FileNotFoundError gracefully and return 0
        loaded_count = load_products(missing_path, self.inventory, self.supplier)
        self.assertEqual(loaded_count, 0)
        self.assertEqual(len(self.inventory.products), 0)


if __name__ == "__main__":
    unittest.main()
