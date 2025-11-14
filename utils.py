import csv
import os
from datetime import datetime

DATA_DIR = "data"
BILLS_DIR = "bills"
PRODUCTS_FILE = os.path.join(DATA_DIR, "products.csv")
SALES_FILE = os.path.join(DATA_DIR, "sales.csv")


def ensure_directories():
    """Ensure required directories and files exist."""
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(BILLS_DIR, exist_ok=True)

    if not os.path.exists(PRODUCTS_FILE):
        with open(PRODUCTS_FILE, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(["id", "name", "price", "stock"])

    if not os.path.exists(SALES_FILE):
        with open(SALES_FILE, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(["bill_id", "datetime", "subtotal", "discount_percent", "total_amount"])


def read_csv_dicts(filepath):
    """Read CSV into list of dicts."""
    with open(filepath, newline="", encoding="utf-8") as f:
        return [row for row in csv.DictReader(f)]


def write_csv(filepath, rows, headers):
    """Write list of dicts or tuples to CSV file."""
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)


def format_currency(value):
    """Format as Indian Rupee currency."""
    return f"₹{float(value):,.2f}"


def timestamp_id(prefix="bill"):
    """Generate unique timestamp-based ID."""
    return f"{prefix}_{datetime.now().strftime('%Y%m%d%H%M%S')}"


def current_datetime():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
