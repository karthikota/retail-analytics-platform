import os
from dotenv import load_dotenv
import streamlit as st
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt

# ------------------------------
# Load Environment Variables
# ------------------------------
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))
print("DB_PASSWORD:", os.getenv("DB_PASSWORD"))

def get_connection():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )

# ------------------------------
# Streamlit Config
# ------------------------------
st.set_page_config(page_title="Retail Business Intelligence Platform", layout="wide")
st.title("📊 Retail Business Intelligence Platform")

conn = get_connection()

# ------------------------------
# SIDEBAR FILTER
# ------------------------------
year_query = """
SELECT DISTINCT year 
FROM dim_date 
ORDER BY year;
"""
years_df = pd.read_sql(year_query, conn)
years = years_df["year"].tolist()

selected_year = st.sidebar.selectbox("Select Year", years)

# ------------------------------
# KPI SECTION WITH SMART YoY
# ------------------------------
previous_year = selected_year - 1

# Get overlapping months
months_query = """
SELECT DISTINCT d.month
FROM fact_sales f
JOIN dim_date d ON f.date_id = d.date_id
WHERE d.year = %s;
"""
months_df = pd.read_sql(months_query, conn, params=(previous_year,))

if months_df.empty:
    yoy_growth = None
else:
    months_list = months_df["month"].tolist()

    prev_query = """
    SELECT SUM(f.total_price) AS revenue
    FROM fact_sales f
    JOIN dim_date d ON f.date_id = d.date_id
    WHERE d.year = %s
    AND d.month = ANY(%s);
    """
    prev_df = pd.read_sql(prev_query, conn, params=(previous_year, months_list))
    previous_revenue = prev_df["revenue"][0] or 0

    curr_query = """
    SELECT SUM(f.total_price) AS revenue
    FROM fact_sales f
    JOIN dim_date d ON f.date_id = d.date_id
    WHERE d.year = %s
    AND d.month = ANY(%s);
    """
    curr_df = pd.read_sql(curr_query, conn, params=(selected_year, months_list))
    current_revenue_overlap = curr_df["revenue"][0] or 0

    if previous_revenue == 0:
        yoy_growth = None
    else:
        yoy_growth = ((current_revenue_overlap - previous_revenue) / previous_revenue) * 100

# Full Year KPIs
kpi_query = """
SELECT 
    SUM(f.total_price) AS total_revenue,
    COUNT(DISTINCT f.customer_id) AS total_customers,
    COUNT(*) AS total_transactions
FROM fact_sales f
JOIN dim_date d ON f.date_id = d.date_id
WHERE d.year = %s;
"""
kpi_df = pd.read_sql(kpi_query, conn, params=(selected_year,))

total_revenue_full = kpi_df["total_revenue"][0] or 0
total_customers = kpi_df["total_customers"][0]
total_transactions = kpi_df["total_transactions"][0]

# Display KPIs
col1, col2, col3 = st.columns(3)

if yoy_growth is not None:
    col1.metric(
        "Total Revenue",
        f"£{total_revenue_full:,.2f}",
        f"{yoy_growth:.2f}% vs {previous_year}"
    )
else:
    col1.metric("Total Revenue", f"£{total_revenue_full:,.2f}")

col2.metric("Total Customers", f"{total_customers:,}")
col3.metric("Total Transactions", f"{total_transactions:,}")

st.divider()

# ------------------------------
# MONTHLY REVENUE TREND
# ------------------------------
st.subheader("📈 Monthly Revenue Trend")

monthly_query = """
SELECT 
    d.year, 
    d.month, 
    SUM(f.total_price) AS monthly_revenue
FROM fact_sales f
JOIN dim_date d ON f.date_id = d.date_id
WHERE d.year = %s
GROUP BY d.year, d.month
ORDER BY d.year, d.month;
"""
monthly_df = pd.read_sql(monthly_query, conn, params=(selected_year,))

monthly_df["year_month"] = pd.to_datetime(
    monthly_df["year"].astype(str) + "-" + monthly_df["month"].astype(str)
)

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(monthly_df["year_month"], monthly_df["monthly_revenue"], marker="o")
ax.set_title(f"Monthly Revenue - {selected_year}")
ax.set_xlabel("Month")
ax.set_ylabel("Revenue (£)")
plt.xticks(rotation=45)
plt.tight_layout()

st.pyplot(fig)

st.divider()

# ------------------------------
# TOP CUSTOMERS
# ------------------------------
st.subheader("🏆 Top 10 Customers")

top_customer_query = """
SELECT 
    c.customer_id, 
    SUM(f.total_price) AS total_spent
FROM fact_sales f
JOIN dim_customer c ON f.customer_id = c.customer_id
JOIN dim_date d ON f.date_id = d.date_id
WHERE d.year = %s
GROUP BY c.customer_id
ORDER BY total_spent DESC
LIMIT 10;
"""
top_customers = pd.read_sql(top_customer_query, conn, params=(selected_year,))
st.bar_chart(top_customers.set_index("customer_id"))

st.divider()

# ------------------------------
# COUNTRY REVENUE
# ------------------------------
st.subheader("🌍 Top 10 Countries by Revenue")

country_query = """
SELECT 
    c.country, 
    SUM(f.total_price) AS total_revenue
FROM fact_sales f
JOIN dim_customer c ON f.customer_id = c.customer_id
JOIN dim_date d ON f.date_id = d.date_id
WHERE d.year = %s
GROUP BY c.country
ORDER BY total_revenue DESC
LIMIT 10;
"""
country_df = pd.read_sql(country_query, conn, params=(selected_year,))
st.bar_chart(country_df.set_index("country"))

st.divider()

# ------------------------------
# RFM CUSTOMER SEGMENTATION
# ------------------------------
st.subheader("🧠 Customer Segmentation (RFM Analysis)")

segment_query = """
SELECT segment, COUNT(*) AS customer_count
FROM rfm_segments
GROUP BY segment
ORDER BY customer_count DESC;
"""
segment_df = pd.read_sql(segment_query, conn)
st.markdown("### Segment Distribution")
st.bar_chart(segment_df.set_index("segment"))

revenue_segment_query = """
SELECT 
    s.segment,
    SUM(f.total_price) AS total_revenue
FROM fact_sales f
JOIN rfm_segments s ON f.customer_id = s.customer_id
GROUP BY s.segment
ORDER BY total_revenue DESC;
"""
revenue_segment_df = pd.read_sql(revenue_segment_query, conn)
st.markdown("### Revenue by Segment")
st.bar_chart(revenue_segment_df.set_index("segment"))

champions_query = """
SELECT 
    customer_id,
    monetary
FROM rfm_segments
WHERE segment = 'Champions'
ORDER BY monetary DESC
LIMIT 10;
"""
champions_df = pd.read_sql(champions_query, conn)
st.markdown("### 🏆 Top 10 Champion Customers")
st.dataframe(champions_df)

conn.close()