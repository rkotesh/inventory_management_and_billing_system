import sys
from utils import ensure_directories
from products import add_product, update_product, delete_product, search_products, list_all_products
from cart import Cart, checkout
from reports import report_total_sales_by_date, report_low_stock


def product_menu():
    while True:
        print("\n--- Product Management ---")
        print("1. Add product")
        print("2. Update product")
        print("3. Delete product")
        print("4. Search product")
        print("5. List all products")
        print("0. Back")
        choice = input("Choice: ").strip()

        match choice:
            case "1": add_product()
            case "2": update_product()
            case "3": delete_product()
            case "4": search_products()
            case "5": list_all_products()
            case "0": return
            case _: print("Invalid choice.")


def order_menu():
    cart = Cart()
    while True:
        print("\n--- Order Processing ---")
        print("1. Add item to cart")
        print("2. Remove item from cart")
        print("3. View cart")
        print("4. Checkout")
        print("0. Back")
        choice = input("Choice: ").strip()

        match choice:
            case "1":
                try:
                    pid = int(input("Product ID: "))
                    qty = int(input("Quantity: "))
                    cart.add_item(pid, qty)
                except ValueError:
                    print("Invalid input.")
            case "2":
                try:
                    pid = int(input("Product ID to remove: "))
                    cart.remove_item(pid)
                except ValueError:
                    print("Invalid input.")
            case "3": cart.list_cart()
            case "4": checkout(cart); return
            case "0": return
            case _: print("Invalid choice.")


def sales_menu():
    while True:
        print("\n--- Reports ---")
        print("1. Total sales for a day")
        print("2. Low-stock products")
        print("0. Back")
        choice = input("Choice: ").strip()

        match choice:
            case "1": report_total_sales_by_date()
            case "2": report_low_stock()
            case "0": return
            case _: print("Invalid choice.")


def main_menu():
    ensure_directories()
    while True:
        print("\n=== Inventory & Billing System ===")
        print("1. Product Management")
        print("2. Order Processing")
        print("3. Reports")
        print("0. Exit")
        choice = input("Choice: ").strip()

        match choice:
            case "1": product_menu()
            case "2": order_menu()
            case "3": sales_menu()
            case "0": print("Goodbye."); sys.exit(0)
            case _: print("Invalid choice.")


if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\nProgram stopped by user. Bye!")
