
import os
from datetime import datetime
from collections import defaultdict

from utils.data_processor import (
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    customer_analysis,
    daily_sales_trend,
    find_peak_sales_day,
    low_performing_products
)


def format_currency(value):
    return f"INR {value:,.2f}"


def generate_sales_report(transactions, enriched_transactions,
                          output_file="output/sales_report.txt"):
    """
    Generates a comprehensive formatted text report
    """

    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    total_revenue = calculate_total_revenue(transactions)
    total_transactions = len(transactions)
    avg_order_value = total_revenue / total_transactions if total_transactions else 0

    dates = sorted(t["Date"] for t in transactions)
    date_range = f"{dates[0]} to {dates[-1]}" if dates else "N/A"

    region_data = region_wise_sales(transactions)
    top_products = top_selling_products(transactions, 5)
    customers = customer_analysis(transactions)
    daily_trend = daily_sales_trend(transactions)
    peak_day = find_peak_sales_day(transactions)
    low_products = low_performing_products(transactions)

    # API enrichment summary
    enriched_count = sum(1 for t in enriched_transactions if t.get("API_Match"))
    total_enriched = len(enriched_transactions)
    enrichment_rate = (enriched_count / total_enriched) * 100 if total_enriched else 0

    unenriched_products = sorted({
        t["ProductName"]
        for t in enriched_transactions
        if not t.get("API_Match")
    })

    with open(output_file, "w", encoding="utf-8") as report:
        # =====================================================
        # 1. HEADER
        # =====================================================
        report.write("=" * 60 + "\n")
        report.write("SALES ANALYTICS REPORT\n")
        report.write(f"Generated: {now}\n")
        report.write(f"Records Processed: {total_transactions}\n")
        report.write("=" * 60 + "\n\n")

        # =====================================================
        # 2. OVERALL SUMMARY
        # =====================================================
        report.write("OVERALL SUMMARY\n")
        report.write("-" * 60 + "\n")
        report.write(f"Total Revenue: {format_currency(total_revenue)}\n")
        report.write(f"Total Transactions: {total_transactions}\n")
        report.write(f"Average Order Value: {format_currency(avg_order_value)}\n")
        report.write(f"Date Range: {date_range}\n\n")

        # =====================================================
        # 3. REGION-WISE PERFORMANCE
        # =====================================================
        report.write("REGION-WISE PERFORMANCE\n")
        report.write("-" * 60 + "\n")
        report.write(f"{'Region':<10}{'Sales':<15}{'% of Total':<15}{'Transactions'}\n")

        for region, data in region_data.items():
            report.write(
                f"{region:<10}"
                f"{format_currency(data['total_sales']):<15}"
                f"{data['percentage']:<15}%"
                f"{data['transaction_count']}\n"
            )
        report.write("\n")

        # =====================================================
        # 4. TOP 5 PRODUCTS
        # =====================================================
        report.write("TOP 5 PRODUCTS\n")
        report.write("-" * 60 + "\n")
        report.write(f"{'Rank':<6}{'Product':<25}{'Qty Sold':<12}{'Revenue'}\n")

        for idx, (name, qty, revenue) in enumerate(top_products, start=1):
            report.write(
                f"{idx:<6}{name:<25}{qty:<12}{format_currency(revenue)}\n"
            )
        report.write("\n")

        # =====================================================
        # 5. TOP 5 CUSTOMERS
        # =====================================================
        report.write("TOP 5 CUSTOMERS\n")
        report.write("-" * 60 + "\n")
        report.write(f"{'Rank':<6}{'Customer':<15}{'Total Spent':<18}{'Orders'}\n")

        for idx, (cid, data) in enumerate(list(customers.items())[:5], start=1):
            report.write(
                f"{idx:<6}{cid:<15}"
                f"{format_currency(data['total_spent']):<18}"
                f"{data['purchase_count']}\n"
            )
        report.write("\n")

        # =====================================================
        # 6. DAILY SALES TREND
        # =====================================================
        report.write("DAILY SALES TREND\n")
        report.write("-" * 60 + "\n")
        report.write(f"{'Date':<12}{'Revenue':<15}{'Txns':<10}{'Customers'}\n")

        for date, data in daily_trend.items():
            report.write(
                f"{date:<12}"
                f"{format_currency(data['revenue']):<15}"
                f"{data['transaction_count']:<10}"
                f"{data['unique_customers']}\n"
            )
        report.write("\n")

        # =====================================================
        # 7. PRODUCT PERFORMANCE ANALYSIS
        # =====================================================
        report.write("PRODUCT PERFORMANCE ANALYSIS\n")
        report.write("-" * 60 + "\n")
        report.write(
            f"Best Selling Day: {peak_day[0]} "
            f"({format_currency(peak_day[1])}, {peak_day[2]} transactions)\n"
        )

        if low_products:
            report.write("Low Performing Products:\n")
            for name, qty, revenue in low_products:
                report.write(
                    f"- {name}: {qty} units, {format_currency(revenue)}\n"
                )
        else:
            report.write("No low performing products found.\n")
        report.write("\n")

        # =====================================================
        # 8. API ENRICHMENT SUMMARY
        # =====================================================
        report.write("API ENRICHMENT SUMMARY\n")
        report.write("-" * 60 + "\n")
        report.write(f"Total Records Enriched: {enriched_count}\n")
        report.write(f"Enrichment Success Rate: {enrichment_rate:.2f}%\n")

        if unenriched_products:
            report.write("Products Not Enriched:\n")
            for p in unenriched_products:
                report.write(f"- {p}\n")
        else:
            report.write("All products successfully enriched.\n")

    print(f"Sales report generated at: {output_file}")
