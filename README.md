# Sales Analytics System

**Student Name:** Anju P S  
**Student ID:** BITSoM_BA_25071351
**Email:** anjupsmec@gmail.com
**Date:** 06-01-2026


## Project Overview
This project is a Python-based Sales Data Analytics System built to process,
clean, analyze, enrich, and report on e-commerce sales transactions.

The system handles messy real-world data, integrates with an external API,
and generates business-ready reports.

---

## Features
- Handles non-UTF-8 encoded sales files
- Cleans and validates transaction data
- Interactive filtering by region and transaction amount
- Performs detailed sales analytics
- Integrates with DummyJSON Products API
- Enriches sales data with product metadata
- Generates a comprehensive text-based report

---

## Project Structure
sales-analytics-system/
├── main.py
├── README.md
├── requirements.txt
├── data/
│ ├── sales_data.txt
│ └── enriched_sales_data.txt
├── output/
│ └── sales_report.txt
└── utils/
├── file_handler.py
├── data_processor.py
├── api_handler.py
└── report_generator.py

## How to Run

### 1. Create virtual environment (optional)

python -m venv venv
venv\Scripts\activate
### 2. Install dependencies

pip install requests
### 3. Run the application

python main.py

## Output Files
data/enriched_sales_data.txt → API-enriched transactions
output/sales_report.txt → Final analytics report

## Technologies Used
Python 3
Requests library
DummyJSON API