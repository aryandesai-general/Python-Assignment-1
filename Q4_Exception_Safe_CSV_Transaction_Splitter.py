"""Q4: Validate a transaction CSV and split valid/invalid rows.

Usage: python Q4_Exception_Safe_CSV_Transaction_Splitter.py
Then enter the input CSV path when prompted.
"""
import csv
from collections import defaultdict
from datetime import datetime
from pathlib import Path


def normalize_row(row):
    # Supports both the descriptive names and the short names in the assignment sample.
    aliases = {
        "transaction_id": ("transaction_id", "tid"),
        "account_id": ("account_id", "acc"),
        "type": ("type",),
        "amount": ("amount",),
        "timestamp": ("timestamp", "time"),
    }
    normalized = {}
    lowered = {str(k).strip().casefold(): (v or "").strip() for k, v in row.items()}
    for target, names in aliases.items():
        for name in names:
            if name in lowered:
                normalized[target] = lowered[name]
                break
        else:
            raise ValueError(f"Missing column: {target}")
    return normalized


def validate_transaction(row):
    data = normalize_row(row)
    if not data["transaction_id"] or not data["account_id"]:
        raise ValueError("transaction_id and account_id are required")
    kind = data["type"].upper()
    if kind not in {"CREDIT", "DEBIT"}:
        raise ValueError("type must be CREDIT or DEBIT")
    try:
        amount = float(data["amount"])
    except ValueError:
        raise ValueError("amount is not numeric")
    if amount <= 0:
        raise ValueError("amount must be greater than zero")
    try:
        datetime.fromisoformat(data["timestamp"])
    except ValueError:
        raise ValueError("timestamp must be ISO-like yyyy-mm-ddThh:mm:ss")
    data["type"] = kind
    data["amount"] = amount
    return data


def main():
    source = Path(input("Input CSV path: ").strip())
    if not source.is_file():
        print("File not found.")
        return

    balances = defaultdict(float)
    output_fields = ["transaction_id", "account_id", "type", "amount", "timestamp"]
    error_fields = list(csv.DictReader(source.open(newline="", encoding="utf-8-sig")).fieldnames or []) + ["reason"]

    with source.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        with open("credit.csv", "w", newline="", encoding="utf-8") as credit_file, \
             open("debit.csv", "w", newline="", encoding="utf-8") as debit_file, \
             open("error.csv", "w", newline="", encoding="utf-8") as error_file:
            credit_writer = csv.DictWriter(credit_file, fieldnames=output_fields)
            debit_writer = csv.DictWriter(debit_file, fieldnames=output_fields)
            error_writer = csv.DictWriter(error_file, fieldnames=error_fields)
            credit_writer.writeheader()
            debit_writer.writeheader()
            error_writer.writeheader()

            for row in reader:
                try:
                    data = validate_transaction(row)
                    clean = {
                        "transaction_id": data["transaction_id"],
                        "account_id": data["account_id"],
                        "type": data["type"],
                        "amount": data["amount"],
                        "timestamp": data["timestamp"],
                    }
                    if data["type"] == "CREDIT":
                        credit_writer.writerow(clean)
                        balances[data["account_id"]] += data["amount"]
                    else:
                        debit_writer.writerow(clean)
                        balances[data["account_id"]] -= data["amount"]
                except (ValueError, TypeError) as exc:
                    rejected = dict(row)
                    rejected["reason"] = str(exc)
                    error_writer.writerow(rejected)

    for account, balance in sorted(balances.items(), key=lambda item: (-abs(item[1]), item[0])):
        print(account, f"{balance:g}")
    print("Files created: credit.csv, debit.csv, error.csv")


if __name__ == "__main__":
    main()
