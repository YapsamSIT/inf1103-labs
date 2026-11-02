import json

from inventory import Inventory
from products import Product

DATA_FILE = "inventory.json"

def load_inventory(inventory, filename):
    try:
        with open(filename, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        print("No saved inventory found, Starting empty.")
        return
    for item in data:
        product = Product(item["product_id"], item["name"],
                          item["price"], item["stock"])
        inventory.add_product(product)

def save_inventory(inventory, filename):
    data = [product.to_dict() for product in inventory.get_products()]
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)


def add_product_menu(inventory):
    try:
        product_id = input("Product ID: ").strip()
        name = input("Name: ").strip()
        price = float(input("Price: "))
        stock = int(input("Stock: "))
        inventory.add_product(Product(product_id, name, price, stock))
        print("Product added.")
    except ValueError as error:
        print(f"Error: {error}")

def update_stock_menu(inventory):
    try:
        product_id = input("Product ID: ").strip()
        quantity = int(input("New stock quantity: "))
        inventory.update_stock(product_id, quantity)
        print("Stock updated.")
    except (ValueError, KeyError) as error:
        print(f"Error: {error}")

def search_menu(inventory):
    product_id = input("Product ID to search: ").strip()
    product = inventory.search_product(product_id)
    if product is None:
        print("Product not found.")
    else:
        product.display_information()

def main():
    inventory = Inventory()
    load_inventory(inventory, DATA_FILE)

    while True:
        print("\n===== Inventory Management =====")
        print("1. Display all products")
        print("2. Add a product")
        print("3. Update stock")
        print("4. Search for a product")
        print("5. Save inventory")
        print("6. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            inventory.display_all()
        elif choice == "2":
            add_product_menu(inventory)
        elif choice == "3":
            update_stock_menu(inventory)
        elif choice == "4":
            search_menu(inventory)
        elif choice == "5":
            save_inventory(inventory, DATA_FILE)
            print("Inventory saved.")
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()