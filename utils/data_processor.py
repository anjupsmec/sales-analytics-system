from collections import defaultdict


def calculate_total_revenue(transactions):
    return sum(t["Quantity"] * t["UnitPrice"] for t in transactions)


def region_wise_sales(transactions):
    region_data = defaultdict(lambda: {"total_sales": 0, "transaction_count": 0})
    total_revenue = calculate_total_revenue(transactions)

    for t in transactions:
        revenue = t["Quantity"] * t["UnitPrice"]
        region = t["Region"]

        region_data[region]["total_sales"] += revenue
        region_data[region]["transaction_count"] += 1

    for region in region_data:
        region_data[region]["percentage"] = round(
            (region_data[region]["total_sales"] / total_revenue) * 100, 2
        )

    return dict(
        sorted(region_data.items(), key=lambda x: x[1]["total_sales"], reverse=True)
    )


def top_selling_products(transactions, n=5):
    products = defaultdict(lambda: {"qty": 0, "revenue": 0})

    for t in transactions:
        name = t["ProductName"]
        products[name]["qty"] += t["Quantity"]
        products[name]["revenue"] += t["Quantity"] * t["UnitPrice"]

    result = [(k, v["qty"], v["revenue"]) for k, v in products.items()]
    return sorted(result, key=lambda x: x[1], reverse=True)[:n]


def customer_analysis(transactions):
    customers = defaultdict(lambda: {
        "total_spent": 0,
        "purchase_count": 0,
        "products_bought": set()
    })

    for t in transactions:
        amount = t["Quantity"] * t["UnitPrice"]
        cid = t["CustomerID"]

        customers[cid]["total_spent"] += amount
        customers[cid]["purchase_count"] += 1
        customers[cid]["products_bought"].add(t["ProductName"])

    result = {}
    for cid, data in customers.items():
        result[cid] = {
            "total_spent": data["total_spent"],
            "purchase_count": data["purchase_count"],
            "avg_order_value": round(
                data["total_spent"] / data["purchase_count"], 2
            ),
            "products_bought": sorted(data["products_bought"])
        }

    return dict(
        sorted(result.items(), key=lambda x: x[1]["total_spent"], reverse=True)
    )


def daily_sales_trend(transactions):
    daily = defaultdict(lambda: {
        "revenue": 0,
        "transaction_count": 0,
        "customers": set()
    })

    for t in transactions:
        date = t["Date"]
        amount = t["Quantity"] * t["UnitPrice"]

        daily[date]["revenue"] += amount
        daily[date]["transaction_count"] += 1
        daily[date]["customers"].add(t["CustomerID"])

    result = {}
    for date in sorted(daily):
        result[date] = {
            "revenue": daily[date]["revenue"],
            "transaction_count": daily[date]["transaction_count"],
            "unique_customers": len(daily[date]["customers"])
        }

    return result


def find_peak_sales_day(transactions):
    daily = daily_sales_trend(transactions)
    peak = max(daily.items(), key=lambda x: x[1]["revenue"])
    return peak[0], peak[1]["revenue"], peak[1]["transaction_count"]


def low_performing_products(transactions, threshold=10):
    products = defaultdict(lambda: {"qty": 0, "revenue": 0})

    for t in transactions:
        name = t["ProductName"]
        products[name]["qty"] += t["Quantity"]
        products[name]["revenue"] += t["Quantity"] * t["UnitPrice"]

    low = [
        (k, v["qty"], v["revenue"])
        for k, v in products.items()
        if v["qty"] < threshold
    ]

    return sorted(low, key=lambda x: x[1])
