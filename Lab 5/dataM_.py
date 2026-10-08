import json
import os

INVENTORY_FILE = os.environ.get("INVENTORY_FILE", "Lab 5\inventory.json")

def load_inventory():
    """Load inventory from JSON file if it exists, else return empty list."""
    if os.path.exists(INVENTORY_FILE):
        print(f"{os.path.basename(INVENTORY_FILE)} found.")
        try:
            with open(INVENTORY_FILE, "r") as f:
                inventory = json.load(f)
            print("Inventory loaded successfully.")
            return inventory
        except (json.JSONDecodeError, OSError):
            print("Could not read file. Starting with an empty inventory.")
            return []
    print(f"{os.path.basename(INVENTORY_FILE)} not found. Starting with an empty inventory.")
    return []


def save_inventory(inventory):
    """Save inventory list to JSON file."""
    try:
        with open(INVENTORY_FILE, "w") as f:
            json.dump(inventory, f, indent=4)
        print(f"Inventory saved successfully to {os.path.basename(INVENTORY_FILE)}.")
    except OSError as e:
        print(f"Error saving inventory: {e}")

def find_product(inventory, product_id):
    """Return the product dictionary matching product_id, or None."""
    for product in inventory:
        if product["id"].lower() == product_id.lower():
            return product
    return None


def add_product(inventory, product_id, name, price, stock):
    """Add a new product dictionary to the inventory list."""
    if find_product(inventory, product_id):
        print("A product with that ID already exists.")
        return False
    inventory.append({
        "id": product_id,
        "name": name,
        "price": price,
        "stock": stock,
    })
    print("Product added successfully!")
    return True


def update_stock(inventory, product_id, new_stock):
    """Update the stock quantity for an existing product."""
    product = find_product(inventory, product_id)
    if product is None:
        print("Product not found.")
        return False
    product["stock"] = new_stock
    print("Stock updated successfully!")
    return True


def search_product(inventory, product_id):
    """Return the product dictionary if found, otherwise None."""
    return find_product(inventory, product_id)


def display_all(inventory):
    """Print every product in the inventory."""
    print("\nCurrent Inventory")
    print("-" * 48)
    if not inventory:
        print("Inventory is empty.")
    for p in inventory:
        print(f"ID: {p['id']} | Name: {p['name']} | "
              f"Price: ${p['price']:.2f} | Stock: {p['stock']}")
    print("-" * 48)

def read_float(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                print("Value cannot be negative.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number.")


def read_int(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value < 0:
                print("Value cannot be negative.")
                continue
            return value
        except ValueError:
            print("Please enter a whole number.")


def show_menu():
    print("\n----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("----------------------------")


def main():
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)

    inventory = load_inventory()

    while True:
        show_menu()
        try:
            choice = input("Enter option: ").strip()
        except EOFError:
            choice = "6"

        if choice == "1":
            display_all(inventory)

        elif choice == "2":
            print("\nAdd New Product")
            product_id = input("Product ID: ").strip()
            name = input("Product Name: ").strip()
            price = read_float("Price: ")
            stock = read_int("Stock Quantity: ")
            add_product(inventory, product_id, name, price, stock)

        elif choice == "3":
            print("\nUpdate Stock")
            product_id = input("Enter Product ID: ").strip()
            product = find_product(inventory, product_id)
            if product is None:
                print("Product not found.")
            else:
                print("Product Found:")
                print(f"Name: {product['name']}")
                print(f"Current Stock: {product['stock']}")
                new_stock = read_int("New Stock Quantity: ")
                update_stock(inventory, product_id, new_stock)

        elif choice == "4":
            print("\nSearch Product")
            product_id = input("Enter Product ID: ").strip()
            product = search_product(inventory, product_id)
            if product:
                print("Product Found")
                print("-" * 48)
                print(f"ID: {product['id']}")
                print(f"Name: {product['name']}")
                print(f"Price: ${product['price']:.2f}")
                print(f"Stock: {product['stock']}")
                print("-" * 48)
            else:
                print("Product not found.")

        elif choice == "5":
            print("Saving inventory...")
            save_inventory(inventory)

        elif choice == "6":
            print("Saving inventory before exit...")
            save_inventory(inventory)
            print("Thank you for using Inventory Management System.")
            print("Program terminated.")
            break

        else:
            print("Invalid option. Please choose 1-6.")


if __name__ == "__main__":
    main()