#!/usr/bin/env python3
"""Generate a reproducible 100,000-row synthetic e-commerce transaction CSV."""
import csv
import random
import argparse
from datetime import datetime
from pathlib import Path

def generate(output_path, rows=100_000, seed=42):
    random.seed(seed)
    categories = ["Electronics", "Fashion", "Home & Kitchen", "Beauty",
                  "Books", "Sports", "Grocery", "Toys"]
    payments = ["UPI", "Credit Card", "Debit Card", "Net Banking",
                "Wallet", "Cash on Delivery"]
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Transaction ID", "Customer ID", "Product Category",
                    "Quantity Purchased", "Unit Price", "Transaction Status",
                    "Payment Mode"])
        for i in range(1, rows + 1):
            customer = random.randint(1, 12_000)
            quantity = random.choices([1,2,3,4,5,6,8,10,12],
                                      weights=[30,22,15,10,8,5,4,3,3])[0]
            price = random.choices(
                [random.uniform(100, 4999), random.uniform(5000, 19999),
                 random.uniform(20000, 49999), random.uniform(50000, 120000)],
                weights=[58,25,12,5])[0]
            status = random.choices(["SUCCESS", "FAILED"], weights=[88,12])[0]
            w.writerow([f"TXN{i:07d}", f"CUST{customer:05d}",
                        random.choice(categories), quantity, f"{price:.2f}",
                        status, random.choice(payments)])
    print(f"Created {rows:,} records: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="ecommerce_transactions.csv")
    parser.add_argument("--rows", type=int, default=100_000)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    generate(args.output, args.rows, args.seed)
