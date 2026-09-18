
def process_delivery(current_total, new_value):
    return current_total + new_value


def calculate_tax(amount):
    return amount * 0.10


def generate_report(total_units, failed_attempts):
    print("Total Units Processed: ", total_units)
    print("Number of Failed/Refected Entries: ", failed_attempts)    

def get_valid_input():
    global inventory
    global failed_entries
    inventory = 0
    failed_entries = 0 
    while True: 
        stock_quantity = input("Enter Stock Quantity (Type 'quit' to quit): ")
        if stock_quantity.lower() == "quit": 
            print("Total Units Processed:", inventory)
            break
        elif not stock_quantity.isdigit():
            print("The number is rejected.")
            failed_entries += 1
            continue

        actual = int(stock_quantity)
        actual = actual + calculate_tax(actual)
        inventory = process_delivery(inventory, actual)

        if  inventory > 500: 
            print("Alert, overloaded")
            inventory -= actual
            break
    return inventory 
    return failed_entries
    




def main():
    get_valid_input()
    generate_report(inventory, failed_entries)
    

main()