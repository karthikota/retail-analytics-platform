# Retail Business Intelligence Platform

## Live Application

https://retail-analytics-platform-2fbkqttsqobitirwqzhxoi.streamlit.app/

---

## Overview

This project implements an end-to-end data analytics pipeline for retail transaction data. It covers data preprocessing, storage in a cloud-based PostgreSQL database, and visualization through an interactive dashboard.

The goal is to simulate a real-world analytics workflow where raw data is transformed into actionable business insights.

---

## Architecture

The system follows a simple data pipeline architecture:

1. **Data Ingestion**
   Raw transactional data is sourced from a CSV dataset.

2. **Data Transformation**
   Data is cleaned and processed using Python (Pandas), including:

   * Handling missing values
   * Feature engineering (total price, date breakdown)
   * Data type corrections

3. **Data Storage**
   Processed data is stored in a PostgreSQL database hosted on Supabase.

4. **Visualization Layer**
   A Streamlit dashboard connects to the cloud database and presents insights interactively.

---

## Features

* Year-based filtering for analysis
* Key performance indicators:

  * Total revenue
  * Total customers
  * Total transactions
* Monthly revenue trend analysis
* Top customers based on spending
* Country-wise revenue distribution

---

## Tech Stack

* **Python** (Pandas, Matplotlib)
* **PostgreSQL** (Supabase)
* **Streamlit**
* **psycopg2**
* **Git & GitHub**

---

## Database Design

The primary table used:

`retail_transactions`

Key columns include:

* invoice_no
* stock_code
* description
* quantity
* invoice_date
* unit_price
* customer_id
* country
* total_price
* year, month, day

A surrogate primary key (`id`) is used to ensure row-level uniqueness due to the absence of a natural primary key in the dataset.

---

## Key Challenges and Solutions

**1. Data Format Issues**

* Problem: Inconsistent date formats
* Solution: Standardized to PostgreSQL-compatible timestamp format

**2. Schema Mismatch**

* Problem: CSV headers did not match database schema
* Solution: Normalized column names and aligned structure

**3. Primary Key Design**

* Problem: No unique identifier in source data
* Solution: Introduced auto-increment surrogate key

**4. Cloud Connectivity**

* Problem: Authentication and connection inconsistencies
* Solution: Configured environment-based credentials and secure connection handling

---

## Running the Project Locally

1. Clone the repository
2. Create a `.env` file with database credentials:

   ```
   DB_HOST=...
   DB_PORT=...
   DB_NAME=...
   DB_USER=...
   DB_PASSWORD=...
   ```
3. Install dependencies:

   ```
   pip install -r requirements.txt
   ```
4. Run the dashboard:

   ```
   streamlit run dashboard/app.py
   ```

---

## Future Improvements

* Customer segmentation (RFM analysis)
* Predictive analytics for sales forecasting
* Advanced filtering and drill-down capabilities
* Role-based access control

---

## Author

K. Sriramkarthikeya
