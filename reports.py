from utils import SALES_FILE, read_csv_dicts, format_currency
from products import read_products
from datetime import datetime


def report_total_sales_by_date():
    date_str = input("Enter date (YYYY-MM-DD) or leave blank for today: ").strip() or datetime.now().strftime("%Y-%m-%d")
    total, count = 0.0, 0

    for row in read_csv_dicts(SALES_FILE):
        if not row.get("datetime"):
            continue
        row_date = row["datetime"].split()[0]
        if row_date == date_str:
            total += float(row["total_amount"])
            count += 1

    print(f"Date: {date_str} | Bills: {count} | Total Sales: {format_currency(total)}")


def report_low_stock():
    try:
        threshold = int(input("Enter low-stock threshold (e.g., 5): ").strip())
    except ValueError:
        print("Invalid threshold.")
        return

    low = [p for p in read_products() if p["stock"] <= threshold]
    if not low:
        print("No low-stock products.")
        return

    print("Low-stock products:")
    for p in low:
        print(f"ID:{p['id']} | {p['name']} | Stock:{p['stock']}")
