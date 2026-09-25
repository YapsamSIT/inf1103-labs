order_file = 'orders.txt'

def load_inventory():
    history = []
    try:
        with open(order_file, 'r') as o:
            lines = o.read().splitlines()

        for line in lines:
            if not line:
                continue
            name, quantity = line.split(',', 1)
            history.append((name.strip(), int(quantity.strip())))
    except FileNotFoundError:
        pass
    return history


def save_inventory(history):

    with open(order_file, 'w') as o:
        for name, quantity in history:
            o.write(f"{name},{quantity}\n")

def print_current_orders(history):
    print("Current Orders:\n")
    if not history:
        print("It is empty for now...")
    else:
        for i, (name, quantity) in enumerate(history):
            print(f"{1001 + i}, {name}, {quantity}")



def process_delivery(current_total, new_value):
    return current_total + new_value


def calculate_tax(amount):
    return amount * 0.10


def generate_report(total_units, failed_attempts):
    print("Total Units Processed: ", total_units)
    print("Number of Failed/Refected Entries: ", failed_attempts)    



def get_valid_input(history):
    failed_entries = 0
    while True:
        product_name = input("Enter Product Name (Type 'quit' to quit): ")
        if product_name.lower() == "quit":
            save_inventory(history)
            print("\nOrder successfully saved to", order_file)
            break

        quantity = input("Enter Quantity: ")
        if not quantity.isdigit():
            print("The number is rejected.")
            failed_entries += 1
            continue

        quantity = int(quantity)
        history.append((product_name, quantity))

        new_id = 1001 + len(history) - 1
        print(f"\nNew Order Added:\n{new_id}, {product_name}, {quantity}\n")

    return failed_entries


def main():
    history = load_inventory()
    print_current_orders(history)

    failed_entries = get_valid_input(history)

main()