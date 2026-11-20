#!/usr/bin/env python3

import sys

current_customer = None
totals = [0, 0, 0, 0, 0, 0]

def emit(customer, metrics):
    print(f"{customer}\t{','.join(map(str, metrics))}")

for line in sys.stdin:
    try:
        customer, values = line.strip().split("\t", 1)
        metrics = [int(x) for x in values.split(",")]

        if len(metrics) != 6:
            print(
                "reporter:counter:DataQuality,InvalidCombinerRows,1",
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
            "reporter:counter:DataQuality,InvalidCombinerRows,1",
            file=sys.stderr
        )

if current_customer is not None:
    emit(current_customer, totals)

