import os
import csv
from datetime import datetime
from utils import PRODUCTS_FILE, SALES_FILE, BILLS_DIR, read_csv_dicts, write_csv, format_currency, timestamp_id, current_datetime
from products import read_products, write_products


class CartItem:
    def __init__(self, product_id, name, price, qty):
        self.product_id = int(product_id)
        self.name = name
        self.price = float(price)
        self.qty = int(qty)

    def line_total(self):
        return self.price * self.qty


class Cart:
    def __init__(self):
        self.items = []

    def add_item(self, pid, qty):
        products = read_products()
        prod = next((p for p in products if p["id"] == pid), None)
        if not prod:
            print("Product not found.")
            return
        if qty <= 0:
            print("Quantity must be > 0.")
            return
        if prod["stock"] < qty:
            print(f"Insufficient stock. Available: {prod['stock']}")
            return

        for it in self.items:
            if it.product_id == pid:
                it.qty += qty
                print(f"Added {qty} more of {prod['name']} to cart.")
                return

        self.items.append(CartItem(pid, prod["name"], prod["price"], qty))
        print(f"Added {qty} * {prod['name']} to cart.")

    def remove_item(self, pid):
        for it in self.items:
            if it.product_id == pid:
                self.items.remove(it)
                print("Item removed.")
                return
        print("Item not in cart.")

    def is_empty(self):
        return not self.items

    def subtotal(self):
        return sum(it.line_total() for it in self.items)

    def list_cart(self):
        if self.is_empty():
            print("Cart is empty.")
            return
        print("{:<6} {:<30} {:>8} {:>6} {:>10}".format("PID", "Name", "UnitPrice", "Qty", "Total"))
        for it in self.items:
            print("{:<6} {:<30} {:>8} {:>6} {:>10}".format(it.product_id, it.name, format_currency(it.price), it.qty, format_currency(it.line_total())))
        print("Subtotal:", format_currency(self.subtotal()))


def checkout(cart: Cart):
    if cart.is_empty():
        print("Cart empty. Cannot checkout.")
        return

    subtotal = cart.subtotal()
    print("Subtotal:", format_currency(subtotal))
    discount_pct = float(input("Enter discount % (0 for none): ") or 0)
    discount_amount = subtotal * discount_pct / 100
    total = subtotal - discount_amount

    confirm = input(f"Total: {format_currency(total)}. Confirm purchase? (y/n): ").strip().lower()
    if confirm != "y":
        print("Checkout cancelled.")
        return

    products = read_products()
    for it in cart.items:
        for p in products:
            if p["id"] == it.product_id:
                p["stock"] = max(0, p["stock"] - it.qty)
    write_products(products)

    bill_id = timestamp_id("bill")
    ts = current_datetime()
    txt_path = os.path.join(BILLS_DIR, f"{bill_id}.txt")
    csv_path = os.path.join(BILLS_DIR, f"{bill_id}.csv")

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(f"=== BILL ===\nBill ID: {bill_id}\nDateTime: {ts}\n\n")
        f.write("{:<6} {:<30} {:>10} {:>6} {:>12}\n".format("PID", "Name", "UnitPrice", "Qty", "LineTotal"))
        for it in cart.items:
            f.write("{:<6} {:<30} {:>10} {:>6} {:>12}\n".format(it.product_id, it.name, format_currency(it.price), it.qty, format_currency(it.line_total())))
        f.write(f"\nSubtotal: {format_currency(subtotal)}\nDiscount({discount_pct}%): {format_currency(discount_amount)}\nTotal: {format_currency(total)}\nThank you!\n")

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["bill_id", "datetime", "product_id", "name", "unit_price", "qty", "line_total"])
        for it in cart.items:
            w.writerow([bill_id, ts, it.product_id, it.name, f"{it.price:.2f}", it.qty, f"{it.line_total():.2f}"])
        w.writerow([])
        w.writerow(["", "", "", "SUBTOTAL", f"{subtotal:.2f}"])
        w.writerow(["", "", "", f"DISCOUNT_{discount_pct}%", f"{discount_amount:.2f}"])
        w.writerow(["", "", "", "TOTAL", f"{total:.2f}"])

    with open(SALES_FILE, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow([bill_id, ts, f"{subtotal:.2f}", f"{discount_pct:.2f}", f"{total:.2f}"])

    print(f"Checkout complete. Bill saved: {txt_path}")
