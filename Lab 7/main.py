from inventory import Inventory
from physical_product import PhysicalProduct
from digital_product import DigitalProduct

DATA_FILE = "inventory.json"


def read_number(prompt, cast=float):
    while True:
        try:
            return cast(input(prompt))
        except ValueError:
            print("Invalid number, try again.")


def add_product_menu(inventory):
    kind = input("Type - (p)hysical or (d)igital? ").strip().lower()
    if kind not in ("p", "d"):
        print("Invalid type.")
        return
    product_id = input("Product ID: ").strip()
    name = input("Name: ").strip()
    price = read_number("Price: ")
    stock = read_number("Stock quantity: ", int)
    try:
        if kind == "p":
            weight = read_number("Weight (kg): ")
            product = PhysicalProduct(product_id, name, price, stock, weight)
        else:
            size = read_number("Download size (MB): ")
            product = DigitalProduct(product_id, name, price, stock, size)
        inventory.add_product(product)
        print("Product added.")
    except ValueError as e:
        print(f"Error: {e}")


def update_stock_menu(inventory):
    product_id = input("Product ID: ").strip()
    change = read_number("Change in stock (+/-): ", int)
    try:
        inventory.update_stock(product_id, change)
        print("Stock updated.")
    except (KeyError, ValueError) as e:
        print(f"Error: {e}")


def search_menu(inventory):
    results = inventory.search(input("Search term: ").strip())
    if not results:
        print("No products found.")
    for product in results:
        product.display_information()
        print("-" * 30)


def save_menu(inventory):
    inventory.save(DATA_FILE)
    print(f"Saved to {DATA_FILE}.")


def load_menu(inventory):
    try:
        inventory.load(DATA_FILE)
        print(f"Loaded from {DATA_FILE}.")
    except FileNotFoundError:
        print("No saved file found.")
    except (ValueError, KeyError) as e:
        print(f"Could not load data: {e}")


def main():
    inventory = Inventory()
    actions = {
        "1": lambda: inventory.display_all(),
        "2": lambda: add_product_menu(inventory),
        "3": lambda: update_stock_menu(inventory),
        "4": lambda: search_menu(inventory),
        "5": lambda: save_menu(inventory),
        "6": lambda: load_menu(inventory),
    }
    while True:
        print("\n=== Inventory Management ===")
        print("1. Display all products\n2. Add a product\n3. Update stock")
        print("4. Search for a product\n5. Save inventory\n6. Load inventory\n7. Exit")
        choice = input("Choose: ").strip()
        if choice == "7":
            print("Goodbye!")
            break
        action = actions.get(choice)
        if action:
            action()
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
