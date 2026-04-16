import pandas as pd

# Load original file
df = pd.read_csv("data/cleaned/transformed_data.csv")

# Fix column names
df.columns = [
    "invoice_no","stock_code","description","quantity","invoice_date",
    "unit_price","customer_id","country","is_cancelled","is_return",
    "total_price","year","month","day"
]

# 🔥 FORCE DATE FIX (STRONG METHOD)
df["invoice_date"] = pd.to_datetime(df["invoice_date"], format="%d-%m-%Y %H:%M", errors="coerce")

# Convert to PostgreSQL format
df["invoice_date"] = df["invoice_date"].dt.strftime("%Y-%m-%d %H:%M:%S")

# 🚨 CHECK (VERY IMPORTANT)
print(df["invoice_date"].head())

# Save new file
df.to_csv("data/cleaned/transformed_data_fixed.csv", index=False)

print("✅ CSV FULLY FIXED")