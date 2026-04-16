import streamlit as st
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv

# ----------------------------
# LOAD ENV VARIABLES
# ----------------------------
load_dotenv()

# ----------------------------
# DATABASE CONNECTION
# ----------------------------
def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        sslmode="require"  # Required for Supabase
    )

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(page_title="Retail BI Platform", layout="wide")
st.title("📊 Retail Business Intelligence Platform")

# ----------------------------
# CONNECT TO DATABASE
# ----------------------------
try:
    conn = get_connection()
except Exception as e:
    st.error(f"❌ Database Connection Failed: {e}")
    st.stop()

# ----------------------------
# YEAR FILTER
# ----------------------------
year_query = "SELECT DISTINCT year FROM retail_transactions ORDER BY year;"

try:
    years_df = pd.read_sql(year_query, conn)
except Exception as e:
    st.error(f"❌ Error fetching years: {e}")
    st.stop()

if years_df.empty:
    st.warning("⚠️ No data found in database.")
    st.stop()

years = years_df["year"].tolist()
selected_year = st.sidebar.selectbox("Select Year", years)

# ----------------------------
# KPI SECTION
# ----------------------------
kpi_query = f"""
SELECT 
    SUM(total_price) AS total_revenue,
    COUNT(DISTINCT customer_id) AS total_customers,
    COUNT(*) AS total_transactions
FROM retail_transactions
WHERE year = {selected_year};
"""

kpi_df = pd.read_sql(kpi_query, conn)

col1, col2, col3 = st.columns(3)

col1.metric("💰 Total Revenue", f"£{kpi_df['total_revenue'][0]:,.2f}")
col2.metric("👥 Total Customers", f"{kpi_df['total_customers'][0]:,}")
col3.metric("🧾 Total Transactions", f"{kpi_df['total_transactions'][0]:,}")

st.divider()

# ----------------------------
# MONTHLY REVENUE TREND
# ----------------------------
st.subheader("📈 Monthly Revenue Trend")

monthly_query = f"""
SELECT year, month, SUM(total_price) AS monthly_revenue
FROM retail_transactions
WHERE year = {selected_year}
GROUP BY year, month
ORDER BY year, month;
"""

monthly_df = pd.read_sql(monthly_query, conn)

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

# ----------------------------
# TOP CUSTOMERS
# ----------------------------
st.subheader("🏆 Top 10 Customers")

top_query = f"""
SELECT customer_id, SUM(total_price) AS total_spent
FROM retail_transactions
WHERE year = {selected_year}
GROUP BY customer_id
ORDER BY total_spent DESC
LIMIT 10;
"""

top_df = pd.read_sql(top_query, conn)

st.bar_chart(top_df.set_index("customer_id"))

st.divider()

# ----------------------------
# COUNTRY REVENUE
# ----------------------------
st.subheader("🌍 Top Countries by Revenue")

country_query = f"""
SELECT country, SUM(total_price) AS total_revenue
FROM retail_transactions
WHERE year = {selected_year}
GROUP BY country
ORDER BY total_revenue DESC
LIMIT 10;
"""

country_df = pd.read_sql(country_query, conn)

st.bar_chart(country_df.set_index("country"))

# ----------------------------
# CLOSE CONNECTION
# ----------------------------
conn.close()