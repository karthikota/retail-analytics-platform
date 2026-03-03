import pandas as pd
import os
INPUT_PATH = "data/cleaned/validated_data.csv"
OUTPUT_PATH = "data/cleaned/transformed_data.csv"

def transform_data():
    df = pd.read_csv(INPUT_PATH)

    # Create total price column
    df["TotalPrice"] = df["Quantity"] * df["UnitPrice"]

    # Convert InvoiceDate again to ensure datetime
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")

    # Extract date parts
    df["Year"] = df["InvoiceDate"].dt.year
    df["Month"] = df["InvoiceDate"].dt.month
    df["Day"] = df["InvoiceDate"].dt.day

    # Normalize Country names
    df["Country"] = df["Country"].str.strip()

    print("Transformation complete")
    print("Rows:", len(df))
    print("Columns:", df.columns.tolist())


    # Save transformed data
    os.makedirs("data/cleaned", exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)
    print("Transformed data saved to:", OUTPUT_PATH)

if __name__ == "__main__":
    transform_data()
