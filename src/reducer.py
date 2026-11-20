#!/usr/bin/env python3

import sys

current_customer = None
totals = [0, 0, 0, 0, 0, 0]

def emit(customer, metrics):
    total_transactions, total_amount, success_count, failed_count, high_value_count, successful_amount = metrics

    # Customer classification
    premium = successful_amount >= 10000000
    frequent = success_count >= 4

    if premium and frequent:
        category = "PREMIUM_FREQUENT"
    elif premium:
        category = "PREMIUM"
    elif frequent:
        category = "FREQUENT"
    else:
        category = "NORMAL"

    # Convert paise into rupees for final output
    total_amount_rupees = total_amount / 100
    successful_amount_rupees = successful_amount / 100

    print(
        f"{customer}\t"
        f"{total_transactions},"
        f"{total_amount_rupees:.2f},"
        f"{success_count},"
        f"{failed_count},"
        f"{high_value_count},"
        f"{successful_amount_rupees:.2f},"
        f"{category}"
    )

for line in sys.stdin:
    try:
        customer, values = line.strip().split("\t", 1)
        metrics = [int(x) for x in values.split(",")]

        if len(metrics) != 6:
            print(
                "reporter:counter:DataQuality,InvalidReducerRows,1",
                file=sys.stderr
            )
            continue

        if current_customer is None:
            current_customer = customer

        if customer != current_customer:
            emit(current_customer, totals)
            current_customer = customer
            totals = [0, 0, 0, 0, 0, 0]

        totals = [
            old + new
            for old, new in zip(totals, metrics)
        ]

    except (ValueError, IndexError):
        print(
            "reporter:counter:DataQuality,InvalidReducerRows,1",
            file=sys.stderr
        )

if current_customer is not None:
    emit(current_customer, totals)
