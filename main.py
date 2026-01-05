# main.py

from utils.file_handler import (
    read_sales_data,
    parse_transactions,
    validate_and_filter
)

from utils.data_processor import (
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    customer_analysis,
    daily_sales_trend,
    find_peak_sales_day,
    low_performing_products
)

from utils.api_handler import (
    fetch_all_products,
    create_product_mapping,
    enrich_sales_data
)

from utils.report_generator import generate_sales_report


DATA_FILE = "data/sales_data.txt"


def main():
    print("=" * 40)
    print("SALES ANALYTICS SYSTEM")
    print("=" * 40)

    try:
        # [1/10] Read sales data
        print("[1/10] Reading sales data...")
        raw_lines = read_sales_data(DATA_FILE)
        print(f"✓ Successfully read {len(raw_lines)} transactions")

        # [2/10] Parse and clean
        print("[2/10] Parsing and cleaning data...")
        transactions = parse_transactions(raw_lines)
        print(f"✓ Parsed {len(transactions)} records")

        # [3/10] Display filter options
        regions = sorted({t["Region"] for t in transactions})
        amounts = [t["Quantity"] * t["UnitPrice"] for t in transactions]

        print("[3/10] Filter Options Available:")
        print(f"Regions: {', '.join(regions)}")
        print(f"Amount Range: INR {min(amounts)} - INR {max(amounts)}")

        apply_filter = input("Do you want to filter data? (y/n): ").strip().lower()

        region = None
        min_amount = None
        max_amount = None

        if apply_filter == "y":
            region = input("Enter region (or press Enter to skip): ").strip() or None

            min_amt = input("Enter minimum amount (or press Enter to skip): ").strip()
            max_amt = input("Enter maximum amount (or press Enter to skip): ").strip()

            min_amount = float(min_amt) if min_amt else None
            max_amount = float(max_amt) if max_amt else None

        # [4/10] Validate and filter
        print("[4/10] Validating transactions...")
        valid_tx, invalid_count, summary = validate_and_filter(
            transactions,
            region=region,
            min_amount=min_amount,
            max_amount=max_amount
        )
        print(f"✓ Valid: {len(valid_tx)} | Invalid: {invalid_count}")

        # [5/10] Analysis
        print("[5/10] Analyzing sales data...")
        calculate_total_revenue(valid_tx)
        region_wise_sales(valid_tx)
        top_selling_products(valid_tx)
        customer_analysis(valid_tx)
        daily_sales_trend(valid_tx)
        find_peak_sales_day(valid_tx)
        low_performing_products(valid_tx)
        print("✓ Analysis complete")

        # [6/10] Fetch API data
        print("[6/10] Fetching product data from API...")
        api_products = fetch_all_products()
        print(f"✓ Fetched {len(api_products)} products")

        # [7/10] Enrich data
        print("[7/10] Enriching sales data...")
        product_mapping = create_product_mapping(api_products)
        enriched_tx = enrich_sales_data(valid_tx, product_mapping)

        enriched_count = sum(1 for t in enriched_tx if t.get("API_Match"))
        success_rate = (enriched_count / len(enriched_tx)) * 100 if enriched_tx else 0
        print(
            f"✓ Enriched {enriched_count}/{len(enriched_tx)} "
            f"transactions ({success_rate:.1f}%)"
        )

        # [8/10] Save enriched data
        print("[8/10] Saving enriched data...")
        print("✓ Saved to: data/enriched_sales_data.txt")

        # [9/10] Generate report
        print("[9/10] Generating report...")
        generate_sales_report(valid_tx, enriched_tx)
        print("✓ Report saved to: output/sales_report.txt")

        # [10/10] Complete
        print("[10/10] Process Complete!")
        print("=" * 40)

    except Exception as e:
        print("❌ An error occurred during execution.")
        print(f"Details: {e}")


if __name__ == "__main__":
    main()
