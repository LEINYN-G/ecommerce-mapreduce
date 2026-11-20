import csv
from collections import Counter

file_path = "data/raw/ecommerce_transactions_100k_synthetic.csv"

total = 0
statuses = Counter()
customers = set()
transaction_ids = set()
duplicate_ids = 0
missing_values = 0
invalid_numeric = 0
malformed_rows = 0
high_value = 0

with open(file_path, "r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    print("COLUMNS:", reader.fieldnames)

    for row in reader:
        total += 1

        if None in row:
            malformed_rows += 1
            continue

        if any(not str(v).strip() for v in row.values()):
            missing_values += 1

        txn_id = row["Transaction ID"]
        customer_id = row["Customer ID"]

        if txn_id in transaction_ids:
            duplicate_ids += 1
        transaction_ids.add(txn_id)

        customers.add(customer_id)
        statuses[row["Transaction Status"]] += 1

        try:
            quantity = int(row["Quantity Purchased"])
            price = float(row["Unit Price"])

            if quantity <= 0 or price < 0:
                invalid_numeric += 1
                continue

            if quantity * price >= 50000:
                high_value += 1

        except (ValueError, TypeError):
            invalid_numeric += 1

print("\n--- DATASET AUDIT ---")
print("Total records:", total)
print("Unique customers:", len(customers))
print("Transaction statuses:", dict(statuses))
print("Duplicate transaction IDs:", duplicate_ids)
print("Missing-value rows:", missing_values)
print("Invalid numeric rows:", invalid_numeric)
print("Malformed rows:", malformed_rows)
print("High-value transactions:", high_value)
