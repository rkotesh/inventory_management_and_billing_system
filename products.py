from utils import PRODUCTS_FILE, read_csv_dicts, write_csv, format_currency

def read_products():
    rows = read_csv_dicts(PRODUCTS_FILE)
    products = []
    for r in rows:
        if not r.get("id"):
            continue
        products.append({
            "id": int(r["id"]),
            "name": r["name"],
            "price": float(r["price"]),
            "stock": int(r["stock"])
        })
    return products


def write_products(products):
    rows = [[p["id"], p["name"], f"{p['price']:.2f}", p["stock"]] for p in products]
    write_csv(PRODUCTS_FILE, rows, ["id", "name", "price", "stock"])


def next_product_id(products):
    return max((p["id"] for p in products), default=0) + 1


def add_product():
    products = read_products()
    pid = next_product_id(products)
    name = input("Product name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return

    try:
        price = float(input("Price: ").strip())
        stock = int(input("Stock quantity: ").strip())
    except ValueError:
        print("Invalid numeric input.")
        return

    products.append({"id": pid, "name": name, "price": price, "stock": stock})
    write_products(products)
    print(f"Product added with ID {pid}.")


def update_product():
    try:
        pid = int(input("Enter product ID to update: ").strip())
    except ValueError:
        print("Invalid ID.")
        return

    products = read_products()
    for p in products:
        if p["id"] == pid:
            print(f"Current: Name='{p['name']}', Price={format_currency(p['price'])}, Stock={p['stock']}")
            new_name = input("New name (leave blank to keep): ").strip()
            if new_name:
                p["name"] = new_name

            try:
                new_price = input("New price (blank to keep): ").strip()
                if new_price:
                    p["price"] = float(new_price)

                new_stock = input("New stock (blank to keep): ").strip()
                if new_stock:
                    p["stock"] = int(new_stock)
            except ValueError:
                print("Invalid numeric input.")
                return

            write_products(products)
            print("Product updated.")
            return
    print("Product ID not found.")


def delete_product():
    try:
        pid = int(input("Enter product ID to delete: ").strip())
    except ValueError:
        print("Invalid ID.")
        return

    products = read_products()
    new_products = [p for p in products if p["id"] != pid]
    if len(new_products) == len(products):
        print("Product ID not found.")
        return

    write_products(new_products)
    print("Product deleted.")


def search_products():
    products = read_products()
    q = input("Search by name or ID: ").strip()
    if not q:
        print("Empty search.")
        return

    results = []
    if q.isdigit():
        results = [p for p in products if p["id"] == int(q)]
    else:
        qlow = q.lower()
        results = [p for p in products if qlow in p["name"].lower()]

    if not results:
        print("No products found.")
        return

    print("Found products:")
    for p in results:
        print(f"ID:{p['id']} | {p['name']} | Price:{format_currency(p['price'])} | Stock:{p['stock']}")


def list_all_products():
    products = read_products()
    if not products:
        print("No products available.")
        return
    print("{:<6} {:<30} {:>10} {:>8}".format("ID", "Name", "Price", "Stock"))
    for p in products:
        print("{:<6} {:<30} {:>10} {:>8}".format(p["id"], p["name"], format_currency(p["price"]), p["stock"]))
