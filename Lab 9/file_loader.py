import csv
from product_factory import ProductFactory
from inventory import Inventory
from supplier import Supplier


def get_positive_float(prompt: str) -> float:
    """Repeatedly ask the user for a positive float until valid.
    Handles ValueError from invalid conversion and checks that value > 0.
    """
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("Please enter a number greater than zero.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number, e.g. 12.50")


def load_products(path: str, inventory: Inventory, supplier: Supplier) -> int:
    """Load products from a CSV file into an inventory using ProductFactory.
    Employs try / except FileNotFoundError / else / finally structure:
    - Reports missing file gracefully without crashing.
    - Uses an inner try/except ValueError to report and skip corrupt rows while continuing.
    - Always executes the finally block.
    Returns the count of successfully loaded products.
    """
    loaded = 0
    try:
        file = open(path, newline="", encoding="utf-8")
    except FileNotFoundError:
        print(f"Products file not found: {path}")
    else:
        with file:
            reader = csv.reader(file)
            header = next(reader, None)  # Skip header row
            for row_idx, row in enumerate(reader, start=2):
                if not row or not any(cell.strip() for cell in row):
                    continue
                try:
                    if len(row) < 5:
                        raise ValueError(f"Insufficient columns ({len(row)} found, 5 required)")
                    p_type, p_id, p_name, p_price_str, p_stock_str = [cell.strip() for cell in row[:5]]
                    # Float/Int conversion validation
                    price = float(p_price_str)
                    stock_qty = int(p_stock_str)
                    # ProductFactory creation & domain validation
                    product = ProductFactory.create(
                        product_type=p_type,
                        product_id=p_id,
                        name=p_name,
                        price=price,
                        stock_quantity=stock_qty,
                        supplier=supplier,
                    )
                    inventory.add_product(product)
                    loaded += 1
                except ValueError as e:
                    print(f"Row {row_idx} skipped - invalid data {row}: {e}")
            print(f"{loaded} products loaded.")
    finally:
        print("Load attempt finished.")
    return loaded
