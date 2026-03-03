import pandas as pd
import os

DATA_PATH = "data/raw/online_retail.csv"
OUTPUT_PATH = "data/cleaned/validated_data.csv"

def validate_data():
    df = pd.read_csv(DATA_PATH, encoding="ISO-8859-1")

    print("Initial rows:", len(df))

    df["Description"] = df["Description"].fillna("Unknown Product")
    df["CustomerID"] = df["CustomerID"].fillna("Unknown")

    df["IsCancelled"] = df["InvoiceNo"].astype(str).str.startswith("C")
    df["IsReturn"] = df["Quantity"] <= 0

    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")
    df = df[df["UnitPrice"] > 0]

    print("Rows after validation:", len(df))

    # 🔑 ensure output directory exists
    os.makedirs("data/cleaned", exist_ok=True)

    df.to_csv(OUTPUT_PATH, index=False)
    print("Validated data saved to:", OUTPUT_PATH)

if __name__ == "__main__":
    validate_data()