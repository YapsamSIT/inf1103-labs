import os
import tempfile
import unittest

from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from can_be_shipped import CanBeShipped
from inventory import Inventory


class TestProducts(unittest.TestCase):
    def setUp(self):
        self.guitar = PhysicalProduct("P1", "Guitar", 500.0, 3, 4.0)
        self.os = DigitalProduct("D1", "Operating System", 99.0, 100, 4500)

    def test_abstract_product_cannot_be_instantiated(self):
        with self.assertRaises(TypeError):
            Product("X", "Nope", 1.0, 1)

    def test_attributes(self):
        self.assertEqual(self.guitar.weight, 4.0)
        self.assertEqual(self.os.download_size, 4500)

    def test_fulfilment_info(self):
        self.assertIn("shipping", self.guitar.get_fulfilment_info())
        self.assertIn("digitally", self.os.get_fulfilment_info())

    def test_shipping(self):
        self.assertTrue(isinstance(self.guitar, CanBeShipped))
        self.assertFalse(isinstance(self.os, CanBeShipped))
        light = PhysicalProduct("P2", "Pick", 1.0, 10, 0.1)
        self.assertGreater(self.guitar.calculate_shipping_cost(),
                           light.calculate_shipping_cost())

    def test_stock_cannot_go_negative(self):
        with self.assertRaises(ValueError):
            self.guitar.update_stock(-10)


class TestInventory(unittest.TestCase):
    def test_save_and_load_preserve_types(self):
        inv = Inventory()
        inv.add_product(PhysicalProduct("P1", "Guitar", 500.0, 3, 4.0))
        inv.add_product(DigitalProduct("D1", "Operating System", 99.0, 100, 4500))
        path = os.path.join(tempfile.mkdtemp(), "inv.json")
        inv.save(path)

        loaded = Inventory()
        loaded.load(path)
        self.assertIsInstance(loaded.get_product("P1"), PhysicalProduct)
        self.assertIsInstance(loaded.get_product("D1"), DigitalProduct)
        self.assertEqual(loaded.get_product("P1").weight, 4.0)
        self.assertEqual(loaded.get_product("D1").download_size, 4500)

    def test_search_and_update(self):
        inv = Inventory()
        inv.add_product(PhysicalProduct("P1", "Guitar", 500.0, 3, 4.0))
        self.assertEqual(len(inv.search("guit")), 1)
        inv.update_stock("P1", 2)
        self.assertEqual(inv.get_product("P1").stock_quantity, 5)


if __name__ == "__main__":
    unittest.main()
