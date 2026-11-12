"""Automated tests for Lab 8:
Object-Oriented Relationships Part 2 (Association, Aggregation, Composition, LSP, Polymorphism)
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(__file__))

from supplier import Supplier
from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from inventory import Inventory
from order import Order
from order_line import OrderLine


class TestAssociation(unittest.TestCase):
    """Section 2: Supplier and Product Association tests."""

    def setUp(self):
        self.supplier = Supplier("S001", "Acme Supplies", "acme@example.com")
        self.physical = PhysicalProduct("P101", "Toolbox", 45.0, 5, self.supplier, weight=3.5)
        self.digital = DigitalProduct("D101", "PDF Manual", 10.0, 50, self.supplier, download_size=2.5)

    def test_supplier_attributes_and_independence(self):
        self.assertEqual(self.supplier.supplier_id, "S001")
        self.assertEqual(self.supplier.name, "Acme Supplies")
        self.assertEqual(self.supplier.contact_email, "acme@example.com")

    def test_product_references_supplier(self):
        self.assertIs(self.physical.supplier, self.supplier)
        self.assertIs(self.digital.supplier, self.supplier)
        self.assertEqual(self.physical.supplier.name, "Acme Supplies")

    def test_deleting_local_variable_preserves_product_supplier(self):
        temp_sup = Supplier("S999", "Temp Supplier", "temp@example.com")
        prod = PhysicalProduct("P999", "Temp Item", 15.0, 2, temp_sup)
        del temp_sup
        # Product still references the Supplier object in memory
        self.assertEqual(prod.supplier.name, "Temp Supplier")


class TestAggregation(unittest.TestCase):
    """Section 3: Inventory and Product Aggregation tests."""

    def setUp(self):
        self.supplier = Supplier("S002", "Logi Supplies", "logi@example.com")
        self.prod = PhysicalProduct("P201", "Webcam", 60.0, 8, self.supplier, weight=0.3)
        self.inv_a = Inventory("Inventory Alpha")
        self.inv_b = Inventory("Inventory Beta")

    def test_product_exists_independently_of_inventory(self):
        self.inv_a.add_product(self.prod)
        self.assertEqual(len(self.inv_a.products), 1)

        # Remove from Alpha
        removed = self.inv_a.remove_product("P201")
        self.assertIs(removed, self.prod)
        self.assertEqual(len(self.inv_a.products), 0)

        # Product is not destroyed and can be added to Beta
        self.inv_b.add_product(removed)
        self.assertEqual(len(self.inv_b.products), 1)
        self.assertIs(self.inv_b.find_product("P201"), self.prod)

    def test_find_product_returns_none_if_missing(self):
        self.assertIsNone(self.inv_a.find_product("NONEXISTENT"))


class TestComposition(unittest.TestCase):
    """Section 4: Order and OrderLine Composition tests."""

    def setUp(self):
        self.supplier = Supplier("S003", "Component World", "cw@example.com")
        self.p1 = PhysicalProduct("P301", "USB Cable", 8.0, 50, self.supplier, weight=0.1)
        self.p2 = DigitalProduct("D301", "Antivirus 1Yr", 30.0, 100, self.supplier, download_size=50.0)

    def test_order_creates_and_manages_order_lines(self):
        order = Order("ORD-500")
        order.add_order_line(self.p1, 3)   # 3 * 8.0 = 24.0
        order.add_order_line(self.p2, 2)   # 2 * 30.0 = 60.0

        self.assertEqual(len(order.order_lines), 2)
        self.assertEqual(order.calculate_total(), 84.0)

    def test_order_line_subtotal(self):
        line = OrderLine(self.p1, 4)
        self.assertEqual(line.calculate_subtotal(), 32.0)

    def test_order_line_invalid_quantity(self):
        with self.assertRaises(ValueError):
            OrderLine(self.p1, 0)
        with self.assertRaises(ValueError):
            OrderLine(self.p1, -5)

    def test_same_product_in_different_orders_creates_distinct_order_lines(self):
        order1 = Order("O1")
        order2 = Order("O2")
        order1.add_order_line(self.p1, 2)
        order2.add_order_line(self.p1, 5)

        line1 = order1.order_lines[0]
        line2 = order2.order_lines[0]

        # Distinct OrderLine objects (Composition)
        self.assertIsNot(line1, line2)
        # But both reference the exact same Product object
        self.assertIs(line1.product, line2.product)


class TestLSPAndPolymorphism(unittest.TestCase):
    """Sections 6 & 7: Liskov Substitution Principle and Polymorphism."""

    def setUp(self):
        self.supplier = Supplier("S004", "OmniTech", "omni@example.com")
        self.physical = PhysicalProduct("P401", "Mousepad", 15.0, 20, self.supplier, weight=0.2)
        self.digital = DigitalProduct("D401", "Game DLC", 12.0, 200, self.supplier, download_size=800.0)

    def test_lsp_substitutability(self):
        # show_product_details helper accepts any Product
        def get_summary(p: Product) -> str:
            return f"{p.name} - {p.get_fulfilment_info()}"

        # Both subclasses satisfy Product contracts without breaking expectations
        self.assertIn("shipping", get_summary(self.physical))
        self.assertIn("digitally", get_summary(self.digital))

    def test_polymorphism_in_inventory(self):
        inv = Inventory("Polymorphic Shelf")
        inv.add_product(self.physical)
        inv.add_product(self.digital)

        fulfilments = [p.get_fulfilment_info() for p in inv.products]
        self.assertEqual(len(fulfilments), 2)
        self.assertEqual(fulfilments[0], "This product requires physical shipping.")
        self.assertEqual(fulfilments[1], "This product is delivered digitally via download.")


if __name__ == "__main__":
    unittest.main()
