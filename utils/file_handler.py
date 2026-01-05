
def read_sales_data(filename):
    """
    Reads sales data from file handling encoding issues
    Returns list of raw transaction lines (without header)
    """

    encodings = ["utf-8", "latin-1", "cp1252"]

    for enc in encodings:
        try:
            with open(filename, "r", encoding=enc) as file:
                lines = file.readlines()
                break
        except UnicodeDecodeError:
            continue
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
            return []
    else:
        print("Error: Unable to read file with supported encodings.")
        return []

    return [line.strip() for line in lines[1:] if line.strip()]


def parse_transactions(raw_lines):
    transactions = []

    fields = [
        "TransactionID", "Date", "ProductID", "ProductName",
        "Quantity", "UnitPrice", "CustomerID", "Region"
    ]

    for line in raw_lines:
        parts = line.split("|")
        if len(parts) != 8:
            continue

        record = dict(zip(fields, parts))

        record["ProductName"] = record["ProductName"].replace(",", "").strip()

        try:
            record["Quantity"] = int(record["Quantity"].replace(",", ""))
            record["UnitPrice"] = float(record["UnitPrice"].replace(",", ""))
        except ValueError:
            continue

        transactions.append(record)

    return transactions


def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    valid = []
    invalid_count = 0

    regions = set()
    amounts = []

    for t in transactions:
        regions.add(t["Region"])
        amounts.append(t["Quantity"] * t["UnitPrice"])

        if (
            t["Quantity"] <= 0
            or t["UnitPrice"] <= 0
            or not t["TransactionID"].startswith("T")
            or not t["ProductID"].startswith("P")
            or not t["CustomerID"].startswith("C")
            or not t["Region"]
        ):
            invalid_count += 1
            continue

        valid.append(t)

    print(f"Available regions: {sorted(regions)}")
    print(f"Transaction amount range: {min(amounts)} - {max(amounts)}")

    filtered = valid[:]

    if region:
        filtered = [t for t in filtered if t["Region"] == region]

    if min_amount is not None:
        filtered = [
            t for t in filtered
            if (t["Quantity"] * t["UnitPrice"]) >= min_amount
        ]

    if max_amount is not None:
        filtered = [
            t for t in filtered
            if (t["Quantity"] * t["UnitPrice"]) <= max_amount
        ]

    summary = {
        "total_input": len(transactions),
        "invalid": invalid_count,
        "final_count": len(filtered)
    }

    return filtered, invalid_count, summary
