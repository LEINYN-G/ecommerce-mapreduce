#!/usr/bin/env python3

import sys
import csv
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

# Convert rupees into integer paise
def to_paise(value):
    amount = Decimal(value)
    return int(
        (amount * 100).quantize(
            Decimal("1"),
            rounding=ROUND_HALF_UP
        )
    )

for line in sys.stdin:
    try:
        row = next(csv.reader([line]))

        # Skip CSV header
        if row and row[0].strip() == "Transaction ID":
            continue

        # Expected seven columns
        if len(row) != 7:
            print("reporter:counter:DataQuality,MalformedRows,1",
                  file=sys.stderr)
            continue

        transaction_id, customer_id, category, quantity, unit_price, status, payment_mode = [
            field.strip() for field in row
        ]

        # Validate required fields
        if not transaction_id or not customer_id:
            print("reporter:counter:DataQuality,MissingRequiredFields,1",
                  file=sys.stderr)
            continue

        quantity = int(quantity)
        unit_price = to_paise(unit_price)

        if quantity <= 0 or unit_price < 0:
            print("reporter:counter:DataQuality,InvalidNumericRows,1",
                  file=sys.stderr)
            continue

        amount = quantity * unit_price

        # Assignment metrics
        total_transactions = 1
        total_amount = amount
        success_count = 0
        failed_count = 0
        high_value_count = 0
        successful_amount = 0

        if status == "SUCCESS":
            success_count = 1
            successful_amount = amount

        elif status == "FAILED":
            failed_count = 1

        else:
            print("reporter:counter:DataQuality,UnknownStatusRows,1",
                  file=sys.stderr)
            continue

        if amount >= 5000000:
            high_value_count = 1

        # Emit customer ID and six additive metrics
        metrics = [
            total_transactions,
            total_amount,
            success_count,
            failed_count,
            high_value_count,
            successful_amount
        ]

        print(f"{customer_id}\t{','.join(map(str, metrics))}")

    except (ValueError, InvalidOperation, StopIteration):
        print("reporter:counter:DataQuality,InvalidRows,1",
              file=sys.stderr)
