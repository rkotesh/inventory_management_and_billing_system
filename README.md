# Inventory Management & Billing System (Console)

Console-based Python app to manage products, process orders, generate bills, and view sales reports. Data is stored in CSV files using only the Python standard library. This README reflects how the current codebase works.

## Features

- Product management: add, update, delete, search, list
- Order processing with a cart (add/remove/view)
- Stock validation and auto-update after checkout
- Optional discount at checkout
- Bills generated as `.txt` and `.csv`
- Sales and low-stock reports

## Project Structure

- `main.py` – app entry point and menus
- `products.py` – product CRUD and search
- `cart.py` – cart and checkout (billing)
- `reports.py` – sales and low-stock reports
- `utils.py` – CSV helpers and paths
- `data/` – CSV storage (`products.csv`, `sales.csv`)
- `bills/` – generated bills (`.txt`, `.csv`)

## Requirements

- Python 3.7+ recommended
- No third-party packages

## Setup

1. Open a terminal in the project directory.
2. Run:

   ```bash

   python main.py
   ```

The first run creates required folders and CSV files automatically.

## Usage

Main menu:

- `1` Product Management
- `2` Order Processing
- `3` Reports
- `0` Exit

Product Management:

- Add product (auto-generates Product ID)
- Update product (change name, price, stock)
- Delete product
- Search by ID or name
- List all products

Order Processing:

- Add item to cart
- Remove item from cart
- View cart
- Checkout (optional discount %, confirms before purchase)

Reports:

- Total sales for a specific day (YYYY-MM-DD)
- Low-stock products (<= threshold)

Bills are saved to `bills/` as both `.txt` and `.csv`.

## Data Files

- `data/products.csv` – product catalog
  - Columns: `id`, `name`, `price`, `stock`
- `data/sales.csv` – sales log (one row per checkout)
  - Columns: `bill_id`, `datetime`, `subtotal`, `discount_percent`, `total_amount`

## Example Bill Output

`bills/bill_YYYYMMDDHHMMSS.txt`:

=== BILL ===
Bill ID: bill_20260328174510
DateTime: 2026-03-28 17:45:10

PID    Name                          UnitPrice    Qty    LineTotal
1      Tea Powder                    ₹250.00      2      ₹500.00

Subtotal: ₹500.00
Discount(10.0%): ₹50.00
Total: ₹450.00
Thank you!
```

## Notes

- Currency is formatted in INR (₹).
- Data persists in CSV files between runs.
