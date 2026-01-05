import requests
import os

BASE_URL = "https://dummyjson.com/products"


def fetch_all_products():
    try:
        response = requests.get(f"{BASE_URL}?limit=100", timeout=10)
        response.raise_for_status()

        data = response.json()
        products = data.get("products", [])

        result = []
        for p in products:
            result.append({
                "id": p.get("id"),
                "title": p.get("title"),
                "category": p.get("category"),
                "brand": p.get("brand"),
                "rating": p.get("rating")
            })

        print(f"Successfully fetched {len(result)} products from API")
        return result

    except requests.exceptions.RequestException as e:
        print(f"API fetch failed: {e}")
        return []


def create_product_mapping(api_products):
    mapping = {}
    for p in api_products:
        mapping[p["id"]] = {
            "category": p["category"],
            "brand": p["brand"],
            "rating": p["rating"]
        }
    return mapping


def extract_numeric_product_id(product_id):
    try:
        return int("".join(filter(str.isdigit, product_id)))
    except ValueError:
        return None


def enrich_sales_data(transactions, product_mapping):
    enriched = []

    for t in transactions:
        tx = t.copy()
        pid = extract_numeric_product_id(t["ProductID"])

        if pid in product_mapping:
            api = product_mapping[pid]
            tx["API_Category"] = api["category"]
            tx["API_Brand"] = api["brand"]
            tx["API_Rating"] = api["rating"]
            tx["API_Match"] = True
        else:
            tx["API_Category"] = None
            tx["API_Brand"] = None
            tx["API_Rating"] = None
            tx["API_Match"] = False

        enriched.append(tx)

    save_enriched_data(enriched)
    return enriched


def save_enriched_data(enriched_transactions,
                       filename="data/enriched_sales_data.txt"):
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    headers = [
        "TransactionID", "Date", "ProductID", "ProductName",
        "Quantity", "UnitPrice", "CustomerID", "Region",
        "API_Category", "API_Brand", "API_Rating", "API_Match"
    ]

    with open(filename, "w", encoding="utf-8") as f:
        f.write("|".join(headers) + "\n")
        for t in enriched_transactions:
            row = ["" if t.get(h) is None else str(t.get(h)) for h in headers]
            f.write("|".join(row) + "\n")

    print(f"Enriched data saved to {filename}")
